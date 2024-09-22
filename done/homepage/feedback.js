function onoff() {
    
    let btn1 = document.getElementById('beform');
    let btn2 = document.getElementById('afform');
    let edit1 = (btn1.style.display == 'none'?'block':'none');
    btn1.style.display = edit1;
    let edit2 = (btn2.style.display == 'none'?'block':'none');
    btn2.style.display = edit2;
    return false;
}

let stat = 0;

document.addEventListener('DOMContentLoaded', function() {
    if (stat == 0) {
        let tagEdit = document.getElementById('afform');
        let newDisplay = (tagEdit.style.display == 'none'?'block':'none');
        tagEdit.style.display = newDisplay;
    };
    document.getElementById('btn01').onclick = onoff;
    document.getElementById('btn02').onclick = onoff;
});
