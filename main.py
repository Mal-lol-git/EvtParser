from EvtScan.EvtParser_class import *
from setting import _PATH

evtparser = EvtParser()

evtparser._FileList(_PATH)

for filename in EVENT_FILE:
	log_handle = evtparser._CustromEvtLogHandle(os.path.join(_PATH, filename))
	flags = evtparser._EvtLogFlags()
	print('LogFileName : ', filename)
	print('Total : ', evtparser._TotalNumEvtLog(log_handle))
	evtparser._Scan(log_handle, flags, filename[:-5], filename)
	print('*'*30)

