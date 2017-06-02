# -*- coding:utf-8 -*-  

import csv
dataset_filename = "dataset.csv"	# 数据集的名称
categoryCountDict = {}              # 视频的类别字典{id,category}

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

###### 依据字典categoryCountDict进行排序，将用户点播频数最高的“类别”当成用户的视频点播偏好 ######
def getTheFavorite(categoryCountDict):
	return str(max(categoryCountDict, key=categoryCountDict.get)).decode('utf-8')

###### 依据数据集“dataset.csv”进行分类 ######
def classify(filename):
	with open(filename,'r') as f1:
		for line in f1:
			l = line.split(",")
			id = l[0]
			title = l[1]
			category = l[2]

			#  用于统计各类别的视频的个数
			if category in categoryCountDict:
				categoryCountDict[category] += 1
			else:
				categoryCountDict[category] = 1

	# 打印视频的类别及其播放频次
	for key,value in categoryCountDict.items():
		print 'key=',key,'，value=',value
	print "用户的视频点播偏好是：" + getTheFavorite(categoryCountDict)
			
if __name__ == '__main__':
    classify(dataset_filename)

