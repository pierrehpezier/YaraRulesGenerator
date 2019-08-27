#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import tkinter
import tkinter.ttk
import compile
import compileyara


class MainWindow(tkinter.ttk.Frame):
    def __init__(self):
        super().__init__()
        self.windowwidth = 50
        self.windowheight = 40
        self.yaragen = compileyara.yaragen()
        self.initUI()

    def initUI(self):
        self.master.title('yara generator')
        self.pack(fill=tkinter.BOTH, expand=1)
        tkinter.ttk.Style().configure('TFrame', background='#333')
        self.pack(fill=tkinter.BOTH, expand=True)
        self.TEXT = tkinter.Text(root, height=self.windowheight, width=self.windowwidth)
        self.RESULT = tkinter.Text(root, height=self.windowheight, width=self.windowwidth)
        self.TEXT.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.RESULT.pack(side=tkinter.LEFT, padx=5, pady=5)
        self.TEXT.bind('<Key>', self.codeModified)
        self.YARABOX = tkinter.Text(root, height=self.windowheight, width=self.windowwidth + 10)
        self.YARABOX.pack(side=tkinter.LEFT, padx=5, pady=5)

        #self.TEXT.bind('<Double-Button-1>', )

    #@staticmethod
    #def clipboardcopy():
        

    def codeModified(self, event):
        try:
            binvalue = compile.compile(self.TEXT.get(1.0, tkinter.END))
            self.RESULT.delete(1.0, tkinter.END)
            decompiled = compile.decompile(binvalue)
            self.RESULT.insert(tkinter.END, decompiled)
            self.YARABOX.delete(1.0, tkinter.END)
            self.YARABOX.insert(tkinter.END, self.yaragen.update(decompiled))
        except compile.Yarasm:
            pass

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry('1200x600+300+300')
    app = MainWindow()
    root.mainloop()
