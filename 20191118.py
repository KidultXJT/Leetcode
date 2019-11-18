#!usr/bin/python
# -*- coding:utf-8 -*-

## --------------------------------------------------------
## Author: Kidult
## Email : junting.xie@sagene.com.cn
## Date  : 2019-11-11
## --------------------------------------------------------
## Description:
## DownLoad Abstract From NCBI.

# module
from optparse import OptionParser
from pandas import Series, DataFrame
import pandas as pd
import sys
import os
import re
import time

import random
import string

import re
import smtplib
import sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown
from Bio import Entrez


keyword = sys.argv[1] # 1 ID each line
prefix  = sys.argv[2] # outNAME
Top     = sys.argv[3] #

keywords = keyword.split("_")
keyword  = " ".join(keywords)

print str(time.time())

# BioPython
from Bio import Entrez
# urllib
try:
    from urllib.error import HTTPError
except ImportError:
    from urllib2 import HTTPError

print str(time.time())

def GetPMID(
    email="xie@sagene.com.cn",
    keyword="Cerebrospinal fluid",
    Top=int(1000)
    ): # Unhappy Face
    # Description:
    from Bio import Entrez
    randomNUM = int(random.sample('012345678',1)[0])
    randomSTR = "".join(random.sample('abcdefghijklmnopqrstuvwxyz',randomNUM))
    email = randomSTR+email
    Entrez.email = str(email)
    handle = Entrez.esearch(db="pubmed",
                            term=keyword,
                            retmax=int(Top))
                            #mindate= "2015/01",
                            #maxdate= "2019/11")
    record = Entrez.read(handle) # list
    PMID = record["IdList"]
    return PMID

def GetAbstract(PMIDs=['31703006']):
    ## PMIDs from GetPMID(keyword)
    Lst = []
    for i in PMIDs:
        i = int(i)
        handle=Entrez.efetch(db='pubmed', rettype='abstract', id=i, retmode='text')
        handle_text=handle.read()
        Lst.append(handle_text)
    Abstracts="\n\nNextItem".join(Lst)
    return Abstracts


out=open(prefix+"_Abstract.txt","w")
out.write(GetAbstract(PMIDs=GetPMID(keyword=str(keyword),Top=int(Top))))
out.close()

print str(time.time())

print len(GetPMID(keyword=str(keyword),Top=int(Top)))
