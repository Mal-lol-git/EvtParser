import datetime
import win32evtlogutil
from EvtScan.EvtParser_class import *
from setting import *
from EvtScan.csv import *

import datetime

today = datetime.datetime.now().date()
day_ago = today - datetime.timedelta(days=1)

RESULT = []

def _Result(evt):
	TimeGenerated = evt.TimeGenerated
	EventID = evt.EventID
	EventLog = filename[:-5]
	SourceName = evt.SourceName
	description = win32evtlogutil.SafeFormatMessage(evt, os.path.join(_PATH, filename))
	return TimeGenerated, EventID, EventLog, SourceName, description

_PATH = input("이벤트 로그 폴더 경로 : ")

evtparser = EvtParser()
count = 0
evtparser._FileList(_PATH)
for filename in EVENT_FILE:
	log_handle = evtparser._CustromEvtLogHandle(os.path.join(_PATH, filename))
	flags = evtparser._EvtLogFlags('start')
	print(filename, evtparser._TotalNumEvtLog(log_handle))
	#events = evtparser._ReadEvtLog(log_handle, flags)
	events = evtparser._ReadEvtLog(log_handle, flags)
	for evt in events:
		if str(evt.TimeGenerated)[:10] == '2023-05-08':
			RESULT.append(_Result(evt))
		elif str(evt.TimeGenerated)[:10] == '2023-05-07':
			break

EvtCsv(RESULT)



