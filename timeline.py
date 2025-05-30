'''
Timeline Parser
- build a list of events

'''
import os
import re
from pathlib import Path
import numpy as np
import pandas as pd


class events(object):
    def __init__(self, **kwargs):
        ''' tx is multiline event text, 1st line is used as kw '''
        self.evDict = {}
        self.loadTimeLine(**kwargs)

    def loadTimeLine(self, **kwargs):
        self.FN = kwargs['FN']
        if self.FN is None:
            print("Empty timeline created")
            return
            
        with open(self.FN, 'r') as fio:
            tx = fio.read()
        self.walk(tx)

    def walk(self, tx):
        '''
        Parse all lines in timeline text
        Each event is a block of lines, seperated by Year prefix
        '''
        p = r'\n(?=\d+.*)'
        evList = re.split(p, tx, flags=re.MULTILINE)
        for ev in evList:
            if ev[0] == '#' : continue
            self.add(ev)

    def add(self, tx):
        lnList = tx.split('\n')
        mKw = lnList[0].strip()
        mDesc = '\n'.join(lnList[1:])
        self.evDict[mKw] = mDesc
        
    def evStr(self, k):
        desc = self.evDict[k]
        return f"{k}\n{desc.strip()}"
        
    def evDt(self, tx):
        
        p = r'^(\d+)(?:-|\D)(\d+)*\D.*'
        mList = []
        for m in re.split(p, tx):
            if m is None: continue
            if (m.strip() == '') : continue
            mList.append(m)
        
        # check if BC time stamp
        BC = 'BC' in tx.upper()
        if (len(mList) == 1):
            dt = mList[0]
        elif BC:
            dt = mList[0]
        else: 
            dt = mList[1]

        if BC: return -int(dt)
        return int(dt)

    def merge(self, tlList):
        '''
        tlList is list of other timeline objects containing events (tl.evDict)
        '''
        for tl in tlList:
            for k,desc in tl.evDict.items():
                self.evDict[k] = desc
        

        # Sort based on date
        self.evDict = dict(sorted(self.evDict.items(), key=lambda tup: self.evDt(tup[0])))
        return

    def slice(self, fromDt, toDt):
        tlNew = events(FN=None)
        for k,desc in self.evDict.items():
            dt = self.evDt(k)
            if dt < fromDt : continue
            if dt > toDt : continue
            tlNew.evDict[k] = desc
        return tlNew
        
    def find(self, pattern):
        tlNew = events(FN=None)
        for k,desc in self.evDict.items():
            if (pattern in k) or (pattern in desc):
                #print("FOUND:", k)
                tlNew.evDict[k] = desc
                continue
        return tlNew

    def __repr__(self):
        tx = ''
        for kw,desc in self.evDict.items():
            tx += f"{self.evDt(kw)} ==> {kw}\n"
            tx += f"{desc}\n"
        return tx