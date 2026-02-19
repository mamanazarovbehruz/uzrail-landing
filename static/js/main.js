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
  