$(document).ready(function () {
    $("#btn_load_image").on("click", function () {
        $("#file_load_image")[0].click();
    });

    function handleFileSelect(evt) {
        var files = evt.target.files;

        for (var i = 0, f; f = files[i]; i++) {

            if (!f.type.match('image.*')) {
                continue;
            }

            var reader = new FileReader();

            reader.onload = (function () {
                return function (e) {
                    $("#image").attr('src', e.target.result)
                    const image = $("#image")[0]
                    const cropper = new Cropper(image);
                    $("#crop_loaded_image").on("click", function () {
                        x = cropper.getData().x;
                        y = cropper.getData().y;
                        width = cropper.getData().width;
                        height = cropper.getData().height;
                        scaleX = cropper.getData().scaleX;
                        scaleY = cropper.getData().scaleY;
                        $("#hidden-data").attr('value', 'x=' + x + '&y=' + y + '&width=' + width + '&height=' + height + '&scaleX=' + scaleX + '&scaleY=' + scaleY)
                        $("#send-data")[0].click()
                    })
                };
            })(f);
            reader.readAsDataURL(f);
        }
    }

    document.getElementById("file_load_image").addEventListener('change', handleFileSelect, false);
});