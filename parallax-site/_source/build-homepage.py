#!/usr/bin/env python3
"""
Rebuild index.html from _source/homepage.html.

index.html is a packed file: most of it is base64 images and libraries, and the
page's real source sits on ONE line, inside <script type="__bundler/template">,
stored as an escaped JSON string. That is unreadable and un-editable by hand.

So we keep the readable copy in _source/homepage.html, edit that, and run this
script to fold it back in. Nothing else in index.html is touched.

    python3 _source/build-homepage.py

Run it from anywhere. It stops with a clear message rather than writing a
half-built file.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
SOURCE = os.path.join(HERE, "homepage.html")
INDEX = os.path.join(SITE, "index.html")

OPEN_TAG = '  <script type="__bundler/template">'


def die(msg):
    sys.exit("BUILD FAILED — %s\nindex.html was not changed." % msg)


def main():
    for path in (SOURCE, INDEX):
        if not os.path.exists(path):
            die("cannot find %s" % path)

    with open(SOURCE, encoding="utf-8") as f:
        page = f.read()

    with open(INDEX, encoding="utf-8") as f:
        lines = f.read().split("\n")

    # Find the template slot by its opening tag rather than a fixed line number,
    # so the script survives the packed file being regenerated.
    try:
        open_at = lines.index(OPEN_TAG)
    except ValueError:
        die("index.html has no %s line — is it the packed file?" % OPEN_TAG.strip())

    payload_at = open_at + 1
    if payload_at + 1 >= len(lines) or lines[payload_at + 1].strip() != "</script>":
        die("the template slot in index.html is not the expected one line long")

    # The page source contains </script> tags of its own. Left literal, the first
    # one would close the wrapper script early and the page would break. Escaping
    # the slash is how the original file avoids this.
    encoded = json.dumps(page, ensure_ascii=False).replace("</", "<\\u002F")

    # Prove it survives the round trip before writing anything.
    if json.loads(encoded) != page:
        die("the encoded page did not decode back to the original")

    lines[payload_at] = encoded

    tmp = INDEX + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    os.replace(tmp, INDEX)

    kb = os.path.getsize(INDEX) / 1024
    print("Built index.html  (%s, %.0f KB)" % (INDEX, kb))
    print("Open it in a browser to check, then upload it to GitHub.")


if __name__ == "__main__":
    main()
