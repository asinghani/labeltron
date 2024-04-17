
setInterval(function() {
    var text = $("#label_text").val();
    var msize = $("input[name='sizeradio']:checked").val();
    var mwidth = $("input[name='widthradio']:checked").val();
    text = mwidth+"=//="+msize+"=//="+text

    $("#preview_img").attr("src", "/render_preview.png?text="+encodeURIComponent(text));
}, 250);

$("#preview_img")[0].onload = function() {
    var width = "(Width = " + (this.naturalWidth/128).toFixed(1) + " in)";
    if (this.src.endsWith("=")) {
        $("#preview_width").text("");
    } else {
        $("#preview_width").text(width);
    }
}
