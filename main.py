#encoding=utf-8
import os;
import time;
from removeFile import removeFile
from compressFile import *;

#让使用者输入需要执行的目录
exeDir = input('请输入执行目录');
#切换到执行目录
dirInfo = os.path.split(exeDir);
os.chdir(dirInfo[0]);

#给文件增加版本号
compressObject = compressFile();
compressObject.searchFileChange(exeDir);

#创建clone后的文件名
fileName = int(time.time());

#克隆项目代码
cloneCmd = 'git clone git@************.git %s' % fileName;
os.system(cloneCmd);

#切到文件目录并切换分支
os.chdir(os.getcwd()+'\\'+str(fileName));
goReleaseBranch = 'git checkout -b release origin/release';
os.system(goReleaseBranch)

#删除非git信息内容
removeFile.remove();

#压缩js和css从原始目录输出到目标目录
os.chdir(dirInfo[0]);
compressObject.searchFile(dirInfo[1],str(fileName));

#切到clone下来的分支，并进行代码提交
os.chdir(os.getcwd()+'\\'+str(fileName));
#add 代码
addCmd = 'git add .';
os.system(addCmd);
#commit 代码
commitCmd = 'git commit -m %s' % fileName;
os.system(commitCmd);
#push 代码
pushCmd = 'git push';
os.system(pushCmd);

#删除克隆得到的项目文件
os.system('rd /s /q %s' % fileName);
#操作完成标识
print('done');