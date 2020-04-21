let fakeData = [
    [ "", "", "I", "O" ],
    [ "", "", "I", "I" ],
    [ "", "0", "0", "I" ],
    [ "0", "I", "I", "O" ],
    [ "0", "0", "0", "O" ]
];
buildArray(fakeData);

// Build array
function buildArray(data) {
    $("table.board").empty();
    for(let i = 0; i < data.length; i++) {
        let tr = $(document.createElement("tr"));
        for(let y = 0; y < data[i].length; y++) {
            let td = $(document.createElement("td"));
            td.text(data[i][y]);
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
                console.log(json)
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
                console.log(json)
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
    autoSize: function(){
        if(this.parent.width() > this.parent.height()) {
            this.canvas.attr("height", this.parent.height());
            this.canvas.attr("width", this.parent.height());
        } else {
            this.canvas.attr("height", this.parent.width());
            this.canvas.attr("width", this.parent.width());
        }
        this.canvas.show();
    },
    draw: function(rows, column) {
        let ctx = this.canvas.get(0).getContext('2d');
        // Background
        ctx.fillStyle = "#1e62f4";
        ctx.fillRect(0, 0, this.canvas.width(), this.canvas.height());
        // Empty holes
        let holeSize = this.canvas.width() / column;
        let holeRadius = (holeSize / 2) * 0.8;

        console.log(holeSize, holeRadius);

        for(let y = 1; y <= rows; y++) {
            for(let x = 1; x <= column; x++) {
                cx = (x*holeSize) - (holeSize/2);
                cy = (y*holeSize) - (holeSize/2);
                console.log(cx, cy, holeRadius);
                ctx.beginPath();
                ctx.arc(cx, cy, holeRadius, 0, 2*Math.PI);
                ctx.fillStyle = "#fff";
                ctx.fill();
                ctx.closePath();
            }

        }
    }
}


// INIT
Board.autoSize();
Board.draw(6, 7);
