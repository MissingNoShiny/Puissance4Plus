// Options automations and validation
$("input.slider").on("input change", e => {
    $(".sliderValue." + e.target.name).text(e.target.value);
})
$("input.slider[name=winLength]").on("input change", e => {
    $("input.slider[name^=board").attr("min", e.target.value).change();
})
// Class Player
let maxPlayers = 5;
let Players = [];
class Player {
    constructor() {
        if(Players.length < maxPlayers) {
            // Create and append node
            this.elmt = $($("template.player")[0].content).clone().children(".player");
            this.elmt.appendTo($(".players"));
            // Add to players list
            Players.push(this);
            // Display id
            this.id = Players.length;
            this.elmt.find(".id").text(this.id);
            // Event listeners : name
            this.name;
            this.elmt.children("[name=name]").on("input", e => {
                this.name = e.target.value;
                if(e.target.value.length >= 2 && e.target.value.length <= 10) {
                    this.nameValid = true
                } else this.nameValid = false
            })
            // Formatting select color
            this.elmt.find("[name=color] option").each((i, e) => {
                $(e).css("background", e.value)
            })
            this.elmt.find("[name=color]").change(e => {
                $(e.target).css("background", $(e.target).val())
            }).change();
            console.log(Players);
        } else return false;
    }
}