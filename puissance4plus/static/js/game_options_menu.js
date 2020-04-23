// Options automations and validation
$("input.slider").on("input change", e => {
    $(".sliderValue." + e.target.name).text(e.target.value);
})
$("input.slider[name=win_condition]").on("input change", e => {
    $("input.slider.toMinimalize").attr("min", e.target.value).change();
})
// Class Player
let maxPlayers = 5;
let players = [];
let ids = [];
for(let i = 1; i <= maxPlayers; i++) ids.push(i);
let colors = {
    1: "#fcd53d", 
    2: "#ff0000",
    3: "#24D12B",
    4: "#E8578D",
    5: "#00adad"
};
function newPlayer() {
    if(players.length < maxPlayers) {
        let p = new Player(ids.shift());
        p.elmt.find(".delete").click(() => { p.delete() })
        players.push(p);
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
        this.color = colors[this.id];
        this.elmt.find(".color").css("background", this.color);
        // Event listeners : name
        this.name;
        this.elmt.find(".name").on("input", e => {
            this.name = e.target.value;
            if(e.target.value.length >= 2 && e.target.value.length <= 10) {
                this.nameValid = true
            } else this.nameValid = false
        })
    }
    delete() {
        this.elmt.remove();
        ids.push(this.id);
        for(let i = 0; i < players.length; i++) {
            if(players[i].id == this.id) players.splice(i, 1);
        }
    }
}
// FOOTER BUTTONS
$("footer .back").click(() => {
    window.location.href = "/";
})
$("footer .play").click(() => {
    // Get players
    if(players.length >= 2) {
        let invalids = 0;
        players.forEach(p => {
            if(!p.nameValid) invalids++;
        })
        if(invalids == 0) {
            // Get board options
            let body = {
                win_condition: $(".slider[name=win_condition]").val(),
                height: $(".slider[name=height]").val(),
                width: $(".slider[name=width]").val(),
                mode: new URLSearchParams(window.location.search).get("mode"),
                players: {}
            };
            players.forEach(p => {
                body.players[p.id] = {
                    name: p.name,
                    color: p.color
                }
            });
            // Fetch
            fetch("/gameOptions", {
                method: 'POST',
                headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            })
            .then(res => {
                if(res.status == 200) {
                    window.location.href = "/game";
                } else {
                    ErrorAlert(
                        "Refusé<br><br>"
                        + "Denied"
                    )
                }
            })
            .catch(err => {
                ErrorAlert(
                    "Erreur de réseau<br>Tentez de redémarrer l'application<br><br>"
                    + "Network error<br>Try restart the application"
                )
                console.error(err);
            })
        } else {
            ErrorAlert(
                "Noms de joueur invalides : " + invalids + "<br><br>"
                + "Invalids player names: " + invalids
            )
        }
    } else {
        ErrorAlert(
            "Pas assez de joueurs pour commencer !<br><br>"
            + "Not enough players for start"
        )
    }
})
// Class Error alert
function ErrorAlert(message) {
    let box = $($("#ErrorAlert")[0].content)
    .find(".ErrorAlert")
    .clone()
    .appendTo("body")

    box.find(".content")
    .append(message);

    box.find(".close").click(() => {
        box.remove();
    })
}