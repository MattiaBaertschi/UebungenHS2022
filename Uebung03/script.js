function text() {
    var randcol = Math.floor(Math.random()*10303304).toString(16);
    var eing = document.querySelector("#src");
    var ausg = document.querySelector("#text");

    ausg.innerHTML = eing.value;
    ausg.style["color"] = "#"+randcol;
    
}

