# First try to extract basic info from an IFC file and create an HTML file from this.
# This is focused on the use case of tall buildings
# The idea is that it can read the IFC and give a simple 2d representation
# This can then be used to provide feedback to the user.
# It can also be displayed on the users homepage and in their teams group.

# obviously we need to ...
import ifcopenshell

# get the IFC file
model = ifcopenshell.open("model/Duplex_A_20110907_optimized.ifc")
# model = ifcopenshell.open("model/Office_A_20110811_optimized.ifc")
# model = ifcopenshell.open("model/F21_80_3W_Team01_Sub1.ifc")

# create an HTML file to write to
f = open("output/index.html", "w")
cont=""

# variable for to store the elevation of the site
site_elev = 0

# ---- start of standard HTML, this could probably just be read from a file.


# start the indent of the HTML file
indent = 0

# ADD HTML
cont+=0*"\t"+"<html>\n"

# ADD HEAD
cont+=1*"\t"+"<head>\n"
cont+=2*"\t"+"<link rel='stylesheet' href='css/html-build.css'></link>\n"
cont+=2*"\t"+"<!--- put some links in here...--->\n"
cont+=1*"\t"+"</head>\n"

# ADD BODY
cont+=1*"\t"+"<body>\n"



# ---- end of standard HTML

# ---- start of custom HTML entities

# TODO: How to know the level of indent?
# TODO: Can we make these in functions?

# ADD PROJECT
project = model.by_type('IfcProject')[0]
cont+=2*"\t"+"<project- name=\"{d}\">\n".format(d=project.LongName)
# it looks like it would make sense to use the DOM here and append stuff to it...

# ADD SITE
site = model.by_type('IfcSite')[0]
site_elev = site.RefElevation
cont+=3*"\t"+"<site- lat=\"{}\" long=\"{}\" elev=\"{}\">\n".format(site.RefLatitude,site.RefLongitude,site_elev )

# ADD BUILDING
cont+=4*"\t"+"<building->\n"

# ADD CORE - I know its not normal,  but I think it might be useful...
cont+=5*"\t"+"<core->\n"

# ADD FLOOR(S)
floors = model.by_type('IfcBuildingStorey')
floors.sort(key=lambda x: x.Elevation, reverse=True)

for floor in floors:
    # check if floor is lower than elevation...
    # TODO: we need to sort these, IFC doesn't do it automatically...
    
    if (site_elev == floor.Elevation):
        cont+=6*"\t"+"<floor- class=\"floor_ground\" elev=\"{}\" >{}</floor->\n".format(floor.Elevation, floor.Name)
    elif (site_elev < floor.Elevation):
        cont+=6*"\t"+"<floor- class=\"floor_upper\" elev=\"{}\" >{}</floor->\n".format(floor.Elevation, floor.Name)
    else:
        cont+=6*"\t"+"<floor- class=\"floor_lower\" elev=\"{}\" >{}</floor->\n".format(floor.Elevation, floor.Name)

# CLOSE IT ALL
cont+=5*"\t"+"</core->\n"
cont+=4*"\t"+"</building->\n"
cont+=3*"\t"+"</site->\n"
cont+=2*"\t"+"</project->\n"
cont+=1*"\t"+"</body>\n"
cont+=0*"\t"+"</html>\n"

# WRITE IT OUT
f.write(cont)
f.close()

# TELL EVERYONE ABOUT IT
print("html build complete")

# functions here ...

def floors():
  print("Hello from a function")



