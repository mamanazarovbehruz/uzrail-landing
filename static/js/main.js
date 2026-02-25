function setLoading(a){
  if(!a) return;
  a.classList.add("loading");
  const arrow = a.querySelector(".arrow");
  if(arrow){
    arrow.innerHTML = '<span class="spinner" aria-label="loading"></span>';
  }
}

function isIOS() {
  return /iPhone|iPad|iPod/i.test(navigator.userAgent);
}

document.getElementById("btn-chrome")?.addEventListener("click", function(){
  setLoading(this);
});

document.getElementById("btn-app")?.addEventListener("click", function(e){
  setLoading(this);

  // iOS: intent ishlamasligi mumkin, shuning uchun App Store'ga yuboramiz
  if(isIOS()){
    e.preventDefault();
    const apple = this.dataset.apple;
    if (apple) window.location.href = apple;
  }
  // Android: href="intent:..." o'zi ishlaydi (app yoki Play Market fallback)
});

function isAndroid() {
  return /Android/i.test(navigator.userAgent);
}

document.addEventListener("DOMContentLoaded", () => {
  // Desktopda intent ishlamaydi — oddiy https linkga o'tkazamiz
  if (!isAndroid()) {
    const c = document.getElementById("btn-chrome");
    if (c && c.dataset.web) c.href = c.dataset.web;

    const a = document.getElementById("btn-app");
    if (a && a.dataset.web) a.href = a.dataset.web;
  }
});