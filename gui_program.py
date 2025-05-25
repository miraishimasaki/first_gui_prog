from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from tkinter.ttk import Progressbar
from tkinter.filedialog import askdirectory
import os
from re import compile
import requests
from time import time
from time import sleep
from _tkinter import TclError
from threading import Thread
import pyperclip

tips =''' 
# 使用须知：
# 每次爬取要注意的有以下几点：
# 1）保存文件的路径
# 2) 保证你选取的页数可以满足你要爬取的数量.
# 3) 该脚本只能爬取部分百度图片，请检查所要爬取页面的源代码的network\\fetch\\xhr页面。若该页面的preview的data项目旁边有个小三角形，则可以爬取该页面
# 4) 如果输入的路径为空，该程序将会自动在工作目录下创建一个image文件夹用以存储数据
# 5) 如果报错信息中出现：\'请检查输入的url格式是否正确！\' 则说明您输入的url无效
# 6）如果报错信息中出现:\'请检查输入的url是否为能爬取的网页对象的url\'  则说明该网页属于暂时无法爬取的那一类百度图片
# 7) 系统初设的爬取页数为2,爬取张数为1.用户可以根据需要自行更改.'''

headers = {'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Host':
                'image.baidu.com',
'Referer':
'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDEsMiw2LDQsNSw3LDgsOQ%3D%3D&word=%E8%B5%9B%E6%96%87'
           }


class Timer:
    def __init__(self):
        self.st = None
        self.ed =  None

    def start(self):
        st = time()
        self.st = st

    def end(self):
        ed = time()
        self.ed = ed


def data_clear():
    global saveas,url_var,piece_var,page_var
    saveas.set(value='')
    url_var.set(value='')
    try:
        page_var.set(value="")
        piece_var.set(value="")
    except TclError:
        pass


#开多一个线程解决实时响应问题
def run_long_func(*args):
    t = Thread(target=baidu_scapy)
    t.start()
    show_progress()


def baidu_scapy():
    global url,page,path,piece,number,timer
    pop = True
    situation1 = True
    if url == '':
        pop = False
    replace = compile('pn=\d+')
    if page > 1:
        timer.start()
        for page in range(1, page):
            if number <= piece:
                pn = (page*30)
                pag = f'pn={pn}'
                sub_url = replace.sub(pag,url)
                ##################################################检查url是否输入正确
                try:
                    res = requests.get(sub_url,headers = headers)
                    json_res = res.json()
                    json_data = json_res['data']
                except requests.exceptions.JSONDecodeError:
                    situation1 = False
                except requests.exceptions.MissingSchema:
                    #pass
                    url_errormessage()
                    print('\n请检查输入的url格式是否正确！')
                    pop = False
                    #return
                ###################################################检查url是否输入正确
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
                                            save_dir_path = os.path.join(path,'image')
                                            os.makedirs(save_dir_path,exist_ok=True)
                                            name = os.path.join(save_dir_path,f'{number}.jpg')
                                            with open(name,'wb') as f:
                                                f.write(real_ima)
                                            print(f'已经将图片保存到以下路径：{name}')
                                            print(hover_name, ima_url)
                                            number += 1
                                        else:
                                            path_error()
                                            pop = False
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
                                    timer.end()
                                    #duration = ed - st
                                    #print('\n已经爬取了%d张图片 ! 总用时%.5f秒 !' % (piece, duration))
                                    break
                            except requests.exceptions.MissingSchema:
                                continue
                    #########################################这个东西是由json引起的，第二种情况不用json，就不用预判这个错误
                    except UnboundLocalError:
                        #pass
                        url_errormessage()
                        print('\n输入的url对象无效！')

                        pop = False
                    #########################################这个东西是由json引起的，第二种情况不用json，就不用预判这个错误
                else:
                    real_urls = []

                    res1 = requests.get(url, headers=headers)
                    respond = res1.text

                    patter = compile(r'("hoverURL":)("https://.*h=\d+")')
                    title_compile = compile(r'("fromPageTitleEnc":)(".*")(,"bd.*").*')
                    titles = title_compile.findall(respond)
                    urls = patter.findall(respond)
                    for a_url in urls:
                        real_urls.append(a_url[1].strip('\"\"'))
                    try:
                        for really_url, title in zip(real_urls, titles):
                            if number <= piece:
                                if path != '':
                                    if os.path.exists(path):
                                        ima = requests.get(really_url)
                                        real_ima = ima.content
                                        name = os.path.join(path, f'{number}.jpg')
                                        with open(name, 'wb') as f:
                                            f.write(real_ima)
                                        print(f'已经将图片保存到以下路径：{name}')
                                        print(title[1], really_url)
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
                                    print(title[1], really_url)
                                    number += 1

                            else:
                                timer.end()
                                #duration = ed - st
                                #print('\n已经爬取了%d张图片 ! 总用时%.5f秒 !' % (piece, duration))
                                break
                    except requests.exceptions.MissingSchema:
                        continue
                    #return
            #这个地方出了问题:break语句
            # else:
            #     break
    else:
        pages_error()
        pop = False
    number=1#还原修改为下一次爬取打基础
    data_clear()#优化clear函数
    if pop:
        pop_congratulations()
    else:
        pop_finish()

def creat_button(root):
    exit_button = Button(root,text="Exit",bg='LightSlateGrey',command=root.destroy)
    scapy_btn = Button(root,text='Do it',bg='LightSteelBlue',command=run_long_func)
    pg_btn = Button(root,text='Show progress',bg='Lightyellow',command=show_progress)
    scapy_btn.place(x=810,y=620,width=40,height=30)
    exit_button.place(x=770,y=620,width=40,height=30)
    pg_btn.place(x=670,y=620,width=100,height=30)

def show_progress():
    global number,piece
    tl = Toplevel(root)
    tl.title('Progress Bar')
    tl.geometry('250x80+600+350')
    pb = Progressbar(tl, name='pgb', maximum=piece,length=150)
    def update_pgb():
        while number<piece:
            text.config(text=f'已爬取{number}/{piece}')
            pb['value'] = number
            sleep(0.05)
            tl.update()
        if number >= piece :
            tl.destroy()

    #bt = Button(tl, text='显示进度', command=update_pgb)

    text = Label(tl,text=f'已爬取{number}/{piece}')
    text.pack()
    pb.pack()
    #bt.pack(pady = 5)
    update_pgb()   #这一句是一个循环，一直在进行，除非达到停止条件





# def gui_test():                 #证明了不是break的问题
#     for i in range(100):
#         if i < 5:
#             print(i)
#         else:
#             return



def url_errormessage2():
    tryornot = messagebox.showwarning(title='Error', message="输入的url不是能够爬取的一类百度图片url\n此次爬取中可能出现了坏图")
def creat_root():
    root = Tk()
    root.title('shiba_gui_scapy')
    root.geometry('850x650+300+100')
    root.config(bg='Papayawhip')
    return root
def url_errormessage():
    global url_var
    tryornot = messagebox.showwarning(title='Error',message="输入的url有误，是否要重新输入")
    #url_var.set(value='')


def path_error():
    global saveas
    path_try = messagebox.askretrycancel(title='Error',message='请输入正确的保存路径！！！！！')
    saveas.set(value='')

def pop_finish():
    messagebox.showwarning(message='任务结束!\n本次爬取中可能出现了坏图，或者输入的信息有误!',title='Finish')

def pages_error():
    global page_var
    pages_try = messagebox.askretrycancel(title="Error",message='输入的页数应大于等于2')
    try:
        page_var.set(value=2)
    except TclError:
        pass

def pop_direction():
    tl = Toplevel()
    L_F=LabelFrame(tl,text="使用注意事项",bg="pink")
    Label(L_F,text=tips,anchor=W,bg='lightyellow',justify='left').pack()
    Label(L_F,text='PS:当要爬取的页数一定能够满足爬取张数时,页数是多少对最终结果没有影响!',bg='lightyellow',justify='center',
          font=('Arial',12,"bold")).pack(pady = 10)

    L_F.grid(row=0,column=1)
    tl.resizable(False,False)
    return 'direction'

def resize_photos(path,size=(400,200)):
    original_image = Image.open(path)
    resize_image = original_image.resize(size)
    #resize_image.show()
    return ImageTk.PhotoImage(resize_image)
#resize_photos(r'D:\python_work\useful_tool\Python_scapy\baidu_scapy\steps\微信图片_20240608224649.png')
def pop_graphic():
    tl = Toplevel()
    p1 = resize_photos('.\steps\微信图片_20240608224649.png')
    p2 = resize_photos('.\steps\微信图片_20240608224700.png')
    p3 = resize_photos('.\steps\微信图片_20240608224714.png')
    p4 = resize_photos('.\steps\微信图片_20240608224707.png')
    step1 = Label(tl,text='1)打开要爬取的网址，单击鼠标右键，找到’检查选项‘',wraplength=150,padx=20,
                  pady=10,image=p1,compound='top')
    step1.image = p1

    step2 = Label(tl,text='2)打开后找到’网络‘这一栏',wraplength=120,padx=20,
                  pady=10,image=p2,compound='top')
    step2.image = p2

    step3 = Label(tl,text='3)在‘网络’这一栏中选中Fetch/XHR',wraplength=120,padx=20,
                  pady=10,image=p3,compound='top')
    step3.image = p3

    step4 = Label(tl,text='4)上下滑动网页，直至Fetch/XHR栏中出现以“ajson”开头的选项，在这个选项中复制请求URL。CTRL+V可以粘贴',
                  wraplength=350,padx=20,pady=10,image=p4,compound="top")
    step4.image = p4
    step1.grid(row=0,column=0)
    step2.grid(row=0,column=1)
    step3.grid(row=1,column=0)
    step4.grid(row=1,column=1)
    tl.resizable(False,False)
def thank_gif():
    tl = Toplevel()
    p = resize_photos(".\steps\R-C.jpg",size=(450,400))
    label = Label(tl,
                  text='感谢使用。\nThanks for using.\nご 利用 ありがとうございます。\n이용해주셔서 감사합니다。\nСпасибо.\nMerci d’utiliser.',
                  image=p,compound='top',bg='pink')
    label.image = p
    label.pack()
    tl.resizable(False,False)

def creat_menu(root):
    menubar = Menu(root)
    helpmenu = Menu(menubar, fg='black', bd=2, tearoff=False)
    Moremenu = Menu(menubar, tearoff=False)
    menubar.add_cascade(label='Help', menu=helpmenu)
    menubar.add_cascade(label='More', menu=Moremenu)
    # 只能传入函数名，若是传入函数调用，则打开窗口就会调用函数
    helpmenu.add_command(label='Direction', command=pop_direction)
    helpmenu.add_command(label='图示教程', command=pop_graphic)
    Moremenu.add_command(label='致谢', command=thank_gif)
    # 这一步比较关键，要把创建的菜单放在主窗口里面
    root.config(menu=menubar)


def creat_logo(root):
    lf = LabelFrame(root,text='introduction',bg='LightSkyBlue')
    p = resize_photos(".\steps\螢幕擷取畫面 2024-06-09 000437.png",(450,200))
    label = Label(lf,image=p,text='欢迎使用，本程序可以自定义爬取一定数量的百度图片',compound='top',wraplength=150,bg='LightSkyBlue')
    label.image = p
    label.pack()
    lf.place(x=0,y=400,width=450,height=250)
    #850x650

def save_path():
    global saveas
    path = askdirectory()
    saveas.set(path)



def callback1(*args):
    global page
    try:
        page = page_var.get()
    except TclError:
        pass

def callback2(*args):
    global piece
    try:
        piece = piece_var.get()
    except TclError:
        pass

def url_callback(*args):
    global url
    url = url_var.get()

def path_callback(*args):
    global path
    path = saveas.get()

def pop_congratulations():
    global piece,timer
    messagebox.showinfo(title='Congratulations',message=f'爬取完成!\n成功爬取了{piece}张图片！共用时{timer.ed-timer.st}秒!\n')


def detect():
    global piece,url,page,path
    print(piece,page,path,url)

def paint_bg(root):
    canvas = Canvas(root,width=850,height=650)
    canvas.pack()
    bg_image = resize_photos('.\steps\微信图片_20240609202940.jpg',(850,650))
    bg_image.image = bg_image
    canvas.create_image(0,0,anchor = NW,image=bg_image)

def paste_url():
    global url_var,url
    url_var.set(value=pyperclip.paste())
    url = url_var.get()

def paste_page():
    global page,page_var
    page_var.set(value=pyperclip.paste())
    try:
        page = page_var.get()
    except TclError:
        pass

def paste_piece():
    global piece, piece_var
    piece_var.set(value=pyperclip.paste())
    try:
        piece = page_var.get()
    except TclError:
        pass
def paste_path():
    global path,saveas
    saveas.set(value=pyperclip.paste())
    path = saveas.get()

def show_popmenu(event):
    global popmenu,root_pos,root_poss
    popmenu.post(event.x_root,event.y_root)


#20像素Entry,第一个框width450,height120;第二个框width450,height70,起点y250,显示区height起点多50像素

if __name__ == '__main__':
    timer = Timer()
    number = 1
    root = creat_root()
    root.resizable(False,False)
    root_pos = (root.winfo_rootx(),root.winfo_rooty())
    root_poss = (root.winfo_x(), root.winfo_y())

    #创建背景

#若是创建背景通过函数进行，则进行完一次爬虫后背景会消失，怀疑和垃圾回收机制相关。
    canvas = Canvas(root, width=850, height=650)
    canvas.pack()
    bg_image = resize_photos('.\steps\微信图片_20240609202940.jpg', (850, 650))
    bg_image.image = bg_image
    canvas.create_image(0, 0, anchor=NW, image=bg_image)

    saveas = StringVar(value='') #创建一个全局变量供两个函数共同使用
    url_var = StringVar(value='输入url')
    page_var = IntVar(value=2)
    piece_var = IntVar(value=1)
    creat_menu(root)
    creat_button(root)

    creat_logo(root)

#粘贴菜单的设计
    popmenu = Menu(root, tearoff=0)
    paste = Menu(popmenu,tearoff=False)
    popmenu.add_cascade(label='粘贴',menu=paste)
    paste.add_command(label='粘贴url',command=paste_url)
    paste.add_command(label='粘贴文件路径',command=paste_path)
    paste.add_command(label='粘贴页数',command=paste_page)
    paste.add_command(label='粘贴张数',command=paste_piece)
    root.bind('<Button-3>',show_popmenu)

#创建Entry
    lf = LabelFrame(root, text='数据收集：',bg='lightyellow', )
    lab1 = Label(lf, text='要爬取的URL：', bg='lightyellow')
    E1 = Entry(lf, width=50,textvariable=url_var)
    E1.bind('<Return>',run_long_func)


    lab1.grid(row=0, column=0)
    E1.grid(row=0, column=1)
    lab2 = Label(lf, text="页数：", bg='lightyellow')
    E2 = Entry(lf, width=50,textvariable=page_var)
    E2.bind('<Return>', run_long_func)

    lab2.grid(row=1, column=0)
    E2.grid(row=1, column=1)
    lab3 = Label(lf, text='张数：', bg='lightyellow')
    E3 = Entry(lf, width=50,textvariable=piece_var)
    E3.bind('<Return>', run_long_func)

    lab3.grid(row=2, column=0)
    E3.grid(row=2, column=1)
    lf.place(x=0,y=0,width=450,height=120)
#创建文件路径Entry
    lf2 = LabelFrame(root, text='选择文件路径', bg='pink')
    entry = Entry(lf2, textvariable=saveas, width=64)
    entry.bind('<Return>', run_long_func)
    loadbtn = Button(lf2, text='浏览', command=save_path)
    entry.grid(row=0)
    loadbtn.grid(row=1)
    lf2.place(x=0,y=250,width=450,height = 70)


    url = url_var.get()
    page = page_var.get()
    piece = piece_var.get()
    path = saveas.get()

    #处理entry为空时产生的报错，需要在callback函数中except，对其调用进行except不会组织报错
    #弄清楚command传递的本质
    url_var.trace('w',url_callback)
    page_var.trace('w',callback1)
    piece_var.trace('w',callback2)
    saveas.trace('w',path_callback)

    root.mainloop()