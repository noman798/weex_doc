#!/usr/bin/env python3

import polib
from config import LANG, PATH
from _util import walk_md
from os.path import join


def transalte_po(lang, po):
    li = []
    for i in po:
        if not i.msgstr:
            li.append(i.msgid.strip())
    print(li[0])
    input()

def main():
    for dirpath, md_li in walk_md():
        for i in md_li:
            for lang in LANG:
                f = join(PATH, "po", lang, dirpath, i)
                po = polib.pofile(f[:-2] + "po")
                transalte_po(lang.split("-")[0], po)


if __name__ == "__main__":
    main()
