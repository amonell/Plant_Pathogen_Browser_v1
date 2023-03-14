var scale9 = 1,
panning9 = false,
pointX9 = 0,
pointY9 = 0,
recentx9 = 0;
recenty9 = 0;
start9 = { x9: 0, y9: 0 },
zoom9 = document.getElementById("zoom9");

function setTransform9() {
    if (scale9 <= 0.8) {
        scale9 *= 1.06;
    }
    else if (scale9 > 4) {
        scale9 /= 1.06;
    }
    else {
        zoom9.style.transform = "translate(" + pointX9 + "px, " + pointY9 + "px) scale(" + scale9 + ")";
        recentx9 = pointX9
        recenty9 = pointY9
    }
}

zoom9.onmousedown = function (e9) {
    e9.preventDefault();
    start9 = { x9: e9.clientX - recentx9, y9: e9.clientY - recenty9 };
    panning9 = true;
}

zoom9.onmouseup = function (e9) {
    panning9 = false;
}

zoom9.onmousemove = function (e9) {
    e9.preventDefault();
    if (!panning9) {
        return;
    }
    pointX9 = (e9.clientX - start9.x9);
    pointY9 = (e9.clientY - start9.y9);
    setTransform9();
}

zoom9.onmouseout = function (e9) {
    panning9 = false;
}

zoom9.onwheel = function (e9) {
e9.preventDefault();
var xs9 = (e9.clientX - recentx9) / scale9,
ys9 = (e9.clientY - recenty9) / scale9,
delta9 = (e9.wheelDelta ? e9.wheelDelta : -e9.deltaY);
(delta9 > 0) ? (scale9 *= 1.06) : (scale9 /= 1.06);
(delta9 > 0) ? (pointX9 = 3 + e9.clientX - 0.98*xs9 * scale9) : (pointX9 = -3 + e9.clientX - 1.02*xs9 * scale9);
(delta9 > 0) ? (pointY9 = 8 + e9.clientY - 0.98*ys9 * scale9) : (pointY9 = -8 + e9.clientY - 1.02*ys9 * scale9);

setTransform9();
}
