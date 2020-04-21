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
            res.json().then(handleResponseData)
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
            res.json().then(handleResponseData)
        } else {
            console.error(res);
        }
    })
    .catch(err => {
        console.log(err)
    })
}
// Function which handle the fetch's response object
function handleResponseData(data) {
    console.log(data);
    if(!data.newBoard) {
        // Initiale fetch
        Board.initialize(data.height, data.width);
        Board.setData(data.grid);
    } else {
        // Looping fetch
        Board.initialize(data.newBoard.height, data.newBoard.width);
        Board.setData(data.newBoard.grid);
    }
}
// Board object
let Board = {
    canvas: $("canvas.board"),
    parent: $("main"),
    previousState: null,
    rows: null,
    columns: null,
    _setRowsCols: function(rows, columns) {
        this.rows = rows;
        this.columns = columns;
    },
    _autoSize: function() {
        if(this.parent.width() > this.parent.height()) {
            this.canvas.attr("height", this.parent.height());
            this.canvas.attr("width", this.parent.height());
        } else {
            this.canvas.attr("height", this.parent.width());
            this.canvas.attr("width", this.parent.width());
        }
    },
    _drawCircle: function(column, row, color, border) {
        if(this.rows && this.columns) {
            ctx = this.canvas.get(0).getContext('2d');
            // Values
            holeHeight = this.canvas.height() / this.rows;
            holeWidth = this.canvas.width() / this.columns;
            ratio = border ? 0.85 : 0.8;
            holeRadius = holeHeight < holeWidth ? (holeHeight / 2) * ratio : (holeWidth / 2) * ratio;
            // Draw circle
            cx = ((column+1) * holeWidth) - (holeWidth / 2);
            cy = ((row+1) * holeHeight) - (holeHeight / 2);
            ctx.beginPath();
            ctx.arc(cx, cy, holeRadius, 0, 2*Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
        } else Error("No rows & columns set");
    },
    _clicEvent: function(e) {
        bcr = this.canvas.get(0).getBoundingClientRect();
        cx = (e.clientX - bcr.left) * (this.canvas.width() / bcr.width);
        col = Math.floor(cx / this.canvas.width() * this.columns);
        fetchLooping(col);
    },
    initialize: function(rows, columns) {
        // Default adjustments
        this._autoSize();
        this._setRowsCols(rows, columns);
        // Context
        ctx = this.canvas.get(0).getContext('2d');
        // Background
        ctx.fillStyle = "#1e62f4";
        ctx.fillRect(0, 0, this.canvas.width(), this.canvas.height());
        // Empty holes
        for(let y = 0; y < this.rows; y++) {
            for(let x = 0; x < this.columns; x++) {
                this._drawCircle(x, y, "#fff", false);
            }
        }
    },
    setData: function(array) {
        console.log("set data", array);
        for(let y = 0; y < array.length; y++) {
            for(let x = 0; x < array[y].length; x++) {
                if(array[y][x]) {
                    console.log(array[y][x]);
                    console.log("draw", x, y);
                    this._drawCircle(x, y, array[y][x].color)
                };
            }
        }
    }
}

// START
fetchInitial();

// Click event on canva
$("canvas.board").click(e => {
    Board._clicEvent(e);
});