import os
import time
import subprocess
import concurrent.futures
from tkinter import *
from tkinter import filedialog
from pathlib import Path

def convert_epub_to_mobi(epub_path, mobi_path):
    """
    使用Calibre的ebook-convert工具将EPUB文件转换为MOBI文件。

    :param epub_path: EPUB文件的路径
    :param mobi_path: MOBI文件的输出路径
    """
    # 检查输入文件是否存在
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"文件 {epub_path} 不存在")

    # 构建命令
    command = ['ebook-convert', epub_path, mobi_path]
    print(f"Running command: {' '.join(command)}")

    # 执行命令
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{epub_path} 转换成功！")
        print(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"{epub_path} 转换失败！")
        print(e.stderr.decode('utf-8'))

def find_epub_files(directory):
    """
    递归查找指定目录及其子目录下的所有EPUB文件。

    :param directory: 要搜索的目录
    :return: EPUB文件列表
    """
    return list(Path(directory).rglob('*.epub'))

def select_folder(title):
    """
    弹出文件夹选择对话框。

    :param title: 对话框标题
    :return: 选定的文件夹路径
    """
    folder = filedialog.askdirectory(title=title)
    return folder

def start_conversion():
    """
    开始转换过程。
    """
    epub_folder = entry_epub_folder.get()
    mobi_folder = entry_mobi_folder.get()
    max_workers_str = entry_threads.get().strip()

    if not max_workers_str:
        max_workers = 4  # 默认线程数为4
    else:
        try:
            max_workers = int(max_workers_str)
        except ValueError:
            status_label.config(text="请输入有效的线程数！")
            return

    if not epub_folder or not mobi_folder:
        status_label.config(text="请输入所有必要信息！")
        return

    # 记录开始时间
    start_time = time.time()

    # 创建输出文件夹（如果不存在）
    Path(mobi_folder).mkdir(parents=True, exist_ok=True)

    # 获取所有EPUB文件
    epub_files = find_epub_files(epub_folder)

    # 使用ThreadPoolExecutor进行多线程转换
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for epub_file in epub_files:
            relative_path = epub_file.relative_to(epub_folder)
            mobi_file = Path(mobi_folder) / relative_path.with_suffix('.mobi')
            mobi_file.parent.mkdir(parents=True, exist_ok=True)
            futures.append(executor.submit(convert_epub_to_mobi, str(epub_file), str(mobi_file)))

        # 等待所有任务完成
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"处理文件时发生错误: {e}")

    # 记录结束时间
    end_time = time.time()
    elapsed_time = end_time - start_time
    status_label.config(text=f"转换完成！总耗时: {elapsed_time:.2f} 秒")

# 创建主窗口
root = Tk()
root.title("EPUB to MOBI Converter")

# 创建和放置标签
Label(root, text="EPUB文件夹:").grid(row=0, column=0, padx=10, pady=5)
Label(root, text="MOBI文件夹:").grid(row=1, column=0, padx=10, pady=5)
Label(root, text="线程数:").grid(row=2, column=0, padx=10, pady=5)

# 创建和放置输入框
entry_epub_folder = Entry(root, width=50)
entry_epub_folder.grid(row=0, column=1, padx=10, pady=5)

entry_mobi_folder = Entry(root, width=50)
entry_mobi_folder.grid(row=1, column=1, padx=10, pady=5)

entry_threads = Entry(root, width=50)
entry_threads.grid(row=2, column=1, padx=10, pady=5)

# 创建和放置按钮
Button(root, text="选择EPUB文件夹", command=lambda: entry_epub_folder.insert(0, select_folder("选择EPUB文件夹"))).grid(row=0, column=2, padx=10, pady=5)
Button(root, text="选择MOBI文件夹", command=lambda: entry_mobi_folder.insert(0, select_folder("选择MOBI文件夹"))).grid(row=1, column=2, padx=10, pady=5)
Button(root, text="开始转换", command=start_conversion).grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# 创建和放置状态标签
status_label = Label(root, text="")
status_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

# 运行主循环
root.mainloop()
