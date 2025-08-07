(function(){var r=document.getElementById('react-island-root');if(!r||!window.React||!window.ReactDOM)return;
var m=r.dataset.message||'Hello from React Island';function W(){return React.createElement('div',{className:'card',style:{padding:'12px'}},m)}
ReactDOM.createRoot(r).render(React.createElement(W));})();
