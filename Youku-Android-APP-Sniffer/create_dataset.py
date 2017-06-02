# -*- coding:utf-8 -*-  
import re
import urllib2
import json
import csv

from scapy.all import *
from YoukuVideo import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

video_id_list = []                  # 视频的id列表
youku_video_list = []               # 视频的列表
categoryCountDict = {}              # 视频的类别字典{id,category}
dataset_filename = "dataset.csv"	# 数据集的名称

####### 分析优酷数据包 #######
def findYouku(pkt):
	if pkt.haslayer(Raw):
		payload = pkt.getlayer(Raw).load		
		if 'GET' in payload:
			# “获得JSON数据的HTTP请求地址”包含了“layout”字符串
			if 'layout' in payload:
				# 通过字符串拼接，组成完整的HTTP请求地址（调用了getJsonUrl函数）
				json_url = str('http://detail.api.mobile.youku.com' + getJsonUrl(payload))
				# 调用解析JSON的函数
				dealJson(json_url)

###### 从payload中返回JSON的URL地址 ######
def getJsonUrl(payload):
	str_payload = str(payload)
	print str_payload
	# 运用正则表达式
	pattern = re.compile(r'GET (.*?)HTTP/1.1', re.S)
	item_list = pattern.findall(str_payload)
	if item_list:
		return item_list[0]

###### 处理JSON，并将获得的数据存储到CSV文件里######
def dealJson(url):
	try:
		html = urllib2.urlopen(url)
		json_str = json.loads(html.read())
		#print json_str
		temp_id = json_str["detail"]["videoid"]           # 当前视频的id
		temp_title = json_str["detail"]["title"]          # 当前视频的标题
		temp_category = json_str["detail"]["cats"]        # 当前视频的类别
		temp_description = json_str["detail"]["desc"]     # 当前视频的描述  		
		
		#  如果该视频的id已经在视频的id列表中
		if (str(temp_id) in video_id_list):
			print "这个视频已经被记录过"
		#  如果该视频的id不在视频的id列表中
		else:
			#  将视频的id加入视频的id列表中
			video_id_list.append(str(temp_id))
			#  调用saveVideo函数
			saveVideo(temp_id, temp_title, temp_category, temp_description)	
		
	except Exception, e:
		traceback.print_exc()  
	
###### 将视频的id、标题、类别、描述封装成一个对象并将该对象存入列表 ######
def saveVideo(id, title, category, describtion):
	youkuVideo = YoukuVideo()
	youkuVideo.id = id		
	youkuVideo.title = title
	youkuVideo.describtion = describtion
	youkuVideo.category = category
	youku_video_list.append(youkuVideo)	
	saveYoukuVideoToCSV(youkuVideo, dataset_filename)

###### 将YoukuVideo对象保存到名为filename的CSV文件中 ######
def saveYoukuVideoToCSV(youkuVideo, filename):
	id = youkuVideo.id		
	title = youkuVideo.title
	# 使用python的csv库修改CSV文件
	category = youkuVideo.category
	csvFile = open(filename,"a")
	try:
		writer = csv.writer(csvFile)
		writer.writerow((id, title, category))
	finally:
		csvFile.close()
	
def main():
	try:
		print('[*] Starting Youku Sniffer.')
		sniff(filter='tcp port 80', prn=findYouku, iface='wlan2')
		# 调用的scapy的sniff方法，该方法就可用来监听数据
		# prn是数据包的处理函数，我们要在此做数据包的解析，分析等工作
		# 可参见：https://zhuanlan.zhihu.com/p/23198924?refer=xh-coding
	except Exception, e:
		traceback.print_exc()  
			
if __name__ == '__main__':
    main()