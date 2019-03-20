var count = 0;

function addFluxCondition () {
    var sectionHeaderElem = document.getElementById("flux-condition-section");
    var newSectionElem = document.createElement("div");
    newSectionElem.className = "section-wrapper";
    newSectionElem.id = `flux-condition-${count}`;
    newSectionElem.innerHTML = `<h3>Geometry</h3>
        X interval <input type="text" name="flux-condition-upper-x" placeholder="Start..."> - <input type="text" name="flux-condition-lower-x" placeholder="End..."><br>
        Y interval <input type="text" name="flux-condition-upper-y" placeholder="Start..."> - <input type="text" name="flux-condition-lower-y" placeholder="End..."><br>
        Z interval <input type="text" name="flux-condition-upper-z" placeholder="Start..."> - <input type="text" name="flux-condition-lower-z" placeholder="End..."><br><br>
        <h3>Properties</h3>
        Value <input type="text" name="flux-value"><br><br>
        <button type="button" name="remove-flux-condition" onclick="removeFluxCondition(this.parentElement.id)">Delete</button>`;
    sectionHeaderElem.appendChild(newSectionElem);
    count += 1;
}

function removeFluxCondition (elemId) {
    document.getElementById("flux-condition-section").removeChild(document.getElementById(elemId));
}
