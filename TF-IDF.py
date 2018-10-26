#统计TF-IDF值
import requests
from bs4 import BeautifulSoup
import re	
import math

#定义IDF(逆向文本频率)为全局变量，减少重复计算
IDF = {}

#获取网页内容
def getHTMLtext(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print("getHTMLtext error")
		return ""

#读取文件，并改为小写，并处理特殊字符为空格
def getText(fileName):
	txt = open(fileName, 'r').read()				#打开文件，读入txt
	txt = txt.lower()								#改为小写字母
	for c in '!"$%^&*()+,-./:;<=>?@[\\]_\'’{|}~':	#去除特殊字符，用空格代替
		txt = txt.replace(c, " ")
	return txt

#查询单词在所有文本出现的次数
def cntInAllText(corpusUrl, word):
	html = getHTMLtext(corpusUrl + word)										#搜索对应单词，获取内容
	soup = BeautifulSoup(html, "html.parser")
	panel = soup.find_all('div', attrs = {'class':'panel panel-primary'})[0]	#找到class为panel panel-primary的div
	p = panel.find_all('p', attrs = {'style':'float:right'})[0].text 			#找到包含文本总个数的字符串
	num = re.findall(r'\d+ results', p)[0][0:-8]								#得到包含单词的文本个数
	return eval(num)

#计算每个单词的IDF值
def getIDF(words):
	corpusUrl = 'http://bcc.blcu.edu.cn/en/search/10/'		#语料库url
	#先计算文本的总数，假设包含'a'的文本数量为文本总数
	totalCnt = cntInAllText(corpusUrl, 'a') + 1
	#分别计算每个单词在多少个文件中出现
	global IDF
	i = 1
	for word in words:
		if IDF.get(word, 0) == 0:							#未计算过此单词的IDF才计算
			IDF[word] = math.log(totalCnt / (1 + cntInAllText(corpusUrl, word)))
		else :
			print('{}命中'.format(word))
		print('{}/{}'.format(i, len(words)))
		i = i + 1 

#计算每个单词的TF值
def getTF(words):
	totalNum = len(words)			#求总的单词数
	TF = {}							#字典数据类型，存放单词对应的TF值
	for word in words:
		TF[word] = TF.get(word, 0) + 1 / totalNum
	return TF

#计算文本中每个单词的TF-IDF值
def getTF_IDF(txt):	
	words = txt.split()		#按照空格分隔单词
	TF = getTF(words)		#计算词频
	getIDF(words)			#计算逆向文件频率
	TF_IDF = {}

	global IDF
	words = TF.keys()		#得到所有键值对的键的信息，即去重后的单词
	for word in words:
		TF_IDF[word] = TF[word] * IDF[word]		#计算TF_IDF值

	return TF_IDF

#打印结果信息
def printf(items):
	for i in range(len(items)):
		word, TF_IDF = items[i]
		print("{0:<20}{1:>10}".format(word, TF_IDF))
	print('*******************************************************')

#主函数
def main():
	#初始化变量和参数
	fileList = ['AI becomes more alien.txt', 'China won’t be major rival to US.txt', 'KFC told to stop using chicken treated with antibiotics.txt']
	ans = []		#存放最终TF-IDF的计算结果
	
	#分别计算每一个文件的TF-IDF
	for fileName in fileList:
		txt = getText(fileName)
		TF_IDF = getTF_IDF(txt)
		ans.append(TF_IDF)
	
	#排序
	for counts in ans:
		items = list(counts.items())				#将字典类型变为列表类型 便于排序
		items.sort(key=lambda x:x[1], reverse=True)	#对键值对的第二个元素进行排序  reverse为True是从大到小
		
		#打印结果
		printf(items)

main()
