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

?actionable=1&action=download_manifest&manifest=someUrl&dirName=someDirName
"""

import os
import pathlib
import requests

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

def download_manifest(qs_results:dict) -> None:
    manifest = qs_results.get('manifest')[0]
    dir_name = qs_results.get('dirName')[0]
    print(dir_name)
    user_palette_dir = pathlib.Path(app.userPaletteFolder)
    cache_folder = user_palette_dir.parent.absolute()
    nav_root_path = f'{cache_folder}\\navigator'
    download_path = f'{cache_folder}\\navigator\\{dir_name}'

    if manifest != None:
        
        # check to see if directory exists
        if os.path.isdir(download_path):
            print('🧭 TD Navigator | navigator root path exists')
        
        else:
            # create root dir if it does not yet exist
            os.makedirs(download_path, exist_ok=True)
            print('🧭 TD Navigator | navigator root path does not exist, creating dir')
        
        # generate asset list        
        # request data
        request = requests.get(manifest)

        # check status code
        if request.status_code == 200:
            manifest_text = request.text
            lines = manifest_text.splitlines()
            tox_links = [each_line for each_line in lines if each_line[0:4] == 'http']

            for each_link in tox_links:
                print(each_link.split('/')[-1])

            # download files
            Navigator.op('base_threaded_downloader').par.Cachelocation = download_path
            Navigator.op('base_threaded_downloader').Fetch_files(tox_links)

            # callback to open a file explorer
            def buttonChoice(info):
                if info['buttonNum'] == 2:
                    ui.viewFile(download_path)
                else:
                    pass
            
            # opens a popdialog to alert the user about the download
            op.TDResources.PopDialog.OpenDefault(
                title = 'Downloading Example TOX Files',
                text='The Navigator is currently caching TOX examples for offline review',
                buttons=['Close', 'Open'],
                callback=buttonChoice,
                textEntry=False,
                escOnClickAway=False
            )
            # clear qs from path
            Navigator.ext.NavController.remove_qs_from_path()
        pass
    pass