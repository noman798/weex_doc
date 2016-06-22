# Weex 文档翻译


确保 weex_doc 与 weex 源代码在同一个目录下，weex_doc/weex 是一个有效的软链。

文档基于po4a工具进行翻译。ubuntu 可以使用 `apt-get install po4a -y` 安装po4a。

所有的 python 脚本都基于 python3，使用前请先 `pip3 install -r pyutil/requirement.txt` 安装依赖。

运行 po4a.py 会更新 po 文件，并生成在 doc 目录下生成新翻译的文档。 

至于编辑工具，由于 po 文件本身就是一个文本文件，所以任何文本编辑器都可以使用。

也可以用 [poedit](https://poedit.net/) 更方便的编辑po文件。 

运行 baidu_transalte.py 可以通过百度翻译的API自动翻译未翻译的英文，自动翻译的英文都以 ??? 作为行的结尾，以便于修改。






