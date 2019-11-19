# Leetcode
最近觉得人生有点无聊，所以决定干一件事----刷Leetcode。这个仓库是Leetcode题 和 平时自己想到/用到的一些小技巧(来自Biostar大神/国内CDNS大神/知乎大神/简书大神的分享)。自己监督吧，每天上传至少1个Leetcode的题目解答或者其他实用小技巧。

## 根据使用工具分类
### Bash
- 20190221 [Word Frequency](https://leetcode.com/problems/word-frequency/)
```bash
# 速度最快&资源最少的Accept
awk '{for(i=1;i<=NF;++i){++m[$i]}}END{for(k in m){print k, m[k]}}' words.txt | sort -nr -k 2
```
- 20190221 [随机抽取序列PairEnd]()
```bash
# 一行bash 随机抽取双端fastq并输出到R1.fq&R2.fq文件
awk '{ printf("%s",\$0); n++; if(n%4==0) { printf("\\n");} else { printf("\\t\\t");} }' | shuf | head -n $extCont | sed 's/\\t\\t/\\n/g' | awk -F "\\t" '{print \$1 > "R1.fq"; print \$2 > "R2.fq"}'
# shuf
```
- 20190221 [过滤长度低于某长度序列PairEnd]()
```bash
# 一行bash 过滤双端fastq(Read1+Read2 < 100)并输出到R1.fq&R2.fq文件
awk '{ printf("%s",\$0); n++; if(n%4==0) { printf("\\n");} else { printf("\\t\\t");} }' | sed 's/\\t\\t/\\n/g' | awk 'NR%4==1{a=\$0;{getline b; getline c; getline d; if(length(b) > $Lenthrd){print a"\\n"b"\\n"c"\\n"d}}}' | awk -F "\\t" '{print \$1 > "R1.fq"; print \$2 > "R2.fq"}'
# getline
``` 
- 20190222 [Valid Phone Number](https://leetcode.com/problems/valid-phone-numbers/)
```bash
grep -P '^(\d{3}-|\(\d{3}\) )\d{3}-\d{4}$' file.txt
sed -n -r '/^([0-9]{3}-|\([0-9]{3}\) )[0-9]{3}-[0-9]{4}$/p' file.txt
awk '/^([0-9]{3}-|\([0-9]{3}\) )[0-9]{3}-[0-9]{4}$/' file.txt
# regular express
# [0-9]{repNUM} == d{repNUM}
# (A|B) == A or B
# grep -P PATTERN is a Perl regular expression
# sed -r --regexp-extended use extended regular expressions in the script.
```

- 20190226 [transpose-file](https://leetcode.com/problems/transpose-file/)
```bash
awk '{for(i = 1; i <= NF; i++){if(NR == 1){a[i]=$i}else{a[i]=(a[i]" "$i)}}}END{for(i in a){print a[i]}}' file.txt
awk '{for(i=1; i<=NF; i++) a[i,NR]=$i} END {for(i=1; a[i,1]!=""; i++) {for(j=1; j<NR; j++) printf a[i,j] " "; print a[i,NR]}}' file.txt
```

最近在和某牙医合作写小论文，耽搁了不少事情啊～（都是借口）
那篇3月底的论文约稿能顺利完成啦～（好好干就能行）
已经**犯规**了（都是借口，做个小题目根本花不了多少时间），宽松一点，``平均``每天至少1个Leetcode的题目解答或者其他实用小技巧（杨同学说得对，不要给自己那么多框框条条啦～）

- 20190227 [Tenth Line](https://leetcode.com/problems/tenth-line/)
```bash
head -n 10 file.txt  | tail -n +10
tail -n +10 file.txt | head -n 1
# 这道题很损 看着很简单，其实有个小点损 If the file contains less than 10 lines
```

- 20190319 filter fasta by Length
```bash
cat test.fna | awk '{ printf("%s",$0); n++; if(n%2==0) { printf("\n");} else { printf("\t\t");} }' | sed 's/\t\t/\n/g' | awk 'NR%2==1{a=$0;{getline b; if(length(b) > 100){print a"\n"b}}}' > test_len100.fna
# getline to save next line
```

- 20190326 About '\n' '\t' '\' ' '(space) 的操作
```bash
# 空行
grep '^$'
# \t
grep -P "\t" # 这里注意，一定是双引号～
# 替换\n
sed ':a;N;s/\n/替换内容/g;ta' file.txt
# \ 匹配
grep "/\"
```

- 20190513 About "ls Argument list too long"
```bash
# ls *gff* | wc -l 
# ls Argument list too long
# find
find . -name '*gff*' | wc -l
```

### python
- 20190329 About [pool](https://docs.python.org/2/library/multiprocessing.html)(multiprocessing) in Python
```python
import multiprocessing

def func(argv):
    return "somethings"
    
pool = multiprocessing.Pool(processes=20) # 并行数
OUT = pool.map(mapID,(numLst)) # numLst must be iterable
pool.close()
pool.join()
```
- 20190329 [networkx](https://networkx.github.io/documentation/stable/_downloads/networkx_reference.pdf) 
```python
# make graph
G = nx.Graph([{from1,to1},{from1,to2} ...])
# get branch dict (when Graph isTree, setting source = root)
branch_dict = nx.single_source_shortest_path(G, 1) # root's nodenID = 1 in G
```
[Example_20190329](https://github.com/KidultXJT/Leetcode/blob/master/20190329.py) 处理nodes.dmp和names.dmp文件，输出：
```bash
# taxonomy_7.txt
@species\tkingdom__taxid__taxname\tphylum__taxid__taxname\tclass__taxid__taxname\torder__taxid__taxname\tfamily__taxid__taxname\tgenus__taxid__taxname\tspecies__taxid__taxname
@phylum\tkingdom____taxname\tphylum__taxid__taxname
```

##### Biopython
> Tools for **computational molecular biology**. Basically, the goal of Biopython is to make it as easy as possible to use Python for **bioinformatics** by creating high-quality, reusable modules and classes. Biopython features include parsers for various Bioinformatics file formats, **access to online services** (NCBI, Expasy,...), interfaces to common and not-so-common programs, a standard sequence class, various clustering modules, a KD tree data structure etc. 

- 20190404 [download_sequence_from_NCBI](biopython.org/DIST/docs/tutorial/Tutorial.html)
```python
from Bio import Entrez
# search in ncbi
search_handle = Entrez.esearch(db="nucleotide",term="search",usehistory="y", idtype="acc")
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
batch_size = 3 # download num of sequence each times
fa_handle = open("out.fasta", "w")
gb_handle = open("out.gb", "w")
for start in range(0, count, batch_size):
    end = min(count, start+batch_size)
    print("Going to download record %i to %i" % (start+1, end))
    attempt = 0
    while attempt < 3:
        attempt += 1
        try:
            # fetch by accession ID
            fetch_fa_handle = Entrez.efetch(db="nucleotide",rettype="fasta",retmode="text",retstart=start, retmax=batch_size,webenv=webenv,query_key=query_key,idtype="acc")
            fetch_gb_handle = Entrez.efetch(db="nucleotide",rettype="genbank",retmode="text",retstart=start, retmax=batch_size,webenv=webenv,query_key=query_key,idtype="acc")
        # if HTTPError just wait ~
        except HTTPError as err:
            if 500 <= err.code <= 599:
                print("Received error from server %s" % err)
                print("Attempt %i of 3" % attempt)
                time.sleep(15)
            else:
                raise
    fa = fetch_fa_handle.read()
    gb = fetch_gb_handle.read()
    fetch_fa_handle.close()
    fetch_gb_handle.close()
    fa_handle.write(fa)
    gb_handle.write(gb)
fa_handle.close()
gb_handle.close()
```
- 20190404 [get_accID_by_taxID](biopython.org/DIST/docs/tutorial/Tutorial.html)
```python
# taxID is a standard ID from NCBI/Taxonomy Database, taxID can convert to a Lineage information
# Step 1 convert taxID to a orgn information
handle = Entrez.efetch(db="Taxonomy", id=str(taxID), retmode="xml")
records = Entrez.read(handle)
records[0].keys()
out: ['Lineage', 'Division', 'ParentTaxId', 'PubDate', 'LineageEx', 'CreateDate', 'TaxId', 'Rank', 'GeneticCode', 'ScientificName', 'MitoGeneticCode', 'UpdateDate']
OrgnName = records[0]["ScientificName"]
# species name
# Step 2 base on orgn information to get the accession ID List
# set up the search ITEM
# "Arcanobacterium haemolyticum"[Organism] AND bacteria[filter]
searchSTR = '"{orgn}"[Organism] AND {division}[filter]'.format(
    orgn=str(orgn),
    division=str(records[0]["Division"]).lower())
search_handle = Entrez.esearch(db="nucleotide",term=searchSTR,usehistory="y", idtype="acc")
... # see below
```
- 20190404 [get_orgn_genomic_by_taxID](biopython.org/DIST/docs/tutorial/Tutorial.html)
```python
# taxID is a standard ID from NCBI/Taxonomy Database, taxID can convert to a Lineage information
# Step 1 convert taxID to a orgn information
... # see below
# Step 2 base on orgn information to get the genomic accession ID List
# set up the search ITEM
# "Arcanobacterium haemolyticum"[Organism] AND (bacteria[filter] AND biomol_genomic[PROP])
searchSTR = '"{orgn}"[Organism] AND ({division}[filter] AND biomol_genomic[PROP])'.format(
    orgn=str(orgn),
    division=str(records[0]["Division"]).lower())
... # see below
```
[Example_20190404](https://github.com/KidultXJT/Leetcode/blob/master/20190404.py) 根据taxid查找物种名称并进行精确匹配下载基因组序列（e.g. "Arcanobacterium haemolyticum"[Organism] AND (bacteria[filter] AND biomol_genomic[PROP])）：
```bash
python 20190404.py taxidFile taxidFile_outdir
## input taxid from NCBI::taxonomy
46125
32002
85698
187327
80869
470
## output fasta
## e.g. Division-speciesName-taxid.fasta
.
`-- taxidFile_outdir
|  |-- Bacteria-Abiotrophia_defectiva-46125.fasta
|  |-- Bacteria-Achromobacter_denitrificans-32002.fasta
|  |-- Bacteria-Achromobacter_xylosoxidans-85698.fasta
|  |-- Bacteria-Acidaminococcus_intestini-187327.fasta
|  |-- Bacteria-Acidovorax_citrulli-80869.fasta
|  `-- Bacteria-Acinetobacter_baumannii-470.fasta
`-- taxidFile.completed
```

- 20191118 [DownLoadAbstractbyKeyword](https://biopython-cn.readthedocs.io/zh_CN/latest/cn/chr09.html)
Entrez (http://www.ncbi.nlm.nih.gov/Entrez) 是一个给客户提供NCBI各个数据库（如PubMed, GeneBank, GEO等等）访问的检索系统。 用户可以通过浏览器手动输入查询条目访问Entrez，也可以使用Biopython的 Bio.Entrez 模块以编程方式访问来访问Entrez。 如果使用第二种方法，用户用一个Python脚本就可以实现在PubMed里面搜索或者从GenBank下载数据。
```python
# Keywords that search in the NCBI brower, like AAAA AND BBB 
# " " instead of "_"
# Step 1 dealing the keyword
# Step 2 use Bio.Entrez get PMID
# ... Entrez.esearch(db="pubmed",term=keyword,retmax=int(Top)) ...
# Step 3 get Abstract Text
# ... Entrez.efetch(db='pubmed',rettype='abstract',id=pmid,retmode='text') ...
```
[Example_20191118](https://github.com/KidultXJT/Leetcode/blob/master/20191118.py) 根据关键词查找PMID并下载对应的Abstract：
```bash
# keyword  Cryptococcus_neoformans_AND_Meningitis
# prefix Cryptococcus_neoformans_AND_Meningitis_200
# Top 200 (Try 200)
python 20181118.py Cryptococcus_neoformans_AND_Meningitis Cryptococcus_neoformans_AND_Meningitis_200 200
# output:
# with PMID: 
# with Abstract All Text
```
注意一个问题：
本次代码用到了 Bio.Entrez 模块，这个模块可以保证用来查询的URL的正确性，<u>并且向NCBI要求的一样，``每三秒钟查询的次数不超过一``。</u>

- 20191119 SummaryAbstract From [Example_20191118](https://github.com/KidultXJT/Leetcode/blob/master/20191118.py)
注意一个问题：
Example_20191118 代码在Abstract文本之间插入了 "\n\nNextItem"
```python 
#...
def GetAbstract(PMIDs=['31703006']):
    ## PMIDs from GetPMID(keyword)
    Lst = []
    for i in PMIDs:
        i = int(i)
        handle=Entrez.efetch(db='pubmed', rettype='abstract', id=i, retmode='text')
        handle_text=handle.read()
        Lst.append(handle_text)
    Abstracts="\n\nNextItem".join(Lst) ## <--------- Here !!!!
    return Abstracts
#...
```
所以对应的 Example 20191119 中对应的代码需要留意：
```python
# ...
abstract_format=open(abstract.split(".")[0]+".ab","w")
Abstract=Abstract.read().replace("\n"," ").replace("  "," ")
PMID=[" ".join(str(i.split("PMID")[-1].strip().replace(":","PMID:")).split(" ")[:2]) for i in Abstract.split("NextItem")]
Abstract=[i.strip() for i in Abstract.split("NextItem")]
# ...
```
输出结果包含两部分：
1. 整理后的Abstract表格(column1为PMID；column2为其他文本，后缀为.ab)
2. 信息提取(column1为PMID；column2-9为bacteria/fungi/viruses/parasite NUM和genus信息；column10-11为Keyword NUM及包含keyword句子，后缀为.keyword)
3. log文件
```bash
for i in `ls *.txt`; do echo ${i%%_200_Abstract.txt} ; cat Summary/${i%%_Abstract.txt}*.log | sort -u ;done
# Keyword Match: x
# Keyword maybe Match: y
# There are n/m genus in PARASITE
# There are n/m genus in BACTERIA
# There are n/m genus in FUNGI
# There are n/m genus in VIRUSES
# Match 代表全匹配
# maybe Match 代表部分匹配
# There are n/m genus in *
# n 为 Abstract 文本中出现匹配的单词次数
# m 为 db/*.genus 数据库列表中genus的数量，其中，db的字符串可能是重复（例如simplex和hsv，同时存在）
```
代码见 [Example_20191118](https://github.com/KidultXJT/Leetcode/blob/master/20191119.py)

- 20190409 [pandas001](http://pandas.pydata.org/)
pandas: powerful Python data analysis toolkit[(Documents)](http://pandas.pydata.org/pandas-docs/stable/). And Coursera ::[python data analysis](https://www.coursera.org/learn/python-data-analysis)

- 20191119 [Graphene](https://docs.graphene-python.org/en/latest/quickstart/) 
Graphene is a library that provides tools to implement a GraphQL API in Python using a code-first approach. Compare Graphene’s code-first approach to building a GraphQL ``API`` with schema-first approaches like Apollo Server (JavaScript) or Ariadne (``Python``). Instead of writing GraphQL Schema Definition Language (SDL), <u>we write Python code to describe the data provided by your server.</u> **Graphene** is fully featured with integrations for the most popular ``web frameworks`` and ``ORMs``. Graphene produces schemas tha are fully compliant with the [GraphQL](https://graphql.org/code/?source=post_page---------------------------#python) spec and provides tools and patterns for building a Relay-Compliant API as well. 
[GraphQL to Json by Graphene](https://docs.graphene-python.org/en/latest/_modules/graphene/types/json/#JSONString)
