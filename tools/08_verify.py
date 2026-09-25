#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""08_verify.py — 校验译文：字符数与汉字占比

用法:
    python tools/08_verify.py <path-to-zh.md>
若传入目录或省略参数，则批量校验 dist/zh/*.zh.md。
汉字占比 (han_pct) 是判断"是否真的译成中文"的硬指标：
真译文通常 > 25%；0% 即未翻译（占位/英文原文）。
"""
import sys
import os
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ZH = os.path.normpath(os.path.join(HERE, '..', 'dist', 'zh'))


def stats(path):
    txt = open(path, encoding='utf-8', errors='ignore').read()
    han = sum(1 for c in txt if '\u4e00' <= c <= '\u9fff')
    pct = han / max(1, len(txt)) * 100
    return len(txt), han, pct


def one(path):
    n, h, p = stats(path)
    flag = 'OK' if p > 25 else ('EMPTY' if n < 200 else 'NOT_TRANSLATED')
    print('%-52s chars=%7d han=%7d han_pct=%6.2f%% %s'
          % (os.path.basename(path), n, h, p, flag))


def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = ZH
    if os.path.isdir(target):
        for f in sorted(glob.glob(os.path.join(target, '*.zh.md'))):
            one(f)
    else:
        one(target)
    return 0


if __name__ == '__main__':
    sys.exit(main())
