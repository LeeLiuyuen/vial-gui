#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

import ast
import json
import os
import re
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PYTHON_ROOT = os.path.join(PROJECT_ROOT, "src", "main", "python")
TRANSLATIONS_ROOT = os.path.join(PYTHON_ROOT, "translations")
LOCALES = ("es", "fr", "de", "ko", "ja", "zh-CN", "zh-TW")
DYNAMIC_MESSAGES = {
    "Keymap", "Layout", "Macros", "Lighting", "Tap Dance", "Combos", "Key Overrides",
    "Alt Repeat Key", "QMK Settings", "Matrix tester", "Firmware updater",
    "Basic", "ISO/JIS", "Layers", "Quantum", "Backlight", "App, Media and Mouse", "User", "Macro",
}
PLACEHOLDER = re.compile(r"\{[^{}]+\}")


def source_messages():
    messages = set(DYNAMIC_MESSAGES)
    for root, _, files in os.walk(PYTHON_ROOT):
        for filename in files:
            if not filename.endswith(".py") or filename.startswith("test_"):
                continue
            path = os.path.join(root, filename)
            with open(path, "r", encoding="utf-8") as source_file:
                tree = ast.parse(source_file.read(), filename=path)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != "tr":
                    continue
                if len(node.args) < 2:
                    continue
                message = getattr(node.args[1], "value", getattr(node.args[1], "s", None))
                if isinstance(message, str):
                    messages.add(message)
    return messages


def load_catalog(locale):
    path = os.path.join(TRANSLATIONS_ROOT, locale + ".json")
    with open(path, "r", encoding="utf-8") as catalog_file:
        return json.load(catalog_file, object_pairs_hook=reject_duplicate_keys)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate translation key: {}".format(key))
        result[key] = value
    return result


def main():
    messages = source_messages()
    failures = []
    for locale in LOCALES:
        catalog = load_catalog(locale)
        missing = sorted(messages - set(catalog))
        if missing:
            failures.append("{} missing: {}".format(locale, ", ".join(missing)))
        for source, translation in catalog.items():
            if sorted(PLACEHOLDER.findall(source)) != sorted(PLACEHOLDER.findall(translation)):
                failures.append("{} placeholder mismatch: {}".format(locale, source))
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("Silicore Vial translations cover {} messages across 8 locales.".format(len(messages)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
