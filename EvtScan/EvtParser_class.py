#-*- coding: utf-8 -*-
import os
import sys
import csv
import re
import sqlite3
import win32evtlogutil
import win32evtlog as winevt

from datetime import datetime

class EvtParser():

	def __init__(self):
		super().__init__()
		self._PATH = None
		self._PATHTYPE = None
		self.SRC = None
		self.DST = None
		self._SAVE_PATH = None
		self._SAVE_TYPE = None
		self.EVENT_FILE = []
		self.RESULT = []
		self.EVENTID = None
		self.Select_EventID = None

	def _Start(self):
		print('*'*18 + '\n* EventLogParser *\n' + '*'*18)
		self._PATH, self._PATHTYPE = self._EventLogPath()
		self.SRC, self.DST = self._EventLogDate()
		self.Select_EventID = self._EventID()
		self._SAVE_PATH = self._EventLogSavePath()
		self._SAVE_TYPE = self._EventLogSaveType()
		self._Scan(self._PATH, self._PATHTYPE, self.SRC, self.DST, self._SAVE_PATH, self._SAVE_TYPE)


	def _EventLogPath(self):
		while True:
			try:
				EventLog_Type = int(input("\n[EventLogPath]\n 1.Local EventLog\n 2.Custom EventLog\n 3.Exit\n >> "))
				if EventLog_Type == 1:
					_EVTPATH = r'C:\Windows\System32\winevt\Logs'
					return _EVTPATH, EventLog_Type
				if EventLog_Type == 2:
					_EVTPATH = input("EVTLog Folder Path : ")
					return _EVTPATH, EventLog_Type
				if EventLog_Type == 3:
					sys.exit(0)
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
				EventLog_Date = int(input("[EventLogDate]\n 1.All Date\n 2.Custom Date\n 3.Exit\n >> "))
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
					sys.exit(0)
				else:
					print(" [Please Input Number '1-3']")
					os.system('pause')
					os.system('cls')
			except Exception as e:
				print(" [Please Input Number '1-3']")
				os.system('pause')
				os.system('cls')

	def _EventID(self):
		try:
			Select_EventID = int(input("[Select EventID]\n 1.All EventID\n 2.Select EventID\n >> "))
			if Select_EventID == 1:
				Select_EventID = False
				return Select_EventID
			if Select_EventID == 2:
				Select_EventID = True
				self.EVENTID = input("[EventID]\n EventID ex) 7045, 7046\n >> ").replace(' ','').split(',')
				return Select_EventID
		except Exception as e:
			print(e)	

	def _EventLogSavePath(self):
		try:
			return input("[EventLog Save Path]\n File Save Path : ")
		except Exception as e:
			print(e)

	def _EventLogSaveType(self):
		while True:
			try:
				Save_Type = int(input("\n[EventLog Save Type]\n 1.CSV\n 2.DB\n 3.Exit\n >> "))
				if Save_Type == 1 or Save_Type == 2:
					return Save_Type
				if Save_Type == 3:
					sys.exit(0)
				else:
					print("\n[Error]\n Please Input Number '1-3'\n")
					os.system('pause')
					os.system('cls')
			except Exception as e:
				print("\n[Error]\n Please Input Number '1-3'\n")
				os.system('pause')
				os.system('cls')

	def _LocalEvtLogHandle(self, logtype):
		try:
			return winevt.OpenEventLog(None, logtype)
		except Exception as e:
			print(e)

	def _CustromEvtLogHandle(self, path):
		try:
			return winevt.OpenBackupEventLog(None, path)
		except Exception as e:
			print(e)

	def _EvtLogFlags(self):
		try:
			return winevt.EVENTLOG_BACKWARDS_READ|winevt.EVENTLOG_SEQUENTIAL_READ
		except Exception as e:
			print(e)

	def _ReadEvtLog(self, handle, flags):
		try:
			return winevt.ReadEventLog(handle, flags, 0)
		except Exception as e:
			print(e)

	def _TotalNumEvtLog(self, handle):
		try:
			return winevt.GetNumberOfEventLogRecords(handle)
		except Exception as e:
			print(e)

	def _FileList(self, path):
		try:
			for file in os.listdir(path):
				if file.endswith('.evtx'):
					self.EVENT_FILE.append(file)
				if file.endswith('.evt'):
					self.EVENT_FILE.append(file)
		except Exception as e:
			print(e)

	def _Scan(self, path, pathtype, src, dst, save_path, save_type):
		count=0
		self._FileList(path)
		for filename in self.EVENT_FILE:
			_LOG_TYPE = filename[:-5]
			if pathtype == 1:
				_LOG_HANDLE = self._LocalEvtLogHandle(_LOG_TYPE)
			if pathtype == 2:
				_LOG_HANDLE = self._CustromEvtLogHandle(os.path.join(path,filename))
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
								if save_type == 1:
									self.EvtCsv(self.RESULT, _LOG_TYPE, save_path)
									self.RESULT.clear()
									count = 0
								if save_type == 2:	
									self.EvtDB(self.RESULT, _LOG_TYPE, save_path)
									self.RESULT.clear()
									count = 0
							if dst >= evt.TimeGenerated >= src:
								if self.Select_EventID:
									if str(evt.EventID & 0x1FFFFFFF) in self.EVENTID:
										self.RESULT.append(self._Result(evt, filename))
										count = count + 1
								else:
									self.RESULT.append(self._Result(evt, filename))
									count = count + 1
						else:
							break
				else:
					if self.RESULT:
						if save_type == 1:
							self.EvtCsv(self.RESULT, _LOG_TYPE, save_path)
							self.RESULT.clear()
						if save_type == 2:	
							self.EvtDB(self.RESULT, _LOG_TYPE, save_path)
							self.RESULT.clear()
					print('Number of Logs Parsing : %d' % count)
					print('*'*54)
					count = 0
					break

	def _Result(self, evt, filename):
		TimeGenerated = evt.TimeGenerated
		TimeWritten = evt.TimeWritten
		EventID = evt.EventID & 0x1FFFFFFF
		EventLog = filename[:-5]
		SourceName = evt.SourceName
		ComputerName = evt.ComputerName
		try:
			description = win32evtlogutil.SafeFormatMessage(evt, filename[:-5])
			des_result = re.search('following insertion string\(s\)\:\'(.*)\'\.>', description)
			if des_result != None:
				description = des_result.group(1)
		except Exception:
			description = ''
		if evt.StringInserts:
			description2 = evt.StringInserts
		else:
			description2 = ''
		description2 = '||'.join(description2)
		return str(TimeGenerated), str(TimeWritten), EventID, EventLog, SourceName, ComputerName, description, description2

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

	def EvtDB(self, result, logtype, path):
		try:
			con = sqlite3.connect(os.path.join(path, 'EVTDB.db'))
			cur = con.cursor()
			#tablename = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z]", '', logtype)
			tablename = re.sub(r"[^0-35-9a-zA-Zㄱ-ㅣ가-힣]", '', logtype)
			table_check_query = "select count(*) from sqlite_master where name='" + tablename + "'"
			cur.execute(table_check_query)
			if not bool(cur.fetchone()[0]):
				query = "CREATE TABLE " + tablename + " (TimeGenerated text, TimeWritten text, EventID int, EventLog text, SourceName text, ComputerName text, Orgin_Description text, Description text)"
				cur.execute(query)
			#print(result)
			cur.executemany('INSERT INTO ' + tablename + ' VALUES (?,?,?,?,?,?,?,?)', result)
			con.commit()
			con.close()
		except Exception as e:
			print(e)

