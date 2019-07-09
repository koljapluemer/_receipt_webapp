function changeInput(inputField, changeTo) {
    // Input-Feld ändern
    document.getElementById(inputField).value = changeTo;
    // Tabellenfeldfunktion aufrufen, wenn Button geklickt wird
    associatedCell = inputField.replace("input", "table");
    updateTable(associatedCell, changeTo);
}

// Tabellenzelle aktualisieren. Kann auch aus Template direkt über onChange verwendet werden
function updateTable(tableCell, changeTo) {
    document.getElementById(tableCell).innerHTML = changeTo;
}