
var previewPicture  = function (e) {
    var types = [ "image/jpg", "image/jpeg", "image/png" ];

    var image = document.getElementById("image");
    const [picture] = e.files

    if (types.includes(picture.type)) {
            var reader = new FileReader();
            reader.onload = function (e) {
                image.src = e.target.result
            }
            reader.readAsDataURL(picture)
    }
}