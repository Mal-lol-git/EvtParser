import win32evtlog as wevt
import datetime

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
