"""Pane Controls

Controls for pane manipulation
"""

# global op shortcut to TouchDesigner Curriculum Navigator
Navigator = op.TDCN

#####################################################
## PANE CONTROLS
#####################################################

def Save_tox_copy(par):
    """Saves a copy of the tox being viewed
    
    This is called from the navigator "Save" Button
    """
    if par.eval():
        print("🧭 TD Navigator | Save TOX copy")

        disp_buffer = Navigator.disp_buffer
        current_example = disp_buffer.findChildren(type=containerCOMP)[0]
        save_ready_tox = _copy_current_example(current_example)

        tox_path = ui.chooseFile(
            load=False, 
            start=f"{current_example}.tox", 
            fileTypes=['tox'], 
            title='Save Current TOX')
        
        # set hmode, vmode, width, and height for containers
        if save_ready_tox.type == 'container':
            save_ready_tox.par.hmode = 0
            save_ready_tox.par.vmode = 0
            save_ready_tox.par.w = 1080
            save_ready_tox.par.h = 1080
        else:
            pass

        save_ready_tox.save(tox_path)
        save_ready_tox.destroy()

def Set_view(state, view_type):
    """
    """
    if state:
        example_pane = ui.panes['NavigatorExample']

        if view_type == 'panel':
            example_pane.owner = Navigator.ext.NavController.view
            example_pane.changeType(PaneType.PANEL)

        elif view_type == 'network':
            current_example = Navigator.ext.NavController.disp_buffer.findChildren(type=containerCOMP)[0]
            example_pane.owner = current_example
            example_pane.changeType(PaneType.NETWORKEDITOR)
            ui.panes['NavigatorExample'].home()
        
        elif view_type == 'floating':
            # TODO - complete floating window call
            Open_floating()

        else:
            pass

def _copy_current_example(example):
    """Creates a copy of the current tox
    """
    copied_tox = op('/sys/quiet').copy(example)
    copied_tox.nodeX = 0
    copied_tox.nodeY = 200
    return copied_tox

def Win_close() -> None:
    ui.panes['Navigator'].close()
    ui.panes['NavigatorExample'].close()

def Open_floating() -> None:
    """
    Opens Floating Network Window
    
    Args
    ---------------
    None


    """

    if Navigator.ext.NavController.nav_debug.eval():
        debug("🧭 TD Navigator | Open Floating Window")
    floating_pane = ui.panes.createFloating(name="Example")
    current_example = Navigator.ext.NavController.get_current_example()
    floating_pane.owner = current_example
    floating_pane.home()

def Comment_focus_change(menu_index:int) -> None:
    """

    """
    #skip when menu_index is '' 
    if menu_index == '':
        pass
    
    # action based on menu index
    else:
        current_example = Navigator.Current_example

        comments = current_example.findChildren(type=annotateCOMP, depth=1)
        target_op = current_example.par.Comments.menuNames[menu_index]
        
        op(target_op).current = True

        for each_annotate in comments:
            each_annotate.selected = False

        if ui.panes['NavigatorExample'].type == PaneType.NETWORKEDITOR:
            ui.panes['NavigatorExample'].homeSelected()
        
        else:
            Set_view(True, 'network')
            ui.panes['NavigatorExample'].homeSelected()

