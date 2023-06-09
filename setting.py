#VIRUS_TOTAL_SCANNER SETTINGS
from urllib.parse import urljoin


#VIRUS_TOTAL
#URL, API_KEY
API_KEY     = '[API]'
API_URL     = 'https://www.virustotal.com/api/v3/'

API_SEARCH  = urljoin(API_URL, 'intelligence/search')
API_ATTACH  = urljoin(API_URL, 'files/')

#SEARCH_OPTION
OPTION_DAYS         = []
OPTION_SCAN_TYPE    = []

#SEARCH_PARAMS
descriptors_only    = False
cursor              = None
s_limit             = 300

#LIST_INDEX
MD5                 = []
RESULT              = []

#SAVE_PATH
HASH_SAVE_PATH      = '[PATH.txt]'
CSV_PATH            = '[PATH.csv]'