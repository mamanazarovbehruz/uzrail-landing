function setLoading(a){
    if(!a) return;
    a.classList.add("loading");
    const arrow = a.querySelector(".arrow");
    if(arrow){
      arrow.innerHTML = '<span class="spinner" aria-label="loading"></span>';
    }
  }
  
  document.getElementById("btn-chrome")?.addEventListener("click", function(){
    setLoading(this);
  });
  
  document.getElementById("btn-app")?.addEventListener("click", function(){
    setLoading(this);
  });
  

function isIOS() {
  return /iPhone|iPad|iPod/i.test(navigator.userAgent);
}
  
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector(".js-open-app");
  if (!btn) return;

  btn.addEventListener("click", (e) => {
    if (isIOS()) {
      e.preventDefault();
      window.location.href = btn.dataset.apple; // App Store
    }
    // Android: href="intent:..." o‘zi ishlaydi (fallback Play Market)
  });
});