// Technical
Math.randInt = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
}
// Start
$(document).ready(() => {
    $("main menu").hide();
    $("main nav button").click((ev) => {
        
    })
})
// 
function openMenu(menu) {
    $("main menu")
    .hide()
    .filter((i, el) => {
        return $(el).data("menu") == menu
    })
    .show();
}










// Array.randomItems = function(array, count) {
//     let c = count || 1;
//     if(c <= array.length) {
//         let randoms = [];
//         let indexes = [];
//         for(let i = 0; i < c; i++) {
//             let r;
//             do r = Math.randInt(0, array.length - 1);
//             while (indexes.includes(r));
//             randoms.push(array[r]);
//             indexes.push(r);
//         }
//         return randoms;
//     } else return null;
// }
// Functions
// function drawBackground() {
//     let canvas = document.getElementById("background-canvas");
//     let ctx = canvas.getContext("2d");
//     // Size
//     canvas.width = document.body.clientWidth;
//     canvas.height = document.body.clientHeight;
//     let canvasW = canvas.width;
//     let canvasH = canvas.height;
//     let middleX = canvasW / 2;
//     let middleY = canvasH / 2;
//     // Gradient
//     let bgGradient = ctx.createLinearGradient(0, 0, canvasW, canvasH);
//     bgGradient.addColorStop(0, '#1b1464');
//     bgGradient.addColorStop(.25, '#1b1464');
//     bgGradient.addColorStop(.75, "#252a33");
//     bgGradient.addColorStop(1, "#252a33");
//     ctx.fillStyle = bgGradient;
//     ctx.fillRect(0, 0, canvasW, canvasH);
//     // Planet 1
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);
//     drawRandomPlanet(canvas);

    
// }
// // Functions
// function drawRandomPlanet(canvas, x, y, radius) {
//     if(canvas) {
//         let context = canvas.getContext("2d");
//         let canvasW = canvas.width;
//         let canvasH = canvas.height;
//         console.log(canvasW, canvasH);
//         // Random values
//         radius = radius || Math.randInt(25, 150);
//         colors = Array.randomItems([ "#1b1464", "#252a33", "#17f6a0", "#8001d6", "#dbd5e1", "#016b3d", "#ccac79", "#59a1a0" ], 2);
//         console.log(radius, colors);
//         x = x || Math.randInt(radius/2, canvasW - (radius/2));
//         y = y || Math.randInt(radius/2, canvasH - (radius/2));
//         console.log(x, y);
//         // Gradient
//         let planetGradient = context.createLinearGradient(0, 0, radius, 0);
//         planetGradient.addColorStop(0, colors[0]);
//         planetGradient.addColorStop(.25, colors[0]);
//         planetGradient.addColorStop(.75, colors[1]);
//         planetGradient.addColorStop(1, colors[1]);
//         context.beginPath();
//         context.arc(x, y , radius, 0, 2 * Math.PI);
//         context.fillStyle = planetGradient;
//         context.fill();
//         context.closePath();
//     } else return null
// }