var scale10 = 1,
panning10 = false,
pointX10 = 0,
pointY10 = 0,
recentx10 = 0;
recenty10 = 0;
start10 = { x10: 0, y10: 0 },
zoom10 = document.getElementById("zoom10");

function setTransform10() {
    if (scale10 <= 0.8) {
        scale10 *= 1.045;
    }
    else if (scale10 > 4) {
        scale10 /= 1.045;
    }
    else {
        zoom10.style.transform = "translate(" + pointX10 + "px, " + pointY10 + "px) scale(" + scale10 + ")";
        recentx10 = pointX10
        recenty10 = pointY10
    }
}

zoom10.onmousedown = function (e10) {
    e10.preventDefault();
    start10 = { x10: e10.clientX - recentx10, y10: e10.clientY - recenty10 };
    panning10 = true;
}

zoom10.onmouseup = function (e10) {
    panning10 = false;
}

zoom10.onmousemove = function (e10) {
    e10.preventDefault();
    if (!panning10) {
        return;
    }
    pointX10 = (e10.clientX - start10.x10);
    pointY10 = (e10.clientY - start10.y10);
    setTransform10();
}

zoom10.onmouseout = function (e10) {
    panning10 = false;
}

zoom10.onwheel = function (e10) {
e10.preventDefault();
var xs10 = (e10.clientX - recentx10) / scale10,
ys10 = (e10.clientY - recenty10) / scale10,
delta10 = (e10.wheelDelta ? e10.wheelDelta : -e10.deltaY);
(delta10 > 0) ? (scale10 *= 1.045) : (scale10 /= 1.045);
(delta10 > 0) ? (pointX10 = e10.clientX - 0.98*xs10 * scale10) : (pointX10 = e10.clientX - 1.02*xs10 * scale10);
(delta10 > 0) ? (pointY10 = e10.clientY - 0.98*ys10 * scale10) : (pointY10 = e10.clientY - 1.02*ys10 * scale10);

setTransform10();
}
/*var scale10 = 1,
panning10 = false,
pointX10 = 0,
pointY10 = 0,
recentX10 = 0,
recentY10 = 0,
start10 = { x10: 0, y10: 0 },
zoom10 = document.getElementById("zoom10");
zoom10.addEventListener("click", function(){increment(variable);}, false);

function setTransform10() {
    if (scale10 <= 0.8) {
        scale10 *= 1.03;
    }
    else if (scale10 > 10) {
        scale10 /= 1.03;
    }
    else {
        zoom10.style.transform = "translate(" + pointX10 + "px, " + pointY10 + "px) scale(" + scale10 + ")";
        recentX10 = pointX10
        recentY10 = pointY10
    }
}

zoom10.onmousedown = function (e10) {
e10.preventDefault();
start10 = { x10: e10.clientX - recentX10, y10: e10.clientY - recentY10 };
panning10 = true;
}

zoom10.onmouseup = function (e10) {
panning10 = false;
}

zoom10.onmousemove = function (e10) {
e10.preventDefault();
if (!panning10) {
return;
}
pointX10 = (e10.clientX - start10.x10);
pointY10 = (e10.clientY - start10.y10);
setTransform10();
}

zoom10.onwheel = function (e10) {
e10.preventDefault();
var xs10 = (e10.clientX - pointX10) / scale10,
ys10 = (e10.clientY - pointY10) / scale10,
delta10 = (e10.wheelDelta ? e10.wheelDelta : -e10.deltaY);
(delta10 > 0) ? (scale10 *= 1.03) : (scale10 /= 1.03);
(delta10 > 0) ? (pointX10 = 3 + e10.clientX - xs10 * scale10) : (pointX10 = -3 + e10.clientX - xs10 * scale10);
(delta10 > 0) ? (pointY10 = 8 + e10.clientY - ys10 * scale10) : (pointY10 = -8 + e10.clientY - ys10 * scale10);

setTransform10();
}*/