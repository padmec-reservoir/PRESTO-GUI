var count = 0;

function addWell () {
    var sectionHeaderElem = document.getElementById("wells-section");
    var newSectionElem = document.createElement("div");
    newSectionElem.className = "section-wrapper";
    newSectionElem.id = `well-${count}`;
    newSectionElem.innerHTML = `<h3>Label</h3>
        <input type="text" name="well-label" value="Well ${count}"><br><br>
        <h3>Geometry</h3>
        X location <input type="text" name="well-x-location"><br>
        Y location <input type="text" name="well-y-location"><br>
        Area <input type="text" name="well-area"><br>
        Height <input type="text" name="well-height"><br><br>
        <h3>Properties</h3>
        <input type="radio" name="well-type" value="injection"> Injection <input type="radio" name="well-type" value="production"> Production <br>
        Pressure <input type="text" name="well-pressure"><br><br>
        <button type="button" name="remove-well" onclick="removeWell(this.parentElement.id)">Remove well</button>`;
    sectionHeaderElem.appendChild(newSectionElem);
    count += 1;
}

function removeWell (elemId) {
    document.getElementById("wells-section").removeChild(document.getElementById(elemId));
}
