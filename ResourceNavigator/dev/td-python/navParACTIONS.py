"""Navigator Parameter Actions

Function name matches the parameter name, allowing for easier 
matching of function to callback.
"""

import webFuncsMOD as webFuncs

def Resetnavigator(par):
    parent.Navigator.Navigator_reset()

def Webrenderzoom(par):
    webFuncs.Zoom_update(par.eval())

def Winopen(par):
    parent.Navigator.Floating_window(par)

def Winclose(par):
    parent.Navigator.Win_close()