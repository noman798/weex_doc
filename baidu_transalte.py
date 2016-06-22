#!/usr/bin/env python3

import polib
from pyutil.config import LANG, PATH
from pyutil._util import walk_md
from os.path import join
from pyutil._baidu import translate
from pyutil.extract import extract_map


class HideBracket:

    def __init__(self):
        self._hideed = []

    def _hide(self, txt):
        l = len(self._hideed)
        self._hideed.append(txt)
        return "(_%s_)" % l

    def hide(self, txt):
        txt = extract_map("(", ")", txt, self._hide)
        txt = extract_map("```", "```", txt, self._hide)
        txt = extract_map("`", "`", txt, self._hide)
        return txt

    def _restore(self, txt):
        x = txt[2:-2]
        if x.isdigit():
            return self._hideed[int(x)]
        return txt

    def restore(self, txt):
        txt = txt.replace("[ ", "[").replace("；", ";").replace(" ]", "]").replace(
            "（", "(").replace("）", ")")
        return extract_map("(_", "_)", txt, self._restore)


def translate_po(lang, po):
    hide_bracket = HideBracket()
    li = []
    msgid_li = []
    for i in po:
        if not i.msgstr:
            msgid = i.msgid
            if msgid.strip("\n ").startswith("```") or "</" in msgid:
                continue
            msgid = hide_bracket.hide(msgid)
            msgid_li.append((msgid, i))

    for msgid, _ in msgid_li:
        for j in msgid.split("\n"):
            j = j.strip()
            if j:
                li.append(j)
    if not li:
        return
    li = "\n".join(li)

    lang_dict = dict(translate(li, lang))
    for msgid, i in msgid_li:
        if not i.msgstr:
            t = []
            for j in msgid.split("\n"):
                j = j.strip()
                txt = lang_dict.get(j, 0)
                if txt:
                    txt = txt + " ???"
                else:
                    txt = j
                txt = hide_bracket.restore(txt)
                t.append(txt)
            i.msgstr = "\n".join(t)
    po.save()


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
