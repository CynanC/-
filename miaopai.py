#!/usr/bin/python2.6  
# -*- coding: utf-8 -*-  

from Tkinter import *
from tkinter.filedialog import askdirectory
import ttk
import tkMessageBox
import os
import requests


root = Tk()
root.title("秒拍视频管理系统 v1.2")

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root.iconbitmap(resource_path('favicon.ico'))
root.resizable(0,0)

global path_
def select_path():
	global path_
	path_=askdirectory()
	path.set(path_)
	tree.delete(*tree.get_children())
	try:
		for root,dirs,files in os.walk(path_):
			for name in files:
				tree.insert("", 'end', values=(name, "未检查"))  
	except:
		tkMessageBox.showerror("警告", "目录错误或文件夹为空！",parent=root)

def start_sift():
	for node in tree.get_children():
		video_name=tree.item(node)['values'][0]
		if tree.item(node)['values'][1]!=u'未检查' and  tree.item(node)['values'][1]!=u'服务器无响应':
			continue
		video_type=check_title(video_name.encode('utf-8'))
		tree.item(node,values=(video_name,video_type))
		tree.update()
	tkMessageBox.showinfo("提示", "筛选完成！",parent=root)

def delete_items():
	global path_
	for node in tree.get_children():
		video_name=tree.item(node)['values'][0]
		if tree.item(node)['values'][1] != u'符合标准' and tree.item(node)['values'][1] != u'未检查':
			tree.delete(node)
			os.remove(path_+'/'+video_name)
	tkMessageBox.showinfo("提示", "删除完成！",parent=root)

def check_title(title):
	title=".".join(title.split('.')[:-1])
	print title
	str_len = len(title.decode('utf-8'))
	if str_len<8 or str_len>30:
		return "长度不在 8-30 之间"
	for back in [".mp4",".rmvb",".avi",".wmv",".rm",".3gp",".mov",".mkv"]:
		if back in title:
			return "包含视频后缀"
	url = 'http://creator.miaopai.com/videocheck/checkTitle'
	header={
	    "Content-Type":"application/x-www-form-urlencoded", 
	    "Cookie": "SRV_CREATOR_COOKIE_LOGIN_TOKEN=wlJBS5ItpYtTFXlSYJqfgRK0KmZHQMGc; Hm_lvt_e6af01253df49e1d8df23316e3dee264=1526101393; PHPSESSID=up97q3j1j72n315f403ldhcn90",
	    "X-Requested-With":"XMLHttpRequest"
	}
	scid="iZdihbRCENywyBrgU2rGj19Zf6oTD~RNXJCeNA__"
	data="titleinfos[0][scid]="+scid+"&titleinfos[0][title]="+title
	try:
		result=requests.post(url=url,data=data,headers=header,timeout=5)
		if result.json()['data'][0]['status'] == 1:
			return '符合标准'
		else:
			return result.json()[u'data'][0][u'msg']
	except:
		return '服务器无响应'


Label(root,text = "目标文件夹:").grid(row = 0, column = 0,padx=10,pady=10)
path=StringVar()
Entry(root, textvariable = path,state="readonly",width=40).grid(row = 0, column = 1,padx=10,pady=10)
Button(root, text = "文件夹选择", command = select_path).grid(row = 0, column = 2,padx=10,pady=10)
Button(root, text = "开始筛选", command = start_sift).grid(row = 0, column = 3,padx=10,pady=10)


_frame=Frame()
_frame.grid(row=1,column=0,columnspan=4,pady=10)

tree=ttk.Treeview(_frame, selectmode='browse') 
vsb =Scrollbar(_frame,width=500, orient="vertical",command=tree.yview)  
tree.configure(yscrollcommand=vsb.set)
vsb.grid(row=0,column=0,columnspan=4,sticky=N+S)
tree["columns"] = ("1", "2")  
tree['show'] = 'headings'
tree.column("1", width=350, anchor='w')  
tree.column("2", width=130, anchor='c')  
tree.heading("1", text="文件名")  
tree.heading("2", text="状态")  
tree.grid(row=0,column=0,columnspan=4,sticky=W+E+N+S)


Button(_frame, text = "删除重复", command = delete_items).grid(row = 2, column = 3,pady=10,sticky=E)
Label(root,text="by Arris QQ:909123127",fg="#ababab").place(x=3,y=315)

root.mainloop()