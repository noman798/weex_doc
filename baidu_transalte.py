#!/usr/bin/env python3

import polib
from config import LANG, PATH
from _util import walk_md
from os.path import join

def main():
    for dirpath, md_li in walk_md():
        for i in md_li:
            for lang in LANG:
                f = join(PATH, "po", lang, dirpath, i)
                print(f)
                #po = polib.pofile()


if __name__ == "__main__":
    main()
