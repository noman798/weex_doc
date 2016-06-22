#!/usr/bin/env python3

import polib
from pyutil.config import LANG, PATH
from pyutil._util import walk_md
from os.path import join
from pyutil._baidu import translate


def translate_po(lang, po):
    li = []
    for i in po:
        if not i.msgstr:
            for j in i.msgid.split("\n"):
                li.append(j.strip())
    if not li:
        return

    lang_dict = dict(translate("\n".join(li), lang))

    for i in po:
        if not i.msgstr:
            t = []
            for j in i.msgid.split("\n"):
                j = j.strip()
                txt = lang_dict.get(j, 0)
                if txt:
                    txt = "? " + txt
                else:
                    txt = j
                t.append(txt)
            i.msgstr = "\n".join(t)
    po.save()
    input()


def main():
    for dirpath, md_li in walk_md():
        for i in md_li:
            for lang in LANG:
                f = join(PATH, "po", lang, dirpath, i)[:-2] + "po"
                print(lang, f)
                po = polib.pofile(f)
                translate_po(lang.split("-")[0], po)


if __name__ == "__main__":
    main()
