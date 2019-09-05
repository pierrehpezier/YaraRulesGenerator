#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import tkinter
import tkinter.ttk
import compile
import compileyara

WIDTH = 2048


class MainWindow(tkinter.ttk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.windowwidth = WIDTH/8 - 10
        self.windowheight = 50
        self.yaragen = compileyara.yaragen()
        self.arch = 64
        self.buttontext = tkinter.StringVar()
        self.buttontext.set(str(self.arch))
        self.initUI()

    def initUI(self):
        self.master.title('yara generator')
        self.pack(fill=tkinter.BOTH, expand=1)
        tkinter.ttk.Style().configure('TFrame', background='#333')
        self.pack(fill=tkinter.BOTH, expand=True)
        self.ARCH = tkinter.Button(self.root, textvariable=self.buttontext)
        self.ARCH.pack(side=tkinter.TOP, padx=5, pady=5)
        self.ARCH.bind('<Button-1>', self.switcharch)

        self.TEXT = tkinter.Text(self.root, height=self.windowheight, width=int(self.windowwidth / 3))
        self.TEXT.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.TEXT.bind('<Key>', self.codeModified)

        self.RESULT = tkinter.Text(self.root, height=self.windowheight, width=int(self.windowwidth / 3))
        self.RESULT.pack(side=tkinter.LEFT, padx=5, pady=5)
        
        self.YARABOX = tkinter.Text(self.root, height=self.windowheight, width=int(self.windowwidth / 3))
        self.YARABOX.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.YARABOX.bind('<Double-Button-1>', self.clipboardcopy)

    def switcharch(self, event):
        self.arch = {64:32, 32:64}[self.arch]
        self.buttontext.set(str(self.arch))
        self.codeModified(None)

    def clipboardcopy(self, event):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.YARABOX.get(1.0, tkinter.END))
        print('copied to clipboard')

    def codeModified(self, event):
        try:
            binvalue = compile.compile(self.TEXT.get(1.0, tkinter.END), self.arch)
            self.RESULT.delete(1.0, tkinter.END)
            decompiled = compile.decompile(binvalue, self.arch)
            self.RESULT.insert(tkinter.END, decompiled)
            self.YARABOX.delete(1.0, tkinter.END)
            self.YARABOX.insert(tkinter.END, self.yaragen.update(decompiled))
        except compile.Yarasm:
            pass

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry('{}x800+0+0'.format(WIDTH))
    app = MainWindow(root)
    root.mainloop()
