# coding=utf-8

import requests
import sys
from bs4 import BeautifulSoup

class downloader(object):
    def __init__(self):
        self.target="http://www.biquge5200.com/38_38857/"
        self.server="http://www.biquge5200.com/"
        self.names=[]
        self.urls=[]
        self.nums=[]


    def get_download_url(self):
        req=requests.get(url=self.target)
        html=req.text
        div_bf=BeautifulSoup(html)
        div=div_bf.find_all('div',id='list')
        a_bf=BeautifulSoup(str(div[0]))
        a=a_bf.find_all('a')
        self.nums=len(a[9:])
        for each in a[9:]:
            self.names.append(each.string)
            self.urls.append(each.get('href'))


    # 获取章节内容，
    #    target：下载链接
    #    texts：章节内容
    def get_contents(self,target):
        req=requests.get(target)
        html=req.text
        bf=BeautifulSoup(html)
        texts=bf.find_all('div',id='content')
        # texts=texts[0].text.replace('　　','\n\n')
        return texts


    # 写入文件
    # name：章节名称
    # path：小说保存名字
    # text：章节内容

    def writer(self,name,path,text):
        writer_flag=True
        with open(path,'a',encoding='utf-8') as f:
            f.write(name+'\n')
            f.write(str(text))
            f.write('\n\n')

if __name__=="__main__":
    dl=downloader()
    dl.get_download_url()
    print('《一念永恒》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i],'一念永恒.txt',dl.get_contents(dl.urls[i]))
        sys.stdout.write("已下载: %.3f%%" % float(i/dl.nums*100)+'\n')
        sys.stdout.flush()
    print('《一念永恒》下载完成！')



