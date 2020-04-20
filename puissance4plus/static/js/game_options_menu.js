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
let Ids = [];
for(let i = 1; i <= maxPlayers; i++) Ids.push(i);
let Colors = {
    1: "#fcd53d", 
    2: "#ff0000",
    3: "#24D12B",
    4: "#E8578D",
    5: "#00FFFF"
};
function newPlayer() {
    if(Players.length < maxPlayers) {
        let p = new Player(Ids.shift());
        p.elmt.find(".delete").click(() => { p.delete() })
        Players.push(p);
    }
}
class Player {
    constructor(id) {
        // Node
        this.elmt = $($("template.player")[0].content).children(".player").clone(false);
        this.elmt.appendTo(".players");
        // Display id
        this.id = id;
        this.elmt.find(".id").text(this.id);
        // Display color
        this.color = Colors[this.id];
        this.elmt.find(".color").css("background", this.color);
        // Event listeners : name
        this.name;
        this.elmt.find(".name").on("input", e => {
            this.name = e.target.value;
            console.log(this.name);
            if(e.target.value.length >= 2 && e.target.value.length <= 10) {
                this.nameValid = true
            } else this.nameValid = false
        })
    }
    delete() {
        this.elmt.remove();
        Ids.push(this.id);
        for(let i = 0; i < Players.length; i++) {
            if(Players[i].id == this.id) Players.splice(i, 1);
        }
    }
}
// FOOTER BUTTONS
$("footer .back").click(() => {
    window.location.href = "/";
})
$("footer .play").click(() => {
    // TODO PLAY
})