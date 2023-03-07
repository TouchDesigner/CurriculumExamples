# me - This DAT
# 
# dat - The DAT that received the key event
# key - The name of the key attached to the event.
#		This tries to be consistent regardless of which language
#		the keyboard is set to. The values will be the english/ASCII
#		values that most closely match the key pressed.
#		This is what should be used for shortcuts instead of 'character'.
# character - The unicode character generated.
# alt - True if the alt modifier is pressed
# ctrl - True if the ctrl modifier is pressed
# shift - True if the shift modifier is pressed
# state - True if the event is a key press event
# time - The time when the event came in milliseconds
# cmd - True if the cmd modifier is pressed

import webFuncsMOD as webFuncs

actions_map = {
	"ctrl.=" : {
		"func" : webFuncs.Zoom_increment,
		"val" : 10
	},
	"ctrl.-" : {
		"func" : webFuncs.Zoom_increment,
		"val" : -10
	},
	"ctrl.0" : {
		"func" : webFuncs.Zoom_reset,
		"val" : 100		
	}
}


def onKey(dat, key, character, alt, lAlt, rAlt, ctrl, lCtrl, rCtrl, shift, lShift, rShift, state, time, cmd, lCmd, rCmd):
	return

# shortcutName is the name of the shortcut

def onShortcut(dat, shortcutName, time):
	print(shortcutName)
	try:
		action = actions_map.get(shortcutName)
		func = action.get('func')
		val = action.get('val')
		print(val)
		func(val)
		
	except Exception as e:
		debug(e)
	return
	