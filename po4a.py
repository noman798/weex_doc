#!/usr/bin/env python3

import envoy
from os import walk
from os.path import dirname, abspath, join
from distutils.dir_util import mkpath

PATH = abspath(dirname(__file__))
PATH_DOC = join(PATH, "weex", "doc")

LANG = [
    "zh-cn"
]


def print_exist(*args):
    for i in args:
        if i:
            print(i)


def bash(cmd):
    r = envoy.run(cmd)
    print(cmd)
    print_exist(r.std_out, r.std_err)


def _update(lang, path):
    bash(
        "po4a-updatepo -M utf-8 -f text -o markdown -m %s/%s -p %s/po/%s/%s.po" % (
            PATH_DOC, path, PATH, lang, path[:-3]
        )
    )


def _build(lang, path):
    # po4a-translate -f text -m %s -M utf8 -p %s.po -l %s -k 0
    bash(
        "po4a-translate -M utf-8 -f text -o markdown -m %s/%s -p %s/po/%s/%s.po -l %s/doc/%s/%s -k 0" % (
            PATH_DOC, path, PATH, lang, path[:-3], PATH, lang, path
        )
    )


def scan():
    for (dirpath, dirnames, filenames) in walk(PATH_DOC):
        for lang in LANG:
            for i in ("po", "doc"):
                mkpath(join(PATH, i, lang, dirpath[len(PATH_DOC) + 1:]))
        for i in filenames:
            if i.endswith(".md"):
                for lang in LANG:
                    for func in (_update, _build):
                        func(lang, join(dirpath, i)[len(PATH_DOC) + 1:])


if __name__ == "__main__":
    scan()
