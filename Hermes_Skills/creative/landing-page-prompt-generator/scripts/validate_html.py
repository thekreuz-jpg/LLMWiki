#!/usr/bin/env python3
"""Validate one or more landing-page index.html files for the
landing-page-prompt-generator skill.

Checks every file for: a DOCTYPE, balanced HTML tags, and at least one
element carrying class="reveal" (the reveal-on-scroll contract).

Usage:
  python scripts/validate_html.py PATH [PATH ...]
  python scripts/validate_html.py DIR            # checks every <dir>/*/index.html

Exit code 0 = all valid, 1 = any invalid/missing.
"""
import os
import sys
from html.parser import HTMLParser

VOID = {'meta', 'link', 'br', 'hr', 'img', 'input', 'line', 'ellipse', 'path',
        'stop', 'rect', 'circle', 'use', 'source', 'polygon', 'polyline'}


class V(HTMLParser):
    def __init__(s):
        super().__init__()
        s.stack = []
        s.errors = []

    def handle_starttag(s, t, a):
        if t not in VOID:
            s.stack.append(t)

    def handle_endtag(s, t):
        if t in VOID:
            return
        if s.stack and s.stack[-1] == t:
            s.stack.pop()
        elif t in s.stack:
            while s.stack and s.stack[-1] != t:
                s.errors.append('unclosed ' + s.stack.pop())
            if s.stack:
                s.stack.pop()
        else:
            s.errors.append('stray ' + t)


def check(path):
    if not os.path.exists(path):
        return False, 'MISSING FILE'
    html = open(path, encoding='utf-8').read()
    p = V()
    p.feed(html)
    doctype = html.lstrip().lower().startswith('<!doctype html>')
    balanced = (not p.stack) and (not p.errors)
    reveal = html.count('class="reveal') >= 1
    reasons = []
    if not doctype:
        reasons.append('no doctype')
    if not balanced:
        reasons.append('tags: ' + str(p.stack or p.errors))
    if not reveal:
        reasons.append('no reveal')
    return (doctype and balanced and reveal), ('' if not reasons else ', '.join(reasons))


def main():
    paths = sys.argv[1:]
    if not paths:
        print('usage: validate_html.py PATH [PATH ...] | DIR')
        sys.exit(2)
    files = []
    for p in paths:
        if os.path.isdir(p):
            for slug in sorted(os.listdir(p)):
                cand = os.path.join(p, slug, 'index.html')
                if os.path.isfile(cand):
                    files.append(cand)
        else:
            files.append(p)
    ok = True
    for f in files:
        valid, reason = check(f)
        ok = ok and valid
        print(('PASS ' if valid else 'FAIL ') + f + ('' if valid else '  [' + reason + ']'))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
