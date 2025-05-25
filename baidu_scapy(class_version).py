import os
import re
import requests
import time
tips ='''
# 使用须知：
# 每次爬取要注意的有以下两点：

# 1）保存文件的路径
# 2) 保证你选取的页数可以满足你要爬取的数量
# 3) 该脚本只能爬取部分百度图片，请检查所要爬取页面的源代码的network\\fetch\\xhr页面
     若该页面的preview的data项目旁边有个小三角形，则可以爬取该页面
# 4) 如果输入的路径为空，该程序将会自动在工作目录下创建一个image文件夹用以存储数据
# 5) 如果报错信息中出现：
# 5） 如果报错信息中出现
requests.exceptions.JSONDecodeError: Invalid \escape: line 12 column 154 (char 25438)
说明该网页属于不可爬取的百度图片网页一类。'''





headers = {'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#            'Host':
#                'image.baidu.com',
# 'Referer':
# 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDEsMiw2LDQsNSw3LDgsOQ%3D%3D&word=%E8%B5%9B%E6%96%87'
           }






class Scapy:
    def __init__(self,path):
        self.number = 1
        self.check1 = False
        self.name = ''
        self.path = path
        self.check2 = False
        self.check = False
        self.image_path = None

    def download_path1(self,path):
        self.name = os.path.join(path, f'{self.number}.jpg')

    #需要微调
    def download_path2(self,image_path):
        self.name = os.path.join(image_path, f'{self.number}.jpg')
    def _check_path(self, path):
        if os.path.exists(path):
            self.check1 = True
            self.check = True
        elif path == '':
            self.image_path = os.path.join(os.getcwd(), 'image')
            try:
                os.mkdir(self.image_path)
            except FileExistsError:
                pass
            self.check2 = True
            self.check = True

        else:
            print('请输入正确的路径!')

    def baidu_scapy(self,page,piece,url):
        self._check_path(self.path)
        replace = re.compile('pn=\d+')
        if self.check:
            if page > 1:
                st = time.time()
                #网页解析
                for page in range(1, page):
                    if self.number <= piece:
                        pn = page*30
                        pag = f'pn={pn}'
                        sub_url = replace.sub(pag,url)
                        res = requests.get(sub_url,headers = headers)
                        json_res = res.json()
                        json_data = json_res['data']
                        #批量下载图片
                        for data in json_data[:-1] :
                            try:
                                if self.check1 and not self.check2:
                                    hover_name = data['fromPageTitle']
                                    ima_url = data['hoverURL']
                                    if self.number <= piece:
                                        ima = requests.get(ima_url)
                                        real_ima = ima.content
                                        self.download_path1(self.path)
                                        with open(self.name,'wb') as f:
                                            f.write(real_ima)
                                        print(f'已经将图片保存到以下路径：{self.name}')
                                        print(hover_name, ima_url)
                                        self.number += 1
                                    else:
                                        ed = time.time()
                                        duration = ed - st
                                        print('\n已经爬取了%d张图片 ! 总用时%.5f秒 !' % (piece, duration))
                                        break

                                elif self.check2 and not self.check1:
                                    hover_name = data['fromPageTitle']
                                    ima_url = data['hoverURL']
                                    if self.number <= piece:
                                        ima = requests.get(ima_url)
                                        real_ima = ima.content
                                        self.download_path2(self.image_path)
                                        with open(self.name, 'wb') as f:
                                            f.write(real_ima)
                                        print(f'已经将图片保存到以下路径：{self.name}')
                                        print(hover_name, ima_url)
                                        self.number += 1

                                    else:
                                        ed = time.time()
                                        duration = ed - st
                                        print('\n已经爬取了%d张图片 ! 总用时%.5f秒 !' % (piece, duration))
                                        break
                            except requests.exceptions.MissingSchema:
                                continue
                    else:
                        break

            else:
                print("\n请输入大于1的页数(至少为2，输入2则爬取第一页)")

if __name__ == '__main__':
    print(tips)
    print('\n')
    path = input('请选择想要保存到的路径：\n')
    pages = int(input("请输入想要爬取的页数： "))
    pieces = int(input('请输入想要爬取的张数： '))
    url = input('请输入想要爬取的百度图片网址：\n')

    scapy = Scapy(path)

    scapy.baidu_scapy(pages,pieces,url)






