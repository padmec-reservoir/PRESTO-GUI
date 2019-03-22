function updateToSIUnits () {
    const lengthElems = document.getElementsByName("length-unit-option");
    Array.prototype.forEach.call(lengthElems, (e) => {
        e.value = siUnits.length;
        e.innerHTML = siUnits.length;
    })
}

function updateToImperialUnits () {
    const lengthElems = document.getElementsByName("length-unit-option");
    Array.prototype.forEach.call(lengthElems, (e) => {
        e.value = imperialUnits.length;
        e.innerHTML = imperialUnits.length;
    })
}

function updateToFieldUnits () {
    const lengthElems = document.getElementsByName("length-unit-option");
    Array.prototype.forEach.call(lengthElems, (e) => {
        e.value = fieldUnits.length;
        e.innerHTML = fieldUnits.length;
    })
}

function updateToNoUnits () {
    const lengthElems = document.getElementsByName("length-unit-option");
    Array.prototype.forEach.call(lengthElems, (e) => {
        e.value = noUnits.length;
        e.innerHTML = noUnits.length;
    })
}
