"""Timer Functions

Isolates callbacks into a separate module block for easier 
management alongside the extension.
"""

# global op shortcut to TouchDesigner Curriculum Navigator
Navigator = op.TDCN

def Timer_segment_enter(**kwargs):
    '''
    timer onSegmentEnter callback       

    Args
    ---------------
    **kwargs (keyword args)
    > Timer op key word args


    '''
    timerOp = kwargs.get('timerOp')
    segment = kwargs.get('segment')
    interrupt = kwargs.get('interrupt')

    if segment > 0:
        timerOp.par.play = False
        Navigator.ext.NavController.clear_view()
        run(Navigator.ext.NavController.load_remote_tox(), delayFrames = 1)
        timerOp.par.play = True

def Timer_on_done(**kwargs):
    '''
    timer onDone callback

    Args
    ---------------
    **kwargs (keyword args)
    > Timer op key word args

    '''
    Navigator.ext.NavController.loading_view.par['display'] = False
    kwargs.get('timerOp').par.active = False
    pass

