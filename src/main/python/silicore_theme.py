# coding: utf-8
# SPDX-License-Identifier: GPL-2.0-or-later

import os

from PyQt5.QtGui import QFont, QFontDatabase

from silicore_i18n import normalize_locale


FONT_FAMILIES = {
    "ja": "IBM Plex Sans JP",
    "ko": "IBM Plex Sans KR",
    "zh-CN": "IBM Plex Sans SC",
    "zh-TW": "IBM Plex Sans TC",
}

FONT_FILES = (
    "IBMPlexSans-Regular.ttf",
    "IBMPlexSans-Medium.ttf",
    "IBMPlexSans-SemiBold.ttf",
    "IBMPlexSansJP-Silicore.ttf",
    "IBMPlexSansKR-Silicore.ttf",
    "IBMPlexSansSC-Silicore.ttf",
    "IBMPlexSansTC-Silicore.ttf",
)


SILICORE_STYLESHEET = """
QWidget {
    color: #f7f8fb;
    font-size: 10pt;
    selection-background-color: #2f31e8;
    selection-color: #ffffff;
}
QMainWindow, QDialog, QMessageBox { background: #050507; }
QMenuBar {
    background: #09090c;
    border-bottom: 1px solid rgba(217, 220, 226, 46);
    padding: 4px 8px;
}
QMenuBar::item { padding: 8px 12px; background: transparent; }
QMenuBar::item:selected, QMenuBar::item:pressed { background: #2f31e8; color: #ffffff; }
QMenu {
    background: #111116;
    border: 1px solid #34343d;
    padding: 6px;
}
QMenu::item { min-height: 24px; padding: 7px 26px 7px 12px; }
QMenu::item:selected { background: #2f31e8; color: #ffffff; }
QMenu::separator { height: 1px; background: #34343d; margin: 5px 8px; }
QTabWidget::pane { border: 1px solid #34343d; background: #0b0b0e; }
QTabBar::tab {
    min-height: 30px;
    padding: 7px 14px;
    background: #17171d;
    border: 1px solid #34343d;
    border-bottom: 0;
    color: #c8c8c8;
}
QTabBar::tab:selected { background: #2f31e8; color: #ffffff; }
QTabBar::tab:hover:!selected { background: #24242c; color: #ffffff; }
QPushButton, QToolButton {
    min-height: 32px;
    padding: 6px 14px;
    border: 1px solid #4c4c59;
    background: #1b1b21;
    color: #f7f8fb;
}
QPushButton:hover, QToolButton:hover { border-color: #58e8f2; background: #24242c; }
QPushButton:pressed, QToolButton:pressed { border-color: #caff16; background: #2f31e8; }
QPushButton:focus, QToolButton:focus, QComboBox:focus, QLineEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #caff16;
}
QPushButton:disabled, QToolButton:disabled { color: #707079; border-color: #303038; background: #121216; }
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    min-height: 30px;
    padding: 5px 8px;
    border: 1px solid #4c4c59;
    background: #111116;
    color: #ffffff;
}
QComboBox::drop-down { width: 28px; border-left: 1px solid #4c4c59; }
QComboBox QAbstractItemView { background: #111116; border: 1px solid #4c4c59; selection-background-color: #2f31e8; }
QGroupBox { margin-top: 12px; padding-top: 12px; border: 1px solid #34343d; font-weight: 600; }
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #58e8f2; }
QCheckBox, QRadioButton { min-height: 28px; spacing: 8px; }
QCheckBox::indicator, QRadioButton::indicator { width: 18px; height: 18px; }
QCheckBox::indicator:checked, QRadioButton::indicator:checked { background: #caff16; border: 2px solid #050507; }
QProgressBar { min-height: 18px; border: 1px solid #4c4c59; background: #111116; text-align: center; }
QProgressBar::chunk { background: #caff16; }
QScrollBar:vertical { width: 14px; background: #0b0b0e; }
QScrollBar:horizontal { height: 14px; background: #0b0b0e; }
QScrollBar::handle { min-height: 28px; min-width: 28px; background: #3c3c47; border: 2px solid #0b0b0e; }
QScrollBar::handle:hover { background: #58e8f2; }
QToolTip { color: #050507; background: #d9dce2; border: 1px solid #58e8f2; padding: 5px; }
"""


def install_fonts(app, locale):
    font_dir = os.path.join(os.path.dirname(__file__), "assets", "fonts")
    for font_file in FONT_FILES:
        QFontDatabase.addApplicationFont(os.path.join(font_dir, font_file))
    family = FONT_FAMILIES.get(normalize_locale(locale), "IBM Plex Sans")
    font = QFont(family)
    font.setPointSize(10)
    app.setFont(font)
    return family
