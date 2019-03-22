const path = require('path');

var count = 0;

function addNewLayer () {
    var sectionHeaderElem = document.getElementById("reservoir-section");
    var newSectionElem = document.createElement("div");
    newSectionElem.className = "subsection-wrapper";
    newSectionElem.id = `layer-${count}`;
    newSectionElem.innerHTML = `<h3>Layer Dimensions</h3>
        Length <input type="text" name="reservoir-length">
        <select name="length-list">
            <option name="length-unit-option"></option>
        </select><br>
        Width <input type="text" name="reservoir-width">
        <select name="length-list">
            <option name="length-unit-option"></option>
        </select><br>
        Height <input type="text" name="reservoir-height">
        <select name="length-list">
            <option name="length-unit-option"></option>
        </select><br><br>
        <h3>Block Dimensions</h3>
        Length <input type="text" name="block-length">
        <select name="length-list">
            <option name="length-unit-option"></option>
        </select><br>
        Width <input type="text" name="block-width">
        <select name="length-list">
            <option name="length-unit-option"></option>
        </select><br>
        Height <input type="text" name="block-height">
        <select name="length-list">
            <option name="length-unit-option"></option>
        </select><br><br>
        <h3>Rock Properties</h3>
        Absolute Permeability <input type="text" name="absolute-permeability"><br>
        Relative Permeability <input type="text" name="relative-permeability"><br>
        Porosity <input type="text" name="porosity"><br>
        Density <input type="text" name="rock-density"><br><br>
        <h3>Fluid Properties</h3>
        Viscosity <input type="text" name="viscosity"><br>
        Density <input type="text" name="fluid-density"><br><br>
        <button type="button" name="remove-layer" onclick="removeLayer(this.parentElement.id)">Delete</button>`;
    sectionHeaderElem.appendChild(newSectionElem);
    setUnits();
    count += 1;
}

function removeLayer (elemId) {
    document.getElementById("reservoir-section").removeChild(document.getElementById(elemId));
}

function setUnits () {
    const unitSystemOptions = document.getElementsByName("unit-system");
    var unitSystemOptionChecked = Array.from(unitSystemOptions).filter((e) => {
        return e.checked == true;
    })[0];

    // This is a workaround to the problem adding a layer before choosing
    // an unit system. Should be done in a different way.
    if (unitSystemOptionChecked == undefined) {
        unitSystemOptionChecked = {value: ""};
    }

    var unitSystem;
    switch (unitSystemOptionChecked.value) {
        case "si":
            unitSystem = siUnits;
            break;
        case "imperial":
            unitSystem = imperialUnits;
            break;
        case "field":
            unitSystem = fieldUnits;
            break;
        default:
            unitSystem = noUnits;
            break;
    }

    const lengthElems = document.getElementsByName("length-unit-option");
    Array.prototype.forEach.call(lengthElems, (e) => {
        e.value = unitSystem.length;
        e.innerHTML = unitSystem.length;
    })
}
