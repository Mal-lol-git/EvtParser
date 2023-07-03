#-*- coding: utf-8 -*-
import csv

from EvtScan.EvtParser_class import *
from datetime import datetime

def EvtCsv(RESULT, LOGTYPE):
	try:
		TODAY = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.%f')
		save_filename = CSV_PATH+LOGTYPE+TODAY+'.csv'
		f_csv = open(save_filename, 'w', encoding='utf-8-sig', newline='')
		w_csv = csv.writer(f_csv)
		for row in RESULT:
			w_csv.writerow(row)
		f_csv.close()
		print('csv_file_save')

	except Exception as e:
		print(e)
