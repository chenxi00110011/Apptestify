import tkinter as tk
from tkinter import ttk, simpledialog


class CustomInputDialog(simpledialog.Dialog):
    def body(self, master):
        # 创建标签和输入框
        tk.Label(master, text="上电时间最小值:").grid(row=0, sticky=tk.W)
        tk.Label(master, text="上电时间最大值:").grid(row=1, sticky=tk.W)
        tk.Label(master, text="断电时间最小值:").grid(row=2, sticky=tk.W)
        tk.Label(master, text="断电时间最大值:").grid(row=3, sticky=tk.W)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)
        self.e4 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)

        # 创建第一个下拉菜单
        tk.Label(master, text="上电时间单位:").grid(row=4, sticky=tk.W)
        self.option_var1 = tk.StringVar()
        self.option_menu1 = ttk.Combobox(master, textvariable=self.option_var1)
        self.option_menu1['values'] = ('秒', '分钟', '小时')
        self.option_menu1.grid(row=4, column=1)
        self.option_menu1.current(0)  # 设置默认选项

        # 创建第二个下拉菜单
        tk.Label(master, text="断电时间单位:").grid(row=5, sticky=tk.W)
        self.option_var2 = tk.StringVar()
        self.option_menu2 = ttk.Combobox(master, textvariable=self.option_var2)
        self.option_menu2['values'] = ('秒', '分钟', '小时')
        self.option_menu2.grid(row=5, column=1)
        self.option_menu2.current(0)  # 设置默认选项

        return self.e1  # 初始焦点在第一个输入框

    def apply(self):
        try:
            num1 = int(self.e1.get())
            num2 = int(self.e2.get())
            str1 = self.e3.get()
            str2 = self.e4.get()
            selected_option1 = self.option_var1.get()
            selected_option2 = self.option_var2.get()

            self.result = (num1, num2, str1, str2, selected_option1, selected_option2)
        except ValueError:
            tk.messagebox.showerror("输入错误", "请输入有效的整数")
            self.result = None


# 使用自定义对话框
def get_user_input():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    dialog = CustomInputDialog(root, title="输入多个字段并选择选项")
    return dialog.result


if __name__ == "__main__":
    print(get_user_input())
