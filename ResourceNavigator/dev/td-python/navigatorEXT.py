import urllib.request
import requests as Requests
import parserActionsMOD
import paneControlsMOD

class NavController:
    """
    Extension for managing the Curriculum Navigator

    Notes
    ---------------

    TD Palette Dependencies
    - webBrowser==1.1

    The NavController uses the webBrowser palette component to render
    a rich text experience alongside a TouchDesigner example. The Navigator component
    loads and fetches a TOX from a remote source, and loads it dynamically into
    a lightweight shell experience. This keeps all TOX elements outside of the 
    component context, ensuring that fetched examples are always the 
    most recently updated.

    debug() is largely preferred over print() in this extension, relying on the 
    Navigator COMP's Debug parameter to control outputting messages to the 
    text-port. 

    Navigator loading and web-interaction is driven by a query string model 
    for providing data to the webBrowser context to be interpreted by TouchDesigner.
    Query string parsing is handled by the Python built-in library urllib to provide
    for simplified support across platforms.

    This extension utilizes additional modules that have been broken out of the main
    extension:

    - parserActionsMOD
        Parsing mechanics and function-lookup map for handling incoming 
        query string requests.

    - paneControlsMOD
        Controls for pane manipulation

    - webACTIONS
        Supported actions parsable from query strings
        Currently all actions accept a singe arg - query string (qs_string) - 
        passing responsibility for handing the qs_string object to the called
        function. This matches a similar pattern found in lister, where a single
        info object is reliably passed to functions.
    """

    NavigatorCOMP = parent.Navigator
    view = parent.Navigator.op('container_ui/container_view')
    nav_and_text = parent.Navigator.op('container_ui/container_nav_and_text')
    web_browser = parent.Navigator.op('container_ui/container_nav_and_text/webBrowser')
    loading_view = parent.Navigator.op('container_ui/container_view/container_loading')
    settings_view = parent.Navigator.op('container_ui/container_view/container_settings')
    disp_buffer = parent.Navigator.op('container_ui/container_view/container_display_buffer')
    trans_timer = parent.Navigator.op('container_ui/container_view/container_loading/timer1')

    nav_debug = parent.Navigator.par.Debug

    nav_header = parent.Navigator.op('base_assets/Navigator')
    nav_example_header = parent.Navigator.op('base_assets/NavigatorExample')

    def __init__(self, ownerOp):
        """
        EXT Init 


        Args
        ---------------
        ownerOp (TD_operator)
        > The TouchDesigner operator initialzing this ext, usually `me`

        Returns
        ---------------
        None        
        '''
        
        self.Owner_op = ownerOp
        self.selected_remote_tox = None
        self._check_pane_assets()


    def Url_update(self, url) -> None:
        '''
        Updates webrender TOP URL

        Args
        ---------------
        url (str)
        > The URL from the webBrowser COMP

        """

        qs_result = self.query_string_parse(url)
        key_list = [key for key in qs_result.keys()]

        # check for the actionable arg
        if qs_result.get('actionable', [0])[0] == '1':
            parserActionsMOD.Web_action(qs_result)
        else:
            pass

        pass

    def get_current_example(self):
        """
        Get current example

        Returns
        ---------------
        current_example (TD_operator)
        > The current component loaded in the Navigator's display buffer COMP
        """

        current_example = parent.Navigator.op('container_ui/container_view/container_display_buffer').findChildren(depth=1)[0]
        return current_example

    def remove_qs_from_path(self):
        """
        Remove query string from URL path

        """

        if NavController.nav_debug.eval():
            debug("🧭 TD Navigator | remove QS from Path")

        address = NavController.web_browser.par.Address.eval()
        cleanAddress = self.clean_url(address)
        NavController.web_browser.par.Address = cleanAddress
    
    def clean_url(self, url):
        """
        Clean up a URL

        Removes dangling query strings from path.

        Args
        ---------------
        url (str)
        > The URL from the webBrowser COMP


        Returns
        ---------------
        url (str)
        > URL with all query strings removed
        """
        return urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)

    def load_new_selection(self):
        """
        Load selection

        """

        if NavController.nav_debug.eval():
            debug("🧭 TD Navigator | loading new selection")

        self.Set_view(True, "panel")

        NavController.loading_view.par['display'] = True
        self.display_loading_screen()

    def display_loading_screen(self):
        """
        Display loading screen during load

        """

        if NavController.nav_debug.eval():
            debug("🧭 TD Navigator | starting timer")

        NavController.trans_timer.par.active = True
        NavController.trans_timer.par.start.pulse()

    def load_remote_tox(self):
        """
        Load Remote TOX

        """

        remoteTox = self.selected_remote_tox

        try:

            asset = Requests.get(remoteTox)
            tox = asset.content
            loadedTox = NavController.disp_buffer.loadByteArray(tox)
            loadedTox.par['display'] = True
            loadedTox.nodeX = 0
            loadedTox.nodeY = 0
            loadedTox.par.hmode = 1
            loadedTox.par.vmode = 1
            self.update_browser()

        except Exception as e:
            if NavController.nav_debug.eval():
                debug(f"🧭 TD Navigator | {e}")
            else:
                pass

    def clear_view(self):
        """
        Clear display buffer of any ops

        """

        for each in NavController.disp_buffer.findChildren(depth=1):
            each.destroy()

    def set_timer_play(self, playVal):
        """
        Start timer's play

        Args
        ---------------
        playVal (bool)
        > The play parameter value to be passed to the timer CHOP

        """
        NavController.trans_timer.par['play'] = playVal
        self.qu

    def toggle_settings(self):
        """
        Toggle display par for settings
        """
        NavController.settings_view.par.display = (0 if NavController.settings_view.par.display else 1)

    def query_string_parse(self, url:str) -> str:
        """
        Parse query string

        Args
        ---------------
        url (str)
        > The URL from the webBrowser COMP

        Returns
        ---------------
        qs_result (query string obj)
        > the resulting query string from a URL
        """

        parse_result = urllib.parse.urlparse(url).query
        qs_result = urllib.parse.parse_qs(parse_result)
        return qs_result

    def update_browser(self):
        """
        Update webrender TOP / Web Browser  
        """
        url = self.selected_remote_tox
        NavController.web_browser.par['Address'] = url

    def Navigator_reset(self):
        """
        Reset Navigator to default state
        """

        self.clear_view()
        default = parent.Navigator.op('container_ui/container_view/container_loading/container_start')
        copy_op = NavController.disp_buffer.copy(default)
        copy_op.nodeX = 0
        copy_op.nodeY = 0
        copy_op.par.display = True
        copy_op.par.opacity = 1
        copy_op.par.Text = "Navigator"

    def On_page_load(self):
        """
        Send JS command to browser on load
        """
        delay_hide = "args[0]._hide_td_nav_buttons()"
        run(delay_hide, self, delayFrames = 0)

        delay_show = "args[0]._show_td_have_buttons()"
        run(delay_show, self, delayFrames=1)
        pass

    def _hide_td_nav_buttons(self):
        """Hides buttons with flag
        """
        NavController.web_browser.par.Javascript = "document.getElementsByClassName('td-navigator-shown')[0].classList.remove('td-navigator-shown')"
        run('args[0].op("container_ui/container_nav_and_text").op("webBrowser").par.Sendjavascript.pulse()', parent.Navigator)    

    def _show_td_have_buttons(self):
        """Hides buttons with flag
        """
        NavController.web_browser.par.Javascript = "document.getElementsByClassName('td-navigator-hidden')[0].classList.add('td-navigator-shown')"
        run('args[0].op("container_ui/container_nav_and_text").op("webBrowser").par.Sendjavascript.pulse()', parent.Navigator)

    def Comment_focus_change(self, menu_index):
        """Sets focus network view focus to selected comment
        """
        paneControlsMOD.Comment_focus_change(menu_index)

    def Floating_window(self, par):
        #TODO - add some pane clean-up

        nav_panes = ['Navigator', 'NavigatorExample']
        par_val = par.eval()

        open_panes = self._navigator_open
        print(f"🧭 TD Navigator | navigator open - {open_panes}")
        
        for each_pane in open_panes:
            if each_pane in nav_panes:
                try:
                    each_pane.close()
                except Exception as e:
                    pass

        # borrowed from Snippets on demand 
        nav_text = ui.panes.createFloating(
            maxWidth=monitors.primary.width, 
            maxHeight=monitors.primary.height, 
            monitorSpanWidth=0.9, 
            monitorSpanHeight=0.9)

        nav_text.owner = NavController.nav_and_text
        nav_text.name = NavController.nav_header.name
        # nav_text.ratio = 0.25

        tox_example = nav_text.splitRight()
        tox_example.owner = NavController.view
        tox_example.name = NavController.nav_example_header.name
        tox_example.ratio = 0.6

        nav_text.changeType(PaneType.PANEL)
        tox_example.changeType(PaneType.PANEL)
        pass

    @property
    def Current_example(self):
        return NavController.disp_buffer.findChildren(depth=1)[0]

    @property
    def _pane_names(self):
        return [each_op.name for each_op in op('/ui/panes/panebar').findChildren(type=containerCOMP)]
    
    @property
    def _navigator_open(self):
        return [each.name for each in ui.panes]

    def _check_pane_assets(self):
        nav_header_present = NavController.nav_header.name in self._pane_names
        nav_example_header_present =  NavController.nav_example_header.name in self._pane_names

        # copy nav and nav_example headers if they don't exist in pane assets
        if nav_header_present:
            op('/ui/panes/panebar/Navigator').destroy()            
            if parent.Navigator.par.Debug:
                debug("🧭 TD Navigator | destroying previous nav_header")
        else:
            pass

        if nav_example_header_present:
            op('/ui/panes/panebar/NavigatorExample').destroy()
            if parent.Navigator.par.Debug:
                debug("🧭 TD Navigator | destroying previous nav_example_header")
        else:
            pass

        self._copy_pane_asset(NavController.nav_header, 0, -200)
        self._copy_pane_asset(NavController.nav_example_header, 200, -200)

    def _copy_pane_asset(self, asset, nodeX, nodeY):
        print(f"🧭 TD Navigator | copying asset {asset}")
        new_pane_asset = op('/ui/panes/panebar').copy(asset)
        new_pane_asset.nodeX = nodeX
        new_pane_asset.nodeY = nodeY

    #NOTE : pane controls
    def Save_tox_copy(self, par):
        paneControlsMOD.Save_tox_copy(par)

    def Set_view(self, state, view_type):
        paneControlsMOD.Set_view(state, view_type)

    def Win_close(self):
        paneControlsMOD.Win_close()

    #NOTE : parses and uses actions from the web
    def Actions_from_web(self, qs_results:dict) -> None:
        """Launches Actions

        Forwards query string results to parserActionsMOD
        """
        parserActionsMOD.Web_action(qs_results)