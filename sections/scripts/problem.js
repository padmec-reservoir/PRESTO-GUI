// TODO: Rename this module according to conventions. It will not remain
// as the renderer script for problem.html file.

var siUnits = {
    length: "m",
    time: "s",
    mass: "kg",
    area: "m**2",
    volume: "m**3",
    pressure: "Pa",
    viscosity: "Pa*s",
    permeability: "mD",
    density: "kg/m**3",
    massFlow: "kg/s",
    volumeFlow: "m**3/s"
};

var imperialUnits = {
    length: "ft",
    time: "s",
    mass: "lb",
    area: "ft**2",
    volume: "ft**3",
    pressure: "psi",
    viscosity: "cP",
    permeability: "mD",
    density: "lb/ft**3",
    massFlow: "lb/s",
    volumeFlow: "ft**3/s"
};

var fieldUnits = {
    length: "ft",
    time: "s",
    mass: "lb",
    area: "ac",
    volume: "barrel",
    pressure: "psi",
    viscosity: "cP",
    permeability: "mD",
    density: "lb/barrel",
    massFlow: "lb/s",
    volumeFlow: "barrel/s"
};

var noUnits = {
    length: "",
    time: "",
    mass: "",
    area: "",
    volume: "",
    pressure: "",
    viscosity: "",
    permeability: "",
    density: "",
    massFlow: "",
    volumeFlow: ""
}

module.exports = {
    siUnits: siUnits,
    imperialUnits: imperialUnits,
    fieldUnits: fieldUnits,
    noUnits: noUnits
};
