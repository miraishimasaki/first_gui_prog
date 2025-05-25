import os
import re
import requests
import time
tips =''' 
# 使用须知：
# 每次爬取要注意的有以下几点：
# 1）保存文件的路径
# 2) 保证你选取的页数可以满足你要爬取的数量
# 3) 该脚本只能爬取部分百度图片，请检查所要爬取页面的源代码的network\\fetch\\xhr页面。若该页面的preview的data项目旁边有个小三角形，则可以爬取该页面
# 4) 如果输入的路径为空，该程序将会自动在工作目录下创建一个image文件夹用以存储数据
# 5) 如果报错信息中出现：\'请检查输入的url格式是否正确！\' 则说明您输入的url无效
# 5） 如果报错信息中出现:\'请检查输入的url是否为能爬取的网页对象的url\'  则说明该网页属于暂时无法爬取的那一类百度图片'''



headers = {'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
#            'Host':
#                'image.baidu.com',
# 'Referer':
# 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDEsMiw2LDQsNSw3LDgsOQ%3D%3D&word=%E8%B5%9B%E6%96%87'
           }



def baidu_scapy(page, piece, path,url):
    situation1 = True
    replace = re.compile('pn=\d+')
    number = 1
    if page > 1:
        st = time.time()
        for page in range(1, page):
            if number <= piece:
                pn = (page*30)
                pag = f'pn={pn}'
                sub_url = replace.sub(pag,url)
                try:
                    res = requests.get(sub_url,headers = headers)
                    json_res = res.json()
                    json_data = json_res['data']
                except requests.exceptions.JSONDecodeError:
                    situation1 =False
                except requests.exceptions.MissingSchema:
                    print('\n请检查输入的url格式是否正确！')
                if situation1:
                    try:
                        for data in json_data[:-1] :
                            try:
                                hover_name = data['fromPageTitle']
                                ima_url = data['hoverURL']
                                if number <= piece:

                                    if path != '':
                                        if os.path.exists(path):
                                            ima = requests.get(ima_url)
                                            real_ima = ima.content
                                            name = os.path.join(path,f'{number}.jpg')
                                            with open(name,'wb') as f:
                                                f.write(real_ima)
                                            print(f'已经将图片保存到以下路径：{name}')
                                            print(hover_name, ima_url)
                                            number += 1
                                        else:
                                            print('请输入正确的路径！！！！！')
                                            break
                                    else:
                                        ima = requests.get(ima_url)
                                        real_ima = ima.content
                                        image_path = os.path.join(os.getcwd(),'image')
                                        try:
                                            os.mkdir(image_path)
                                        except FileExistsError:
                                            pass
                                        name = os.path.join(image_path,f'{number}.jpg')
                                        with open(name,'wb') as f:
                                            f.write(real_ima)
                                        print(f'已经将图片保存到以下路径：{name}')
                                        print(hover_name, ima_url)
                                        number += 1

                                else:
                                    ed = time.time()
                                    duration = ed - st
                                    print('\n已经爬取了%d张图片 ! 总用时%.5f秒 !' % (piece, duration))
                                    break
                            except requests.exceptions.MissingSchema:
                                continue
                    except UnboundLocalError:
                        print('\n输入的url对象无效！')
                else:
                    real_urls = []

                    res1 = requests.get(url, headers=headers)
                    respond = res1.text

                    patter = re.compile(r'("hoverURL":)("https://.*h=\d+")')
                    title_compile = re.compile(r'("fromPageTitleEnc":)(".*")(,"bd.*").*')
                    titles = title_compile.findall(respond)
                    urls = patter.findall(respond)
                    for a_url in urls :
                        real_urls.append(a_url[1].strip('\"\"'))
                    try:
                        for really_url,title in zip(real_urls,titles):
                            if number <= piece:
                                if path != '':
                                    if os.path.exists(path):
                                        ima = requests.get(really_url)
                                        real_ima = ima.content
                                        name = os.path.join(path, f'{number}.jpg')
                                        with open(name, 'wb') as f:
                                            f.write(real_ima)
                                        print(f'已经将图片保存到以下路径：{name}')
                                        print(title[1],really_url)
                                        number += 1
                                    else:
                                        print('请输入正确的路径！！！！！')
                                        break
                                else:
                                    ima = requests.get(really_url)
                                    real_ima = ima.content
                                    image_path = os.path.join(os.getcwd(), 'image')
                                    try:
                                        os.mkdir(image_path)
                                    except FileExistsError:
                                        pass
                                    name = os.path.join(image_path, f'{number}.jpg')
                                    with open(name, 'wb') as f:
                                        f.write(real_ima)
                                    print(f'已经将图片保存到以下路径：{name}')
                                    print(title[1],really_url)
                                    number += 1

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


print(tips)
print('\n')
path = input('请选择想要保存到的路径：\n')
pages = int(input("请输入想要爬取的页数： "))
pieces = int(input('请输入想要爬取的张数： '))
url = input('请输入想要爬取的百度图片网址：\n')

baidu_scapy(pages,pieces,path,url)












