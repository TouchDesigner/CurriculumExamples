"""Actions Parser

Parsing mechanics and function-lookup map for handling incoming 
query string requests.
"""


import webACTIONS

# global op shortcut to TouchDesigner Curriculum Navigator
Navigator = op.TDCN

def _get_action(action:str) -> None:
    '''
    getattr call that attempts to retrieve a function from another module


    Args
    ---------------
    action (str)
    > String name of coresponding NavController method

    Returns
    ---------------
    func (callabe)
    > matching function from webACTIONS, returns None if module contains 
    no matching function
    '''
    func = None

    try :
        func = getattr(webACTIONS, action)
    
    except Exception as e:
        print(e)

    return func

def Web_action(qs_result:dict) -> None:
    '''
    Action Runner - tries to run the requested web-action

    Args
    ---------------
    qs_result (query string obj):
    > the resulting query string from a URL

    '''

    func = _get_action(qs_result.get('action')[0])
    
    if func != None:
        func(qs_result)

    else:
        raise ValueError("🧭 TD Navigator | No matching function found for action")

    return 