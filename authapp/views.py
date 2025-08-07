import os, secrets, urllib.parse, requests, jwt
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponseBadRequest

ISSUER=os.getenv("LOGTO_ISSUER","").rstrip("/")
CLIENT_ID=os.getenv("LOGTO_CLIENT_ID","")
CLIENT_SECRET=os.getenv("LOGTO_CLIENT_SECRET","")
REDIRECT_URI=os.getenv("LOGTO_REDIRECT_URI","")
SCOPES=os.getenv("LOGTO_SCOPES","openid profile email")
LOGOUT_REDIRECT=os.getenv("LOGTO_LOGOUT_REDIRECT_URI","/")
ROLE_CLAIM=os.getenv("LOGTO_ROLE_CLAIM","roles")

def _discover():
    conf=requests.get(f"{ISSUER}/.well-known/openid-configuration",timeout=10).json()
    jwks_uri=conf.get("jwks_uri")
    return conf, jwks_uri

def _verify_id_token(id_token, audience):
    _, jwks_uri=_discover()
    jwk_client=jwt.PyJWKClient(jwks_uri)
    signing_key=jwk_client.get_signing_key_from_jwt(id_token).key
    decoded=jwt.decode(id_token, signing_key, algorithms=["RS256","ES256"], audience=audience, options={"verify_at_hash": False})
    return decoded

def login_start(request):
    if not (ISSUER and CLIENT_ID and REDIRECT_URI):
        return HttpResponseBadRequest("Logto env not configured")
    state=secrets.token_urlsafe(24); request.session["oidc_state"]=state
    params={"client_id":CLIENT_ID,"response_type":"code","redirect_uri":REDIRECT_URI,"scope":SCOPES,"state":state}
    return redirect(f"{ISSUER}/oidc/auth?{urllib.parse.urlencode(params)}")

def login_callback(request):
    code=request.GET.get("code"); state=request.GET.get("state")
    if not code or not state or state!=request.session.get("oidc_state"):
        return HttpResponseBadRequest("Invalid OIDC state")
    token_url=f"{ISSUER}/oidc/token"
    data={"grant_type":"authorization_code","code":code,"redirect_uri":REDIRECT_URI,"client_id":CLIENT_ID,"client_secret":CLIENT_SECRET}
    tok=requests.post(token_url,data=data,timeout=10)
    if tok.status_code!=200: return HttpResponseBadRequest(f"Token exchange failed: {tok.text[:200]}")
    tokens=tok.json(); access=tokens.get("access_token"); id_token=tokens.get("id_token")
    claims=_verify_id_token(id_token, CLIENT_ID)
    ui=requests.get(f"{ISSUER}/oidc/me",headers={"Authorization":f"Bearer {access}"},timeout=10)
    if ui.status_code!=200: return HttpResponseBadRequest(f"Userinfo failed: {ui.text[:200]}")
    info=ui.json()
    sub=info.get("sub") or claims.get("sub")
    email=info.get("email") or claims.get("email") or f"{sub}@example.local"
    User=get_user_model(); user,_=User.objects.get_or_create(username=sub,defaults={"email":email})
    roles=claims.get(ROLE_CLAIM) or info.get(ROLE_CLAIM) or []
    if isinstance(roles,str): roles=[roles]
    for r in roles:
        g,_=Group.objects.get_or_create(name=str(r)); user.groups.add(g)
    login(request,user,backend="django.contrib.auth.backends.ModelBackend")
    request.session["oidc"]={"sub":sub,"email":email,"access_token":access,"id_token":id_token}
    return redirect("/")

def logout_view(request):
    oidc=request.session.get("oidc") or {}; id_token=oidc.get("id_token")
    logout(request)
    if ISSUER and id_token:
        params={"post_logout_redirect_uri":LOGOUT_REDIRECT,"id_token_hint":id_token}
        return redirect(f"{ISSUER}/oidc/session/end?{urllib.parse.urlencode(params)}")
    return redirect(LOGOUT_REDIRECT)
