#encoding=utf-8
#删除目录中非git相关的信息

import os
import os.path

class removeFile(object):
	def remove():
		for item in os.listdir():
			if '.git' not in item:
				if os.path.isdir(item):
					os.system('rd /s /q %s' % item);
				else:
					os.system('rd %s' % item);