import datetime
import win32evtlogutil
from EvtScan.EvtParser_class import *
from setting import *
from EvtScan.csv import *

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

evtparser._FileList(_PATH)
for filename in EVENT_FILE:
	handle = evtparser._CustromEvtLogHandle(os.path.join(_PATH, filename))
	flags = winevt.EVENTLOG_BACKWARDS_READ|winevt.EVENTLOG_SEQUENTIAL_READ
	print(filename, evtparser._TotalNumEvtLog(handle))
	events = winevt.ReadEventLog(handle, flags,0)
	for evt in events:
		RESULT.append(_Result(evt))


EvtCsv(RESULT)


'''
import win32evtlog as wevt
import datetime
import csv

today = datetime.datetime.now().date()
day_ago = today - datetime.timedelta(days=1)

server = 'localhost'
logtype = 'System'
hand = wevt.OpenEventLog(server,logtype)
flags = wevt.EVENTLOG_BACKWARDS_READ|wevt.EVENTLOG_SEQUENTIAL_READ
total = wevt.GetNumberOfEventLogRecords(hand)

while True:
    events = wevt.ReadEventLog(hand, flags,0)
    if events:
        for evt in events:
            if str(evt.TimeGenerated)[:10] == str(today):
                print('Event ID:', evt.EventID)
                data = evt.StringInserts

                if data:
                    print('Event Data: ', data)

                    #for msg in data:
                    #    print(msg)

                print('*' * 100)

            elif str(evt.TimeGenerated)[:10] == str(day_ago):
                break
'''


