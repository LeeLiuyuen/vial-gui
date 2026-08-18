# SPDX-License-Identifier: GPL-2.0-or-later

import unittest

from silicore_i18n import SUPPORTED_LOCALES, SilicoreTranslator, load_catalog, normalize_locale


class SilicoreI18nTest(unittest.TestCase):
    def test_normalize_locale(self):
        cases = (
            ("en-US", "en"), ("es-MX", "es"), ("fr", "fr"), ("de-DE", "de"),
            ("ko_KR", "ko"), ("ja-JP", "ja"), ("zh-Hans", "zh-CN"),
            ("zh-Hant", "zh-TW"), ("zh-HK", "zh-TW"), ("unsupported", "en"),
        )
        for value, expected in cases:
            self.assertEqual(normalize_locale(value), expected)

    def test_all_locale_catalogs_load(self):
        self.assertEqual(SUPPORTED_LOCALES, ("en", "es", "fr", "de", "ko", "ja", "zh-CN", "zh-TW"))
        for locale in SUPPORTED_LOCALES[1:]:
            self.assertTrue(load_catalog(locale)["Keymap"])

    def test_translator_falls_back_to_source_text(self):
        translator = SilicoreTranslator("zh-CN")
        self.assertEqual(translator.translate("MainWindow", "Keymap"), "键位")
        self.assertEqual(translator.translate("MainWindow", "KC_ESC"), "KC_ESC")

    def test_keycode_category_translations(self):
        translator = SilicoreTranslator("zh-CN")
        expected = {
            "Basic": "基础",
            "Layers": "层",
            "Quantum": "QMK 功能",
            "Backlight": "背光",
            "App, Media and Mouse": "应用、媒体和鼠标",
            "User": "用户",
            "Macro": "宏",
        }
        for source, translation in expected.items():
            self.assertEqual(translator.translate("TabbedKeycodes", source), translation)


if __name__ == "__main__":
    unittest.main()
