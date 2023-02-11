# me - this DAT
# 
# frame - the current frame
# state - True if the timeline is paused
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

def onStart():
	primaryMonitor = [x for x in monitors if x.isPrimary][0]

	scaledWidth = primaryMonitor.width / primaryMonitor.dpiScale

	if scaledWidth < op('container_ui').width:
		op('container_ui').par.w = scaledWidth

	else:
		pass

	return

def onCreate():
	return

def onExit():
	return

def onFrameStart(frame):
	return

def onFrameEnd(frame):
	return

def onPlayStateChange(state):
	return

def onDeviceChange():
	return

def onProjectPreSave():
	return

def onProjectPostSave():
	return

onStart()