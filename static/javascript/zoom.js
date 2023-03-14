
var scale = 1,
panning = false,
pointX = 0,
pointY = 0,
recentx = 0;
recenty = 0;
start = { x: 0, y: 0 },
zoom = document.getElementById("zoom");

function setTransform() {
    if (scale <= 0.8) {
        scale *= 1.06;
    }
    else if (scale > 4) {
        scale /= 1.06;
    }
    else {
        zoom.style.transform = "translate(" + pointX + "px, " + pointY + "px) scale(" + scale + ")";
        recentx = pointX
        recenty = pointY
    }
}

zoom.onmousedown = function (e) {
e.preventDefault();
start = { x: e.clientX - recentx, y: e.clientY - recenty };
panning = true;
}

zoom.onmouseup = function (e) {
panning = false;
}

zoom.onmouseout = function (e) {
    panning = false;
}

zoom.onmousemove = function (e) {
e.preventDefault();
if (!panning) {
return;
}
pointX = (e.clientX - start.x);
pointY = (e.clientY - start.y);
setTransform();
}

zoom.onwheel = function (e) {
e.preventDefault();
var xs = (e.clientX - recentx) / scale,
ys = (e.clientY - recenty) / scale,
delta = (e.wheelDelta ? e.wheelDelta : -e.deltaY);
(delta > 0) ? (scale *= 1.06) : (scale /= 1.06);
(delta > 0) ? (pointX = e.clientX - 0.98*xs * scale) : (pointX = e.clientX - 1.02*xs * scale);
(delta > 0) ? (pointY = e.clientY - 0.98*ys * scale) : (pointY = e.clientY - 1.02*ys * scale);

setTransform();
}