#!usr/bin/python
# -*- coding:utf-8 -*-

## --------------------------------------------------------
## Author: Kidult
## Email : junting.xie@sagene.com.cn
## Date  : 2017-09-26
## --------------------------------------------------------
## Description: 
## DownLoad Sequence From NCBI. 

# module
from optparse import OptionParser
from pandas import Series, DataFrame
import pandas as pd
import sys
import os
import re

import threading
import multiprocessing

taxid_FILE = sys.argv[1] # 1 ID each line
outdir     = sys.argv[2] # exist


# BioPython
from Bio import Entrez
# urllib
try:
	from urllib.error import HTTPError
except ImportError:
	from urllib2 import HTTPError

def NCBIDownLoadSeq(
    email="junting.xie@sagene.com.cn",
    ID=None,    # ID can Be Everythings:: AssesionID
    Top=99999999999999999,
    out=os.path.abspath(outdir)
    ): # Unhappy Face
   # Description:
   # Use BioPython To DownLoad NCBI Sequence By An/Some Informations, Such As "AssesionID", "GeneSymbol" and So on.
   # Try "Top" Argument, if You Don't have Enough Information, Or You might DownLoad So Many Things
    from Bio import Entrez
    Entrez.email = str(email)
    # search species Name
    handle=Entrez.efetch(db="Taxonomy",id=str(ID),retmode="xml")
    records=Entrez.read(handle)
    handle.close()
    orgn = records[0]["ScientificName"]
    print orgn
    # search in ncbi
    searchSTR = '"'+ str(orgn) +'"' + "[Organism] AND (" + str(records[0]["Division"]).lower() + "[filter] AND biomol_genomic[PROP])"
    search_handle = Entrez.esearch(db="nucleotide",term=searchSTR,usehistory="y", idtype="acc")
    search_results = Entrez.read(search_handle)
    search_handle.close()
    # accession ID list
    acc_list = search_results["IdList"]
    count = len(acc_list)
    # webenv session cookies and querykey
    webenv = search_results["WebEnv"]
    query_key = search_results["QueryKey"]
    # Download
    try:
        from urllib.error import HTTPError  # for Python 3
    except ImportError:
        from urllib2 import HTTPError  # for Python 2
    batch_size = 5 # download num of sequence each times
    print str(out)+"/"+str(records[0]["Division"])+"-"+str(orgn.replace(" ","_").replace("/","_"))+"-"+str(ID)+".fasta"
    fa_handle = open(str(out)+"/"+str(records[0]["Division"])+"-"+str(orgn.replace(" ","_").replace("/","_"))+"-"+str(ID)+".fasta", "w")  # Bacteria_speciesName_taxid.fasta
    for start in range(0, count, batch_size):
        end = min(count, start+batch_size)
        print("Going to download record %i to %i" % (start+1, end))
        attempt = 0
        while attempt < 3:
            attempt += 1
            try:
                # fetch by accession ID
                fetch_fa_handle = Entrez.efetch(db="nucleotide",rettype="fasta",retmode="text",retstart=start, retmax=batch_size,webenv=webenv,query_key=query_key,idtype="acc")
            # if HTTPError just wait ~
            except HTTPError as err:
                if 500 <= err.code <= 599:
                    print("Received error from server %s" % err)
                    print("Attempt %i of 3" % attempt)
                    time.sleep(15)
                else:
                    raise
        fa = fetch_fa_handle.read()
        fetch_fa_handle.close()
        fa_handle.write(fa)
    fa_handle.close()
# Loading 
IDLst = [str(line.strip()) for line in open(taxid_FILE).readlines()]

if os.path.exists(taxid_FILE+".completed"):
    IDLst = list(set(IDLst).difference(set([str(line.strip()) for line in open(taxid_FILE+".completed").readlines()])))
    completed = open(taxid_FILE+".completed","a")
else: 
    completed = open(taxid_FILE+".completed","w")
   
if len(IDLst) == 0:
    print "Already Done. The Download files were in the " + str(os.path.abspath(outdir)) + " Please Check ~"
else:
    print "Num of Taxid: " + str(len(IDLst))
    for ID in IDLst:
        print str(ID)
        NCBIDownLoadSeq(ID=str(ID))
        completed.write(str(ID)+"\n")
    completed.close()

