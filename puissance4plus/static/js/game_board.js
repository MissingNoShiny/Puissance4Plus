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
function fetchLooping(column) {
    body = column.toString();
    $("header").text(column);
    fetch("/game", {
        method: 'PUT',
        headers: {
            'Accept': 'text/plain',
            'Content-Type': 'text/plain'
        },
        body: body
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
// Function which handle the fetch's response object
function handleResponseData(data) {
    if(!data.newBoard) {
        // Initiale fetch
        Board.initialize(data.height, data.width);
        Board.setData(data.grid);
        Board.previousGrid = data.grid;
    } else {
        // Looping fetch
        Board.initialize(data.newBoard.height, data.newBoard.width);
        Board.setData(data.newBoard.grid);
        Board.previousGrid = data.grid;
    }
}
// Board object
let Board = {
    canvas: $("canvas.board"),
    parent: $("main"),
    previousGrid: null,
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
            ctx.closePath();
        } else Error("No rows & columns set");
    },
    _clicEvent: function(e) {
        // Calculate on which column
        bcr = this.canvas.get(0).getBoundingClientRect();
        cx = (e.clientX - bcr.left) * (this.canvas.width() / bcr.width);
        col = Math.floor(cx / this.canvas.width() * this.columns);
        // Fetch clic on server
        fetchLooping(col);
    },
    _mouseIn: function(e) {
        // Clear previous hover
        this._mouseOut();
        // Calculate on which column
        bcr = this.canvas.get(0).getBoundingClientRect();
        cx = (e.clientX - bcr.left) * (this.canvas.width() / bcr.width);
        col = Math.floor(cx / this.canvas.width() * this.columns);
        // Check column state & render hover effect
        columnWidth = this.canvas.width() / this.columns;
        ctx = this.canvas.get(0).getContext('2d');
        ctx.fillStyle = "rgba(0, 0, 0, .25)";
        ctx.fillRect(col * columnWidth, 0, columnWidth, this.canvas.height());
        
    },
    _mouseOut: function(e) {
        this.initialize(this.rows, this.columns);
        this.setData(this.previousGrid);
    },
    initialize: function(rows, columns) {
        // Default adjustments
        this._autoSize();
        this._setRowsCols(rows, columns);
        // Context
        ctx = this.canvas.get(0).getContext('2d');
        // Background
        ctx.fillStyle = "rgba(0, 0, 255, .75)";
        ctx.fillRect(0, 0, this.canvas.width(), this.canvas.height());
        // Empty holes
        for(let y = 0; y < this.rows; y++) {
            for(let x = 0; x < this.columns; x++) {
                this._drawCircle(x, y, "rgba(255, 255, 255, .75)", false);
            }
        }
    },
    setData: function(array) {
        for(let y = 0; y < array.length; y++) {
            for(let x = 0; x < array[y].length; x++) {
                if(array[y][x]) {
                    this._drawCircle(x, y, array[y][x].color)
                };
            }
        }
    }
}

// START
fetchInitial();

// Mouse events on canvas
$("canvas.board")
.click(e => {
    Board._clicEvent(e);
})
.mousemove(e => {
    Board._mouseIn(e);
})
.mouseout(e => {
    Board._mouseOut(e);
})