var scale8 = 1,
panning8 = false,
pointX8 = 0,
pointY8 = 0,
recentx8 = 0;
recenty8 = 0;
start8 = { x8: 0, y8: 0 },
zoom8 = document.getElementById("zoom8");

function setTransform8() {
    if (scale8 <= 0.8) {
        scale8 *= 1.045;
    }
    else if (scale8 > 4) {
        scale8 /= 1.045;
    }
    else {
        zoom8.style.transform = "translate(" + pointX8 + "px, " + pointY8 + "px) scale(" + scale8 + ")";
        recentx8 = pointX8
        recenty8 = pointY8
    }
}

zoom8.onmousedown = function (e8) {
    e8.preventDefault();
    start8 = { x8: e8.clientX - recentx8, y8: e8.clientY - recenty8 };
    panning8 = true;
}

zoom8.onmouseup = function (e8) {
    panning8 = false;
}

zoom8.onmousemove = function (e8) {
    e8.preventDefault();
    if (!panning8) {
        return;
    }
    pointX8 = (e8.clientX - start8.x8);
    pointY8 = (e8.clientY - start8.y8);
    setTransform8();
}

zoom8.onmouseout = function (e8) {
    panning8 = false;
}

zoom8.onwheel = function (e8) {
e8.preventDefault();
var xs8 = (e8.clientX - recentx8) / scale8,
ys8 = (e8.clientY - recenty8) / scale8,
delta8 = (e8.wheelDelta ? e8.wheelDelta : -e8.deltaY);
(delta8 > 0) ? (scale8 *= 1.045) : (scale8 /= 1.045);
(delta8 > 0) ? (pointX8 = e8.clientX - 0.98*xs8 * scale8) : (pointX8 = e8.clientX - 1.02*xs8 * scale8);
(delta8 > 0) ? (pointY8 = e8.clientY - 0.98*ys8 * scale8) : (pointY8 = e8.clientY - 1.02*ys8 * scale8);

setTransform8();
}
