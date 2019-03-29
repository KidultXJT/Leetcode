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
