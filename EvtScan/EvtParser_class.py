#-*- coding: utf-8 -*-
import json, os
import win32evtlog as winevt

from setting import *

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

	def _JsonData(self, data):
		try:
			return data.json()

		except Exception as e:
			return False

