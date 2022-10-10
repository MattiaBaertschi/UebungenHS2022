
function uhr() {
    var d = new Date();
    var ds = d.toDateString();
    var ts = d.toTimeString();

    var uhr = document.querySelector("#time");
    var dat = document.querySelector("#date");

    uhr.innerHTML = ts;
    dat.innerHTML = ds;
    setTimeout(uhr,500);
}