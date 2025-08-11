// 头部浮窗状态检测和优化
document.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector(".site-header");

  if (!header) return;

  // 检测滚动位置并添加浮窗状态类
  function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > 100) {
      header.classList.add("is-sticky");
    } else {
      header.classList.remove("is-sticky");
    }
  }

  // 监听滚动事件
  window.addEventListener("scroll", handleScroll);

  // 初始化时检查一次
  handleScroll();

  // 确保头部链接在浮窗状态下正常工作
  const headerLinks = header.querySelectorAll("a");

  headerLinks.forEach((link) => {
    // 确保链接可点击
    link.style.pointerEvents = "auto";
    link.style.cursor = "pointer";

    // 添加点击事件监听器
    link.addEventListener("click", function (e) {
      // 确保链接正常工作
      console.log("Header link clicked:", this.href);
    });

    // 添加焦点事件
    link.addEventListener("focus", function () {
      this.style.outline = "2px solid var(--gold)";
      this.style.outlineOffset = "2px";
    });

    link.addEventListener("blur", function () {
      this.style.outline = "";
      this.style.outlineOffset = "";
    });
  });

  // 防止其他元素覆盖头部链接
  header.addEventListener("mouseenter", function () {
    this.style.zIndex = "1000";
  });

  // 优化移动端浮窗头部
  if (window.innerWidth <= 768) {
    header.style.zIndex = "1001";

    const container = header.querySelector(".container");
    if (container) {
      container.style.zIndex = "1002";
    }

    headerLinks.forEach((link) => {
      link.style.zIndex = "1003";
    });
  }
});

// 监听窗口大小变化
window.addEventListener("resize", function () {
  const header = document.querySelector(".site-header");
  if (!header) return;

  if (window.innerWidth <= 768) {
    header.style.zIndex = "1001";
  } else {
    header.style.zIndex = "1000";
  }
});
