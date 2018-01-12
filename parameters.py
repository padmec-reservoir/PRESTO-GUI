problem = []
model = ["Monophasic", "Two Phase", "Compositional", "Black Oil"]
geometry = [["Length X", "Length"], ["Length Y", "Length"],
            ["Length Z", "Length"]]
well = [["X", "Length"], ["Y", "Length"], ["Z", "Length"],
        ["Diameter", "Length"], ["Rate", "Pressure"]]
properties = []
initial_conditions = [["Initial Pressure", "Pressure"],
                      ["Initial Saturation", "Dimensionless"]]
boundary = []
method = ["Finite Difference"]
output = []
dimensionality = ["1D", "2D", "3D"]
units_systems = ["SI", "Imperial Units", "Field Units"]
reservoir = [["Area", "Area"], ["Height", "Length"]]
mesh = [["Blocks in X", "Dimensionless"], ["Blocks in Y", "Dimensionless"],
        ["Blocks in Z", "Dimensionless"]]
rock = [["Absolute Permeability", "Permeability"],
        ["Relative Permeability", "Permeability"],
        ["Porosity", "Dimensionless"], ["Density", "Density"]]
fluids = [["Oil Viscosity", "Viscosity"], ["Oil Density", "Density"],
          ["Water Viscosity", "Viscosity"], ["Water Density", "Density"],
          ["Gas Viscosity", "Viscosity"], ["Gas Density", "Density"]]
injection_producer = []
aquifer = []
interval = [["From", "Time"], ["To", "Time"]]
variables = ["Water Saturation", "Oil Saturation", "Gas Saturation",
             "Pressure Field"]
entries = {"Problem": ["Dimensionality", "Unit System"],
           "Physical/Mathematical Model": ["Reservoir"],
           "Geometry": ["Mesh"],
           "Wells (Geometry)": [],
           "Physical Properties": ["Rock", "Fluid"],
           "Initial Conditions": [],
           "Boundary Conditions": ["Injection/Producer", "Aquifer"],
           "Numerical Methods": [],
           "Output Configuration": ["Interval", "Variables"]}

si_units = {"Area": ["meter ** 2"],
            "Density": ["kilogram / meter ** 3"],
            "Length": ["meter"],
            "Mass Flow": ["kilogram / second"],
            "Pressure": ["Pa"],
            "Volume": ["meter ** 3"],
            "Volume Flow": ["meter ** 3 / second"],
            "Mass": ["kilogram"],
            "Mass per Length": ["kilogram / meter"],
            "Time": ["second", "minute", "hour", "day", "year"],
            "Viscosity": ["pascal * second"],
            "Permeability": ["millidarcy"],
            "Dimensionless": []}
imperial_units = {"Area": ["acre", "square_foot", "square_yard"],
                  "Density": ["pound / gallon", "pound / foot ** 3"],
                  "Length": ["foot", "inch", "yard"],
                  "Mass Flow": ["pound / day", "ounce / day"],
                  "Pressure": ["psi"],
                  "Volume": ["gallon", "foot ** 3", "yard ** 3"],
                  "Volume Flow": ["foot ** 3 / day", "gallon / day"],
                  "Mass": ["pound", "ounce"],
                  "Mass per Length": ["pound / foot", "pound / inch"],
                  "Time": ["second", "minute", "hour", "day", "year"],
                  "Viscosity": ["centipoise"],
                  "Permeability": ["millidarcy"],
                  "Dimensionless": []}
field_units = {"Area": ["acre"],
               "Density": ["pound / barrel", "gram / centimeter ** 3"],
               "Length": ["foot"],
               "Mass Flow": ["pound / day"],
               "Pressure": ["psi"],
               "Volume": ["barrel", "foot ** 3"],
               "Volume Flow": ["barrel / day", "foot ** 3 / day"],
               "Mass": ["pound"],
               "Mass per Length": ["pound / foot"],
               "Time": ["second", "minute", "hour", "day", "year"],
               "Viscosity": ["centipoise"],
               "Permeability": ["millidarcy"],
               "Dimensionless": []}
start_unit = {"Area": set(),
              "Density": set(),
              "Length": set(),
              "Mass Flow": set(),
              "Pressure": set(),
              "Volume": set(),
              "Volume Flow": set(),
              "Mass": set(),
              "Mass per Length": set(),
              "Time": set(),
              "Viscosity": set(),
              "Permeability": set(),
              "Dimensionless": set()}
