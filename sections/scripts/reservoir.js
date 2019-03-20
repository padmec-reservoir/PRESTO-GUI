var count = 0;
function addNewLayer () {
    var sectionHeaderElem = document.getElementById("reservoir-section");
    var newSectionElem = document.createElement("div");
    newSectionElem.className = "section-wrapper";
    newSectionElem.id = `layer-${count}`;
    newSectionElem.innerHTML = '<h3>Layer Dimensions</h3>Length <input type="text" name="reservoir-length"><br>Width <input type="text" name="reservoir-width"><br>Height <input type="text" name="reservoir-height"><br><br><h3>Block Dimensions</h3>Length <input type="text" name="block-length"><br>Width <input type="text" name="block-width"><br>Height <input type="text" name="block-height"><br><br><h3>Rock Properties</h3>Absolute Permeability <input type="text" name="absolute-permeability"><br>Relative Permeability <input type="text" name="relative-permeability"><br>Porosity <input type="text" name="porosity"><br>Density <input type="text" name="rock-density"><br><br><h3>Fluid Properties</h3>Viscosity <input type="text" name="viscosity"><br>Density <input type="text" name="fluid-density"><br><br><button type="button" name="remove-layer" onclick="removeLayer(this.parentElement.id)">Delete</button>';
    sectionHeaderElem.appendChild(newSectionElem);
    count += 1;
}
function removeLayer (elemId) {
    document.getElementById("reservoir-section").removeChild(document.getElementById(elemId));
}
