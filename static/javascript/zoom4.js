var scale4 = 1,
panning4 = false,
pointX4 = 0,
pointY4 = 0,
recentx4 = 0;
recenty4 = 0;
start4 = { x4: 0, y4: 0 },
zoom4 = document.getElementById("zoom4");

function setTransform4() {
    if (scale4 <= 0.8) {
        scale4 *= 1.045;
    }
    else if (scale4 > 4) {
        scale4 /= 1.045;
    }
    else {
        zoom4.style.transform = "translate(" + pointX4 + "px, " + pointY4 + "px) scale(" + scale4 + ")";
        recentx4 = pointX4
        recenty4 = pointY4
    }
}

zoom4.onmousedown = function (e4) {
    e4.preventDefault();
    start4 = { x4: e4.clientX - recentx4, y4: e4.clientY - recenty4 };
    panning4 = true;
}

zoom4.onmouseup = function (e4) {
    panning4 = false;
}

zoom4.onmousemove = function (e4) {
    e4.preventDefault();
    if (!panning4) {
        return;
    }
    pointX4 = (e4.clientX - start4.x4);
    pointY4 = (e4.clientY - start4.y4);
    setTransform4();
}

zoom4.onmouseout = function (e4) {
    panning4 = false;
}

zoom4.onwheel = function (e4) {
e4.preventDefault();
var xs4 = (e4.clientX - recentx4) / scale4,
ys4 = (e4.clientY - recenty4) / scale4,
delta4 = (e4.wheelDelta ? e4.wheelDelta : -e4.deltaY);
(delta4 > 0) ? (scale4 *= 1.045) : (scale4 /= 1.045);
(delta4 > 0) ? (pointX4 = e4.clientX - 0.98*xs4 * scale4) : (pointX4 = e4.clientX - 1.02*xs4 * scale4);
(delta4 > 0) ? (pointY4 = e4.clientY - 0.98*ys4 * scale4) : (pointY4 = e4.clientY - 1.02*ys4 * scale4);

setTransform4();
}
