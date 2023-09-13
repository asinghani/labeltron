
function print() {
    var text = $("#label_text").val();
    var msize = $("input[name='sizeradio']:checked").val();
    if (text.length != 0) {
        text = msize+"=//=size=//="+text
        $.post("/print_one", {text: text}, function() {
            $("#label_text").val("");
        });
    }
}

function cancel_all() {
    $.post("/cancel_all");
}

$("#label_text").on("keydown", function (e) {
    if (e.keyCode === 13 && (e.ctrlKey || e.metaKey)) {
        print();
        e.preventDefault();
    }
});
