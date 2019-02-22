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
