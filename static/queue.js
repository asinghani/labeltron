
function render_preview(text) {
    return `
        <img src="/render_preview.png?text=${encodeURIComponent(text)}"
            style="display: block; max-height: 48px;
            max-width: 100%; margin-bottom: 5pt; border: 1px solid black;">
    `
}

setInterval(function() {
    $.get("/get_state", function(res) {
        var html = "";
        for (var i = 0; i < res.queue.length; i++) {
            html += render_preview(res.queue[i]);
        }
        if (html == "") {
            html = "<p>Print queue is currently empty</p>"
        }
        $("#queue").html(html);
    });
}, 250);
