#-*- coding: utf-8 -*-
import json
import requests

from settings import *


class EvtParser():

    def __init__(self):
        super().__init__()

    def _JsonData(self, data):
        try:
            return data.json()

        except Exception as e:
            return False
