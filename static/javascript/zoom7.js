var scale7 = 1,
panning7 = false,
pointX7 = 0,
pointY7 = 0,
recentx7 = 0;
recenty7 = 0;
start7 = { x7: 0, y7: 0 },
zoom7 = document.getElementById("zoom7");

function setTransform7() {
    if (scale7 <= 0.8) {
        scale7 *= 1.06;
    }
    else if (scale7 > 4) {
        scale7 /= 1.06;
    }
    else {
        zoom7.style.transform = "translate(" + pointX7 + "px, " + pointY7 + "px) scale(" + scale7 + ")";
        recentx7 = pointX7
        recenty7 = pointY7
    }
}

zoom7.onmousedown = function (e7) {
    e7.preventDefault();
    start7 = { x7: e7.clientX - recentx7, y7: e7.clientY - recenty7 };
    panning7 = true;
}

zoom7.onmouseup = function (e7) {
    panning7 = false;
}

zoom7.onmousemove = function (e7) {
    e7.preventDefault();
    if (!panning7) {
        return;
    }
    pointX7 = (e7.clientX - start7.x7);
    pointY7 = (e7.clientY - start7.y7);
    setTransform7();
}

zoom7.onmouseout = function (e7) {
    panning7 = false;
}

zoom7.onwheel = function (e7) {
e7.preventDefault();
var xs7 = (e7.clientX - recentx7) / scale7,
ys7 = (e7.clientY - recenty7) / scale7,
delta7 = (e7.wheelDelta ? e7.wheelDelta : -e7.deltaY);
(delta7 > 0) ? (scale7 *= 1.06) : (scale7 /= 1.06);
(delta7 > 0) ? (pointX7 = 3 + e7.clientX - 0.98*xs7 * scale7) : (pointX7 = -3 + e7.clientX - 1.02*xs7 * scale7);
(delta7 > 0) ? (pointY7 = 8 + e7.clientY - 0.98*ys7 * scale7) : (pointY7 = -8 + e7.clientY - 1.02*ys7 * scale7);

setTransform7();
}
