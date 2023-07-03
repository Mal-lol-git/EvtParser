#-*- coding: utf-8 -*-
import csv
import os

from EvtScan.EvtParser_class import *
from setting import _CSV_PATH
from datetime import datetime


def EvtCsv(RESULT, LOGTYPE):
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
