from EvtScan.EvtParser_class import *
import ctypes

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

if is_admin():
	try:
		evtparser = EvtParser()
		evtparser._Start()
		os.system('pause')
	except Exception as e:
		print(e)
else:
	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

