# epub2mobi
## 功能：
用python3运行该程序可将批量epub格式的电子书转换成mobi格式。
## 运行方式：
将此脚本保存为一个 .py 文件，例如 epub2mobi.py。
在命令行中运行此脚本，可以使用如下命令：

`python3 epub2mobi.py /path/to/source /path/to/destination`

其中 /path/to/source 和 /path/to/destination 分别是源目录和目标目录的路径。

在0.1版本中，在命令行中运行此脚本，可以使用如下命令：

`python3 epub2mobi.py /path/to/source /path/to/destination [number_of_threads]`

其中 /path/to/source 和 /path/to/destination 分别是源目录和目标目录的路径，[number_of_threads] 是可选参数，用于指定线程池中的线程数，默认为 4。
通过这种方式，你可以显著提高文件转换的速度，特别是在处理大量文件时。

0.2版本中添加了图形界面，除系统中预安装calibre外，还需要预安装pyton tk库，可以运行如下命令：

`python3 epub2mobi_gui.py`
## 借鉴
本脚本基于[juanre/epub2mobi](https://github.com/juanre/epub2mobi)脚本，但其脚本长期未维护已不能在python最新版本下正常运行。

## 注意事项
本脚本运行依赖calibre中的ebook-convert，因此需要系统已安装Calibre软件
