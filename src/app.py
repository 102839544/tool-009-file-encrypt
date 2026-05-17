#!/usr/bin/env python3
"""
文件加密解密工具 - AES加密保护文件
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("文件加密解密工具 v1.0")
        root.geometry("600x500")
        self.files = []
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#4527a0", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🔐 文件加密解密工具", font=("Arial",14,"bold"),
                 fg="white", bg="#4527a0").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="添加文件", command=self.add_files,
                  bg="#4527a0", fg="white", padx=12).pack(side="left", padx=5)
        tk.Button(bf, text="清空", command=self.clear,
                  padx=12).pack(side="left", padx=5)
        
        self.lb = tk.Listbox(main, font=("Consolas",10), bg="#ede7f6", height=10)
        self.lb.pack(fill="both", expand=True, pady=10)
        
        # 密码
        pf = tk.Frame(main)
        pf.pack(fill="x", pady=10)
        tk.Label(pf, text="密码：").pack(side="left")
        self.pwd_entry = tk.Entry(pf, show="*", width=30)
        self.pwd_entry.pack(side="left", padx=10)
        
        # 按钮
        opf = tk.Frame(main)
        opf.pack(fill="x", pady=10)
        tk.Button(opf, text="🔒 加密文件", command=self.encrypt,
                  bg="#4527a0", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(side="left", padx=10)
        tk.Button(opf, text="🔓 解密文件", command=self.decrypt,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(side="left", padx=10)
        
        self.status = tk.Label(main, text="设置密码后加密或解密文件",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def add_files(self):
        fs = filedialog.askopenfilenames(title="选择文件")
        for f in fs:
            if f not in self.files:
                self.files.append(f)
                self.lb.insert("end", Path(f).name)
        self.status.config(text=f"已添加 {len(self.files)} 个文件")
    
    def clear(self):
        self.files.clear()
        self.lb.delete(0, "end")
    
    def get_key(self, password):
        """从密码生成加密密钥"""
        import hashlib
        import base64
        h = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(h)
    
    def encrypt(self):
        if not self.files:
            messagebox.showwarning("提示", "请先添加文件")
            return
        if not HAS_CRYPTO:
            messagebox.showerror("缺少依赖", "请运行：pip install cryptography")
            return
        
        pwd = self.pwd_entry.get()
        if not pwd:
            messagebox.showwarning("提示", "请输入密码")
            return
        
        try:
            key = self.get_key(pwd)
            fernet = Fernet(key)
            
            ok = 0
            for file_path in self.files:
                with open(file_path, "rb") as f:
                    data = f.read()
                
                encrypted = fernet.encrypt(data)
                
                out_path = str(file_path) + ".encrypted"
                with open(out_path, "wb") as f:
                    f.write(encrypted)
                
                ok += 1
            
            messagebox.showinfo("完成", f"成功加密 {ok} 个文件\n加密文件后缀：.encrypted")
            self.status.config(text=f"✅ 已加密 {ok} 个文件")
        except Exception as e:
            messagebox.showerror("错误", str(e))
    
    def decrypt(self):
        if not self.files:
            messagebox.showwarning("提示", "请先添加加密文件")
            return
        if not HAS_CRYPTO:
            messagebox.showerror("缺少依赖", "请运行：pip install cryptography")
            return
        
        pwd = self.pwd_entry.get()
        if not pwd:
            messagebox.showwarning("提示", "请输入密码")
            return
        
        try:
            key = self.get_key(pwd)
            fernet = Fernet(key)
            
            ok = 0
            for file_path in self.files:
                with open(file_path, "rb") as f:
                    encrypted = f.read()
                
                data = fernet.decrypt(encrypted)
                
                out_path = str(file_path).replace(".encrypted", "")
                with open(out_path, "wb") as f:
                    f.write(data)
                
                ok += 1
            
            messagebox.showinfo("完成", f"成功解密 {ok} 个文件")
            self.status.config(text=f"✅ 已解密 {ok} 个文件")
        except Exception as e:
            messagebox.showerror("错误", f"解密失败（密码错误或文件损坏）：{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
