#-*- coding: utf-8 -*-
import csv

from EvtParser.EvtParser_class import *


def EvtCsv(RESULT):
    try:
    	f_csv = open(CSV_PATH, 'w', encoding='utf-8-sig', newline='')
    	w_csv = csv.writer(f_csv)
    	for row in RESULT:
    		w_csv.writer(row)
    	f_csv.close()
        print('csv_file save')
       
    except Exception as e:
        print(e)
