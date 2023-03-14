var scale5 = 1,
panning5 = false,
pointX5 = 0,
pointY5 = 0,
recentx5 = 0;
recenty5 = 0;
start5 = { x5: 0, y5: 0 },
zoom5 = document.getElementById("zoom5");

function setTransform5() {
    if (scale5 <= 0.8) {
        scale5 *= 1.06;
    }
    else if (scale5 > 4) {
        scale5 /= 1.06;
    }
    else {
        zoom5.style.transform = "translate(" + pointX5 + "px, " + pointY5 + "px) scale(" + scale5 + ")";
        recentx5 = pointX5
        recenty5 = pointY5
    }
}

zoom5.onmousedown = function (e5) {
    e5.preventDefault();
    start5 = { x5: e5.clientX - recentx5, y5: e5.clientY - recenty5 };
    panning5 = true;
}

zoom5.onmouseup = function (e5) {
    panning5 = false;
}

zoom5.onmousemove = function (e5) {
    e5.preventDefault();
    if (!panning5) {
        return;
    }
    pointX5 = (e5.clientX - start5.x5);
    pointY5 = (e5.clientY - start5.y5);
    setTransform5();
}

zoom5.onmouseout = function (e5) {
    panning5 = false;
}

zoom5.onwheel = function (e5) {
e5.preventDefault();
var xs5 = (e5.clientX - recentx5) / scale5,
ys5 = (e5.clientY - recenty5) / scale5,
delta5 = (e5.wheelDelta ? e5.wheelDelta : -e5.deltaY);
(delta5 > 0) ? (scale5 *= 1.06) : (scale5 /= 1.06);
(delta5 > 0) ? (pointX5 = e5.clientX - 0.98*xs5 * scale5) : (pointX5 = e5.clientX - 1.02*xs5 * scale5);
(delta5 > 0) ? (pointY5 = e5.clientY - 0.98*ys5 * scale5) : (pointY5 = e5.clientY - 1.02*ys5 * scale5);

setTransform5();
}
