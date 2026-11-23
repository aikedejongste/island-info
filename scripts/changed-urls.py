#!/usr/bin/env python3
"""Print URLs that are new or have a different <lastmod> in the new sitemap.

Usage: changed-urls.py OLD_SITEMAP NEW_SITEMAP

OLD_SITEMAP is the sitemap that was live before this deploy. If it is
missing or can't be parsed, every URL in NEW_SITEMAP is printed.
"""
import sys
import xml.etree.ElementTree as ET

NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def entries(path):
    root = ET.parse(path).getroot()
    return {
        u.findtext("s:loc", namespaces=NS): u.findtext("s:lastmod", namespaces=NS)
        for u in root.findall("s:url", NS)
    }


new = entries(sys.argv[2])
try:
    old = entries(sys.argv[1])
except (OSError, ET.ParseError):
    old = {}

for loc, lastmod in new.items():
    if old.get(loc) != lastmod:
        print(loc)
