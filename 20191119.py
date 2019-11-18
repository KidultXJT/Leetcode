#!usr/bin/python
# -*- coding:utf-8 -*-

## --------------------------------------------------------
## Author: Kidult
## Email : junting.xie@sagene.com.cn
## Date  : 2019-11-19
## --------------------------------------------------------
## Description:
## DownLoad UID2seqID and Download Sequence from NCBI



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
from Bio import Entrez, SeqIO


abstract = sys.argv[1] # abstract FILE Download From NCBI::Entrez::Pubmed
Keyword  = sys.argv[2] # Like Primer / AAAA_BBBB
db       = sys.argv[3] # genus List database (After HandJob)
prefix   = sys.argv[4] # output prefix

Abstract=open(abstract,"r")

abstract_format=open(abstract.split(".")[0]+".ab","w")
Abstract=Abstract.read().replace("\n"," ").replace("  "," ")
PMID=[" ".join(str(i.split("PMID")[-1].strip().replace(":","PMID:")).split(" ")[:2]) for i in Abstract.split("NextItem")]
Abstract=[i.strip() for i in Abstract.split("NextItem")]

for n in range(len(PMID)):
    abstract_format.write((PMID[n]+"\t"+Abstract[n]+"\n"))


log=open(prefix+".log","w")

def s(s):
    i = 0
    ans = []
    while i < len(s):
        start = i
        # find space
        while i < len(s) and s[i] != ' ':
            i += 1
        ans.append(s[start:i])
        i += 1
    if s and s[-1] == " ":
        ans.append("")
    return ans

genusDict=dict()
Lst=[]
for c in ["bacteria","fungi","viruses","parasite"]:
    genus=open(db+"/"+c+".genus","r")
    Lst=[]
    genusLst=[ i.lower() for i in genus.read().split("\n")] # 1 Line with 1 genusNAME
    del genusLst[-1] # Delete ""
    for a in Abstract:
        tmpLst=s(a.lower()) # Clean split by " "
        for word in tmpLst:
            if word in genusLst:
                Lst.append(word)
    genusDict[str(c.upper())] = list(set(Lst))
    print "There are " + str(len(genusDict[str(c.upper())])) + "/" + str(len(genusLst)) + " genus in " + c.upper()
    log.write("There are " + str(len(genusDict[str(c.upper())])) + "/" + str(len(genusLst)) + " genus in " + c.upper() + "\n")

PMIDict=dict()
w=0
W=0
for num in range(len(Abstract)):
    tmpLst=[i.strip().lower() for i in Abstract[int(num)].split(".")] # split Abstract to multi-sentance
    tmp=[]
    for sentance in tmpLst:
        sentanceLst=[i.strip() for i in sentance.split(" ")]
        if Keyword.lower() in sentanceLst: # From Argv[3] Example::primer
            tmp.append(sentance)
            w=w+1
        else: #  primers
            tmp_num=0
            for word in sentanceLst:
                if word.lower().find(str(Keyword.lower())) != -1: # primers find primer
                    tmp_num = tmp_num + 1
            if tmp_num > 0:
                tmp.append(sentance)
                W=W+1
    PMIDict[PMID[num]]=[str(len(tmp)),".".join(tmp)]
print Keyword + " Match: " + str(w)
log.write(Keyword + " Match: " + str(w) + "\n")
print Keyword + " maybe Match: " + str(W)
log.write(Keyword + " maybe Match: " + str(W) + "\n")

SPDict=dict()
w=0
W=0
for c in ["bacteria","fungi","viruses","parasite"]:
    TmpDict = dict()
    for num in range(len(Abstract)):
        tmpLst=[i.strip().lower() for i in Abstract[int(num)].split(" ")] # split Abstract to multi-sentance
        S=set(genusDict[str(c.upper())]) & set(tmpLst)
        TmpDict[PMID[num]]=[str(len(S)),";".join(list(S))]
    SPDict[str(c.upper())] = TmpDict

## OUT TABLEA
out = pd.DataFrame([SPDict["BACTERIA"],SPDict["FUNGI"],SPDict["VIRUSES"],SPDict["PARASITE"],PMIDict]).T
out.to_csv(prefix+".keyword",sep = "\t",header=None)
