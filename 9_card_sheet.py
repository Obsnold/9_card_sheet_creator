#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from turtle import width
from PIL import Image, ImageTk
import os
from functools import partial
from tkinterdnd2 import DND_FILES, TkinterDnD

class Card(object):
    def __init__(self,Frame):
        self.frame = ttk.LabelFrame(Frame,padding="3 3 3 3",width=110,height=220)
        self.frame.grid_propagate(0)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.drop_target_register(DND_FILES)
        self.frame.dnd_bind('<<Drop>>',self.dnd)
        self.title = ttk.Label(self.frame, text = "",width=13)
        self.img = ttk.Label(self.frame, text = "")
        self.button = ttk.Button(self.frame, text="Browse",command = self.load_image)

        self.title.grid(column=0,row=0,sticky=(N))
        self.img.grid(column=0, row=1)
        self.button.grid(column=0,row=2,sticky=(S))

    def load_image(self):
        filename = filedialog.askopenfilename(initialdir =  "./", title = "Select A File", filetypes = (("jpeg files","*.jpg"),("all files","*.*")) )
        if filename:
            self.filename = filename
            self.card_image = ImageTk.PhotoImage(Image.open(self.filename).resize((100, 140),Image.ANTIALIAS))
            self.img.config(image = self.card_image,anchor=CENTER)
            self.title.config(text=os.path.basename(self.filename),anchor=CENTER)

    def dnd(self,e):
        if e:
            self.filename = e.data
            self.card_image = ImageTk.PhotoImage(Image.open(self.filename).resize((100, 140),Image.ANTIALIAS))
            self.img.config(image = self.card_image,anchor=CENTER)
            self.title.config(text=os.path.basename(self.filename),anchor=CENTER)

    def position(self,col, row):
        self.frame.grid(column=col,row=row)



def export(front_cards,back_cards):
    pdf_path = "./out.pdf"
    #dimension sizes in pixels at 300 dpi
    page_x = 2480
    page_y = 3508
    card_x = 750
    card_y = 1050

    x_offset = int((page_x -(card_x*3))/2)
    y_offset = int((page_y - (card_y*3))/2)
    #do front image
    front_img = Image.new('RGB', (page_x, page_y), (255, 255, 255)) 

    for y in range(3):
        for x in range(3):
            try:
                image = Image.open(front_cards[(y*3)+x].filename).resize((card_x, card_y),Image.ANTIALIAS)
                front_img.paste(image,(x_offset+(card_x*x),y_offset+(card_y*y)))
            except:
                print(" no image for front " + str((y*3)+x))
                continue

    #do back image
    back_img = Image.new('RGB', (page_x, page_y), (255, 255, 255)) 
    for y in range(3):
        for x in range(3):
            try:
                image = Image.open(back_cards[(y*3)+x].filename).resize((card_x, card_y),Image.ANTIALIAS)
                if x == 1:
                    back_img.paste(image,(x_offset+(card_x*x), y_offset+(card_y*y)))
                elif x == 0:
                    back_img.paste(image,(x_offset+(card_x*2), y_offset+(card_y*y)))
                elif x == 2:
                    back_img.paste(image,(x_offset+(card_x*0), y_offset+(card_y*y)))
            except:
                print(" no image for back " + str((y*3)+x))
                continue

    
    # save as pdf
    image_list = [back_img]

    front_img.save("./out.pdf", save_all=True, append_images=image_list)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    mainframe = ttk.Frame(root, padding="3 3 3 3")
    mainframe.grid(column=0,row=0,sticky=(N,W,E,S))

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0,weight=1)
    mainframe.grid_columnconfigure(0, weight=1)
    mainframe.grid_rowconfigure(0,weight=1)

    # setup front cards
    frontframe = ttk.Frame(mainframe, padding="3 3 3 3")
    front_cards=[0]*9
    front_cards[0] = Card(frontframe)
    front_cards[0].position(0,0)
    front_cards[1] = Card(frontframe)
    front_cards[1].position(1,0)
    front_cards[2] = Card(frontframe)
    front_cards[2].position(2,0)
    front_cards[3] = Card(frontframe)
    front_cards[3].position(0,1)
    front_cards[4] = Card(frontframe)
    front_cards[4].position(1,1)
    front_cards[5] = Card(frontframe)
    front_cards[5].position(2,1)
    front_cards[6] = Card(frontframe)
    front_cards[6].position(0,2)
    front_cards[7] = Card(frontframe)
    front_cards[7].position(1,2)
    front_cards[8] = Card(frontframe)
    front_cards[8].position(2,2)

    frontframe.grid(column=0,row=0, sticky=W)

    ttk.Label(mainframe, text = "FRONT").grid(column=0,row=1)

    #setup back cards
    backframe = ttk.Frame(mainframe, padding="3 3 3 3")
    back_cards=[0]*9
    back_cards[0] = Card(backframe)
    back_cards[0].position(0,0)
    back_cards[1] = Card(backframe)
    back_cards[1].position(1,0)
    back_cards[2] = Card(backframe)
    back_cards[2].position(2,0)
    back_cards[3] = Card(backframe)
    back_cards[3].position(0,1)
    back_cards[4] = Card(backframe)
    back_cards[4].position(1,1)
    back_cards[5] = Card(backframe)
    back_cards[5].position(2,1)
    back_cards[6] = Card(backframe)
    back_cards[6].position(0,2)
    back_cards[7] = Card(backframe)
    back_cards[7].position(1,2)
    back_cards[8] = Card(backframe)
    back_cards[8].position(2,2)

    backframe.grid(column=3,row=0, sticky=E)

    ttk.Label(mainframe, text = "BACK").grid(column=3,row=1)

    #setup other controls
    ttk.Button(mainframe, text="Export",command=partial(export,front_cards,back_cards)).grid(column=1,row=0)

    root.wm_title("9 Card Sheet Creator")
    #root.geometry("700x700")
    root.mainloop()



