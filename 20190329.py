import os
import sys
import time
import networkx as nx

import threading
import multiprocessing


nodesFILE = sys.argv[1]
namesFILE = sys.argv[2]
IDs       = sys.argv[3]
pfx       = sys.argv[4]

print str(time.time())
edgesLst = [] # [{nodex,nodey},{nodex,nodez}...]
nodes = open(nodesFILE,"r")
for line in nodes.readlines():
    if line.split("\t")[0]!=line.split("\t")[2]:
        edgesLst.append(set([int(line.split("\t")[2]),int(line.split("\t")[0])]))       
nodes.close()

# Make Graph
G = nx.Graph(edgesLst)
# Make Path
path_dict = nx.single_source_shortest_path(G, 1)

IDLst = [int(line.strip()) for line in open(IDs).readlines()]
GraphPathLst = ["\t".join([str(node) for node in list(path_dict[int(ID)])]) for ID in IDLst]

GraphOUT = open(pfx+"root.taxid","w")
GraphOUT.write("\n".join(GraphPathLst))
GraphOUT.close()
print str(time.time())


rootFILE  = pfx+"root.taxid"

nodesLst = [] # [node1,node2,node3,node4 ...]
levelLst = [] # [node1level,node2level,node3level,node4level ...]
namesLst = [] # [name1,name2,name3,name4 ...]
taxidLst = [] # [name1taxid,name2taxid,name3taxid,name4taxid ...]
branches = [line.strip() for line in open(rootFILE).readlines()]

nodes = open(nodesFILE,"r")
for line in nodes.readlines():
    nodesLst.append(int(line.split("\t")[0]))
    levelLst.append(line.split("\t")[4])
nodes.close()
nodes_dict = dict(zip(nodesLst,levelLst))

names = open(namesFILE,"r")
for line in names.readlines():
    namesLst.append(line.split("\t")[2])
    taxidLst.append(int(line.split("\t")[0]))
names.close()
names_dict = dict(zip(taxidLst,namesLst))

def mapID(num):
    taxids = [int(node) for node in branches[num].split("\t")]
    taxid_dict = dict()
    [taxid_dict.update({str(nodes_dict[int(taxid)]):[str(taxid),str(names_dict[int(taxid)])]}) for taxid in taxids] # level__name
    taxid_tmp = ["__".join([str(nodes_dict[int(taxid)]),str(taxid),str(names_dict[int(taxid)])]) for taxid in taxids] # level__name
    taxid_9_Lst = []
    for level in ["superkingdom","kingdom","subkingdom","phylum","class","order","family","genus","species"]:
        if str(level) in taxid_dict.keys():
            taxid_9_Lst.append("__".join([level,taxid_dict[level][0],taxid_dict[level][1]]))
        else:
            taxid_9_Lst.append("__".join([level,"",""]))
           # [@node_level\t...\t...taxid_9...\t...] [@node_level\t...\t...taxid_all...\t...]
    return ["\t".join(["@"+str(nodes_dict[int(taxid)]),"\t".join(taxid_9_Lst)]),"\t".join(["@"+str(nodes_dict[int(taxid)]),"\t".join(taxid_tmp)])]

print str(time.time())
pool = multiprocessing.Pool(processes=20)
numLst = range(len(branches))
OUT = pool.map(mapID,(numLst))
pool.close()
pool.join()

print str(time.time())
taxid_9_OUT   = []
taxid_all_OUT = []
for out in OUT:
    taxid_9_OUT.append(out[0])
    taxid_all_OUT.append(out[1])
taxidallOUTFILE  = open(pfx+"taxonomy_all.txt","w")
taxidallOUTFILE.write("\n".join(taxid_all_OUT))
taxidallOUTFILE.close()
taxid9OUTFILE  = open(pfx+"taxonomy_9.txt","w")
taxid9OUTFILE.write("\n".join(taxid_9_OUT))
taxid9OUTFILE.close()
print str(time.time())

tax9 = open(pfx+"taxonomy_9.txt","r")
tax9STR = tax9.read()
tax9.close()

def kingdom(STR):
    kingdom_dict = {"superkingdom__2759__Eukaryota\tkingdom__33208__Metazoa\tsubkingdom____":"kingdom__2759__Eukaryota",
                    "superkingdom__2__Bacteria\tkingdom____\tsubkingdom____":"kingdom__2__Bacteria",
                    "superkingdom__2759__Eukaryota\tkingdom__33090__Viridiplantae\tsubkingdom____":"kingdom__2759__Eukaryota",
                    "superkingdom__10239__Viruses\tkingdom____\tsubkingdom____":"kingdom__10239__Viruses",
                    "superkingdom__2759__Eukaryota\tkingdom__4751__Fungi\tsubkingdom__451864__Dikarya":"kingdom__4751__Fungi",
                    "superkingdom__2759__Eukaryota\tkingdom____\tsubkingdom____":"kingdom__2759__Eukaryota",
                    "superkingdom__2759__Eukaryota\tkingdom__4751__Fungi\tsubkingdom____":"kingdom__4751__Fungi",
                    "superkingdom____\tkingdom____\tsubkingdom____":"kingdom____",
                    "superkingdom__2157__Archaea\tkingdom____\tsubkingdom____":"kingdom__2157__Archaea",
                    "superkingdom__12884__Viroids\tkingdom____\tsubkingdom____":"kingdom__12884__Viroids"}
    tmp = STR
    for r in kingdom_dict.keys():
        tmp = tmp.replace(str(r),str(kingdom_dict[str(r)]))
    return tmp

tax7STR = kingdom(tax9STR)
tax7STR_OUTFILE  = open(pfx+"taxonomy_7.txt","w")
tax7STR_OUTFILE.write(tax7STR)
tax7STR_OUTFILE.close()
