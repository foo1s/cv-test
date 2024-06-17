#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author zhouhuawei time:2024/6/17
import tkinter as tk
from tkinter import messagebox


def function1():
    messagebox.showinfo("Function 1", "This is Function 1")

def function2():
    messagebox.showinfo("Function 2", "This is Function 2")

def function3():
    messagebox.showinfo("Function 3", "This is Function 3")

# 创建主窗口
root = tk.Tk()
root.title("计算机视觉大作业")
root.attributes("-fullscreen", True)

# 创建并放置按钮
button1 = tk.Button(root, text="Run Function 1", command=function1)
button1.pack(pady=10)

button2 = tk.Button(root, text="Run Function 2", command=function2)
button2.pack(pady=10)

button3 = tk.Button(root, text="Run Function 3", command=function3)
button3.pack(pady=10)

# 运行主循环
root.mainloop()