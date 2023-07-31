#-*- coding: utf-8 -*-
import os
import csv
import win32evtlogutil
import win32evtlog as winevt

from datetime import datetime

class EvtParser():

	def __init__(self):
		super().__init__()
		self._PATH = None
		self.SRC = None
		self.DST = None
		self._CSV_PATH = None
		self.EVENT_FILE = []
		self.RESULT = []

	def _Start(self):
		print('*'*18 + '\n* EventLogParser *\n' + '*'*18)
		self._PATH = self._EventLogPath()
		self.SRC, self.DST = self._EventLogDate()
		self._CSV_PATH = self._EventLogSavePath()
		self._Scan(self._PATH, self.SRC, self.DST, self._CSV_PATH)

	def _EventLogPath(self):
		while True:
			try:
				EventLog_Type = int(input("\n[EventLogPath]\n 1.Local EventLog\n 2.Custrom EventLog\n 3.Exit\n >> "))
				if EventLog_Type == 1:
					return r'C:\Windows\System32\winevt\Logs'

				if EventLog_Type == 2:
					return input("EVTLog Folder Path : ")

				if EventLog_Type == 3:
					exit()

				else:
					print("\n[Error]\n Please Input Number '1-3'\n")
					os.system('pause')
					os.system('cls')

			except Exception as e:
				print("\n[Error]\n Please Input Number '1-3'\n")
				os.system('pause')
				os.system('cls')

	def _EventLogDate(self):				
		while True:
			try:
				EventLog_Date = int(input("[EventLogDate]\n 1.All Date\n 2.Specify Date\n 3.Exit\n >> "))
				if EventLog_Date == 1:
					_SRC = '0001-01-01'
					_DST = '9999-12-31'
					_DST = _DST + ' 23:59:59'
					return datetime.strptime(_SRC, "%Y-%m-%d"), datetime.strptime(_DST, "%Y-%m-%d %H:%M:%S")

				if EventLog_Date == 2:
					_SRC = input("EVTLog Start Date ex)0001-01-01 : ")
					_DST = input("EVTLog Last Date ex)9999-12-30 : ")
					_DST = _DST + ' 23:59:59'
					return datetime.strptime(_SRC, "%Y-%m-%d"), datetime.strptime(_DST, "%Y-%m-%d %H:%M:%S")

				if EventLog_Date == 3:
					exit()

				else:
					print(" [Please Input Number '1-3']")
					os.system('pause')
					os.system('cls')

			except Exception as e:
				print(" [Please Input Number '1-3']")
				os.system('pause')
				os.system('cls')			

	def _EventLogSavePath(self):
		try:
			return input("[EventLog Save Path]\n File Save Path : ")

		except Exception as e:
			return False

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

	def _EvtLogFlags(self):
		try:
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
				if file.endswith('.evtx'):
					self.EVENT_FILE.append(file)
				if file.endswith('.evt'):
					self.EVENT_FILE.append(file)

		except Exception as e:
			return e

	def _Scan(self, path, src, dst, csv_path):
		count=0
		self._FileList(path)
		for filename in self.EVENT_FILE:
			_LOG_TYPE = filename[:-5]
			_LOG_HANDLE = self._LocalEvtLogHandle(_LOG_TYPE)
			_FLAGS = self._EvtLogFlags()
			print('*'*54)
			print('Log FileName : ', filename)
			print('Log Total : ', self._TotalNumEvtLog(_LOG_HANDLE))
			print('Log Date : %s ~ %s' % (src, dst))
			while True:
				events = self._ReadEvtLog(_LOG_HANDLE, _FLAGS)
				if events:
					for evt in events:
						if str(evt.TimeGenerated)[:10]:
							if count == 30000:
								self.EvtCsv(self.RESULT, _LOG_TYPE, csv_path)
								self.RESULT.clear()
								count = 0
							if dst >= evt.TimeGenerated >= src:
								self.RESULT.append(self._Result(evt, filename))
								count = count + 1
						else:
							break
				else:
					if self.RESULT:
						self.EvtCsv(self.RESULT, _LOG_TYPE, csv_path)
						self.RESULT.clear()
					print('Number of Logs Parsing : %d' % count)
					print('*'*54)
					count = 0
					break

	def _Result(self, evt, filename):
		TimeGenerated = evt.TimeGenerated
		EventID = evt.EventID & 0x1FFFFFFF
		EventLog = filename[:-5]
		SourceName = evt.SourceName
		description = win32evtlogutil.SafeFormatMessage(evt, filename[:-5])
		description2 = evt.StringInserts
		return TimeGenerated, EventID, EventLog, SourceName, description, description2

	def EvtCsv(self, result, logtype, path):
		try:
			TODAY = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
			SAVE_FILENAME = logtype + '_' + TODAY + '.csv'
			SAVE_FILEPATH = os.path.join(path, SAVE_FILENAME)
			f_csv = open(SAVE_FILEPATH, 'w', encoding='utf-8-sig', newline='')
			w_csv = csv.writer(f_csv)
			print('Save CSV...')
			for row in result:
				w_csv.writerow(row)
			f_csv.close()
			print('CSV FileName : ', SAVE_FILENAME)

		except Exception as e:
			print(e)
