// Technical
Math.randInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}
// Open menu on click
function openMenu(menu) {
    // alert(menu);
    $("main menu")
    .hide()
    .filter((i, el) => {
        return $(el).data("menu") == menu
    })
    .show();
}
// Slider volume
$("#volume").on("input change", e => {
    $(".displayVolume").text("[" + $(e.target).val() + "]");
})