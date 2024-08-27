def load_tox(qs_results):
    '''Load TOX from URL
    '''
    if nav_debug.eval():
        debug("loading remote")

    remote_tox = qs_results.get('remotePath')
    NavigatorCOMP.store('selectedRemoteTox', remote_tox[0])
    load_new_selection()
    remove_qs_from_path() 
    pass
