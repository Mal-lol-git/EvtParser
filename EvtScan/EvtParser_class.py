#-*- coding: utf-8 -*-
import os
import csv
import win32evtlogutil
import win32evtlog as winevt

from setting import *
from setting import _CSV_PATH

class EvtParser():

	def __init__(self):
		super().__init__()

	def _LocalEvtLogHandle(self, logtype):
		try:
			return winevt.OpenEventLog(None, logtype)

		except Exception as e:
			return False

	def _CustromEvtLogHandle(self, path):
		try:
			return winevt.OpenBackupEventLog(None, path)

		except Exception as e:
			return False

	def _EvtLogFlags(self, flags):
		try:
			if 'start' == flags: 
				return winevt.EVENTLOG_BACKWARDS_READ|winevt.EVENTLOG_SEQUENTIAL_READ

		except Exception as e:
			return False

	def _ReadEvtLog(self, handle, flags):
		try:
			return winevt.ReadEventLog(handle, flags, 0)

		except Exception as e:
			return False

	def _TotalNumEvtLog(self, handle):
		try:
			return winevt.GetNumberOfEventLogRecords(handle)

		except Exception as e:
			return False

	def _FileList(self, path):
		try:
			for file in os.listdir(path):
				if file.endswith(EVTEX):
					EVENT_FILE.append(file)
				if file.endswith(EVTEX2):
					EVENT_FILE.append(file)

		except Exception as e:
			return e

	def _Scan(self, handle, flags, logtype, filename):
		count=0

		while True:
			events = self._ReadEvtLog(handle, flags)
			if events:
				for evt in events:
					if str(evt.TimeGenerated)[:10]:
						if count == 30000:
							self.EvtCsv(RESULT, logtype)
							RESULT.clear()
							count =0

						if DST >= evt.TimeGenerated >= SRC:
							RESULT.append(self._Result(evt, filename))
							count=count+1
		
					else:
						break
	
			else:
				if RESULT:
					self.EvtCsv(RESULT,filename[:-5])
					RESULT.clear()
				break

	def _Result(self, evt, filename):
		TimeGenerated = evt.TimeGenerated
		EventID = evt.EventID & 0x1FFFFFFF
		EventLog = filename[:-5]
		SourceName = evt.SourceName
		description = win32evtlogutil.SafeFormatMessage(evt, filename[:-5])
		return TimeGenerated, EventID, EventLog, SourceName, description

	def EvtCsv(self, RESULT, LOGTYPE):
		try:
			TODAY = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
			SAVE_FILENAME = LOGTYPE+'_'+TODAY+'.csv'
			SAVE_FILEPATH = os.path.join(_CSV_PATH, SAVE_FILENAME)
			f_csv = open(SAVE_FILEPATH, 'w', encoding='utf-8-sig', newline='')
			w_csv = csv.writer(f_csv)
			for row in RESULT:
				w_csv.writerow(row)
			f_csv.close()
			print('csv_file_save')

		except Exception as e:
			print(e)
