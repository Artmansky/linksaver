import requests
from bs4 import BeautifulSoup
import csv
from tkinter import *
import subprocess

class site:
    title = ''
    link = ''

    def __init__(self, *args):
        if len(args) > 1:
            self.link = args[0]
            self.title = args[1]
            return

        if isinstance(args[0],str):
            response = requests.get(args[0])
            soup = BeautifulSoup(response.text, 'html.parser')
            self.title = soup.title.text
            self.link = args[0]
            return
        
    def __del__(self):
        pass
    
    def __repr__(self):
        return 'Title: ' + str(self.title) + ' Link: ' + str(self.link)  

    def title(self):
        return self.title
    
    def link(self):
        return self.link


def saveFile(members: list):
    if members:
        with open('saved.csv','w',encoding="utf-8") as file:
            write = csv.writer(file)
            for x in members:
                data = [x.title,x.link]
                write.writerow(data)
    else:
        file = open('saved.csv','w+',encoding="utf-8")
        file.close()       


def openFile(members: list):
    try:
        with open('saved.csv','r') as file:
            read = csv.reader(file)
            for x in read:
                if x:
                    temp = site(x[1],x[0])
                    members.append(temp)
    except: pass


def copyToClip(element: str, tab: list):
    for index, x in enumerate(tab):
        if x.title == element:
            break;
    data ='echo ' + tab[index].link + '|clip'
    return subprocess.check_call(data,shell=True)


def addNew(listBox: Listbox, tab: list, ent: str):
    if ent:
        tab.append(site(ent))
        listBox.delete(0,END)
        for x in tab:
            listBox.insert(END,x.title)
    else: pass


def getElement(listBox: Listbox, tab: list):
    try:
        selection = listBox.curselection()
        selected = listBox.get(selection[0])
        copyToClip(selected,tab)
    except: pass


def deleteElement(listBox: Listbox, tab: list):
    try:
        selection = listBox.curselection()
        del tab[selection[0]]
        listBox.delete(0,END)
        for x in tab:
            listBox.insert(END,x.title)
    except: pass


def main(tab: list):
    window = Tk()
    window.title("Save links here!")
    window.geometry("600x400+660+340")
    linkList = Listbox(window,width=100,height=15,selectmode=SINGLE)
    linkList.delete(0,END)
    for x in tab:
        linkList.insert(END,x.title)
    scroll = Scrollbar(window,command=linkList.yview)
    linkList.config(yscrollcommand=scroll.set)
    ent = Entry(window,width=55)
    btnAdd = Button(window,text='Add link',width=20,command=lambda:{addNew(linkList,tab,ent.get()),ent.delete(0,'end'),ent.delete(0,"end")})
    btnCopy = Button(window,text='Copy link',width=41,command=lambda:{getElement(linkList,tab)})
    btnDelete = Button(window,text='Delete link',width=41,command=lambda:{deleteElement(linkList,tab)})
    scroll.pack(side=RIGHT,ipady=95)
    window.resizable(False,False)
    ent.pack(pady=15)
    btnAdd.pack()
    linkList.pack(pady=5)
    btnCopy.place(y=330,x=2)
    btnDelete.place(y=330,x=302)
    window.mainloop()


if __name__ == "__main__":
   links = list()
   openFile(links)
   main(links)
   saveFile(links) 