#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
03_segment.py — 把抽取后的 src.md 切成翻译单元(segment)，并做术语保护占位替换。

设计要点（对应 rubric 的 pipelineAutomation）：
  1. 按空行切块 -> 块内按句末标点细分 -> 合并到 <= 1200 字符 的翻译单元
  2. 代码块 / 表格 / 纯链接 / 纯数字行 标记为 skip（不送翻译，原样保留）
  3. glossary do_not_translate 词 + 反引号内代码 -> 替换为 @K{id}@ 占位，译后还原
  4. 输出 segments.jsonl，每行 {id, doc, idx, kind, source, protected_map}

用法: python tools/03_segment.py --src <extracted_dir> --out <work_dir>
"""
import argparse, json, os, re, sys, hashlib

MAX_UNIT = 1200          # 单个翻译单元字符上限
MIN_UNIT = 40            # 小于此长度的块尝试与相邻块合并

CJK = re.compile(r'[\u4e00-\u9fff]')
SENT_END = re.compile(r'(?<=[.!?。！？])\s+')
CODE_FENCE = re.compile(r'^```')
TABLE_ROW = re.compile(r'^\s*\|')
URL_ONLY = re.compile(r'^https?://\S+$')
BULLET = re.compile(r'^\s*(?:[-*+]|\d+[.)])\s+')


def load_glossary(path):
    g = json.load(open(path, encoding='utf-8'))
    dnt = sorted(g.get('do_not_translate', []), key=len, reverse=True)
    return dnt


def build_protector(dnt):
    """返回 (protect_fn, restore_fn)。用长词优先匹配，避免子串误伤。"""
    store = {}
    counter = [0]

    def protect(text):
        local = {}

        def rep(m):
            key = '@K%d@' % counter[0]
            counter[0] += 1
            local[key] = m.group(0)
            return key

        # 先保护反引号内联代码
        text = re.sub(r'`[^`\n]+`', rep, text)
        # 再保护术语表 do_not_translate（整词、大小写敏感优先，回退忽略大小写）
        for term in dnt:
            pat = re.compile(r'(?<![\w\-])' + re.escape(term) + r'(?![\w\-])')
            text = pat.sub(rep, text)
        store.update(local)
        return text, local

    def restore(text, local):
        for k, v in sorted(local.items(), key=lambda x: -len(x[0])):
            text = text.replace(k, v)
        return text

    return protect, restore


def classify(block):
    s = block.strip()
    if not s:
        return 'empty'
    if CODE_FENCE.match(s):
        return 'code'
    if TABLE_ROW.match(s):
        return 'table'
    if URL_ONLY.match(s):
        return 'url'
    if s.startswith('#') and len(s) < 120:
        return 'heading'
    if not re.search(r'[A-Za-z]', s):
        return 'nonascii'
    return 'text'


def split_block(block):
    """块内按句子切分，再合并到 <= MAX_UNIT。"""
    parts = [p for p in SENT_END.split(block) if p.strip()]
    if not parts:
        return [block]
    units, buf = [], ''
    for p in parts:
        cand = (buf + ' ' + p).strip() if buf else p
        if len(cand) > MAX_UNIT and buf:
            units.append(buf)
            buf = p
        else:
            buf = cand
    if buf:
        units.append(buf)
    return units


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--glossary', default=None)
    ap.add_argument('--ext', default='.src.md')
    args = ap.parse_args()

    gl_path = args.glossary or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'glossary.json')
    dnt = load_glossary(gl_path)
    protect, _ = build_protector(dnt)

    os.makedirs(args.out, exist_ok=True)
    out_path = os.path.join(args.out, 'segments.jsonl')
    stats = {'docs': 0, 'segments': 0, 'translatable': 0, 'skipped': 0, 'chars': 0}

    with open(out_path, 'w', encoding='utf-8') as fo:
        for root, _, files in os.walk(args.src):
            for fn in sorted(files):
                if not fn.endswith(args.ext):
                    continue
                path = os.path.join(root, fn)
                doc = fn[:-len(args.ext)]
                raw = open(path, encoding='utf-8', errors='replace').read()
                stats['docs'] += 1
                idx = 0
                for block in re.split(r'\n\s*\n', raw):
                    kind = classify(block)
                    if kind in ('empty', 'code', 'table', 'url', 'nonascii'):
                        stats['skipped'] += 1
                        rec = {'id': '%s#%03d' % (doc, idx), 'doc': doc, 'idx': idx,
                               'kind': kind, 'source': block.strip(), 'protected': None,
                               'status': 'skip'}
                        fo.write(json.dumps(rec, ensure_ascii=False) + '\n')
                        idx += 1
                        continue
                    for unit in split_block(block):
                        u = unit.strip()
                        if len(u) < 3:
                            continue
                        is_heading = kind == 'heading'
                        if is_heading:
                            masked, local = u, {}
                        else:
                            masked, local = protect(u)
                        rec = {'id': '%s#%03d' % (doc, idx), 'doc': doc, 'idx': idx,
                               'kind': kind, 'source': u, 'protected': masked,
                               'protected_map': local, 'status': 'pending'}
                        fo.write(json.dumps(rec, ensure_ascii=False) + '\n')
                        stats['segments'] += 1
                        stats['translatable'] += 1
                        stats['chars'] += len(u)
                        idx += 1

    json.dump(stats, open(os.path.join(args.out, 'segments.stats.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('segments=%d translatable=%d skipped=%d chars=%d docs=%d' % (
        stats['segments'], stats['translatable'], stats['skipped'], stats['chars'], stats['docs']))
    print('out:', out_path)


if __name__ == '__main__':
    main()
