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
    $("#board").empty();
    for(let i = 0; i < data.length; i++) {
        let tr = $(document.createElement("tr"));
        for(let y = 0; y < data[i].length; y++) {
            let td = $(document.createElement("td"));
            td.text(data[i][y]);
            td.appendTo(tr);
        }
        tr.appendTo($("#board"));
    }
}