import datetime

from EvtScan.EvtParser_class import *

path = r'C:\Users\DG\Desktop'

evtparser = EvtParser()

evtparser._FileList(path)
print(EVENT_FILE)

