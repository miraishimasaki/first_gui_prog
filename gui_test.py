from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk

def get_image(filename,width,height):
    im = Image.open(filename).resize((width,height))
    return ImageTk.PhotoImage(im)

root = Tk()
root.title('bg')
root.geometry('800x600+300+500')
root.resizable(False,False)

canvas_root = Canvas(root,width=800,height=600)
im_root = get_image('.\steps\微信图片_20240608224700.png',800,600)
canvas_root.create_image(400,300,image=im_root)
canvas_root.pack()

lb_label = Label(root,text='我是个标签')

lb_label.place(x=50,y=50,width=100,height=50)

root.mainloop()