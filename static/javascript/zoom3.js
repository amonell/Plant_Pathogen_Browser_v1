var scale3 = 1,
panning3 = false,
pointX3 = 0,
pointY3 = 0,
recentx3 = 0;
recenty3 = 0;
start3 = { x3: 0, y3: 0 },
zoom3 = document.getElementById("zoom3");

function setTransform3() {
    if (scale3 <= 0.8) {
        scale3 *= 1.06;
    }
    else if (scale3 > 4) {
        scale3 /= 1.06;
    }
    else {
        zoom3.style.transform = "translate(" + pointX3 + "px, " + pointY3 + "px) scale(" + scale3 + ")";
        recentx3 = pointX3
        recenty3 = pointY3
    }
}

zoom3.onmousedown = function (e3) {
    e3.preventDefault();
    start3 = { x3: e3.clientX - recentx3, y3: e3.clientY - recenty3 };
    panning3 = true;
}

zoom3.onmouseup = function (e3) {
    panning3 = false;
}

zoom3.onmousemove = function (e3) {
    e3.preventDefault();
    if (!panning3) {
        return;
    }
    pointX3 = (e3.clientX - start3.x3);
    pointY3 = (e3.clientY - start3.y3);
    setTransform3();
}

zoom3.onmouseout = function (e3) {
    panning3 = false;
}

zoom3.onwheel = function (e3) {
e3.preventDefault();
var xs3 = (e3.clientX - recentx3) / scale3,
ys3 = (e3.clientY - recenty3) / scale3,
delta3 = (e3.wheelDelta ? e3.wheelDelta : -e3.deltaY);
(delta3 > 0) ? (scale3 *= 1.06) : (scale3 /= 1.06);
(delta3 > 0) ? (pointX3 = 3 + e3.clientX - 0.98*xs3 * scale3) : (pointX3 = -3 + e3.clientX - 1.02*xs3 * scale3);
(delta3 > 0) ? (pointY3 = 8 + e3.clientY - 0.98*ys3 * scale3) : (pointY3 = -8 + e3.clientY - 1.02*ys3 * scale3);

setTransform3();
}
