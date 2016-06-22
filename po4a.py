#!/usr/bin/env python3

import envoy
from os.path import join
from shutil import rmtree, copytree
from distutils.dir_util import mkpath
from config import LANG, PATH, PATH_DOC
from _util import walk_md


def print_exist(*args):
    for i in args:
        if i:
            print(i)


def bash(cmd):
    r = envoy.run(cmd, timeout=300)
    if r.status_code:
        print(cmd)
        print_exist(r.std_out, r.std_err)


def _update(lang, path):
    f = "%s/po/%s/%s.po" % (
        PATH, lang, path[:-3]
    )
    bash(
        "po4a-updatepo -M utf-8 -f text -o markdown -m %s/%s -p %s --copyright-holder weex" % (
            PATH_DOC, path, f
        )
    )

    li = []
    with open(f) as fin:
        li = []
        for i in fin:
            for prefix in (
                '"Project-Id-Version: ',
                '"PO-Revision-Date: ',
                # '#, no-wrap',
                '"Last-Translator: ',
                '"POT-Creation-Date: ',
                '"Language-Team: ',
                '"Language: ',
                '"MIME-Version: ',
                # '"Content-Type: ',
                '"Content-Transfer-Encoding: ',
                '# SOME DESCRIPTIVE TITLE',
                '# Copyright (C) YEAR weex',
                '# This file is distributed under the same license as the PACKAGE package.',
                '# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.',
                '#, fuzzy',
            ):
                if i.startswith(prefix) or i.strip() == "#":
                    break
            else:
                li.append(i)

    with open(f, "w") as fout:
        fout.write("".join(li).strip("\n"))


def _build(lang, path):
    # po4a-translate -f text -m %s -M utf8 -p %s.po -l %s -k 0
    bash(
        "po4a-translate -M utf-8 -f text -o markdown -m %s/%s -p %s/po/%s/%s.po -l %s/doc/%s/%s -k 0" % (
            PATH_DOC, path, PATH, lang, path[:-3], PATH, lang, path
        )
    )


def scan():
    doc_path = join(PATH, "doc")
    rmtree(doc_path, ignore_errors=True)
    for i in LANG:
        copytree(PATH_DOC, join(doc_path, i))

    count = 1
    for dirpath, md_li in walk_md():
        for lang in LANG:
            mkpath(join(PATH, "po", lang, dirpath[len(PATH_DOC) + 1:]))
        for i in md_li:
            for lang in LANG:
                for func in (_update, _build):
                    f = join(dirpath, i)[len(PATH_DOC) + 1:]
                    print(count, f)
                    count += 1
                    func(lang, f)


if __name__ == "__main__":
    scan()
