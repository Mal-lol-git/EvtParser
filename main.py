import win32evtlogutil

from EvtScan.EvtParser_class import *
from setting import _PATH,_SRC,_DST
from EvtScan.csv import *

def _Result(evt):
	TimeGenerated = evt.TimeGenerated
	EventID = evt.EventID & 0x1FFFFFFF
	EventLog = filename[:-5]
	SourceName = evt.SourceName
	description = win32evtlogutil.SafeFormatMessage(evt, filename[:-5])
	return TimeGenerated, EventID, EventLog, SourceName, description

def _Scan(LOGTYPE):
	count=0
	SRC = datetime.strptime(_SRC, "%Y-%m-%d")
	DST = datetime.strptime(_DST, "%Y-%m-%d %H:%M:%S")

	while True:
		events = evtparser._ReadEvtLog(log_handle, flags)
		if events:
			for evt in events:
				if str(evt.TimeGenerated)[:10]:
					if count == 30000:
						EvtCsv(RESULT, LOGTYPE)
						RESULT.clear()
						count =0

					if DST >= evt.TimeGenerated >= SRC:
						print(DST,evt.TimeGenerated,SRC)
						RESULT.append(_Result(evt))
						count=count+1
		
				else:
					break
	
		else:
			if RESULT:
				EvtCsv(RESULT,filename[:-5])
				RESULT.clear()
			break

evtparser = EvtParser()

evtparser._FileList(_PATH)
for filename in EVENT_FILE:
	log_handle = evtparser._CustromEvtLogHandle(os.path.join(_PATH, filename))
	flags = evtparser._EvtLogFlags('start')
	print(filename, evtparser._TotalNumEvtLog(log_handle))
	_Scan(filename[:-5])


#EvtCsv(RESULT)
