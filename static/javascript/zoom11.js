var scale11 = 1,
panning11 = false,
pointX11 = 0,
pointY11 = 0,
recentx11 = 0;
recenty11 = 0;
start11 = { x11: 0, y11: 0 },
zoom11 = document.getElementById("zoom11");

function setTransform11() {
    if (scale11 <= 0.8) {
        scale11 *= 1.06;
    }
    else if (scale11 > 4) {
        scale11 /= 1.06;
    }
    else {
        zoom11.style.transform = "translate(" + pointX11 + "px, " + pointY11 + "px) scale(" + scale11 + ")";
        recentx11 = pointX11
        recenty11 = pointY11
    }
}

zoom11.onmousedown = function (e11) {
    e11.preventDefault();
    start11 = { x11: e11.clientX - recentx11, y11: e11.clientY - recenty11 };
    panning11 = true;
}

zoom11.onmouseup = function (e11) {
    panning11 = false;
}

zoom11.onmousemove = function (e11) {
    e11.preventDefault();
    if (!panning11) {
        return;
    }
    pointX11 = (e11.clientX - start11.x11);
    pointY11 = (e11.clientY - start11.y11);
    setTransform11();
}

zoom11.onmouseout = function (e11) {
    panning11 = false;
}

zoom11.onwheel = function (e11) {
e11.preventDefault();
var xs11 = (e11.clientX - recentx11) / scale11,
ys11 = (e11.clientY - recenty11) / scale11,
delta11 = (e11.wheelDelta ? e11.wheelDelta : -e11.deltaY);
(delta11 > 0) ? (scale11 *= 1.06) : (scale11 /= 1.06);
(delta11 > 0) ? (pointX11 = 3 + e11.clientX - 0.98*xs11 * scale11) : (pointX11 = -3 + e11.clientX - 1.02*xs11 * scale11);
(delta11 > 0) ? (pointY11 = 8 + e11.clientY - 0.98*ys11 * scale11) : (pointY11 = -8 + e11.clientY - 1.02*ys11 * scale11);

setTransform11();
}
