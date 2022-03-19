//배경 이미지 show
let picture = ["/static/aboutme/images/header1.jpg",
     "/static/aboutme/images/header2.jpg", "/static/aboutme/images/header3.jpg"]
let p_idx = 0

showPicture()

function showPicture(){
    let img = document.querySelector("#pic")
    img.src = picture[p_idx]
    p_idx += 1
    if(p_idx == picture.length)
        p_idx = 0;
    setTimeout(showPicture, 2000);
}