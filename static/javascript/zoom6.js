var scale6 = 1,
panning6 = false,
pointX6 = 0,
pointY6 = 0,
recentx6 = 0;
recenty6 = 0;
start6 = { x6: 0, y6: 0 },
zoom6 = document.getElementById("zoom6");

function setTransform6() {
    if (scale6 <= 0.8) {
        scale6 *= 1.045;
    }
    else if (scale6 > 4) {
        scale6 /= 1.045;
    }
    else {
        zoom6.style.transform = "translate(" + pointX6 + "px, " + pointY6 + "px) scale(" + scale6 + ")";
        recentx6 = pointX6
        recenty6 = pointY6
    }
}

zoom6.onmousedown = function (e6) {
    e6.preventDefault();
    start6 = { x6: e6.clientX - recentx6, y6: e6.clientY - recenty6 };
    panning6 = true;
}

zoom6.onmouseup = function (e6) {
    panning6 = false;
}

zoom6.onmousemove = function (e6) {
    e6.preventDefault();
    if (!panning6) {
        return;
    }
    pointX6 = (e6.clientX - start6.x6);
    pointY6 = (e6.clientY - start6.y6);
    setTransform6();
}

zoom6.onmouseout = function (e6) {
    panning6 = false;
}

zoom6.onwheel = function (e6) {
e6.preventDefault();
var xs6 = (e6.clientX - recentx6) / scale6,
ys6 = (e6.clientY - recenty6) / scale6,
delta6 = (e6.wheelDelta ? e6.wheelDelta : -e6.deltaY);
(delta6 > 0) ? (scale6 *= 1.045) : (scale6 /= 1.045);
(delta6 > 0) ? (pointX6 = e6.clientX - 0.98*xs6 * scale6) : (pointX6 = e6.clientX - 1.02*xs6 * scale6);
(delta6 > 0) ? (pointY6 = e6.clientY - 0.98*ys6 * scale6) : (pointY6 = e6.clientY - 1.02*ys6 * scale6);

setTransform6();
}
