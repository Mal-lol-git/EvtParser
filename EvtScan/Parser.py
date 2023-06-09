#-*- coding: utf-8 -*-
import re
import chardet

from urllib import parse
from EvtParser.EvtParser_class import *


def EvtCsv(keyword):
    try:
        #Total Query
        key_enc = parse.quote(keyword)
        query = keyword + OPTION_DAYS[0]

        #TotalScan_class
        evtparser = EvtParser()

        #Total connect
        con = test._Connect()
        result = test._SearchQuery(con, API_SEARCH, query)

        #Check Status_code 
        if result.status_code != 200:
            print(result, ' Check virustotal connection.')
            return

        #Create Json Data
        data = evtparser._JsonData(result)
       
        for row in range(len(data['data'])):            
            if bool(''.join(data['data'][row]['attributes']['names'])):
                if _Option_filter(OPTION_SCAN_TYPE[0], data, row):
                    RESULT.append(_Result(data, row, test))

    except Exception as e:
        print(e)

def _Result(data, row, test):
    md5 = data['data'][row]['attributes']['md5']
    MD5.append(data['data'][row]['attributes']['md5'])
    filename = ''.join(data['data'][row]['attributes']['names'][0])
    encoding = chardet.detect(''.join(data['data'][row]['attributes']['names'][0]).encode())['encoding']
    ahnlab = data['data'][row]['attributes']['last_analysis_results']['AhnLab-V3']['category']
    alyac = data['data'][row]['attributes']['last_analysis_results']['ALYac']['category']
    virobot = data['data'][row]['attributes']['last_analysis_results']['ViRobot']['category']
    filetype = data['data'][row]['attributes']['type_extension'] if test._KeyFind(data['data'][row]['attributes'], 'type_extension') else '-'
    ratio = str(data['data'][row]['attributes']['last_analysis_stats']['malicious'])    
    return md5, filename, encoding, ahnlab, alyac, virobot, filetype, ratio