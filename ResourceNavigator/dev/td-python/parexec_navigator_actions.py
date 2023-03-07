# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
# 
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

import navParACTIONS

def action_func(par):
	func = getattr(navParACTIONS, par.name)
	return func

def onValueChange(par, prev):
	# use par.eval() to get current value
	try:
		func = action_func(par)
		func(par)
	except Exception as e:
		if parent.Navigator.par.Debug:
			debug(e)
		else:
			pass
	return

# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)
def onValuesChanged(changes):
	for c in changes:
		# use par.eval() to get current value
		par = c.par
		prev = c.prev
	return

def onPulse(par):
	try:
		func = action_func(par)
		func(par)
	except Exception as e:
		if parent.Navigator.par.Debug:
			debug(e)
		else:
			pass
	return

def onExpressionChange(par, val, prev):
	return

def onExportChange(par, val, prev):
	return

def onEnableChange(par, val, prev):
	return

def onModeChange(par, val, prev):
	return
	