function onlyUnique(value, index, array) {
    return array.indexOf(value) === index;
}

// helper function
function addCell(tr, text) {
    var td = tr.insertCell();
    td.textContent = text;
    return td;
}
