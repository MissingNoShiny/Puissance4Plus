// let fakeData = [
//     [ "", "", "I", "O" ],
//     [ "", "", "I", "I" ],
//     [ "", "0", "0", "I" ],
//     [ "0", "I", "I", "O" ],
//     [ "0", "0", "0", "O" ]
// ];
// buildArray(fakeData);

// Build array
function buildArray(data) {
    $("table.board").empty();
    for(let i = 0; i < data.length; i++) {
        let tr = $(document.createElement("tr"));
        for(let y = 0; y < data[i].length; y++) {
            let td = $(document.createElement("td"));
            if(data[i][y]) {
                td.text(data[i][y].name);
            } else {
                td.text("?");
            }
            td.appendTo(tr);
        }
        tr.appendTo($("table.board"));
    }
}
// Initial fetch
function fetchInitial() {
    fetch("/game", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        if(res.status == 200) {
            res.json().then(json => {
                // Fetch initial complete
                console.log(json);
                Board.draw(json.height, json.width);
                buildArray(json.grid);
            })
        } else {
            console.error(res);
        }
    })
    .catch(err => {
        console.error(err)
    })
}
// Looping fetch
let body = {};
function fetchLooping(column) {
    fetch("/game", {
        method: 'PUT',
        headers: {
            'Accept': 'text/plain',
            'Content-Type': 'text/plain'
        },
        body: column
    })
    .then(res => {
        if(res.status == 200) {
            res.json().then(json => {
                // Fetch looping complete
                console.log(json);
                buildArray(json.newBoard.grid);
            })
        } else {
            console.error(res);
        }
    })
    .catch(err => {
        console.log(err)
    })
}


let Board = {
    canvas: $("canvas.board"),
    parent: $("main"),
    previousState: null,
    autoSize: function(){
        if(this.parent.width() > this.parent.height()) {
            this.canvas.attr("height", this.parent.height());
            this.canvas.attr("width", this.parent.height());
        } else {
            this.canvas.attr("height", this.parent.width());
            this.canvas.attr("width", this.parent.width());
        }
    },
    draw: function(rows, column) {
        this.autoSize();
        let ctx = this.canvas.get(0).getContext('2d');
        // Background
        ctx.fillStyle = "#1e62f4";
        ctx.fillRect(0, 0, this.canvas.width(), this.canvas.height());
        // Empty holes
        // let holeSize = column > rows ? this.canvas.width() / column : this.canvas.width() / rows;
        let holeHeight = this.canvas.width() / rows;
        let holeWidth = this.canvas.width() / column;
        let holeRadius = holeHeight < holeWidth ? (holeHeight / 2) * 0.8 : (holeWidth / 2) * 0.8;
        for(let y = 1; y <= rows; y++) {
            for(let x = 1; x <= column; x++) {
                cx = (x*holeWidth) - (holeWidth/2);
                cy = (y*holeHeight) - (holeHeight/2);
                ctx.beginPath();
                ctx.arc(cx, cy, holeRadius, 0, 2*Math.PI);
                ctx.fillStyle = "#fff";
                ctx.fill();
                ctx.closePath();
            }

        }
    }
}

// START
fetchInitial();