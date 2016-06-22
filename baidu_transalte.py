#!/usr/bin/env python3

from os import walk
import polib
from config import LANG, PATH, PATH_DOC
from _util import walk_md
    

def main():
    for (dirpath, dirnames, filenames) in walk(PATH_DOC):
        for i in filenames:
            if i.endswith(".md"):
                md_li.append(i)

    po = polib.pofile()


if __name__ == "__main__":
    main()
