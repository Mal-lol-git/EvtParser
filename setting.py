#-*- coding: utf-8 -*-
import os
from datetime import datetime

#EVTFILENAME
EVENT_FILE = []

#EVTRESULTVALUE
RESULT = []

#EVTLOG_FOLDERPATH
_PATH = input("EVTLog Folder Path : ")

#EVTLOG PARSER RANGE
#START DAY
_SRC = input("EVTLog Start Date ex)9999-01-01 : ")

#LAST DAY
_DST = input("EVTLog Last Date ex)9999-12-30 : ")

_DST = _DST + ' 23:59:59'
SRC = datetime.strptime(_SRC, "%Y-%m-%d")
DST = datetime.strptime(_DST, "%Y-%m-%d %H:%M:%S")

#CSV PATH
_CSV_PATH = input("File Save Path : ")

#EVENTLOG_EX
EVTEX  = '.evtx'
EVTEX2 = '.evt'

