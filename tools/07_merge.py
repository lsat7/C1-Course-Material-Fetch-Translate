#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""07_merge.py — 把分块译文 part 文件合并为最终 .zh.md

用法:
    python tools/07_merge.py <name>
其中 <name> 为输出文件名去掉 .zh.md 的部分（如 context-rot）。
合并来源: dist/zh/<name>.part01.md, part02.md, ...（按名称排序）
输出:      dist/zh/<name>.zh.md
"""
import sys
import os
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.normpath(os.path.join(HERE, '..', 'dist', 'zh'))


def main():
    if len(sys.argv) < 2:
        print('USAGE: python tools/07_merge.py <name>')
        return 2
    name = sys.argv[1]
    if name.endswith('.zh.md'):
        name = name[:-6]
    parts = sorted(glob.glob(os.path.join(ZH, name + '.part*.md')))
    if not parts:
        print('NO_PARTS for', name)
        return 1
    out = os.path.join(ZH, name + '.zh.md')
    total = 0
    with open(out, 'w', encoding='utf-8') as w:
        for p in parts:
            txt = open(p, encoding='utf-8').read()
            total += len(txt)
            w.write(txt)
            if not txt.endswith('\n'):
                w.write('\n')
    print('MERGED %d parts -> %s (%d chars)' % (len(parts), out, total))
    return 0


if __name__ == '__main__':
    sys.exit(main())
