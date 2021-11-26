let carousel=document.getElementById("carousel-click");
carousel.addEventListener("click",function(e){
    let item=e.target;
    console.log(item.id);
    let request=new XMLHttpRequest();
    request.open("GET","/"+item.id);
    request.send();
    request.onreadystatechange=function(){
        if(this.readyState==4){
            Swal.fire({
                "title":"Inicia Sesion o Crea una Cuenta",
                "html":this.responseText,
                "width":600
            })
        }
    }
})