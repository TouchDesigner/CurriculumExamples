"""Web Browser COMP helpers
"""

Navigator = op.TDCN

def Zoom_update(zoom_level) -> None:
    """
    Update web render zoom level

    Args
    ---------------
    zoom_level (int)
    > The target zoom level for the webrender TOP
    """
    Navigator.ext.NavController.web_browser.op('webrender1').executeJavaScript(f"document.body.style.zoom = '{zoom_level}%'")

def Zoom_increment(increment_val) -> None:
    """Increments zoom value"""
    prev_val = Navigator.par.Webrenderzoom.eval()
    Navigator.par.Webrenderzoom = increment_val + prev_val

def Zoom_reset(val) -> None:
    """Resets webbrowser soom"""
    Navigator.par.Webrenderzoom = val
