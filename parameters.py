parameter_list = [["Area", "Area"], ["Altura", "Length"],
                  ["Pressao inicial", "Pressure"],
                  ["Pressao barometrica", "Pressure"],
                  ["Porosidade", "Dimensionless"],
                  ["Permeabilidade", "Dimensionless"]]
units_systems = ["SI", "Imperial Units", "Field Units"]
si_units = {"Area": ["meter ** 2"],
            "Density": ["kilogram / meter ** 3"],
            "Length": ["meter"],
            "Mass Flow": ["kilogram / second"],
            "Pressure": ["Pa"],
            "Volume": ["meter ** 3"],
            "Volume Flow": ["meter ** 3 / second"],
            "Weigth": ["kilogram"],
            "Weigth per Length": ["kilogram / meter"],
            "Time": ["second", "minute", "hour", "day", "year"],
            "Viscosity": ["pascal * second"],
            "Dimensionless": [""]}
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
                  "Dimensionless": [""]}
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
               "Dimensionless": [""]}
start_unit = {"Area": "",
              "Density": "",
              "Length": "",
              "Mass Flow": "",
              "Pressure": "",
              "Volume": "",
              "Volume Flow": "",
              "Mass": "",
              "Mass per Length": "",
              "Time": "",
              "Viscosity": "",
              "Dimensionless": ""}
