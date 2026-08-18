#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import argparse
import json
import os
import shutil

from fontTools import subset
from fontTools.ttLib import TTFont


def catalog_characters(project_root, locale):
    path = os.path.join(project_root, "src", "main", "python", "translations", locale + ".json")
    with open(path, "r", encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)
    text = "".join(catalog.keys()) + "".join(catalog.values())
    return text + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}[]()<>/:;,.!?+-=_#%&@ \\n"


def set_font_names(font, family):
    name_table = font["name"]
    postscript = family.replace(" ", "") + "-Regular"
    for platform_id, encoding_id, language_id in ((3, 1, 0x409), (1, 0, 0)):
        name_table.setName(family, 1, platform_id, encoding_id, language_id)
        name_table.setName("Regular", 2, platform_id, encoding_id, language_id)
        name_table.setName(family, 4, platform_id, encoding_id, language_id)
        name_table.setName(postscript, 6, platform_id, encoding_id, language_id)
        name_table.setName(family, 16, platform_id, encoding_id, language_id)
        name_table.setName("Regular", 17, platform_id, encoding_id, language_id)


def subset_font(source, destination, characters, family=None):
    options = subset.Options()
    options.name_IDs = ["*"]
    options.name_legacy = True
    options.name_languages = ["*"]
    options.layout_features = ["*"]
    options.notdef_glyph = True
    options.notdef_outline = True
    font = TTFont(source)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(text=characters)
    subsetter.subset(font)
    if family:
        set_font_names(font, family)
    font.save(destination)


def main():
    parser = argparse.ArgumentParser(description="Build the locale-specific Silicore Vial font bundle")
    parser.add_argument("--ibm-plex-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.makedirs(args.output, exist_ok=True)

    plex_ttf = os.path.join(args.ibm_plex_root, "packages", "plex-sans", "fonts", "complete", "ttf")
    for weight in ("Regular", "Medium", "SemiBold"):
        filename = "IBMPlexSans-{}.ttf".format(weight)
        shutil.copyfile(os.path.join(plex_ttf, filename), os.path.join(args.output, filename))

    subset_font(
        os.path.join(args.ibm_plex_root, "packages", "plex-sans-jp", "fonts", "complete", "ttf", "hinted", "IBMPlexSansJP-Regular.ttf"),
        os.path.join(args.output, "IBMPlexSansJP-Silicore.ttf"),
        catalog_characters(project_root, "ja"),
    )
    subset_font(
        os.path.join(args.ibm_plex_root, "packages", "plex-sans-kr", "fonts", "complete", "ttf", "hinted", "IBMPlexSansKR-Regular.ttf"),
        os.path.join(args.output, "IBMPlexSansKR-Silicore.ttf"),
        catalog_characters(project_root, "ko"),
    )
    subset_font(
        os.path.join(args.ibm_plex_root, "packages", "plex-sans-sc", "fonts", "complete", "ttf", "hinted", "IBMPlexSansSC-Regular.ttf"),
        os.path.join(args.output, "IBMPlexSansSC-Silicore.ttf"),
        catalog_characters(project_root, "zh-CN"),
        family="IBM Plex Sans SC",
    )
    subset_font(
        os.path.join(args.ibm_plex_root, "packages", "plex-sans-tc", "fonts", "complete", "ttf", "hinted", "IBMPlexSansTC-Regular.ttf"),
        os.path.join(args.output, "IBMPlexSansTC-Silicore.ttf"),
        catalog_characters(project_root, "zh-TW"),
        family="IBM Plex Sans TC",
    )

    shutil.copyfile(os.path.join(args.ibm_plex_root, "LICENSE.txt"), os.path.join(args.output, "IBM-Plex-OFL.txt"))


if __name__ == "__main__":
    main()
