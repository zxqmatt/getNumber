try:
    import pygame
    from random import choice, shuffle
    from time import sleep
    from os import mkdir
    from os.path import exists, isfile
    from sys import argv, exit
    argc = len(argv)
    width = 600
    height = 500
    if argc==2 and argv[1][-4:]==".gtn" and isfile(argv[1]):
        with open(argv[1], "r") as f:
            s = eval(f.read())
        name = s["name"]
        var = s["var"]
        tpl = s["template"]
        try:
            shuffle(var)
            shuffle(var)
            n = choice(var)
        except IndexError:
            var = tpl.copy()
            shuffle(var)
            shuffle(var)
            n = choice(var)
        var.remove(n)
        pygame.init()
        pygame.display.set_caption(name)
        screen = pygame.display.set_mode((width, height))
        white = (255, 255, 255)
        black = (0, 0, 0)
        screen.fill(black)
        font = pygame.font.SysFont('Consolas', 288)
        textft = font.render(str(n), True, white)
        textft_rect = textft.get_rect()
        textft_rect.centerx = screen.get_rect().centerx
        textft_rect.centery = screen.get_rect().centery
        screen.blit(textft, textft_rect)
        pygame.display.update()
        sleep(3)
        pygame.quit()
        s = dict()
        s["name"] = name
        s["var"] = var
        s["template"] = tpl
        with open(argv[1], "w") as f:
            f.write(str(s))
        exit(0)
    Mfont = ("微软雅黑", 15)
    from tkinter import *
    from tkinter.messagebox import *
    screen = Tk()
    screen.title("抽号生成界面")
    screen.geometry("%dx%d+%d+%d" % (width, height, (screen.winfo_screenwidth()-width)/2, (screen.winfo_screenheight()-height)/2))
    screen.resizable(False, False)

    Label(screen, text = "请输入抽号程序名称：", font = Mfont).place(x = 25, y = 30, anchor = "nw")

    ent = Entry(screen, font = Mfont)
    ent.place(x = 231, y = 30, width = 325, anchor = "nw")

    lst = StringVar()
    lstb = Listbox(screen, listvariable = lst)
    lstb.place(x = 400, y = 100, width = 150, height = 300, anchor = "nw")
    bar = Scrollbar(screen, command = lstb.yview, activebackground = "gray", bg = "black")
    bar.place(x = 550, y = 100, height = 300, anchor = "nw")
    lstb.config(yscrollcommand = bar.set)

    Label(screen, text = "请在右表中，编辑抽号程序号码列表：", font = Mfont).place(x = 25, y = 100, anchor = "nw")

    entl = Entry(screen, font = Mfont)
    entl.place(x = 200, y = 140, width = 60, anchor = "nw")
    def binsert():
        if not entl.get().isdigit():
            entl.delete(0, "end")
            return
        lstb.insert(0, entl.get())
        glst = list(map(int, list(lstb.get(0, "end"))))
        glst = list(set(glst))
        glst = list(map(str, glst))
        lstb.delete(0, "end")
        lstb.insert("end", *glst)
        entl.delete(0, "end")
    btni = Button(screen, text = "添加 >> ", font = Mfont, command = binsert)
    btni.place(x = 280, y = 140, width = 100, height = 31, anchor = "nw")

    def bdelete():
        for i in lstb.curselection():
            lstb.delete(i)
    btnd = Button(screen, text = "删除 << ", font = Mfont, command = bdelete)
    btnd.place(x = 280, y = 175, width = 100, height = 31, anchor = "nw")
    Label(screen, text = "选中要删除的选项，然后单击“删除”按钮", font = ("微软雅黑", 10)).place(x = 270, y = 177, anchor = "ne")

    el = Entry(screen, font = Mfont)
    el.place(x = 75, y = 225, width = 75, height = 31, anchor = "nw")
    Label(screen, text = "~", font = Mfont).place(x = 150, y = 225, height = 31, anchor = "nw")
    er = Entry(screen, font = Mfont)
    er.place(x = 171, y = 225, width = 75, height = 31, anchor = "nw")
    def inlst():
        l = el.get()
        r = er.get()
        if (not l.isdigit()) or (not r.isdigit()):
            el.delete(0, "end")
            er.delete(0, "end")
            return
        if len(lst.get()) != 0 and len(eval(lst.get())) != 0 and askokcancel("重置列表", "执行此操作要重置列表。\n确定要重置列表吗？"):
            lstb.delete(0, "end")
        lstb.insert("end", *list(range(int(l), int(r)+1)))
        el.delete(0, "end")
        er.delete(0, "end")
    lrbt = Button(screen, text = "快速添加", font = Mfont, command = inlst)
    lrbt.place(x = 280, y = 225, width = 100, height = 31, anchor = "nw")

    def reset():
        if len(lst.get()) == 0 or len(eval(lst.get())) == 0:
            return
        if askokcancel("重置列表", "确定要重置列表吗？"):
            lstb.delete(0, "end")
    rbtn = Button(screen, text = "重置", font = Mfont, command = reset)
    rbtn.place(x = 280, y = 275, width = 100, height = 31, anchor = "nw")

    from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER
    from tkinter.filedialog import *
    desk = QueryValueEx(OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"), "Desktop")[0]
    def saveFile():
        name = ent.get()
        var = list(eval(lst.get()))
        sp = asksaveasfilename(title = "选择保存路径", initialdir = desk, initialfile = ("%s.gtn" % name), filetypes = [("GTN 抽号程序信息文件", "*.gtn")])
        with open(sp, "w") as f:
            string = dict()
            string["name"] = name
            string["template"] = var
            string["var"] = []
            f.write(str(string))
        if askyesno("生成成功", "生成成功！\n是否要关闭程序？"):
            exit(0)
    sbtn = Button(screen, text = "保存", font = Mfont, command = saveFile)
    screen.update()
    sbtn.place(x = screen.winfo_width()/2, y = 450, width = 100, anchor = "center")

    screen.mainloop()
except:
    exit(0)