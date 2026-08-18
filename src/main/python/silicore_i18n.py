# coding: utf-8
# SPDX-License-Identifier: GPL-2.0-or-later

import json
import os

try:
    from PyQt5.QtCore import QTranslator
except ImportError:  # Allows catalog validation without a local Qt installation.
    class QTranslator(object):
        def __init__(self, parent=None):
            self.parent = parent


SUPPORTED_LOCALES = ("en", "es", "fr", "de", "ko", "ja", "zh-CN", "zh-TW")

_translator = None


def normalize_locale(value):
    value = (value or "en").replace("_", "-")
    lowered = value.lower()
    if lowered.startswith(("zh-tw", "zh-hk", "zh-hant")):
        return "zh-TW"
    if lowered.startswith("zh"):
        return "zh-CN"
    for locale in SUPPORTED_LOCALES:
        locale_lower = locale.lower()
        if lowered == locale_lower or lowered.startswith(locale_lower + "-"):
            return locale
    return "en"


def catalog_path(locale):
    return os.path.join(os.path.dirname(__file__), "translations", normalize_locale(locale) + ".json")


def load_catalog(locale):
    normalized = normalize_locale(locale)
    if normalized == "en":
        return {}
    try:
        with open(catalog_path(normalized), "r", encoding="utf-8") as catalog_file:
            return json.load(catalog_file)
    except (OSError, ValueError):
        return {}


class SilicoreTranslator(QTranslator):
    def __init__(self, locale, parent=None):
        super().__init__(parent)
        self.locale = normalize_locale(locale)
        self.catalog = load_catalog(self.locale)

    def translate(self, context, source_text, disambiguation=None, n=-1):
        del context, disambiguation, n
        return self.catalog.get(source_text, source_text)


def install_translator(app, locale):
    global _translator
    normalized = normalize_locale(locale)
    if _translator is not None:
        app.removeTranslator(_translator)
    _translator = SilicoreTranslator(normalized, app)
    app.installTranslator(_translator)
    return normalized
