var scale2 = 1,
panning2 = false,
pointX2 = 0,
pointY2 = 0,
recentx2 = 0;
recenty2 = 0;
start2 = { x2: 0, y2: 0 },
zoom2 = document.getElementById("zoom2");

function setTransform2() {
    if (scale2 <= 0.8) {
        scale2 *= 1.045;
    }
    else if (scale2 > 4) {
        scale2 /= 1.045;
    }
    else {
        zoom2.style.transform = "translate(" + pointX2 + "px, " + pointY2 + "px) scale(" + scale2 + ")";
        recentx2 = pointX2
        recenty2 = pointY2
    }
}

zoom2.onmousedown = function (e2) {
    e2.preventDefault();
    start2 = { x2: e2.clientX - recentx2, y2: e2.clientY - recenty2 };
    panning2 = true;
}

zoom2.onmouseup = function (e2) {
    panning2 = false;
}

zoom2.onmousemove = function (e2) {
    e2.preventDefault();
    if (!panning2) {
        return;
    }
    pointX2 = (e2.clientX - start2.x2);
    pointY2 = (e2.clientY - start2.y2);
    setTransform2();
}

zoom2.onmouseout = function (e2) {
    panning2 = false;
}

zoom2.onwheel = function (e2) {
e2.preventDefault();
var xs2 = (e2.clientX - recentx2) / scale2,
ys2 = (e2.clientY - recenty2) / scale2,
delta2 = (e2.wheelDelta ? e2.wheelDelta : -e2.deltaY);
(delta2 > 0) ? (scale2 *= 1.045) : (scale2 /= 1.045);
(delta2 > 0) ? (pointX2 = e2.clientX - 0.98*xs2 * scale2) : (pointX2 = e2.clientX - 1.02*xs2 * scale2);
(delta2 > 0) ? (pointY2 = e2.clientY - 0.98*ys2 * scale2) : (pointY2 = e2.clientY - 1.02*ys2 * scale2);

setTransform2();
}
/*var scale2 = 1,
panning2 = false,
pointX2 = 0,
pointY2 = 0,
recentX2 = 0,
recentY2 = 0,
start2 = { x2: 0, y2: 0 },
zoom2 = document.getElementById("zoom2");
zoom2.addEventListener("click", function(){increment(variable);}, false);

function setTransform2() {
    if (scale2 <= 0.8) {
        scale2 *= 1.03;
    }
    else if (scale2 > 2) {
        scale2 /= 1.03;
    }
    else {
        zoom2.style.transform = "translate(" + pointX2 + "px, " + pointY2 + "px) scale(" + scale2 + ")";
        recentX2 = pointX2
        recentY2 = pointY2
    }
}

zoom2.onmousedown = function (e2) {
e2.preventDefault();
start2 = { x2: e2.clientX - recentX2, y2: e2.clientY - recentY2 };
panning2 = true;
}

zoom2.onmouseup = function (e2) {
panning2 = false;
}

zoom2.onmousemove = function (e2) {
e2.preventDefault();
if (!panning2) {
return;
}
pointX2 = (e2.clientX - start2.x2);
pointY2 = (e2.clientY - start2.y2);
setTransform2();
}

zoom2.onwheel = function (e2) {
e2.preventDefault();
var xs2 = (e2.clientX - pointX2) / scale2,
ys2 = (e2.clientY - pointY2) / scale2,
delta2 = (e2.wheelDelta ? e2.wheelDelta : -e2.deltaY);
(delta2 > 0) ? (scale2 *= 1.03) : (scale2 /= 1.03);
(delta2 > 0) ? (pointX2 = 3 + e2.clientX - xs2 * scale2) : (pointX2 = -3 + e2.clientX - xs2 * scale2);
(delta2 > 0) ? (pointY2 = 8 + e2.clientY - ys2 * scale2) : (pointY2 = -8 + e2.clientY - ys2 * scale2);

setTransform2();
}*/