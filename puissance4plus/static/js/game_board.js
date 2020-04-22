// Variable : last board state
let lastState;
let lang;
let frozen = false;
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
        console.error(err);
    });
}
// Looping fetch
function fetchLooping(column) {
    let body = column.toString();
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
            res.json().then(handleResponseData);
        } else {
            console.error(res);
        }
    })
    .catch(err => {
        console.error(err);
    });
}
// Function which handles the fetch's response object
function handleResponseData(data) {
    console.log(data);
    if(data.hasOwnProperty("board")) {
        // Initial fetch
        lang = data.language_data;
        handleNewState(data.board);
    } else {
        // Looping fetch
        handleNewState(data);
    }
}
// Handle a new state (grid, players, ...)
function handleNewState(state) {
    Board.initialize(state.height, state.width);
    Board.setData(state.grid);
    lastState = state;
    displayPlayers(state.players, state.current_player);
    if(state.state === 1) {
        newMessage(lang.game_board.winningMessage.replace("{}", state.current_player.name), true);
        frozen = true;
        $("button.giveUp").hide();
        $("button.end").show();
    } else if (state.state === 2) {
        newMessage(lang.game_board.drawMessage, true);
        frozen = true;
        $("button.giveUp").hide();
        $("button.end").show();
    } else {
        if (state.game_mode === 2) {
            if (state.current_effect == 0)
                newMessage(lang.game_board.chipNoEffectMessage);
            else
                newMessage(lang.game_board.chipEffectMessage.replace("{}", lang.effects[state.current_effect]));
        }
    }
}
// Board object
let Board = {
    canvas: $("canvas.board"),
    parent: $("main"),
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
            let ctx = this.canvas.get(0).getContext('2d');
            // Values
            let holeHeight = this.canvas.height() / this.rows;
            let holeWidth = this.canvas.width() / this.columns;
            let ratio = border ? 0.85 : 0.8;
            let holeRadius = holeHeight < holeWidth ? (holeHeight / 2) * ratio : (holeWidth / 2) * ratio;
            // Draw circle
            let cx = ((column+1) * holeWidth) - (holeWidth / 2);
            let cy = ((row+1) * holeHeight) - (holeHeight / 2);
            ctx.beginPath();
            ctx.arc(cx, cy, holeRadius, 0, 2*Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.closePath();
        } else Error("No rows & columns set");
    },
    _clicEvent: function(e) {
        if(!frozen) {
            // Calculate on which column
            let bcr = this.canvas.get(0).getBoundingClientRect();
            let cx = (e.clientX - bcr.left) * (this.canvas.width() / bcr.width);
            let col = Math.floor(cx / this.canvas.width() * this.columns);
            // Fetch clic on server
            if(!lastState || lastState.non_full_columns.includes(col)) {
                fetchLooping(col);
            } else {
                newMessage(lang.game_board.filledColumn.replace("{}", lastState.current_player.name));
            }
        }
    },
    _mouseIn: function(e) {
        // Clear previous hover
        this._mouseOut();
        // Calculate on which column
        let bcr = this.canvas.get(0).getBoundingClientRect();
        let cx = (e.clientX - bcr.left) * (this.canvas.width() / bcr.width);
        let col = Math.floor(cx / this.canvas.width() * this.columns);
        // Check column state and set color
        let color;
        if(!lastState || lastState.non_full_columns.includes(col)) {
            color = "rgba(0, 0, 0, .25)";
        } else {
            color = "rgba(255, 0, 0, .5)";
        }
        // Render hover effect
        let columnWidth = this.canvas.width() / this.columns;
        let ctx = this.canvas.get(0).getContext('2d');
        ctx.fillStyle = color;
        ctx.fillRect(col * columnWidth, 0, columnWidth, this.canvas.height());
        
    },
    _mouseOut: function(e) {
        this.initialize(this.rows, this.columns);
        this.setData(lastState.grid);
    },
    initialize: function(rows, columns) {
        // Default adjustments
        this._autoSize();
        this._setRowsCols(rows, columns);
        // Context
        let ctx = this.canvas.get(0).getContext('2d');
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
                    this._drawCircle(x, y, array[y][x].color);
                }
            }
        }
    }
}
// Display Players
function displayPlayers(array, current) {
    $(".players").empty();
    array.forEach(p => {
        $(document.createElement("div"))
        .addClass(p.name === current.name ? "player current" : "player")
        .text(p.name)
        .css("background", p.color)
        .appendTo(".players")
    });
}
// New message
function newMessage(message, persistent) {
    let m  = $(document.createElement("div"))
    .hide()
    .addClass("message")
    .html(message)
    .prependTo(".messages")
    .slideDown();
    if(!persistent) {
        m.delay(10000)
        .fadeOut();
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

// giveUp button
$("button.giveUp").click(e => {
    setTimeout(() => {
        newMessage(lang.game_board.dbClickForGiveUp);
    }, 500)
})
$("button.giveUp").dblclick(e => {
    window.location.href = "/";
})

// End button
$("button.end").click(e => {
    window.location.href = "/";
})