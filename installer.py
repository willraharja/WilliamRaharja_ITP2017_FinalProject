
#Using cx_Freeze module

import cx_Freeze

#Importing os module

import os

#Get the TCL and TK directories

os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python36\tcl\tcl8.6'

os.environ['TK_LIBRARY'] = r'C:\Program Files\Python36\tcl\tk8.6'

#Variable to select which file that you want to have Its executable file

executing=[cx_Freeze.Executable("Praktikum hit the fuhrer.py")]

#Run cx_Freeze and create needed files to run apps

cx_Freeze.setup(

    #Name of installer

    name="Shoot the Fuhrer",

    #Describe the included files and packages

    options={"build_exe":{"packages":["pygame"],

                          "include_files":["adolf.png","Animated_Pistol.gif","Animated_Pistol1.png","Animated_Pistol2.png",

                                           "Gunfire.wav","LemonMilk.otf",

                                           "Wolfenstein.jpg"]}},

    #Select the files that will have its executable file

    executables = executing,

    #Describe the version of program

    version='1.0.0'

)
