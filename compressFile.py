from bs4 import BeautifulSoup
from hashlib import md5
import os
import random
 
#合并后的js文件目录，并创建该目录
#需要合并的js序列
#合并文件函数
class compressFile(object):
	#给文件增加md5戳
	def fileMd5(self,fileName):
		#首先判断文件是否是写在了根目录，其次判断文件是否存在
		if(fileName[0] == '/'):
			fileName = os.getcwd() + fileName;
		if(os.path.isfile(fileName)):
			m = md5();
			with open(fileName,'rb') as fileContent:
				m.update(fileContent.read());
			return m.hexdigest()[0:8];
		else:
			return str(random.randint(1, 99999999))
    #遍历html或者tpl文件，是的话根据其中文件内容的更改来更改版本号
	def searchFileChange(self,originDir):
		for fileItem in os.listdir(originDir):
			if '.git' not in fileItem:
				newitem = originDir +'\\'+ fileItem
				if(os.path.isdir(newitem)):
					self.searchFileChange(newitem);
				else:
					fileType = os.path.splitext(newitem)[1];
					if(fileType == '.html' or fileType == '.tpl'):
						originList = [];
						replaceList = [];
						#寻找需要替换的文件内容
						with open(newitem, 'r+', buffering=163840, encoding='utf8') as srcHtml:
							line = srcHtml.readline();
							while line:
								bItem = BeautifulSoup(line,'html.parser');
								try:
									#判断外链的script标签
									if(bItem.script != None and bItem.script['src'].find('//') == -1):
										fileSrc = bItem.script['src'];
										filePathName = fileSrc.split('?')[0];
										fileMd5Value = self.fileMd5(filePathName);
										originList.append(fileSrc);
										replaceList.append(filePathName+'?v='+fileMd5Value)
									#判断外链的link标签
									if(bItem.link != None and bItem.link['href'].find('//') == -1):
										fileSrc = bItem.link['href'];
										filePathName = fileSrc.split('?')[0];
										fileMd5Value = self.fileMd5(filePathName);
										originList.append(fileSrc);
										replaceList.append(filePathName+'?v='+fileMd5Value)
								except KeyError:
									pass
								line = srcHtml.readline();
						    #加入版本号后替换
							if len(originList) == len(replaceList):
								srcHtml.seek(0, 0)
								fileContent = srcHtml.read();
								for index in range(len(originList)):
									fileContent = fileContent.replace(originList[index],replaceList[index]);
							srcHtml.seek(0, 0)
							srcHtml.write(fileContent);
	#主文件
	#盛放需要合并js的列表
	def searchFile(self,origin,dist):
		print('spt release -r %s -od %s' % (origin,os.getcwd()+'\\'+dist));
		os.system('spt release -r %s -od %s' % (origin,os.getcwd()+'\\'+dist))