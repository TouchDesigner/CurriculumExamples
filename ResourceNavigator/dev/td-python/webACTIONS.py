"""Web Actions

Supported actions parsable from query strings
Currently all actions accept a singe arg - query string (qs_string) - 
passing responsibility for handing the qs_string object to the called
function. This matches a similar pattern found in lister, where a single
info object is reliably passed to functions.

#################################
##### Action Specifications #####
#################################

query string formatted commands that can be interpreted by TouchDesigner
to drive scripts and actions in TD.

Query strings require the following args:

* actionable:bool
* action:string (function name)
* keyWordArgsDefinedByFunction:value

examples:
?actionable=1&action=load_tox&remotePath=someUrl

?actionable=1&action=open_floating_network

?actionable=1&action=open_in_browser

?actionable=1&action=update_td_pars&somePar=someVal
"""

Navigator = op.TDCN

def load_tox(qs_results:dict) -> None:
    """
    Load TOX from URL

    Args
    ---------------
    qs_results (query_string obj)
    > query string from ULR, contains all necessary args and vals
    
    Returns
    ---------------
    None
    """

    if Navigator.ext.NavController.nav_debug.eval():
        debug("🧭 TD Navigator | loading remote")

    remote_tox = qs_results.get('remotePath')
    Navigator.ext.NavController.selected_remote_tox = remote_tox[0]
    Navigator.ext.NavController.load_new_selection()
    Navigator.ext.NavController.remove_qs_from_path() 
    pass

def open_floating_network(qs_results:dict) -> None:
    """
    Opens Floating Network Window
    
    Args
    ---------------
    qs_results (`dict`)
    > query string from ULR, contains all necessary args and vals
    
    Returns
    ---------------
    None
    """

    if Navigator.ext.NavController.nav_debug.eval():
        debug("🧭 TD Navigator | Open Floating Window")
    floating_pane = ui.panes.createFloating(name="Example")
    current_example = Navigator.ext.NavController.get_current_example()
    floating_pane.owner = current_example
    floating_pane.home()

    Navigator.ext.NavController.remove_qs_from_path()
    pass

def open_in_browser(qs_results:dict) -> None:
    """
    Open URL in web browser
    
    Args
    ---------------
    qs_results (`dict`)
    > query string from ULR, contains all necessary args and vals

    Returns
    ---------------
    None
    """

    address = Navigator.ext.NavController.web_browser.par.Address.eval()
    ui.viewFile(address)
    Navigator.ext.NavController.remove_qs_from_path()

def update_td_pars(qs_results:dict) -> None:
    """
    Update TD parameters
    
    Args
    ---------------
    qs_results (`dict`)
    > query string from ULR, contains all necessary args and vals

    Returns
    ---------------
    None
    """

    target_op = Navigator.ext.NavController.get_current_example()
    exempt_keys = ['action', 'actionable']
    for each_par, each_val in qs_results.items():
        if each_par in exempt_keys:
            pass
        else:
            try:
                target_op.par[each_par] = each_val[0]
            except Exception as e:
                pass
        
        if Navigator.ext.NavController.nav_debug.eval():
            debug(f"🧭 TD Navigator | {each_par}, {each_val}")

    Navigator.ext.NavController.remove_qs_from_path()
    pass

