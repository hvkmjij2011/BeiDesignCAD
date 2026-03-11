"""
BeiDesignCAD v0.1.0-alpha
Ana menü + Editör tek dosyada birleşik uygulama.
python beidcad.py
"""

import sys, math
import os
import json
from pathlib import Path
from datetime import datetime

# ── Gömülü tür ikonları (PNG base64) ──────────────────────────
import base64 as _icon_b64
_ATTACK_PNG_B64  = "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"
_DEFENSE_PNG_B64 = "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"
_BALANCE_PNG_B64 = "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"
_STAMINA_PNG_B64 = "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"

def _load_type_pixmap(b64_str):
    """Base64 string'ten QPixmap yükle."""
    from PySide6.QtGui import QPixmap
    data = _icon_b64.b64decode(b64_str)
    pix = QPixmap()
    pix.loadFromData(data)
    return pix

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea, QDialog, QButtonGroup, QRadioButton,
    QDialogButtonBox, QSizePolicy, QLineEdit, QPushButton,
    QCheckBox, QSpinBox, QDoubleSpinBox, QFileDialog, QMessageBox,
    QGridLayout, QTabWidget, QColorDialog, QSplitter
)
from PySide6.QtCore import Qt, QTimer, QRect, QPoint, Signal
from PySide6.QtGui import (
    QPainter, QColor, QPen, QFont, QPainterPath, QCursor,
    QKeySequence, QShortcut
)

# ── Ayarlar dosyası ───────────────────────────────────────────
SETTINGS_FILE = Path(__file__).parent / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",   # "dark" | "light"
    "lang":  "tr",     # "tr"   | "en"  | "ja"
}

def load_settings() -> dict:
    defaults = {"theme": "dark", "lang": "tr"}
    if SETTINGS_FILE.exists():
        try:
            return {**defaults, **json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))}
        except Exception:
            pass
    return defaults

def save_settings(s: dict):
    SETTINGS_FILE.write_text(json.dumps(s, indent=2), encoding="utf-8")


# ── Tema ──────────────────────────────────────────────────────
class Theme:
    def __init__(self, dark: bool = True):
        if dark:
            self.BG          = QColor("#1e1e1e")
            self.SIDEBAR     = QColor("#252526")
            self.PANEL       = QColor("#2d2d2d")
            self.PANEL_HOVER = QColor("#333333")
            self.BORDER      = QColor("#3c3c3c")
            self.BORDER_LT   = QColor("#505050")
            self.ACCENT      = QColor("#0078d4")
            self.ACCENT2     = QColor("#40a9ff")
            self.TEXT_PRI    = QColor("#cccccc")
            self.TEXT_SEC    = QColor("#888888")
            self.TEXT_DIM    = QColor("#555555")
            self.TITLE       = QColor("#ffffff")
            self.TOPBAR      = QColor("#1a1a1a")
            self.TOPBAR_LOGO = QColor("#111111")
            self.COL_HDR     = QColor("#161616")
            self.ROW_HOVER   = QColor("#272727")
            self.TAG_BEY_BG  = QColor("#1a4a70")
            self.TAG_BEY_FG  = QColor("#7ec8ff")
            self.TAG_BGM_BG  = QColor("#2d5a1e")
            self.TAG_BGM_FG  = QColor("#7ddd6a")
        else:
            self.BG          = QColor("#f3f3f3")
            self.SIDEBAR     = QColor("#e8e8e8")
            self.PANEL       = QColor("#ffffff")
            self.PANEL_HOVER = QColor("#ddeeff")
            self.BORDER      = QColor("#d0d0d0")
            self.BORDER_LT   = QColor("#aaaaaa")
            self.ACCENT      = QColor("#0067b8")
            self.ACCENT2     = QColor("#0084d9")
            self.TEXT_PRI    = QColor("#1e1e1e")
            self.TEXT_SEC    = QColor("#555555")
            self.TEXT_DIM    = QColor("#aaaaaa")
            self.TITLE       = QColor("#000000")
            self.TOPBAR      = QColor("#e0e0e0")
            self.TOPBAR_LOGO = QColor("#d0d0d0")
            self.COL_HDR     = QColor("#ececec")
            self.ROW_HOVER   = QColor("#ddeeff")
            self.TAG_BEY_BG  = QColor("#b3d6f5")
            self.TAG_BEY_FG  = QColor("#004c8c")
            self.TAG_BGM_BG  = QColor("#b3e6a0")
            self.TAG_BGM_FG  = QColor("#1a5e00")

T = Theme(dark=True)   # aktif tema (global, uygulama yeniden başlatılır)


# ── Çeviri ────────────────────────────────────────────────────
TR = {
    # ── Türkçe ───────────────────────────────────────────────
    "tr": {
        "start":           "Başlangıç",
        "new_project":     "Yeni Proje",
        "new_sub":         "Seri seç · sıfırdan başla",
        "open_project":    "Proje Aç",
        "open_sub":        "Kayıtlı .bei dosyasını yükle",
        "settings":        "Ayarlar",
        "settings_sub":    "Uygulama tercihleri",
        "recent":          "Son Projeler",
        "no_recent":       "Henüz proje yok.\n./projects klasörüne .bei dosyası ekleyin.",
        "col_name":        "AD",
        "col_date":        "DEĞİŞTİRİLME",
        "col_series":      "SERİ",
        "settings_title":  "Ayarlar",
        "theme_label":     "Tema",
        "theme_dark":      "Koyu",
        "theme_light":     "Açık",
        "lang_label":      "Dil",
        "lang_tr":         "Türkçe",
        "lang_en":         "English",
        "lang_ja":         "日本語",
        "restart_note":    "Değişiklikler uygulamayı yeniden başlatmanızı gerektirebilir.",
        "ok":              "Tamam",
        "cancel":          "İptal",
        "new_label":       "YENİ",
        "open_label":      "AÇ",
        "other_label":     "DİĞER",
        "soon":            "Yakında",
        "hws_title":       "Hybrid Wheel System",
        "hws_sub":         "Yan sanayi standart parça sistemi",
        "bgm_title":       "Beigoma",
        "bgm_sub":         "Metal Fight standart sistemi",
        "tpl_title":       "Şablon",
        "tpl_sub":         "Hazır şablondan başla",
        "file_exists_msg": "\'{safe}.bei\' zaten var.\nFarklı bir ad seçin.",
        "date_just_now":   "Az önce",
        "date_mins_ago":   "{m} dk önce",
        "date_yesterday":  "Dün",
        "date_days_ago":   "{d} gün önce",
        "date_weeks_ago":  "{w} hafta önce",
        "tex_info":        "PNG veya JPG yükle.\nHexagonal yüzeye\notomatik uyarlanır.",
    },
    # ── English ──────────────────────────────────────────────
    "en": {
        "start":           "Start",
        "new_project":     "New Project",
        "new_sub":         "Choose series · start from scratch",
        "open_project":    "Open Project",
        "open_sub":        "Load a saved .bei file",
        "settings":        "Settings",
        "settings_sub":    "Application preferences",
        "recent":          "Recent Projects",
        "no_recent":       "No projects yet.\nAdd .bei files to the ./projects folder.",
        "col_name":        "NAME",
        "col_date":        "MODIFIED",
        "col_series":      "SERIES",
        "settings_title":  "Settings",
        "theme_label":     "Theme",
        "theme_dark":      "Dark",
        "theme_light":     "Light",
        "lang_label":      "Language",
        "lang_tr":         "Türkçe",
        "lang_en":         "English",
        "lang_ja":         "日本語",
        "restart_note":    "Some changes may require restarting the application.",
        "ok":              "OK",
        "cancel":          "Cancel",
        "new_label":       "NEW",
        "open_label":      "OPEN",
        "other_label":     "OTHER",
        "soon":            "Coming Soon",
        "hws_title":       "Hybrid Wheel System",
        "hws_sub":         "Third-party standard parts system",
        "bgm_title":       "Beigoma",
        "bgm_sub":         "Metal Fight standard system",
        "tpl_title":       "Template",
        "tpl_sub":         "Start from a ready-made template",
        "file_exists_msg": "\'{safe}.bei\' already exists.\nChoose a different name.",
        "date_just_now":   "Just now",
        "date_mins_ago":   "{m} min ago",
        "date_yesterday":  "Yesterday",
        "date_days_ago":   "{d} days ago",
        "date_weeks_ago":  "{w} weeks ago",
        "tex_info":        "Load a PNG or JPG.\nAuto-fitted to the\nhexagonal face.",
    },
    # ── 日本語 ────────────────────────────────────────────────
    "ja": {
        "start":           "スタート",
        "new_project":     "新規プロジェクト",
        "new_sub":         "シリーズを選ぶ · ゼロから始める",
        "open_project":    "プロジェクトを開く",
        "open_sub":        "保存済みの .bei ファイルを読み込む",
        "settings":        "設定",
        "settings_sub":    "アプリケーション設定",
        "recent":          "最近のプロジェクト",
        "no_recent":       "プロジェクトがありません。\n./projects フォルダに .bei ファイルを追加してください。",
        "col_name":        "名前",
        "col_date":        "更新日時",
        "col_series":      "シリーズ",
        "settings_title":  "設定",
        "theme_label":     "テーマ",
        "theme_dark":      "ダーク",
        "theme_light":     "ライト",
        "lang_label":      "言語",
        "lang_tr":         "Türkçe",
        "lang_en":         "English",
        "lang_ja":         "日本語",
        "restart_note":    "変更を反映するには、アプリを再起動してください。",
        "ok":              "OK",
        "cancel":          "キャンセル",
        "new_label":       "新規",
        "open_label":      "開く",
        "other_label":     "その他",
        "soon":            "近日公開",
        "hws_title":       "ハイブリッドホイールシステム",
        "hws_sub":         "サードパーティ標準パーツシステム",
        "bgm_title":       "ベイゴマ",
        "bgm_sub":         "メタルファイト標準システム",
        "tpl_title":       "テンプレート",
        "tpl_sub":         "既製テンプレートから始める",
        "file_exists_msg": "\'{safe}.bei\' はすでに存在します。\n別の名前を選んでください。",
        "date_just_now":   "たった今",
        "date_mins_ago":   "{m} 分前",
        "date_yesterday":  "昨日",
        "date_days_ago":   "{d} 日前",
        "date_weeks_ago":  "{w} 週間前",
        "tex_info":        "PNGまたはJPGを読み込みます。\n六角形の面に\n自動フィットします。",
    },
}

def t(key: str, lang: str) -> str:
    return TR.get(lang, TR["tr"]).get(key, key)


# ── ./projects tarayıcısı ─────────────────────────────────────
def scan_projects() -> list[dict]:
    """
    ./projects/*.bei dosyalarını tarar.
    .bei dosyası ileride düz metin format içerecek;
    şimdilik sadece ilk satırda 'series=Beyblade' veya 'series=Beigoma'
    aranır. Bulunamazsa seri "?" olarak işaretlenir.
    """
    projects_dir = Path("projects")
    projects_dir.mkdir(exist_ok=True)

    _lang = load_settings().get("lang", "tr")
    results = []
    for f in sorted(projects_dir.glob("*.bei"), key=lambda x: x.stat().st_mtime, reverse=True):
        series    = "?"
        series_id = "unknown"
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            for line in content.splitlines():
                line = line.strip()
                if line.lower().startswith("series"):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'").lower()
                    if val == "hybrid_wheel":
                        series    = "Hybrid Wheel"
                        series_id = "hybrid_wheel"
                    elif val in ("beigoma", "bei"):
                        series    = "Beigoma"
                        series_id = "beigoma"
                    break
        except Exception:
            pass

        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        now   = datetime.now()
        delta = now - mtime

        if delta.days == 0:
            if delta.seconds < 3600:
                if delta.seconds >= 60:
                    date_str = t("date_mins_ago", _lang).format(m=delta.seconds // 60)
                else:
                    date_str = t("date_just_now", _lang)
            else:
                date_str = mtime.strftime("%H:%M")
        elif delta.days == 1:
            date_str = t("date_yesterday", _lang)
        elif delta.days < 7:
            date_str = t("date_days_ago", _lang).format(d=delta.days)
        elif delta.days < 30:
            date_str = t("date_weeks_ago", _lang).format(w=delta.days // 7)
        else:
            date_str = mtime.strftime("%d.%m.%Y")

        results.append({
            "name":      f.stem,
            "series":    series,
            "series_id": series_id,
            "date":      date_str,
            "path":      str(f),
        })

    return results


# ── Spinner ───────────────────────────────────────────────────
class MiniSpinner(QWidget):
    def __init__(self, size=28, parent=None):
        super().__init__(parent)
        self._sz = size
        self.setFixedSize(size, size)
        self._angle = 0.0
        timer = QTimer(self)
        timer.timeout.connect(self._tick)
        timer.start(16)

    def _tick(self):
        self._angle = (self._angle + 1.2) % 360
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        cx = cy = self._sz // 2
        r = cx - 3
        p.translate(cx, cy)
        p.setPen(QPen(T.BORDER, 1.5))
        p.setBrush(Qt.NoBrush)
        p.drawEllipse(-r, -r, r * 2, r * 2)
        p.rotate(self._angle)
        pen = QPen(T.ACCENT, 2)
        pen.setCapStyle(Qt.RoundCap)
        p.setPen(pen)
        p.drawArc(-r, -r, r * 2, r * 2, 0, 110 * 16)
        p.rotate(-self._angle)
        p.setPen(Qt.NoPen)
        p.setBrush(T.ACCENT)
        p.drawEllipse(-2, -2, 4, 4)
        p.end()


# ── Eylem butonu ──────────────────────────────────────────────
class ActionButton(QWidget):
    clicked = Signal()

    def __init__(self, icon, title, subtitle, accent=None, parent=None):
        super().__init__(parent)
        self._hover   = False
        self._icon    = icon
        self._title   = title
        self._subtitle = subtitle
        self._accent  = accent
        self.setFixedHeight(68)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def set_accent(self, c): self._accent = c

    def enterEvent(self, e): self._hover = True;  self.update()
    def leaveEvent(self, e): self._hover = False; self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.clicked.emit()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        ac = self._accent or T.ACCENT

        p.fillRect(0, 0, w, h, T.PANEL_HOVER if self._hover else T.PANEL)
        p.fillRect(0, 0, 3, h, ac)
        p.setPen(QPen(T.BORDER_LT if self._hover else T.BORDER, 1))
        p.setBrush(Qt.NoBrush)
        p.drawRect(0, 0, w - 1, h - 1)

        # İkon kutu
        p.fillRect(12, 12, 44, 44, QColor(ac.red(), ac.green(), ac.blue(), 25))
        p.setPen(QPen(QColor(ac.red(), ac.green(), ac.blue(), 70), 1))
        p.drawRect(12, 12, 44, 44)
        p.setFont(QFont("Segoe UI Symbol", 15))
        p.setPen(ac)
        p.drawText(QRect(12, 12, 44, 44), Qt.AlignCenter, self._icon)

        p.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        p.setPen(T.TITLE if self._hover else T.TEXT_PRI)
        p.drawText(QRect(68, 10, w - 90, 26), Qt.AlignVCenter | Qt.AlignLeft, self._title)

        p.setFont(QFont("Segoe UI", 8))
        p.setPen(T.TEXT_SEC)
        p.drawText(QRect(68, 34, w - 90, 22), Qt.AlignVCenter | Qt.AlignLeft, self._subtitle)

        if self._hover:
            p.setPen(QPen(T.ACCENT2, 1.5))
            ax, ay = w - 18, h // 2
            p.drawLine(ax - 5, ay - 4, ax, ay)
            p.drawLine(ax - 5, ay + 4, ax, ay)
        p.end()


# ── Recent satır ──────────────────────────────────────────────
class RecentRow(QWidget):
    opened = Signal(str, str)   # (path, series_id)

    def __init__(self, name, series, series_id, date, path, parent=None):
        super().__init__(parent)
        self._hover     = False
        self._name      = name
        self._series    = series
        self._series_id = series_id
        self._date      = date
        self._path      = path
        self.setFixedHeight(48)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def enterEvent(self, e): self._hover = True;  self.update()
    def leaveEvent(self, e): self._hover = False; self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.opened.emit(self._path, self._series_id)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        p.fillRect(0, 0, w, h, T.ROW_HOVER if self._hover else T.BG)
        p.setPen(QPen(T.BORDER, 1))
        p.drawLine(0, h - 1, w, h - 1)
        if self._hover:
            p.fillRect(0, 0, 2, h, T.ACCENT)

        # Dosya ikonu
        p.setPen(QPen(T.TEXT_DIM, 1))
        p.setBrush(T.PANEL)
        p.drawRect(16, 10, 18, 24)
        fold = QPainterPath()
        fold.moveTo(28, 10); fold.lineTo(34, 16); fold.lineTo(28, 16); fold.closeSubpath()
        p.fillPath(fold, T.ROW_HOVER if self._hover else T.BG)
        p.setPen(QPen(T.TEXT_DIM, 1))
        p.drawLine(28, 10, 34, 16)
        p.drawLine(28, 10, 28, 16)
        p.drawLine(28, 16, 34, 16)
        p.setFont(QFont("Segoe UI", 6))
        p.setPen(T.ACCENT)
        p.drawText(QRect(16, 22, 18, 12), Qt.AlignCenter, ".bei")

        # Ad
        name_w = int(w * 0.42)
        p.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        p.setPen(T.TITLE if self._hover else T.TEXT_PRI)
        p.drawText(QRect(46, 0, name_w, h), Qt.AlignVCenter | Qt.AlignLeft, self._name)

        # Tarih
        date_x = 46 + name_w + 8
        date_w = int(w * 0.26)
        p.setFont(QFont("Segoe UI", 8))
        p.setPen(T.TEXT_SEC)
        p.drawText(QRect(date_x, 0, date_w, h), Qt.AlignVCenter | Qt.AlignLeft, self._date)

        # Seri etiketi
        is_bey   = self._series == "Hybrid Wheel"
        is_bgm   = self._series == "Beigoma"
        tag_bg   = T.TAG_BEY_BG if is_bey else (T.TAG_BGM_BG if is_bgm else T.BORDER)
        tag_fg   = T.TAG_BEY_FG if is_bey else (T.TAG_BGM_FG if is_bgm else T.TEXT_DIM)
        tag_label = self._series if self._series != "?" else "—"
        tag_w    = 64
        tag_rect = QRect(w - tag_w - 16, (h - 18) // 2, tag_w, 18)
        p.fillRect(tag_rect, tag_bg)
        p.setFont(QFont("Segoe UI", 7, QFont.Bold))
        p.setPen(tag_fg)
        p.drawText(tag_rect, Qt.AlignCenter, tag_label.upper())
        p.end()


# ── Üst bar ───────────────────────────────────────────────────
class TopBar(QWidget):
    def __init__(self, lang="tr", parent=None):
        super().__init__(parent)
        self._lang = lang
        self.setFixedHeight(36)

    def paintEvent(self, event):
        p = QPainter(self)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, T.TOPBAR)
        p.setPen(QPen(T.BORDER, 1))
        p.drawLine(0, h - 1, w, h - 1)

        p.fillRect(0, 0, 170, h, T.TOPBAR_LOGO)
        p.setPen(QPen(T.BORDER, 1))
        p.drawLine(170, 0, 170, h)

        p.setFont(QFont("Segoe UI", 10, QFont.Bold))
        p.setPen(T.ACCENT)
        p.drawText(QRect(14, 0, 40, h), Qt.AlignVCenter, "Bei")
        p.setPen(T.TEXT_SEC)
        p.drawText(QRect(46, 0, 120, h), Qt.AlignVCenter, "DesignCAD")

        p.end()


# ── Sütun başlığı ─────────────────────────────────────────────
class ColHeader(QWidget):
    def __init__(self, lang="tr", parent=None):
        super().__init__(parent)
        self._lang = lang
        self.setFixedHeight(26)

    def paintEvent(self, event):
        p = QPainter(self)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, T.COL_HDR)
        p.setPen(QPen(T.BORDER, 1))
        p.drawLine(0, h - 1, w, h - 1)
        p.setFont(QFont("Segoe UI", 7, QFont.Bold))
        p.setPen(T.TEXT_DIM)
        name_w = int(w * 0.42)
        p.drawText(QRect(46, 0, name_w, h), Qt.AlignVCenter, t("col_name", self._lang))
        date_x = 46 + name_w + 8
        p.drawText(QRect(date_x, 0, int(w * 0.26), h), Qt.AlignVCenter, t("col_date", self._lang))
        p.drawText(QRect(w - 80, 0, 64, h), Qt.AlignVCenter | Qt.AlignCenter, t("col_series", self._lang))
        p.end()


# ── Seri kartı (Yeni Proje diyaloğu için) ────────────────────
class SeriesCard(QWidget):
    def __init__(self, series_id, title, subtitle, tag_color, tag_text,
                 disabled=False, lang="tr", parent=None):
        super().__init__(parent)
        self._id       = series_id
        self._title    = title
        self._subtitle = subtitle
        self._tag_col  = tag_color
        self._tag_text = tag_text
        self._disabled = disabled
        self._selected = False
        self._hover    = False
        self._lang     = lang
        self.setFixedHeight(72)
        if not disabled:
            self.setCursor(QCursor(Qt.PointingHandCursor))

    def set_selected(self, v: bool):
        self._selected = v
        self.update()

    def enterEvent(self, e):
        if not self._disabled:
            self._hover = True
            self.update()

    def leaveEvent(self, e):
        self._hover = False
        self.update()

    def mousePressEvent(self, e):
        if not self._disabled and e.button() == Qt.LeftButton:
            self.set_selected(True)
            # parent diyaloğa haber ver
            p = self.parent()
            while p:
                if hasattr(p, "_on_card_clicked"):
                    p._on_card_clicked(self._id)
                    break
                p = p.parent()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()

        # Zemin
        if self._disabled:
            bg = QColor(T.PANEL.red(), T.PANEL.green(), T.PANEL.blue(), 120)
        elif self._selected:
            bg = QColor(T.ACCENT.red(), T.ACCENT.green(), T.ACCENT.blue(), 22)
        elif self._hover:
            bg = T.PANEL_HOVER
        else:
            bg = T.PANEL
        p.fillRect(0, 0, w, h, bg)

        # Kenar
        if self._selected:
            p.setPen(QPen(T.ACCENT, 1.5))
        else:
            p.setPen(QPen(T.BORDER_LT if self._hover else T.BORDER, 1))
        p.setBrush(Qt.NoBrush)
        p.drawRect(0, 0, w - 1, h - 1)

        # Sol şerit
        if self._selected:
            p.fillRect(0, 0, 3, h, T.ACCENT)

        # Seçim noktası (sağ üst)
        if self._selected:
            p.setPen(Qt.NoPen)
            p.setBrush(T.ACCENT)
            p.drawEllipse(w - 22, 8, 14, 14)
            p.setPen(QPen(QColor("white"), 1.5))
            p.drawLine(w - 19, 15, w - 16, 18)
            p.drawLine(w - 16, 18, w - 11, 12)

        # Etiket (sol üst köşe - seri rengi)
        tag_w = 72
        p.fillRect(12, 10, tag_w, 16, self._tag_col)
        p.setFont(QFont("Segoe UI", 7, QFont.Bold))
        tc = QColor(T.TEXT_DIM) if self._disabled else QColor("white")
        p.setPen(tc)
        p.drawText(QRect(12, 10, tag_w, 16), Qt.AlignCenter, self._tag_text)

        # Başlık
        title_col = T.TEXT_DIM if self._disabled else (T.TITLE if self._selected or self._hover else T.TEXT_PRI)
        p.setFont(QFont("Segoe UI", 10, QFont.DemiBold))
        p.setPen(title_col)
        p.drawText(QRect(12, 32, w - 24, 20), Qt.AlignVCenter | Qt.AlignLeft, self._title)

        # Alt yazı
        p.setFont(QFont("Segoe UI", 8))
        p.setPen(T.TEXT_DIM)
        p.drawText(QRect(12, 50, w - 24, 16), Qt.AlignVCenter | Qt.AlignLeft, self._subtitle)

        # Deaktif overlay + "Yakında"
        if self._disabled:
            p.fillRect(0, 0, w, h, QColor(0, 0, 0, 60))
            p.setFont(QFont("Segoe UI", 8, QFont.Bold))
            p.setPen(T.TEXT_DIM)
            p.drawText(QRect(w - 70, 0, 64, h), Qt.AlignVCenter | Qt.AlignRight, t("soon", self._lang if hasattr(self, "_lang") else "tr"))

        p.end()


# ── Yeni Proje diyaloğu ───────────────────────────────────────
class NewProjectDialog(QDialog):
    def __init__(self, lang: str, parent=None):
        super().__init__(parent)
        self._lang     = lang
        self._selected = None   # seçili seri id
        self._cards    = {}

        self.setWindowTitle(t("new_proj_title", lang))
        self.setFixedSize(480, 460)
        self.setStyleSheet(f"""
            QDialog {{ background: {T.SIDEBAR.name()}; }}
            QLabel  {{ background: transparent; color: {T.TEXT_PRI.name()};
                       font-family: 'Segoe UI'; }}
            QLineEdit {{
                background: {T.BG.name()};
                color: {T.TEXT_PRI.name()};
                border: 1px solid {T.BORDER.name()};
                padding: 6px 10px;
                font-family: 'Segoe UI';
                font-size: 11px;
                selection-background-color: {T.ACCENT.name()};
            }}
            QLineEdit:focus {{ border-color: {T.ACCENT.name()}; }}
            QPushButton {{
                background: {T.PANEL.name()};
                color: {T.TEXT_PRI.name()};
                border: 1px solid {T.BORDER.name()};
                padding: 6px 20px;
                font-family: 'Segoe UI'; font-size: 10px;
            }}
            QPushButton:hover {{
                background: {T.PANEL_HOVER.name()};
                border-color: {T.BORDER_LT.name()};
            }}
            QPushButton:default {{
                background: {T.ACCENT.name()};
                color: white;
                border-color: {T.ACCENT.name()};
            }}
            QPushButton:disabled {{
                background: {T.PANEL.name()};
                color: {T.TEXT_DIM.name()};
                border-color: {T.BORDER.name()};
            }}
        """)
        self._build()

    def _divider(self):
        f = QFrame()
        f.setFixedHeight(1)
        f.setStyleSheet(f"background: {T.BORDER.name()};")
        return f

    def _sec_label(self, text):
        l = QLabel(text)
        l.setStyleSheet(
            f"color: {T.TEXT_DIM.name()}; font-size: 8px;"
            "font-weight: 700; letter-spacing: 2px;"
        )
        return l

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(14)

        # ── Proje Adı ─────────────────────────────────────────
        layout.addWidget(self._sec_label(t("proj_name_lbl", self._lang)))
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText(
            t("proj_name_ph", self._lang)
        )
        self._name_edit.textChanged.connect(self._validate)
        layout.addWidget(self._name_edit)

        layout.addWidget(self._divider())

        # ── Seri ──────────────────────────────────────────────
        layout.addWidget(self._sec_label(t("series_lbl", self._lang)))

        series_list = [
            # (id, başlık, alt yazı, etiket rengi, etiket metni, disabled)
            ("hybrid_wheel",
             t("hws_title", self._lang),
             t("hws_sub",   self._lang),
             QColor("#5a3200"), "HYBRID WHEEL",
             False),
            ("beigoma",
             t("bgm_title", self._lang),
             t("bgm_sub",   self._lang),
             QColor("#1a4a0a"), "BEIGOMA",
             False),
            ("template",
             t("tpl_title", self._lang),
             t("tpl_sub",   self._lang),
             QColor("#3a3a3a"), "TEMPLATE",
             True),
        ]

        for sid, title, sub, tag_col, tag_txt, disabled in series_list:
            card = SeriesCard(sid, title, sub, tag_col, tag_txt, disabled, lang=self._lang)
            self._cards[sid] = card
            layout.addWidget(card)

        layout.addWidget(self._divider())

        # Hata / bilgi metni
        self._err_lbl = QLabel("")
        self._err_lbl.setStyleSheet(
            f"color: {QColor('#e07070').name()}; font-size: 9px;"
        )
        layout.addWidget(self._err_lbl)

        layout.addStretch()

        # Butonlar
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self._btn_cancel = self._make_btn(
            t("btn_cancel", self._lang), False
        )
        self._btn_ok = self._make_btn(
            t("btn_create", self._lang), True
        )
        self._btn_ok.setEnabled(False)
        self._btn_cancel.clicked.connect(self.reject)
        self._btn_ok.clicked.connect(self._on_accept)
        btn_row.addWidget(self._btn_cancel)
        btn_row.addSpacing(8)
        btn_row.addWidget(self._btn_ok)
        layout.addLayout(btn_row)

    def _make_btn(self, text, is_default):
        b = QPushButton(text)
        b.setDefault(is_default)
        b.setFixedHeight(30)
        return b

    def _on_card_clicked(self, series_id: str):
        self._selected = series_id
        for sid, card in self._cards.items():
            card.set_selected(sid == series_id)
        self._validate()

    def _validate(self):
        name = self._name_edit.text().strip() if hasattr(self, "_name_edit") else ""
        ok = bool(name) and self._selected is not None
        if hasattr(self, "_btn_ok"):
            self._btn_ok.setEnabled(ok)
        if hasattr(self, "_err_lbl"):
            if not name and self._selected:
                msg = t("err_name_empty", self._lang)
            elif name and not self._selected:
                msg = t("err_no_series", self._lang)
            else:
                msg = ""
            self._err_lbl.setText(msg)

    def _on_accept(self):
        self.accept()

    def result_project(self) -> dict:
        return {
            "name":   self._name_edit.text().strip(),
            "series": self._selected,
        }


# ── Ayarlar penceresi ─────────────────────────────────────────
class SettingsDialog(QDialog):
    def __init__(self, settings: dict, lang: str, parent=None):
        super().__init__(parent)
        self._s = dict(settings)
        self._lang = lang
        self.setWindowTitle(t("settings_title", lang))
        self.setFixedSize(400, 260)
        self.setStyleSheet(f"""
            QDialog {{
                background: {T.SIDEBAR.name()};
            }}
            QLabel {{
                color: {T.TEXT_PRI.name()};
                font-family: 'Segoe UI';
                font-size: 11px;
                background: transparent;
            }}
            QRadioButton {{
                color: {T.TEXT_PRI.name()};
                font-family: 'Segoe UI';
                font-size: 10px;
                background: transparent;
                spacing: 8px;
            }}
            QRadioButton::indicator {{
                width: 14px; height: 14px;
                border: 1px solid {T.BORDER_LT.name()};
                border-radius: 7px;
                background: {T.BG.name()};
            }}
            QRadioButton::indicator:checked {{
                background: {T.ACCENT.name()};
                border-color: {T.ACCENT.name()};
            }}
            QPushButton {{
                background: {T.PANEL.name()};
                color: {T.TEXT_PRI.name()};
                border: 1px solid {T.BORDER.name()};
                padding: 6px 18px;
                font-family: 'Segoe UI';
                font-size: 10px;
            }}
            QPushButton:hover {{
                background: {T.PANEL_HOVER.name()};
                border-color: {T.BORDER_LT.name()};
            }}
            QPushButton:default {{
                background: {T.ACCENT.name()};
                color: white;
                border-color: {T.ACCENT.name()};
            }}
        """)
        self._build()

    def _section(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color: {T.TEXT_DIM.name()}; font-size: 8px; font-weight: 700; "
            "letter-spacing: 2px; background: transparent;"
        )
        return lbl

    def _divider(self):
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet(f"background: {T.BORDER.name()};")
        return line

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 16)
        layout.setSpacing(12)

        # ── Tema ──────────────────────────────────────────────
        layout.addWidget(self._section(t("theme_label", self._lang)))

        theme_row = QHBoxLayout()
        theme_row.setSpacing(20)
        self._rb_dark  = QRadioButton(t("theme_dark",  self._lang))
        self._rb_light = QRadioButton(t("theme_light", self._lang))
        self._rb_dark.setChecked(self._s["theme"] == "dark")
        self._rb_light.setChecked(self._s["theme"] == "light")
        tg = QButtonGroup(self)
        tg.addButton(self._rb_dark)
        tg.addButton(self._rb_light)
        theme_row.addWidget(self._rb_dark)
        theme_row.addWidget(self._rb_light)
        theme_row.addStretch()
        layout.addLayout(theme_row)

        layout.addWidget(self._divider())

        # ── Dil ───────────────────────────────────────────────
        layout.addWidget(self._section(t("lang_label", self._lang)))

        lang_row = QHBoxLayout()
        lang_row.setSpacing(20)
        self._rb_tr = QRadioButton(t("lang_tr", self._lang))
        self._rb_en = QRadioButton(t("lang_en", self._lang))
        self._rb_ja = QRadioButton(t("lang_ja", self._lang))
        self._rb_tr.setChecked(self._s["lang"] == "tr")
        self._rb_en.setChecked(self._s["lang"] == "en")
        self._rb_ja.setChecked(self._s["lang"] == "ja")
        lg = QButtonGroup(self)
        lg.addButton(self._rb_tr)
        lg.addButton(self._rb_en)
        lg.addButton(self._rb_ja)
        lang_row.addWidget(self._rb_tr)
        lang_row.addWidget(self._rb_en)
        lang_row.addWidget(self._rb_ja)
        lang_row.addStretch()
        layout.addLayout(lang_row)

        layout.addWidget(self._divider())

        # Not
        note = QLabel(t("restart_note", self._lang))
        note.setStyleSheet(
            f"color: {T.TEXT_DIM.name()}; font-size: 8px; background: transparent;"
        )
        note.setWordWrap(True)
        layout.addWidget(note)

        layout.addStretch()

        # Butonlar
        btns = QDialogButtonBox(Qt.Horizontal)
        ok_btn     = btns.addButton(t("ok", self._lang),     QDialogButtonBox.AcceptRole)
        cancel_btn = btns.addButton(t("cancel", self._lang), QDialogButtonBox.RejectRole)
        ok_btn.setDefault(True)
        btns.accepted.connect(self._on_accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _on_accept(self):
        self._s["theme"] = "dark"  if self._rb_dark.isChecked()  else "light"
        self._s["lang"]  = ("tr" if self._rb_tr.isChecked() else
                            "ja" if self._rb_ja.isChecked() else "en")
        save_settings(self._s)
        self.accept()

    def result_settings(self) -> dict:
        return self._s


# ── Ana pencere ───────────────────────────────────────────────
class MainMenu(QMainWindow):
    def __init__(self, settings: dict):
        super().__init__()
        self._settings = settings
        self._lang = settings["lang"]
        global T
        T = Theme(dark=(settings["theme"] == "dark"))

        self.setWindowTitle("BeiDesignCAD")
        self.setMinimumSize(820, 520)
        self.resize(1040, 660)
        self._build_ui()

    def _build_ui(self):
        projects = scan_projects()

        root = QWidget()
        root.setStyleSheet(f"background: {T.BG.name()};")
        self.setCentralWidget(root)

        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        vbox.addWidget(TopBar(self._lang))

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        # ── Sol panel ─────────────────────────────────────────
        left = QWidget()
        left.setFixedWidth(360)
        left.setStyleSheet(
            f"background: {T.SIDEBAR.name()};"
            f"border-right: 1px solid {T.BORDER.name()};"
        )
        lv = QVBoxLayout(left)
        lv.setContentsMargins(0, 0, 0, 0)
        lv.setSpacing(0)

        # Başlık satırı
        hdr = QWidget()
        hdr.setFixedHeight(44)
        hdr.setStyleSheet(
            f"background: {T.SIDEBAR.name()};"
            f"border-bottom: 1px solid {T.BORDER.name()};"
        )
        hdr_lay = QHBoxLayout(hdr)
        hdr_lay.setContentsMargins(20, 0, 14, 0)
        lbl_hdr = QLabel(t("start", self._lang))
        lbl_hdr.setStyleSheet(
            f"color: {T.TEXT_PRI.name()}; font-family: 'Segoe UI';"
            "font-size: 12px; font-weight: 600; background: transparent;"
        )
        sp = MiniSpinner(26)
        sp.setStyleSheet("background: transparent;")
        hdr_lay.addWidget(lbl_hdr)
        hdr_lay.addStretch()
        hdr_lay.addWidget(sp)
        lv.addWidget(hdr)

        # Eylemler
        av = QVBoxLayout()
        av.setContentsMargins(16, 20, 16, 16)
        av.setSpacing(0)

        def sec_lbl(txt):
            l = QLabel(txt)
            l.setStyleSheet(
                f"color: {T.TEXT_DIM.name()}; font-family: 'Segoe UI';"
                "font-size: 8px; font-weight: 700; letter-spacing: 2px;"
                "background: transparent;"
            )
            return l

        av.addWidget(sec_lbl(t("new_label", self._lang)))
        av.addSpacing(6)
        btn_new = ActionButton("＋", t("new_project", self._lang),
                               t("new_sub", self._lang), T.ACCENT)
        btn_new.clicked.connect(self._open_new_project)
        av.addWidget(btn_new)

        av.addSpacing(18)
        av.addWidget(sec_lbl(t("open_label", self._lang)))
        av.addSpacing(6)
        btn_open = ActionButton("📂", t("open_project", self._lang),
                                t("open_sub", self._lang), T.TEXT_SEC)
        av.addWidget(btn_open)

        av.addSpacing(18)
        av.addWidget(sec_lbl(t("other_label", self._lang)))
        av.addSpacing(6)
        btn_settings = ActionButton("⚙", t("settings", self._lang),
                                    t("settings_sub", self._lang), T.TEXT_SEC)
        btn_settings.clicked.connect(self._open_settings)
        av.addWidget(btn_settings)
        av.addStretch()

        act_w = QWidget()
        act_w.setStyleSheet("background: transparent;")
        act_w.setLayout(av)
        lv.addWidget(act_w, 1)

        # Footer
        ftr = QWidget()
        ftr.setFixedHeight(32)
        ftr.setStyleSheet(
            f"background: {T.SIDEBAR.name()};"
            f"border-top: 1px solid {T.BORDER.name()};"
        )
        fl = QHBoxLayout(ftr)
        fl.setContentsMargins(20, 0, 20, 0)
        lv_ver = QLabel("v0.1.0-alpha")
        lv_ver.setStyleSheet(
            f"color: {T.TEXT_DIM.name()}; font-family: 'Segoe UI';"
            "font-size: 8px; background: transparent;"
        )
        lv_bei = QLabel("Bei Project")
        lv_bei.setStyleSheet(
            f"color: {T.TEXT_DIM.name()}; font-family: 'Segoe UI';"
            "font-size: 8px; background: transparent;"
        )
        fl.addWidget(lv_ver); fl.addStretch(); fl.addWidget(lv_bei)
        lv.addWidget(ftr)

        # ── Sağ panel ─────────────────────────────────────────
        right = QWidget()
        right.setStyleSheet(f"background: {T.BG.name()};")
        rv = QVBoxLayout(right)
        rv.setContentsMargins(0, 0, 0, 0)
        rv.setSpacing(0)

        # Recent başlık
        rh = QWidget()
        rh.setFixedHeight(44)
        rh.setStyleSheet(
            f"background: {T.BG.name()};"
            f"border-bottom: 1px solid {T.BORDER.name()};"
        )
        rh_lay = QHBoxLayout(rh)
        rh_lay.setContentsMargins(24, 0, 24, 0)
        lbl_rec = QLabel(t("recent", self._lang))
        lbl_rec.setStyleSheet(
            f"color: {T.TEXT_PRI.name()}; font-family: 'Segoe UI';"
            "font-size: 12px; font-weight: 600; background: transparent;"
        )
        lbl_count = QLabel(f"({len(projects)})")
        lbl_count.setStyleSheet(
            f"color: {T.TEXT_DIM.name()}; font-family: 'Segoe UI';"
            "font-size: 10px; background: transparent;"
        )
        rh_lay.addWidget(lbl_rec)
        rh_lay.addSpacing(6)
        rh_lay.addWidget(lbl_count)
        rh_lay.addStretch()
        rv.addWidget(rh)

        # Sütun başlığı
        rv.addWidget(ColHeader(self._lang))

        # Liste
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{
                background: {T.BG.name()}; width: 5px; margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {T.BORDER.name()}; border-radius: 2px; min-height: 20px;
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{ height: 0; }}
        """)

        sc_w = QWidget()
        sc_w.setStyleSheet("background: transparent;")
        sc_v = QVBoxLayout(sc_w)
        sc_v.setContentsMargins(0, 0, 0, 0)
        sc_v.setSpacing(0)

        if projects:
            for proj in projects:
                row = RecentRow(proj["name"], proj["series"],
                                proj["series_id"], proj["date"], proj["path"])
                row.opened.connect(self._launch_editor_from_recent)
                sc_v.addWidget(row)
        else:
            empty = QLabel(t("no_recent", self._lang))
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet(
                f"color: {T.TEXT_DIM.name()}; font-family: 'Segoe UI';"
                "font-size: 10px; background: transparent; padding: 40px;"
            )
            sc_v.addWidget(empty)

        sc_v.addStretch()
        scroll.setWidget(sc_w)
        rv.addWidget(scroll)

        body.addWidget(left)
        body.addWidget(right, 1)
        vbox.addLayout(body, 1)
        self.setStyleSheet(f"QMainWindow {{ background: {T.BG.name()}; }}")

    def _launch_editor_from_recent(self, path: str, series_id: str):
        self._launch_editor(Path(path), series_id)

    def _open_new_project(self):
        dlg = NewProjectDialog(self._lang, self)
        if dlg.exec() == QDialog.Accepted:
            result = dlg.result_project()
            proj_path = self._create_bei_file(result["name"], result["series"])
            if proj_path:
                self._launch_editor(proj_path, result["series"])

    def _create_bei_file(self, name: str, series: str) -> Path | None:
        """./projects/<name>.bei dosyasını TOML formatında oluşturur."""
        projects_dir = Path("projects")
        projects_dir.mkdir(exist_ok=True)

        # Güvenli dosya adı: sadece harf, rakam, _ ve -
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        path = projects_dir / f"{safe}.bei"

        if path.exists():
            from PySide6.QtWidgets import QMessageBox
            msg = QMessageBox(self)
            msg.setWindowTitle(t("err_file_exists_t", self._lang))
            msg.setText(t("file_exists_msg", self._lang).format(safe=safe))
            msg.setStyleSheet(f"background: {T.SIDEBAR.name()}; color: {T.TEXT_PRI.name()};")
            msg.exec()
            return None

        from datetime import datetime
        content = (
            f'series   = "{series}"\n'
            f'name     = "{name}"\n'
            f'created  = "{datetime.now().isoformat(timespec="seconds")}"\n'
            f'modified = "{datetime.now().isoformat(timespec="seconds")}"\n'
            f'spiral   = false\n'
            f'symbol   = ""\n'
        )
        path.write_text(content, encoding="utf-8")
        return path

    def _launch_editor(self, proj_path: Path, series: str):
        """EditorWindow'u aynı process içinde yeni pencere olarak açar.
        EXE derlemesiyle tam uyumlu — subprocess veya dosya yolu gerektirmez."""
        win = EditorWindow(Path(proj_path).resolve(), series)
        win.show()
        # Referansı sakla: GC tarafından silinmesin
        if not hasattr(self, '_editor_windows'):
            self._editor_windows = []
        self._editor_windows.append(win)
        # Pencere kapanınca listeden çıkar
        win.destroyed.connect(
            lambda obj=win: self._editor_windows.remove(obj)
            if obj in self._editor_windows else None
        )

    def _open_settings(self):
        dlg = SettingsDialog(self._settings, self._lang, self)
        if dlg.exec() == QDialog.Accepted:
            new_s = dlg.result_settings()
            self._settings = new_s
            # Pencereyi yeniden inşa et (tema/dil değişimi)
            global T, _DARK, _LANG, BG, SIDEBAR, PANEL, PHOVER, BORDER, BLIT
            global ACCENT, TPRI, TSEC, TDIM, TTITLE, CANVAS, GRID
            T = Theme(dark=(new_s["theme"] == "dark"))
            _DARK = (new_s["theme"] == "dark")
            _LANG = new_s["lang"]
            # Editor renk globallerini güncelle
            if _DARK:
                BG=QColor("#1e1e1e"); SIDEBAR=QColor("#252526")
                PANEL=QColor("#2d2d2d"); PHOVER=QColor("#333333")
                BORDER=QColor("#3c3c3c"); BLIT=QColor("#505050")
                ACCENT=QColor("#0078d4"); TPRI=QColor("#cccccc")
                TSEC=QColor("#888888"); TDIM=QColor("#555555")
                TTITLE=QColor("#ffffff")
                CANVAS=QColor("#161616"); GRID=QColor(255,255,255,7)
            else:
                BG=QColor("#f3f3f3"); SIDEBAR=QColor("#e8e8e8")
                PANEL=QColor("#ffffff"); PHOVER=QColor("#ddeeff")
                BORDER=QColor("#d0d0d0"); BLIT=QColor("#aaaaaa")
                ACCENT=QColor("#0067b8"); TPRI=QColor("#1e1e1e")
                TSEC=QColor("#555555"); TDIM=QColor("#aaaaaa")
                TTITLE=QColor("#000000")
                CANVAS=QColor("#ececec"); GRID=QColor(0,0,0,12)
            # QPalette güncelle
            _apply_palette(QApplication.instance())
            self._lang = new_s["lang"]
            # Merkez widget'ı sıfırla
            self._build_ui()





# ── OpenGL ───────────────────────────────────────────────────
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtOpenGL import QOpenGLShaderProgram, QOpenGLShader, QOpenGLBuffer, QOpenGLVertexArrayObject
try:
    from OpenGL import GL as gl
    import numpy as np
    _HAS_OPENGL = True
except ImportError:
    _HAS_OPENGL = False
    print("[UYARI] PyOpenGL veya numpy bulunamadı.")
    print("  pip install PyOpenGL numpy")
    print("  OpenGL desteği olmadan devam ediliyor (yavaş mod).")
    class _DummyGL:
        def __getattr__(self, name): return lambda *a, **k: None
    gl = _DummyGL()
    try:
        import numpy as np
    except ImportError:
        np = None

_FACE_BOLT_B64 = (
    "eNqsnQlcTc///09Cki0h2bKHEJKl252Za4uS0CdR99pSIfSxU8i+7zvZ932NpO7MIXuSfY/skqRIFPU/c2/383sf3b4+n8fj/3k8"
    "vo/HfL1ez14zc2bmzDl3ugnC/9//5rYRhAbNPNjNqjZM+r/Tz9bphBPaacRKY6upFlq1w/HN++nKhn8P8a6mkhECVCBhKOuJYc08"
    "8PiqNphnxCMVef7uJ+OKz5P2pHy1FF3Z8O+clhECVCBhKOsJ/rP1/5uOff2VOPekWpdurIb6Wv3ff9Nx6e+OeMU9vZJTugaOGacn"
    "zprWxU4X1EYIqFTbboe9BuvL8CcVnQGJJtebYZu2IGO6MQK6im4HVCDxOLM1Pueu/gMBXbAP5UTHmPYkNbWmWNLsKzk6UUHMnlTX"
    "ldljF+K42EZXlrcDKpA4+bMX8Wz2nf1DCMYI6FrmiEnY6UpiYeJxFVvtgHtYp7QZas78Syn15V6BbFHQGCNEUplFOOltkE5Juj8d"
    "t30ZqCsfsBiGUw6OMkJABRKPHUZhq7IBcmL67wR0ZX3eiso+G2+sHcDlW1+NX4wd/AcCKpAILdEdt2804A8EdPkShEcSPyPtgL0I"
    "eze/OmUX7wQZyYAKJHK3zGTpOa2NZEACulSTiokRO32MZEAFEn4mWqZ8a2ckAxLQFdawkvjujbuRDKhAwt0lk2G7KkYyIAFdp9q1"
    "EvPbtDKSARVIXB5eQbRyEYxkQAK6Nr9zFy/WNzY/oAIJ03P1xC/TE1jhDEhAl8eKgeKyR6+NzFqoQGLkulaixZ3VRjIgAV3zT4aI"
    "9S5HGMmACiTWzHYR5xZrYSQDEtD15tMk8b62ppGMmuf247Ep+jmovLIV3xoa9B9WBkjcG7cG16k09A8EdMFVSU7A2fnGIQE9eaEs"
    "emWY/vs8hwRcK4teGaArZtg6ams70UgGVGRr8O/r7j93Z9jv8Hq0Np8iNlY7RReuFVQg8UWlEh8kdaaF7ziQgC6e7by3Ji6cARVI"
    "PDhMxNXpm1DhDEhAFx9vCTER2PjYNSiQGHDdWayGuuPCGZCALj5vlDdeY+Nz0KBAwvuyg5jUfIeRDEhAF5//1W0rEeNriUGBhFma"
    "rThHfGQkAxLQxdcxn5atiPE10aBAovoRC3HZrhKkcAYkoIuvx4pkd2J8bTcokHje+h3ziaxmJAMS0JX/9DVLXzDQSAZUIKE4e4xl"
    "T7Y3kgEJ6Fp3LYLZHQoxkgEVSLx9Npw5TGtrJAMS0HX6Qk02790kIxlQgYT7uyf0YDAykgEJ6Co3ckX0HZMpRjKgAon1Exq7LGtI"
    "/kBAl9u2mljWjn9qNWBVT9LkSW/dWLoT14c4n6qkK8+bHEKafJ9mZEYlXvQnc+Ku6pSOc3uT/Gtmup97x7I1uff9khEC/iyYkeg7"
    "nkTmXUWFCf+alYhhXF289hobrr93moifuzcy0g6Y7pOmJLt9D+kzQG2Lbgck5h3vQtYMWP4HArqK7iuoQMJC3YNUaxD4BwK64HWS"
    "E7BHyx/zI5HzD6D/3btQgcQivwGkd9ndyv9NQJdjl/HEurQfLUxABRKpFweRqBOtjRBQuawaTNQTZ9J/nwGJ6tX9SWBDM/a/Cehy"
    "cAkhVXb0NEJABRK5+weTS6+7s8IjsbSLKx57q71ujDb5MhFbBbbRlQPOROBC69X03wnoCo3pjD1T2hsZ7fDn7m4xEwcFOhWdoSOg"
    "Aol7D1bi5xNa/YGALjgf5QRUIOH9Yzs2nejwBwK6ip7nW4cXJ4odlvq7TIXyZJGlua4c4dCKGL9z7tyjISfn79VdqYgZvqSeT4yu"
    "bD/InywKP2HkCsKV81TvhcjaAxtfRf/JgAokNuaUxKn2yj8Q0PXvriAkNjp1xLkVnP9EAFfR4wr2+5piz3HEO1tdGa7HRa/UkDh1"
    "+j1um1zjDwR0FX0FoQKJdyNNydZBFf9AQBccPb/tMsBYwl8sSdu1Jf9DrSCRWteF2O61M0JABRKJ42sTp5KZ+H8T0AXvu7+9jQIK"
    "JA7WaUzW1E3G/5uArkL38+nGZhScRbnpGjJ2wm4jqyhcLeNLDCIWH+b9h3UXEn7FB5LE16v+QEBXoXn+DwEVSGxN6E9eXd3yBwK6"
    "im45fEMH39xdjiRk/5LyRp45oQKJkFcdSMrL0n8goCuuvIqkjyprhHjwuhdZp32l+7k+nh4kO+MrM/oG8p9rDlfOVZX7kedWcf+h"
    "dyHhs8yHRFy79gcCuop+LwoVSARd700iKiYbefsBCeiCPSLPgP1zp787idqR+x9qBYmIk24k/PmvPxDQJb/miU09WEcbG5YYdrUN"
    "fPtxL/o2GpSIxCqLy6qcLt1ER8OQ+LZ1WZUgjG7mwYZXtWGdyieegkrAuhvIshYS+xwuo5K/5YyVMjRSxqriX2QZkDC8O9l+1ULK"
    "6CZlbCv4/MPYOxnugm9bBKGSRLwt+IzFQGRPrKTy7d0KO6p8xDVxVr/VylUidkjEgmqzIqECicczzHD6+67iYaWlVKuPEnHR2ob5"
    "fFl2GhLQNXyCCR77sot48kEFiagnEbeljOBaB52g4uTwFbkO7yR+blvht1r5SMQSibiadllWK0g4Nf6IWlbsKFaPLy9l5Em9ayr1"
    "7n6lo6x3oWu8+Ab55KtEcQgnzkgZpaUMq3GLTkNlvPYJyu5FxHYR5X6rVReJ2CUR+GVxJ6hA4qJ4B4XkIjH8JB8lJs092H6pr2J2"
    "m0ZBArrgGBOEDs088P6Cz6PwL2diXe8ju+FfVWUo1/mUT76ktyFxXV6wmQutJaKGRDyViCsLVkZCBRL+A9uTsJvvWF4/QSL+kogV"
    "EvHD/dUJSEDXrIoOJL/ldbbpVjGJUEvEXIkovutDZMj1RsRuUAwrE1pCtXVZI2JLz7K/DpZQyWuV09QDm9vY4O7BuA1UIDGvfCMS"
    "HxjNnOuXlIg7UsY7axvssHnnaUhAV/wHO+JTPJp9686JqVLGMSmjR8yJtpAIs7Yj7xJOM7erFVSOte2I15vT7FJzPnbfS0RdiXhr"
    "9dIJttD6RTMyIP8Ku1/H9Ld2DJdqNVZq+WrfjqegAomgbHty51kci71oKhHrJKKtREw//1FGQJf7gyZk3WOROamKS0S8RGRILQ9P"
    "7XUaKumOTUhUfcY2rir+W63qS8QtKcPmwk0nqECifEojcudwDFMMKSERx+w98IVqNtg5bbCsr6ALXllB6NzcA/eQatXNzDoK9vur"
    "eDsy8fgZ5jqm5G+1KikROyRiXESy7ApCYtZcOzIvO4odvsuvYHOpHXFSO5oE3pe1A7o6drYjO7tGsR/eZhKxS7qCU6UreGHs5zZQ"
    "8XG0I+uqRrF2C8x+q9U+KaO2lDFo3zBZrSBhGDFVcSmVbvXBiwvmoLFxxV1wjAlCmRYe+GMlG7woovqZ5zWaEteOF1jV2pVloy/I"
    "XiqbRjG/wXwkdpDakS+14++vw9tCIrV4M9L2+CU2Z1jl38buKqlWLlKt4j3PnoYKJAxjmn2oLBG+ErFAIor1vnEKEtAl76uh0iip"
    "X90GT+zi1TZuYSNiffwsG+FmJau7dYdGxP1TNFtoYSURmY088N+1bLDF0x9toQKJ8kvsSHXzM2xN+4oSMcHBA5+qbIO7zouIghlW"
    "exqTWfu0rGXpSr/1VR2pHfeldigiNreBCiSsK9oTx0nnWJ+YShJBpd71lXr3pLVtW1ndgQv2unzPoF05H6/b2K3I0wn/nAP4Z+8T"
    "7qUiJm1L65Sjf6mIUzl9ed2z+mTZ9dJGCOiaeLADWeVtVjShf5MKFEjIzzMURRg721CYSO1Xm3ROaKsjDJ++//taQcLwubrszIT+"
    "PAPoxZzXbjjpub4Me73o6wGJHByOw+sFGMmQEcClibqBDy9vaSQDKjLi+0J88E2QkSsIW2h4Fvn3fQUJw1NG4XZAArrgeCs6I7uG"
    "NfGeXkVXhle26GsOCbs3ZQgzr/kHArrMXE1IQidPI30FFUgUfT0gAV0Xv2px5chBRjKgAgnDZ6yFexdeW8Mno/9+lEDC8Ens/yag"
    "S16roVvKMm0Hb91O33BywNn5nexEgvzkgEOPr7RhzkAdwT/HWbdsoBgYuIcYypyOK/uTveroq/t3QWj59jvNOD2AzV423xkqkIDZ"
    "ghC9Mon2uBpYKONOn0RW72xAIVoQnpeJof26j2IHTiUpoAKJsOXbWNq7UQW1Mk2Poz1njWCx0WedIQFd/DOkxOMhBRnBdTvQSX5h"
    "ulrxT36apU3SuQxl7hrlP5ClnhpfkNHdIoTW/TiJWfURFVCBhDyjSpv5VHVpgi4DEtBlKOszRu7aRiMrjtURUIGEvOW+l8vTSxOm"
    "FmqH+/0cerViaKEaCsIUiw1ah67hrEeP+QqoQOLw1qvakV/CCjKuHdmm3eUUznpF9pIR0MU/2Qozm1KQ8Sjlo7Jk12m6WvE3qYZa"
    "Gcrc1XnuWlTZy5DR8cg2ZWLrcFb9bZwCKpCQZ8xqaKNsejtclwEJ6DKU9Rkm7brHpuToCahAQt7yesUao3ZTpxRqx8ac5tjbsXCb"
    "BCHoqT8SV09mN1sWU0AFEt6h87HtpjEFGWcsQtAqaVyRq6tlBHTxN8X/N66WxlbAzo28dLWKOl2KTD3tpXPxN7d8bsOynmgxeTX6"
    "mj9ORxj7uYUz5p8+hE7m/a0joAKJsjXO4KMRww3z41McCpw5gu1vHa2ABHTxzxP+b553yL+FhNBhugyoGCP0GRPOl8Dbu/gWIqBL"
    "3vK4rPfo6Ut/JtwUXaACCWXKGzyoiyHj0q98lHpcw+yTSsoI6IK9Lu3bK1fH5Y+462oFr0FqjZok16KzkVr95d8Yx3zG7PaUGwqo"
    "QMLviwNpPKJ1QUajDg3xm/0dWL2wN86QgC7+xpufstJnWMV0w78iaupqNeuZO+Fno7jLUOYuq9Iq4m1StyDDZn8HHKpqyEZ9OKeA"
    "CiTkGW2pC570pakuAxLQZSjrMza+csQz6rfREVCBhLzl2d698CU/q0Lt2OrUk/TLKVuohoLw4W9fPGlKCfbr/QQFVCDh56khfpUy"
    "WMHY7eKLVedLsAO9BssI6HKcP5Dws1/6DNe3IXjqqROU1yrkQAjhJ7a4y1DmLtM2Q8nRG3EFGV1mjsCen+IotYlTQAUS8oxODYfi"
    "HgkPdBmQgC5DWZ8xLWwwHnH4k46ACiTkLfcuNw5/Xb6xUDsSE/4m79auLlRDQehbeRK2OzKFHhr22BkqkHgnTCRtrrkWZMz/OAnP"
    "k+6efaM3KiABXfFvJhF+ykqfoc4Iw3SNk65WxlyFifGvp+LptU11BFQgMYuFko93r9CCcdU6HJ+X7mx9zU8rIAFd1YUphJ/L0mdM"
    "kDJG1TZFunPhEsFPUxlqwssGevXeK+j/Ms5KdzYsZUAFEvKM+UfCcY59d6VutAMCugzlgt7VE1pOQAUS8pb7Sb37fI1ToXbwnl54"
    "0rVQm6RrXmkSrnd4CnpwgCmgAgl+/dcsWo31GdXSJmHbMiFoczczGQFdfCzw02L6DCyNdv+EB7pa8fHKz3gZxi4vG2aUJi4Oy2YU"
    "Cq2mn1EGBRLyDDdp1o46dQIZZpSBgC5DWTY/dLWCCiTkLS+Yg4XaweddCfOMQjUUhDxpvZo9pQQ2/a5RQAUSfO06+rUs0Wdgab1y"
    "lu6F1ZuMkRHQxdcxfoZNnzGyoTOur3XAhnXX8Mko/ATTUNYTBeuujjD2cwtnFNxxsGGlNiiQ4HeJg7l1DO3QuOJR62rjgPbFFZCA"
    "LnmtGkp3nGFfmuItHx6dhQokDO0r2FODlkMCuuSfItePnsYCUuK1g1peUgjRYeI6+266mbOx3WSxoVsV3VoiP/2ZKe2Omx3dpv31"
    "cKQzVCAhP79b7P14Fui7VLdeGU78chc8/dsUjRObx08qWEWnSHvENdIquiB7iwIqkJBnrIwJZYF7e+gyIAFdhrI+wyp/CjsRWENH"
    "QAUSsE2CMLPsGJZ0bE+hdgy4P0LcO+xQoRoKwrA3wWxb8iXa8+pkBVQgYVHJX6we9bggo7n0ZJct3Tkbrq4tI6BLfso7KeMv9ta6"
    "nG7PYDgXzl3wjHiJCj5i5RGmBbuMT519WSlpB3AsbacCKpCQZzwPGcAc3vzQtRwS0GUo6zPs/QOYh+crHQEVSMhbnrLeg32fV7VQ"
    "O56/7yp2bl61UA2l54/qndiuJfXZzfhfzlCBxIbz7USPkfYFLd8l7SozpF3fyY8jFZCALvnvAgwa0I713NhSVytjrsKEn5sDW7DS"
    "WfeJIlQg4Xmpoej43aWgVrFSjQKlmn3I2aSABHTJ32UcqlGblRNddRlQMUboM8D7EhkBXfJ3Ga++VGbLQz3Z6Sl3FVCBREwdK9Fv"
    "R/eCjA6vS7NkCx/W6fSNs5CALvkbloKnCd1vnxnO4hieIAzncvhzglfJzgUr3DNVQ7xU2rs/uT9HARVIyFe4JkMa48MZGLuy1c6Q"
    "gC6+Cw8PbE1k+3bdKgoVSMjX3b3SU2rjRl6F2sGfnR4c8ypUQ+lem5ePFpzQ4AEdXyigAgn+FBZFBhZkjJfugduke+GVqzvbQwK6"
    "5OfhCp5rdbUynL8yPP0azmLx50+ztcMLMhZKO4zj0k7jx4GNCqhAQp5R8Fyr6ytIQJehrM9wK5mCSn7x19UKKpCQt3yR9ET/Ln9c"
    "oXbwp/uJa8cUqqEgbH/ij9DqyTil+GoFVCDB31IcbDapICNY2r/ZSPs4zxkmCvnptv9zyc/cPalvo2x2O1xXK8NZZ8MbFsO5Z/6u"
    "JsQjrCCjqrQ7buIUjlM37FRABRLyjIJ3S9jw3sdAQJehrM9IMm2MGkydoqsVVORn/GDLC94UYcObIkM7+NuhuLTCNRSEXmU2aBd0"
    "Dce3nRsooAIJ/obNtmxoQcZg6dlju9TyHxf6yAjokp9vT3OaT10vTcCGt4OGaw5Px/P3jPjY+IKMBGm/MF56+sratE0BFUjIM3rU"
    "60BH+oVhwztLAwFdhrI+Y/LF8vTBhKnY8AbSoMjO08ta/mtlElVeDcSGN8KG0Q5/k4C/6w2LDCggtkh3//vSHJxaf6ECKpCQ/77B"
    "l7Ix9IzHKDwveqgzJKCLv0l1fTmqIKPkzm30c8WxulpBBRKw1wUhy+MrbZMzsFA7+HquQL6FaigIy1+VZtdL++BPy+8ooAIJfmc4"
    "ual7QcY4aU+yRVrhfEkdZ0hAl/w3RgrutbpaGX7HxHBHNqzU/J64KNOFyO61mN9roQIJeUbBvVaXAQnoMpT1GVFZlVlGqKe+d4EC"
    "CXnLw6RdRpuNLQu1g+84dgbZF6qhdA2qdWIhS+pLt7X5CqhAgu+DtjaqWpDxSNph1OrQEG8ZbCkjoEv+e0UFuz5k2MMZnu7gbyXx"
    "3WBwoCmR7SyxYWdpUCAhzyjYvWLDztJAQJehrM8ou8GDXZlXFRv2iQYFEvKWF+xFC7WD7z8vHnxcqE2CcFLatz9PvoRWnbVUQAUS"
    "fA/v3f9QwZOwIO3bb0p3T9Njg2UEdMl/+6zgiQUZnj8Mbybg767xJ5mFkZPw/z0VbbMIQecKnooMCiTkGfnvxrOJvkuR4anIQECX"
    "oSx7xkGGZxyDIvttN1nLbaTnKMvAGoXawZ+dQh2rFKqhIPQ+O40FfohXTpzbxBkqkODPoik3uxa8W1JLz5yXpbvnympLFbKfBVzy"
    "p9TtqeEsXXHdhddKphgh9BmcKO9yPZbfOSEhc4EnZEHoLjRiMxurdCPxyYY34laPoeT69e7EUNadpnRKEbeWHKwrF01Al6HM/116"
    "2k7pwFpnN9ARUIHERM+PogP1LcgoioAuQ1mf8XFSP/auvJmOgAokRt37JGZv7l2QURQBXYayPmNk02CW5XpNN0qgAolG0Z/F4Lvd"
    "CjKKIqDLUNZn/NwykW1MnaEjoAKJh+kZYuIqUpBRFAFdhrI+Y+aCaez6tse6d5ZQgcSSMZmihWXbgoyiCOgylPUZIy6EM/Xm5vwt"
    "53SoQMIXZYqzZjYryACEAAnoMpT1GUtcprHI7+k6YkjgA3Hs+cUidxnKv9NyAirGCH1GZNcwtmR3R/4OYDp0wbwJU+6LncetEPUZ"
    "gBAgAV2Gsj4jx2E0W7DjoC4DKpAo8fKumJC1piADEAIkoMtQ1meUjBzENm7K0GVABRLKbbdF12YbCzIAIUACugxlfYbh/C7PgAok"
    "Sl5IFNcW21KQAQgBEtBlKOszPC1bs97ZTroMqEDirOa6mDBge0EGIARIQJehrM/YmF6FhVzsof/OGqBA4vr0K+LRlrsKMgAhQAK6"
    "DGV9hm/SR9oka7AuAyqQ6N3xglhz6J6CDEAIkIAuQ7lgXLleoyOkFYgTla1eoT7jhXPcZSj/TssJqBgj9BntV+yhXyuO0bUDumDe"
    "gajKONzF5Jw+AxACJKDLUNZnVKrank69ojv7MR0qkBjeT4HtDhoyACFAAroMZX3GtmOmWttnurMG06ECCbd1g/B9asgAhAAJ6DKU"
    "9RkXv6cr+QqkO50AFEiMjJ+Fq080ZBRFQJehrM9oV30eqpWmP8MCFUho8Fq87J5QkFEUAV2Gsj7jgWMiWmszXEdABRJvtHvx1pj8"
    "gnFVFAFdhnJBX3mbY0+LvjoCKpAo8SoKX23yqyCjKAK6DGV9xvKqNthbWoF0e+o1b4ir11Cdy1D+nZYTUDFG6DOaCY3w5sYqWQZX"
    "YF6DlinEtczggoyiCOgylAv2PikdsCK7gY6ACiRS3T6SB3G+BRlFEdBlKOszqk/uhyPKm+kIqEDi+c1PZPPO3gUZRRHQZSjrMzya"
    "BuMFXa/p7jhQgURE5Gdi9bhbQUZRBHQZyvqM4lsnYk3qDB0BFUi4p2aQiRtIQUZRBHQZyvqM8AXT8JHtj3W7DKhAIn9kJjlVpW1B"
    "RlEEdBnK+oxhF8Jxu+3NdTsyqEAioX0maTa/WUFGUQR0Gcr6jKUu0/AeaQXia+KDQQ/IVrZYt1sylH+n5QRUjBH6jGNdw/DH3R11"
    "u1fognkpE++T0aNXFOzhiiKgy1DWZ5i1GI3xjoM6AiqQmJx0l/zIXFOQURQBXYayPkOIHISPbcrQEVCBxPGI22Rsk40FGUUR0GUo"
    "6zMGNvPA0wt+QwEqkJjMEsm5/M0FGUUR0GUo6zPqWLbG4dlOOgIqkGjW7zr5od5ekFEUAV2GcsG9Nr0KDr7YQ0dABRJ4yhXypPmu"
    "goyiCOgylPUZc5I+ItuswfrfqAIKJC6iC6RbwJ6CjKII6DKU9Rm/pCe7YGkF0p3L8HtF08by37Oajg3l32k5ARVjhD5jzPI9qIrV"
    "GP03FQIXzKv1tDKrrDBR6TOKIqDLUNZn1K7aHkm7JR0BFUhcmqpg2v2GjKII6DKU9Rm2J02VNZ/p39BDBRKnYwaxkVpDRlEEdBnK"
    "+oy32ena5S76TxqgAom9SbPY8fGGjKII6DKU9Rn9qs+j1dL07/ShAolVvdayBneFgoyiCOgylPUZ9q0T6Syb4ToCKpCofnMvu3om"
    "v2BcFUVAl6GszyjTx5zVteirI6ACCUVWFMuw+1WQURQBXYZywf1DerLrI61A8E0Rd8G3RvIMSEDFGFGw7oJT94oxt8kXMycxMHAu"
    "sRC2FJysksptN5MpibmUl+UEVEo820g+zQplvAx/UtEZkMjKWUtCep1l/5uALu26FSR1bpYRAipW5xeSVw2sxX9fK0j4LZpJ4s1a"
    "/YGArvQKY8jF+u5yQvebFk3vzxW3XqxPuFIlLUz0SUC68tUJt0X3Yk6kcMbbW31Yt5mvdIrr4cUspvRGXbkhqclyL236P+Kf383g"
    "6dVt3YmhVvWKtdKVO2+MItH5841kQAUSvBcUta3/QEAX7/U1YVnYeK0MfdJxp5qkuQz+D9cDEg7FO5MZlSf+gYCu0MN9sO2cV0YI"
    "qEAiPsSeaGNnGyGel6wlbrinb/mXXyaie4nlujK8TkVfQUjs/esqW3JpzR8I6ILXX967vL4p0bOJoR0Pyk/8D9ccErynO7Yd/AcC"
    "uuB4kxOwFx3sKpASmxf/l+sBiCXP3+Ll1qv+QECXssFB/KL6eiPEnS1R4vJiCwrVhPe0/9U1RmZtr9ubxf1PwhBXbpBNYhM/F/y/"
    "Zy1UIHGxzgbxV3oELpwB53PakZ9a76+b/8O4gkTnq7EoYdnmPxDQdW2UHx60McLIuILzma+7Nbucxf9+XEGCr/NuI0Px/yag69/f"
    "PwwEvxNV2pGL/jcBXfAOJyfgaOCztnap5boyHD2/fdsbUCDBV4yRD+f/YSRCV/zUduLK7tONjEQ4fhpOXS3ubvDwP4xESJzvv1Tc"
    "Wc38DwR0wXuXvFbwTvbxUJC4Lr0P+fe1goTGtpeY/WnEHwjo+nfzAxK8d7Xdpv+BgC645su/JxXOHL7iWNis/w+1ggRfu2IqrfoD"
    "AV3/bg5Cgq+oLTcu/tPdALjgfUVOwPWV90KbzRFFr+3Tf1+pIcFXoh0rN/9hbYcuvtrZZxsjoMJX1JtXN/2HOw4k+L12RdmNfyCg"
    "y+j9Q38fBPOZj8TNX0cYX0uMrgyQ4HMFZ/X5AwFdfG7m30ZGCKjwue0aX/8/1AoSfJXwrG3+BwK6+EqU3eKhkX07VPhq55Ubwf59"
    "rSDB77s3RruwwiMREtD17+/nBoLvDHzaTKH/m4AuuJeQ3T+Y4R4lCKENDGOMlw1zk5dlGQwqkDC07x9iujECugxrTOEMqEDC0D49"
    "8eVUDiqhTlJum6Jh8Ns711UfTlpn7EPTqn4nQanDSe83X5RTw7L5ia0fP1BYmTJo0V41gy5I2y0bSpy7m+Mxkd8l4lb1LFS7UVXU"
    "ZLaGQQUS8HtHBWG4dxa6frk22lNRTkBX6tIg8nhwXfxXPs+4Ni0D1Qoi6NZiNYMKJOTfejr67Wd0vZgS/fVGTkBXvYb+xK3MWHz2"
    "yw9+7tUyFYWW64tiPqgZVCAh/y7We8tSUOXmAQhNlRPQ5bBFQ5wmbMbBt3P4adw2r9H4u6PQWqxhUIGE/Dtll81+gSoET0Ouj9Uy"
    "Arr843xJzXuHsL1jLj8pm/AYlay2AMWU1zCoQAJ+h60gNPn2GLVOnocqtpET0HXZqw9R5p7Dj6J5xrqXpfCJ232061N8GPzGPfjd"
    "fU92BJKGlk7sq00WP5fxJAdVGecea9ZgAIMKJOTfxTo+Oh9tqmERO/GiRkZAl2f1oWTaUytWfgrP2PPSFKtyrru87eXHoAIJ+N2v"
    "gjCwRj5SVNjoUuq9RkZAV3Dn4UT9ci1d7/FNIr53MMFzFrgqczerGVQgIf/e2m5nTfHhJjOV0975ygjoks/BUqYC3q1ZqxSlsQsV"
    "SMi/fzftey6yefda2bKYRkZAF5yPUjtKf1Zmf8qhy2tp2KkmC9DORu7iyfgKqjWXt6PUV0Fi/I9Kqv7OnRWJxbuLJ334NwJ1V2cq"
    "r67LoU2aaRhUILHAoTcKvztc7NiQfwNN7boqVCIxnXb9rmbwu9ucn3bC3t00Yuy9SqqFmRgnvlCLs0/zb7k504qgHpnpVMyVE9AF"
    "v8dNWuU0CLmN/UyrZEoEUCBx7WNbvC5ILaKFPMOylAsKS/hMp/+QE9CV8601fu6uFodM4cTJOc5oV+Zn+sBUw6BS+ksLvLWtWrQa"
    "8XutVt1ph87/+EyPVdXIMiCxMKwZfiCVZw3kGeUrKlCQTQZ9kvFbO4BL/q112+a0QfkNM2lxaZRABRIL2zbCk/3UYp4Xz5ghtEb0"
    "QCbNevEbAVwHvOvhg3vV4qIenCg2qxW68CmTbn6pZlB5vKEuto5Si249fq9VdNlWqKXpF/rhpTwDEgtN6+L2F9Ria12G4nULZNrm"
    "C3326rdaAdfC9zVxfGuNuKgnJ3ZZO6BpoV9oxjs1g4rhrw/97fV7rRYVr4PuBmbRchYaWQYkvOu/QNE//cWEWJ7hWLU2yvPLoteq"
    "ygnogvNGED7Mq4Aazf9O50u9CxVIeM+5iKIvBoifHvKMz73N0LB7P2hS8m8EcMHZJQivz91FiSGr0eVINYMrMlypvdZ5kqT1SXjD"
    "iJ/SPLf4dQO199yAZiMNgwok5N/e6rM4Ac3qvAkllJcT0PUuwoNU/vwaR27iGU+9LqD7Rw6gDOk+CBVIyL9TtrnZRfTBZS86nycn"
    "oGtriorYhZcgzzby9+QrzsSghW+Po4DPagYVSLya2oiMt3qJcRWeoaoShd4OikLDrskJ6DrZph1xjKpIEvvk8e9I2XYC3UuLRin2"
    "GgYVSBw9Uosom/7CDb7yjND8g2jukXNIeVstI6Br0fGWZNa2auRlAs+IxDvQ9qNXUK1qGgYVSFgftyLugRak+0N+V6u0dwfaWfYK"
    "umsvJ6DLdrI92bqiDsl25p9uODZaj/KCbqNXO9QMKpB4ItiS4J/NSPsS/DMXy2HL0dhV95CJtLZDBRLLIswI87Imk0V+H/xLGlGv"
    "o5PR9J5qGQFdz+1Kk+BGmLjt5hkbXKei6cdfIK00z6ECCW3lLPxcUZe4H+D3wZfN+qPm+Smo5205AV0Bg3/iMI0ryc/hGZnZ3siW"
    "fkB/1dEwqEBC2+ERrmfSlPRZxXeWB1I6opiSn1HuObWcAK5f1d5hvxsepGQn/hmY0twBnd2SiSo20DCoQCLAIhbbL25NWk7mO8sW"
    "3rXQgNnfUb6bWkZA15JeUfjg8X5k6DOekXbPDD0+/x11bKxhUIFE2nlpJ3hdQVb34zvL0MjrytsV81FPaQ5CArruLZ+DQ84NJlXH"
    "82/A3DXlvDJ6bR6qfUnNoAKJal2mYj+tipxszXd9D1cEKWePFnDGdzkBXb7Jftg1L4AUj+UZt2p4KWepBNxdagdUIBF63gVnj+hC"
    "BlTma8nh3S9dpoSb4C1RahkBXdXy6+JV5sOIrSX/dkrFaAuXqU8F3L6lhkEFEmsSvqJ517qREbk8g/VdFFtxZDF8TKmWEdC1f+cA"
    "lNpvBFl/jGeMsbXQrrkj4ICyGgYVSFwd6YfuXHInS17z9arm0jla8ZCA/zqilhHQ5TvWXxv2dASZUZV/Z2aJ5RHavaWkPW9tqa+A"
    "AonHT3trD/brTvrd4GvJ3c1MG7k+D61LVMsI6Ipy70mPrh9BRvfkGdM/fNIO8MhFO0ppGFQgkZq/nQbPdCcBp/last00Rfutbi5K"
    "biYnoCviYDRNfxlM5i/mGScHVaBbXH+gOofVDCqQ6PK0Fgu5NoysSONEkxm2tG+NLKSSriBUIPH2vRVLdO1GGnnweX5ZcKHvczPR"
    "04FqGQFdMYpZzMxyCGkwh3/3586bnemhqE9oh4mGQQUSo7A3Y1GdSUYMz6hdK4CmNH+P/J+oZQR0KSptY/NmDyCznvAMv23B9Gmv"
    "N0gh9RVUIHFy8UKWep+Q5k34PI/NCKfN3F+gyOtqGQFdQStPsUVj/Ui5Wvz7RUPLLaAvJz1GwQ2lnT5QIJH7bD8LinAm2gieMbz4"
    "Aroz7DFyt5MT0NXW/wLLdetLKnrwDA/FWpr8+g5y3KRmUIGEXZO37GiaJykWy4nODSPo0V8JyKSR9EQPFEg8wVeYQ1lHMrc8Xxls"
    "dx+gVp8voJ9qtYyALlastGi3T0XM1fx7Ul8tOERnu59D6VJfQUVG+L5hyxRNSP/ZPCPhdDRt3D0SrU2WE9DFtlYSw6LbkyEHeEaP"
    "QTE0oedx9FOag1CBRMDfghjnUpuU/8Ez2j2Mo+1LHECNz6plBHS9q2UrHn3XgpTK5Rn76l+llb22o1tNNAwqkEjqXFbEzSqTISP4"
    "6lPZ4zbd7roRvZLuH5CArurmrcRXpWqRr2v4972+Db9HqyctR6L0dAcVSJhXsBEjmpsTxySeYRXwjF4Mm4O+SOsuJKArZb5SvNOo"
    "Amn9k2fsKpdMRxUPRz2aaxhUIGEeU0/sHPcdP3fj8/zvlm+oNuxvlCHtkGUEcD1a2kFc5GdOZjQ1l4gn3h9ocrl+6HoZDYMKJLYP"
    "aCbu7pOEl53lGaYtU6ibpx/a1UZOQNey013FdR0F8jqYZ9w78ZkmnFehOcfVDCqQOH6jp3hv5Btc9gonhvXMpO02OKAgRw2DCiSa"
    "pTmJlZuKuGEzvjLcevmDepergtZ0UssI6EqYqhaVdyKxV1Bpieg6/wd9tqIkKintkKECCRtXpdh5/nY8czvP6Nk2j26cfV3ZTysn"
    "oCut6WBxpNdafOEyz3B8+otuZlHKRdJohwokDvfpKDaLnoFDqvB5PqCrwKZ4r1T2u6KWEdC1tm+AqLkxA3cy49/4/nOCwBpWcFWO"
    "qqxhUIHEG4uuYk7DDjh6Ic/o5CGwy8U9lG0ayQnoMt8RJOZkDcTlXHhG8hETtudUrMvpXWoGFUjYtQ0WP9Bq+OouTtx5JTA3MUcR"
    "Kq3UUIHED427GEnzUbNfvFZdKxdjS4LPxr4aqpYR0LW0/Chxf1gn9MmljESMszRh1meLaYM/qRlUILHZ3UNMaTse7R/BVwbpfste"
    "7pyr9f8gJ6DLVzNKPFP8aqy4iGdk18mnwo9V2gbSHIQKJGY89hDPzDwQG/yYZwxbk0fruJ7XKi+rZQR0ZaSNFNetGULb3OMZz01z"
    "aafdH7QJDhoGFUiMNfcQ1bVW0KHufGXw9cmlPe6WoVVd1DICur5eGC4ufVGP3RzDvyP+Q88smhZrS3/ZahhUIDHvlps46oIFe0x5"
    "xpK3GXRrkJK+36CWEdDltydQRK1CWOprnjHpSBo9vKEr/SCNdqhA4nIrV7EP6cHWOvJ5jjqn0vmBfensB2oZAV14xRDRbMZcdqli"
    "OYkQ67+hW+6E0L3SUypUIMFadxA77pvHAvfxjKz+b+hsq2DqKK0lkICuO08HigrPzSymH8+YUDGZml+fSXueUDOoQCJ6pJ84yyWa"
    "CSc4MZo9ot2KL6QfpdEOFUgo3ipE0wZ7WZUafGUo1eEe/VB9LR3ooZYR0GW90lO845DC/vbgf3vAxPsGTWwVQcdaahhUIJGgbi1O"
    "dL3IQpfwDOfoi3Tipr00+YJaRkCXyaUuYue3xcTkQzyjY/NztEn0AbpMagdUIOF60l4Mi3/BFuXyjNvRMbRX5xPULEktI6DrIFaJ"
    "0Y9KizmveEbCqhO0Kj5Lu9fUMKhA4sHzOuLR5z/ZouF8LQnPPUFVE6LpglZyArrKDlaIqvUVxeTq/E1Rcs/91PH0BTrxoJpBBRLh"
    "fi3EgGW2omk4Jz7S7XTUwSt0n5QBFUh0fFZFbKy0EPc+5bW6e2ctjYi9S9v3UMsI6HK3rCnaDW4llq/F35ENvbecbul7n65KVTOo"
    "QMLqYmnR1c5ajOvJV4ZV1jPpmkrJNOS6nICudX9bihOfK8RiE3lG4uYw2tz5BV0hzUGoQCJocC7balFXPHyRZ5yZNpzmOb+jZaXn"
    "c0hAV3yUmdj2YwfRivKMvZO96ckXH+hsaS2BCiRMFz5n7Lq92NyZrwybunahcf4Z9A5Rywjoihr/gh1O6il+9ePf+H59UnN69Hgm"
    "NZH21FCBhH+P80zj1VqsfJhneO0qT0MdcqjzWLWMgK7sRseZv4laPPuVZ7wYUoruv/WDDpFWH6hA4nKxXcx8mUJ0rsnn+arz17Q5"
    "s37RAdlyArpWhW9gCT0HirVd+HvqpflUe8X7F50p3T+gAomxz2ezJWEqMX4hzwhQLtc20kh3aOl6QAK65q6cyoL7DRGDF/OM1PY9"
    "tV8dBNZG2pFBBRKXHLux/Q27iE1zeUajGo9ix/YoxipJ1wMS0JU3qRJb9WyYuKMxfy96vkSJWJ+yJiy3koZBBRI3bpdk4eHdROdR"
    "fJ6Pzo51qbnHhCXuV8sI6FLc20DNXwWLdVfzjMzHZZWLjwjMuY70dAcUSFgsmEvfTXAXE17q1qsj3sqJ9wR24aZaRkCXdXw92mvw"
    "CHHGVZ4RuHyTst+wfJosPaVCBRLyT2V2p65RHqmQT182kxPQ5eCUo5g3b4RYypx/KuM664pyTkgefRqjZlCBhPxznOaLRGXMt4/0"
    "5Z5BMgK6zLElWuU+QoxXcOLQmR8oMvOXFreT1is3L3Jw7Rm2dXU1VVyNXiQkO4aFeFdTdSytICcPRrA7O6tIxLVf2Wjh6eL06TQN"
    "g64H23qSuDXMCPFu/Tc0+W4pqj6rYVCBBFvmTnzqXmWqmzb8juObi3oPztd2lloOCegKa9qa7B0TzUY68ozA0Fw050u6tq80o2A7"
    "IH3Q0Zdkmx5l0YHVJYKVF/ASlyPapuvVDCqQeH6ckDanJ7PllfhfqKh9IB8VP3hMO+mEnIAur9eDiPWvGWzLF55x9IaAU8Y5aRdl"
    "qBlUIJFeuTMpGeHMls/mGQ+7CLj5wS7a2JYaGQFd7jFDSK0Rfdkbpxp8f/VXMaxYfSHmkbe0tgNFRjh0JT+7ZVExk2fUsRJwevCe"
    "2KYbNDICuh6wILJ0fQ1WbhnPCIgthm13FVcezfBjUIGE569upO3NYbRW/6oSMcTcBL+ce9SlfymNjIAuhwPDic/BXrRfg5p8Fx4m"
    "4PIzJikvJEujHSiQsB3oRj4d/ap9sIhn2K0QsFWvWcorcXICujqWCiZdE++4uE7mGRO+5SER7VGeL6lh0OU3x4103Rztknn5d2J1"
    "5TwU+Pid8q2vNBKBIiMudSN/4SXoZms+djNic1CTHVT54KNGRkCX4uhw0hj3Qq1jeMYh+5+oUkJNdLmLH4MKJNZFu5Jq481wiV08"
    "4+mDbDR6XSmk9dfICOiyjQsi1yJq4kF9avH3V30y0Po+ndGPXmoGFUik9+9EmhxyxbMr8b8LkG6SgYp/IajXXjkBXQ+SBxEPOhNb"
    "fuUZY6a8RZ5rh6Ou0miHCiT8YjHx6D0Lt5/DM6afeYuc0wJQtvTEAgno2juvP9ndbD1e2sZWIu6veoYmPJ6H5nmqGVQg4fmsPUl6"
    "sR2Xz+IZmi3PEOo3DU1bp5ER0PXOth9Jy43E3VfwjHF77qLULhtQl3d+DCqQqP6gFUlyYThrMJ/nqWfvonJHV6Jh0t0AEtDlc9KD"
    "/Nr4Gte2ry0Rdc9dRGuP7kWhTM2gAgl32oRcrPsEpybwjMxHl1DynJ2oVleNjICudy27kDk/fmESzjOcG0ajfk5RKDxAzaACicvr"
    "65CADVm4WDs+z29diEG7Hx5CP9M0MgK62j7DZN6YUiSa8Yy9AYeQouQV1MjLj0EFEjHe1uTOYDPSZjfP+KU+gj69iUULhmhkBHQt"
    "W+RAvKrUJC986vBPXyPXozbKO2i9j5pBBRLZJcsQ3NKK7KjEZ1SP+RuQp88tJO6RE9AV86gGWffFgfh85Rn50+ag4IlJyP6LmkEF"
    "Elnz83GEdS3SZg7PCHo5F8UdeoJ2SWMXEtDlN7ASeefSlixqU5e/YZk2DB1pk4LU3aWnVKBAYk2fN3jdDzvyPItntLw0Bh168AL9"
    "vVYjI6ArvGopYr+HEKeVPKPc5h7o/cp05NRZug8CBRJpAY/wnSx7ktOQz9qrfTxRy1bpaNVfcgK6fvV9hbcm9SDhzetJxGHLSO1y"
    "BxPsmeTHou4Vo4x0JzMC66gaX/gL2QeMINNWNlCl7DRF6TW7k/dZfJSMdy2uFZPykUpqB1QgUfnXG1T+/XCyrk0D/kSf3kEbf9cE"
    "D5P6ChLQ5bTiAsrd70Y6zOEZLSb0iRnwQsBnWmgYVCDRJKkWrtd+GGmcVV8iBk1Pi6mhMsFKac8ACejyvVIX56e4kt2VecbiCzWV"
    "NYNNcOd9agYVSCQ9m4nnNfInFfx4RiC2VH75YoIDB8oJ6BqeMAi7p3Qktfbx1Sfrg6g8P+UnehKgYVCBRJZlJFYM9iV/XeLXI9dj"
    "p7JDz2K4eZCfjICuX/7LsFk0IvuVPCOalESnR35Dy55rGFQg4VTmKvY85E3GzuYZR2I/KU8t/4XO+6tlBHTt/nEIP+/bjtS6w8fV"
    "qjV10T2fryimo4ZBBRK/jauONdCMXtnoyRm1jIAuj+ir+BVrQeYF6DK+tEP+0zNQ10w1gwok5KO9wX5TOvnzd3Srk4alVrhCx74a"
    "RPZbNlDlhp2i8dH+5LiygQqOaeke9Xe6tr/5T3RXejaAromDvWm9c8OJZ9rvhBe9qb0X8gs9fauWzQ9IWN+3o+6RI8hA24YScXP+"
    "Wm38kzw0TqGREdAF54og+Ob0oLUCM9GyyX6sR+JAFva5ExlyuK5qrUNN9m5XH2JWu76qXJO6zHVrV+LSka8MqXWtaNnETGSr7s+g"
    "AgnYI1I7vBpTi1XZqGoZtYyQ9VtyHE21ciff7vGWrx1RjFb2/oHattYwqEBC3ldrggJp35i7KGbLIGbx1wIWVlZFYk3rqcqnzGbh"
    "6zqQyuXqqWD7pF3GnJH0256PKL+6vOWQaJ7uww4ucSfTg/m4+ri9Ba2S8xYFNR4oI6AL9oIgtF+ejex6WNMlz9QMPnM8CXQjEXHx"
    "rOKp358/lgR9Q06eNemAT2oGFUjsfdiFOFS7zbr68j3c5fZZKG1cHTqyokZGQJf9ui7Ea9dt5vcXJ041/Ipq1mhANY4aBpVsh05k"
    "2aSHrGvd32vVZmQmehjamN6fKM+AxMmxHUn8+sdsQWWe0ar+N9TvdW365IG8HdAl/0t/g/2+oJJiCzrkiZpBl6tJB7Jq9HO22OR3"
    "YvSUTNR/TGua9F7NoAKJVadUJHtFMpubx3f6r2ZkoFn92tHUH3ICuuR/TbD759dov/sg6p+pYRNRB2J6pLiY0l7+1+vg38EThGlH"
    "MtGdwG50wRk/tjcRk3qP81jyahuVHVWS8h+/sqxiNqqYs5gcFT4wmx+8VruupKD2loPp+u1qBn+WWUUVCbcoIVavKuWBbEEoKd39"
    "V7z1pTcU8lpBIrs0IRbNBXHEPn493h77hp6Fd6U99/rKCOiS1+rt9x9o/HhXuv5yPwYVSFhJ+67yTvlswQaesfX2d9Tpiiu1sPaV"
    "EdAFe0QQpo7LQAfMnelnaYWD1+BVOiYxCe9Zse+/Xw9rz88oKQJTfmZb9vc5ASFvR/Ex6Si6U0c66YucgC74V2oF4ca2dLSmmyv1"
    "PqxmUIEEvJpSrU5QlLrqGG2xQo2flFYR+/vFxeunckmYo4qMb11STAnMJSy7I/lhU0ysuI2frJnhoNLGPEhH1o8HYdu3s9m89R3I"
    "xoiWKsPaNeFKS1Wt4t5sa0xn0qB/Synjy+ZfLju6muL52/2wX8sZ9OQDd3J5UAvVsxM1pb1pH1I1r7nqktaCPd/WjTx70YLvwjts"
    "jGUlBTxvhwZDBRKB2zSs3kw38mAXJx42XhV7s7kpVlz1kxHQJa9Vq+qDtBVO56NbfTQYKpBwD5rF4mp1JFUXc+LA6W5a8fAX1Dp+"
    "oIyALtgj0ppYtrpy8HwBL2uuwYrQEzS4xBByM72pyn3qKXpQuosm5zZVwR6RrscZS+XAEQJu2lkj6ysZseoKnXV/EOnUtZnuHMAJ"
    "l4VX8tDSXDkBXbDfBOFi2Yeoyt2ldP9dNV50wplM7LWZjRzcQBWT0IN4xTB2a34dVVg3L+Kw/gzr2YXfo4qvuo081q+hB0ppMHRB"
    "OvxFFzKv5A224jknQnNuoXq5a2irGhoMFUiUT3Uk70afZX995XecKOV1tM18G719TC0joMtuUSvif4KxasmcmPFoPxI7x1HhlRpv"
    "fVafLLpeWpyTUUfVcV9D4lfOXLz/rY6q7YuaJGhBHjv1it8H57aJRJYfo+n1R2oMFUhY+TuRqPeZbGY1fq+1HxSJzoXH0ONhcgK6"
    "Fr1sROyck5kwkNeq5r1zqPmmA3RPOQ2GCiTSS2AS9iOJ7SrHM0qlnUM9I/bTG85yArrkLf+49yqasXkH7X9TjaECiZDTHUi4x33W"
    "7he/Hk5BCajX8M009LWcgC75FTxaczd6M/QSPV9ZI+td2AuJitokrmp58c1rTlQTt6Bu9a5Q26caDBVZvy21JHe8yooVh/LrYfNi"
    "E1pZLpGW2KiWEdDlM68KyfpYRdx4n2eMtFuB3I7do8klNRgqkLCdY04slZXFZjV4RoUZy1FOzgM6dpVaRkCX4a9imr/gGbey56JH"
    "q57SR5lSXwEFEicfmpKAv6qJf7/nV7BE1Bw0z/U5vTpeTkCX9dfiZHxObXFyLs/ovngESm3xin7Zr8FQgUTN+BSsqtRQ7BPIM6KW"
    "jUSXGr+h06rICejSuqTh+C2NxDG6J/rB27qg7HYZdKOrGkMFEt4Xr2LzoS3E0a84EfC+PepR+hXdemKgjICui41v4ZibLUS33bq+"
    "ciqD8kM+UXRrAE4rvQ/Pa9ZeHDeojmoNO4UtlrcX95Sv81vGWmqHdnfKofZqPwwVSByOvIFnrGgp3tvICcfkVigtLYP2qa+REdAl"
    "r9WxpDvKdaG/6IsHalzWcg628iCixUvpmXPhfBy2uZu4aZqtCtZW2slkLFf69MygJcoNkrUDEpubbMLvxnQQM1X8SXji45LIfHc+"
    "7ePsJyOgC7ZJEJTWI5RpW/Lo5QgNXrilA44621ncE1hbNXzvVGxm7yF2qGKrgrUVhOCQjcreefk07qm8HZBImDsPv/vZTXwxlj/X"
    "rsjdo2y5Mp8u/q3l0AXbJAjrT3VwsT0tsC+dpN7tn4nWzOwmlvtgqzrbrT12/NVXPB5RUwVrKwgZH+oq73Q0YUtj1LJ2QMKtmRpP"
    "re8lWmr4M+fu3UOVZiif7hktbzl0wTZJT8KXm2hvpwnszTs17vbQCdV5N1T0bVBdFWByANk3CxTP76+umjNAi9LHuImZsZwIr7gk"
    "9tdIE3bijhpDBRKhzYvj8XSgGDGbv4drE7gzdvguE5ZyVE5AF+wRQVjapJJL42Im7H01eV9B4toPR+x+r594YBp/f1VOu9XFzT+P"
    "2tboLyOgC/abIKyMOI/anjpAWz9TY/+B7UnYzXcsr5/wz06vzqd8clLTlZj6fGMT8vmObG/AeRRZ/yCdId3PoQIJn7tKYtshi70P"
    "5qdxD3meR8fWHaSl4uQEdKVnKkn62SwW0o8TZ1udRw/JITp+nxpD5UESJuGO+ey+8Ou3WnmMOY9Wvz5ER4XKMyBx8Ccmubn5zP8t"
    "P+vcXXEOrW9xgJaQ9j6QgC75XrTMAIqWJR+h2h9qDBVIJLYkZNZpQQw5zTNOfNUiU3aUTnstJ6AL7oOl9SoyAW05v4XeWq3GnkFt"
    "iMOYY2y3i6lqZ5eWZOegC6zq52Iqecsnr7qEDiXtpqr38pZDwvAMt+kWP5npn3AendEcoDVfywnogmNBEBTlM5DVs9a0tasGu1/r"
    "Sro3uUMnfCuuipjUmbRJd2QVJxZXnTQJJM/CVaxEND8dffHaR5TVbghVHfPDUIHEl6GEfGs3ldlk8XOWE69+QIlVvOgaN42MgC7r"
    "/P7EL3Y1iwjTjZKXz9DQFvOo1luNoQKJtnvakziXHaz1GJ6xZNIztH7QZOoi7V4hAV2mal9i0f4Ie/uYn1Zv0P8BOm2/ltpf9sNQ"
    "gQS8ToLQd/tDFMkW0KvTNDICuh6U8SbWHy+x4wqekV/2JnrTbjPt2EONoQIJ+TXPsBRwau3WMS2l+3lu9yCS064RDv1govL37kb+"
    "mnscLXEuqXolDCNf878jN933rG0aVwxX69ZdO+qNH4YKJNoq3ciwsQ5o/Cd+arJifxP8tr+d9qE0ByEBXavyh5PbdZYqp5TlGbUW"
    "5SG25Jj2dAkNhgok7vR3I58+f9feG80z3l/7her336WdOlhOQNfOtOHkiCpZW+Y6H4mrX/1Es6xK0lrl1BgqkIAjVBCeVv+ONgU9"
    "0a7B/WUEdHnmDyNlvh+l6RN4RvHiP9CcT9WppoM0B4ECCflo/3rwJ6pf6bJyRQdpXPm0Iw0S9uH1WWYqHzUmTrPnYPNxZqqTn/zI"
    "1Jg9OPA9n4N36pjiw22HKScOkuYHUCAR5dqJNKnRDX/UnbP8fDwPrfq8QnnLSyMjoMv+mz/ZOCIQb+nKM0JGmuBT47NdtsSqMVQg"
    "YXG2E3n8QYVbZfAM9wgTPGjfMxfPfXICuuB4E4TYWwKe3WO04kx7+UiERLq6KxkX+AldHsUzWlY0xZ87PIl1jfeTEdAFR6XU8vI/"
    "0ZMZJdGaLmpZy8Ose5Fmdx7ghXOklQH0uiBUPvYJzejbGF2Z0l92PSAx64sbWdP7E/ZN5LO2z5YctOGaNSI//WQEdLlecSAeg67h"
    "9uP4Ocs9fT6i3hW7oToTNBgqkAiJ6khOJhYjzWrykRh9PB11ceqIykpPkJCArvhbDci9Tym4WjrPuHbuNTrhMwZppLszVCBx8I4j"
    "8atZldw8xTPujU9FrTcNR07b/GQEdB2tYUuUlX7i+s78nGXS0FcovUsourlfjaECiYkDqhH/Z6ZkzwhOBFS5hyr7LEdVemgwVCBh"
    "+ncd4hhpT1Z68Xk+OigJNVqyBAWc8pMR0LVzSlky66IlWZrGM9QVLqN3o7ej0M0aDBVIzPOqQty3OpHYgzyjwfEE1Pb2FnRzpVpG"
    "QFezjXnYfnIt4vQ3PwNp94Ci3l2PoPe/1BgqkAh7VIaYNVKSsC88I+JGLLIbeRRpHTUyArou5j7Hcdcbk9RMnvEyaRraMDsZNbXS"
    "4IAfi7Br3CDyOs5MpT26GS+6qSBXMyxUAcFabKvuS8Y042PXLnM9GnDxFjq2R42hAokG8xh+vsmR/BzLTzS2FFYhTeBttHSmRkZA"
    "l3LCYxzStRdpepPPqId/H0a7R1xAMz/5YahAQt6O/dabUfzmi+hFVH8ZAV1r3n/E6bbdybiVPGP542Oo7mSG3kpLGlQgIe/dH46l"
    "lZ+VJvhJoho372rJZvUaTk4pSqus7/rQnabdydnR5VTZTWzoutgRpNEWPkomnDqubKvIR20kAiqQuDPouDLGuTtpn85PG86bHqM8"
    "l5+Pno2XE9BVucMi5GMzgrjm8Tm4vVYp1PLDdxRUXYOhAgnv9hdQ0EE3EjyCZ2jvmaPewg/UpLicgK7xtfNQ6rThJGEfz9i0zQkt"
    "n/oFbZLGLlQg0SS5KY5Su5L8D/z0Z2hqfeSRnYGqJGpkBHQ5+7fAVkFDSbMBPCO0hS/a+OMTsor1w1CBxPDr0qrRrxMZtYFnLL7X"
    "HZ3+noau3VDLCOiCY1raw9mPRA2fvUEBn9Sy0Q6JD3PGY7tBHaR7C8+I+jYb1fuZjO7XkxPQBUe+IEyqWC526TsBH2yiwadfuLFF"
    "A7uQOiHlVaPcTNiT0m6kfWY5FRw9guD1bbXLvTkmOPiCfFxBIrXMJzpguBsRk/k5y+j5TZRVfIvh95ZyArrgGBMEx1Z7tJ2z8hA2"
    "0+B6tkeZRayafAm2UPWvGsAO7uxEFkeUV9Hek9myb0NI7h1eK6f7TbUeXwU866UaQwUSsH2C4Bxjp80rY4JLPpQT0NV/TDfmeSOI"
    "mC3lGUfVbWLNrE1w7bIaDBVIyPvqiD+m40d/QiYhGny0mplof6gjabi/jCq/5zk270Nr4hFdQWX6/TnLX9uL9DTnV1BxuQydtS8H"
    "DRulxlCBxBO3QyyuvDOZMoyfzAxsX4Y2eJODbg2WE9AF+1AQ4j3itfe3/0RV2sh7FxK2eAGztVQRzw+8r05qF2rfHCuGvUf7yQjo"
    "gj0tCIcnHaSujiJywBpcYhoRQ9qWIf1Dy6maxVYVyy8yJ8e3VFTNO+Qgeu6oTV6/4vP8pOdGmjf0Jhoo7a+gAomI71aibUQ54vE3"
    "P7mcd34j9bmXiPKvyQnouuzbQExsYE8OLOUZdPEiSoY9QgulPTVUILHZvqTI5lYnIZ/5Ke/xFkvo13oP0Nc+cgK6lk2oIca4OBJ1"
    "V56R2XA0LdHzPXItocZQgcRO10/Mv7kdcR7FM+r4T6CVTV+hH+YaGQFdcPQIwkHnDhSbZqBf0nMtVCCxzvYGw0EtSd9UPkoqpTel"
    "CzbmoQpP+skI6IJjTBBq27+nuUn90VZpF+5VtZvoW74FtgiprNLadRKHj5uMHdMqqZZ5DRGVl+bj1146wuwl7ThsLrLc64ehAomU"
    "mUrx4t/bcM/h/BzyqJPJ9PGPUDRR2vtAArrMqviJF6fF4K8n+biyn3SbHk/agGy91BgqkOiHncS0k+ex9Xt+Lrz519t0ZPZSdNC8"
    "v4yArjdbvcXNlndwvSCeoWh+jfpu24tanPPDUIFEyNmWYoPmiXh4FM/YGnqduo+MQF3Ha2QEdK0q4ymWOJyKbSrzjNrm52jH80fR"
    "6XZqDBVI1JtqL56q8go7DeUZdTecoxmrD6Pl8+QEdMGZJq0+XY/ToD4x6GN9+RyEhCagtjhxs0BcPvIZ1f/mPtqkx3WUUcpPRkAX"
    "nI+CsMI1n7a46qisvk2Db/ccKV53P049AiqqxsZ7iEeObtH2jqqiYrajROs+TWj9upw4eldgu2qfVY7O88NQgUQ30UO8ve+R0ncY"
    "PwfQIi+ftm60TxkZqZYR0HXo0Uhx2Omp6PxCPqPsH/+g1muLoTrSSg0VSGx26y629olHLT/xT/Wbev6goeezleZj5AR0pSePEMdt"
    "vYeOdecZwyd+o8FHW6EOb/wwVCAB5420b3fNpPvaV0Vubv1lBHSN3jBc3GjSGN/K4DNqb48M2qSYK2rgosZQgYR8Dv5VTmD9x/tp"
    "7yIN7qbqINYbNI/VGlFVNVHrKh651pn1TLFWNd4QINY6M40l9ufjauVTU6bAfWPvBfphqEBicg13sfnL4mznRP5p+JTFAnsS+D42"
    "v6NGRkCXyeBg8b5nZVaF8WvefI0JqzKvu0vZ82oMFUgkhruL3T2/0cRAnpF2xIRtPTbJxeaYnIAuON4EAY8VmGUbW+XLtvKRCImo"
    "cA8xuyembm/5uKpQqRgb479YqbrmJyOgC45KQbg7TWCna0VqN3dSy1r+5Yla9BxwgjnnWalgrwvCKyGLCuo8bf7c/rLrAQlNsI84"
    "yyyeNfDga+LlQIEV19zXvnjgJyOgq5+tQny39ACbm8YztOW+0omNbGl0uAZDBRKO/XuJ1jEvWaeNPCN+djZ9WLEq9XyklhHQ5T6h"
    "lbhOuM5eB/OzBi8qfaIOE9zp9CdqDBVI3AvoKKbeNxM/tOCjPdH6K11p05GOPeonI6DrHG4qnqybzM5H84yoFR/p2uS/6PRTagwV"
    "SPgFNhKPBqeyyLecUDsnU2s0hdaW7s5QgcTE563EuLgaomU8r5Wv53u6vd14OkbrJyOgS/Gohrh/cXFx/hB+6sUp7g61arWcjt6t"
    "wVCBhLZ7I9Hki50Y2oCPko2rHtN97xfTXbPVMgK6LieVFx8NqChuecMzsi5cp9fGbqZ/l5J2GUCBxOEUW/FJkoO4Q7cmzuwVTyeE"
    "bKEtWsoJ6ApbbyI2/llL9B7KT2CH/r2Seu64SyMtNXhR/TOs13pfcZyqqmrr0zg2OcVRfBZcQ5VY/z3D5TzF5L18Dt4pf5AOnB1H"
    "XTaoMVQgkTvyNdvs1ETM+cAz/NbtoiViLtBTSzUyArpGrjYRvQRXcas7z5jUmVKby5F06Q0/DBVIyNthGnaYxrWKokPO95cR0LX1"
    "QWnRRkvECHOeEctEen/EUZrQT42hAgl579av3UY786TA7goa2adLwy62RcM2uovnh9mq4CdbgvDh6TTtruUCa5Eg/8xLRryxRvfO"
    "uIt11fzzqH3OU7RpywS2/aacgK6GXc2UnjNHiKfG8VHypN0x7YslefSHtHuFCiSa9cjQ+mS4i33f8c/uync6rY2/m0fTktQyArqi"
    "agym2U4jxIm635uIe1+cXpiUQy2lPTVUIJHqfpfGz3ATpw/hGYs8zOmvbzm0cZicgK4jcfVYnQ7DxFfj+KzdU7MVTW2dSaOraTBU"
    "ILGlpBMz6+0qpr3kn6vNi2tFvdpk0u+WcgK68kr5ssTlgaJYj2dUP6z5f2ydeTwVX/z/ry0hkTUkIRSyZHfdc86lkhQtJCKVtKm0"
    "SRK3fS/tm/Z904aK686ZFpV2lZT2RSrtmzb5zSl9f+/5fL//nce8Xk+vmTMz55y5c+bgkr1rucB58RgqkLhyJ4vmTwjmOw9hGTdb"
    "dOf2yl9xqsoEEQFdxg5z6I3eSfyQ26zdNT2u4KI7VHO51/pjqEDCavRKuq4A8S4WLGOI7QTuXdUz7ndZvIiALnhvSiSlxfO438l3"
    "uf3f4kV3LSQevt9KlzVI+UEv2ZvRyq5ruW57hfvcSExAF7yDJZKIS++QxnnMVekl4H9fO7X+YCtPHxpCzvpG0ymWjv/zZdjBaPY2"
    "XDK+BqVMH8GNOh2PoQKJmAA5WaI7gYZXs9m48+Oeo405E7jlA8QEdP37Ku3Cefam+vWS+6i+70zunfAECRVIwBlJQq92+B5KuzSb"
    "s7UQE9AV8rkvsemeTw212XHEXqxChSYLOP+X8RgqkBDPplpysh75eW9WBU8UeoPGb5c6W9vLsWc34sf7cSP9nP7ny7CRc9ncjxGy"
    "n+hklDa3aUo8hgoklNZhZBHiuJpqNp86N/QnKjutzY2fICagC54nicRx4Uf0Y4wbZ9BRfAYhcVW3C5m0sD1VG8YyhgV9RC9xNPeh"
    "bX8RAV3wbEokZ4x+o17tC2UjhNr995VQwqe2cq+vcmJ5bCTea97+f76osuvLZjqpu6vhbxN9ZKFF8RgqkMg37kS6hXfHqY/bsVkW"
    "amq4p65MdvCymICuzT2SyY8LkVhXk2W07amGWz9wDzJ8LbTtQIHEhC+hxJJTw1UDWEb1DAnuabcwyD4hQURA178vxsafYLOQtNeq"
    "47DkZqoM9XgMFUj8NOlGRihjkf0DJzYCuCvB77+fLAmwSRAR0AWvHonkZIQEW87erhooPNFDBRJrJnYjbminqmYgy3jUXgN/W/dA"
    "9dQ4TkRAF7zGhDvqdS1aezMMdZqbgP99u1Rm6yivW+RJVumcwTUBzv/znZfHYnZHuW79jl47m6JbA+MxVCCxO9CPVG/Ow2Or27Mn"
    "Fo/viLMwQ/MniQnoglePRFLT7xd6QCpkoxzE1xUknDIQqVi8AHccwjL05Bp4Zs0KGdHoLyKgC15jEsms6RR1OXoAqdol4H9fCXX+"
    "7CQPP6xFpM0syCwT1//5ompYX1ZXthuuot/bcpHpkXgMFUiELtcj/bcak0P3XdjKLROuoF6KDYi7KiagKwQ7kZm/HEicGstAx26j"
    "0cGL0fdaofUBCiRcdrUkSU+0yJh4lhETVoGq4nLQpZEJIgK6/n0x9qGI3bX+9c9RlmU6uvS5P4YKJOp6tCX1fm9xnwfO7IvDzEeo"
    "3D4LEZ8EEQFd8OqRSM4PfoceVnRDoxfEi68rQKxIdyM7317B85NYRqpzPXq/1he1PR8rIqALXmPCCLlriOzBFwl+eiVeNBsXzpr9"
    "973J2Omsrlzid8jcZA2ovi4eQwUSjkf8ZCkR3cmkh+7sW7KozTLDZ7/RqDYJIgK6bkTtktWcGUU2tmUZlnvVUEv5L6Q+LB5DBRLJ"
    "GodQ/u9uZE08yygtui7z9/6GEuMGiAjo+vetzNLP7Min3nJER+N+oZZX4jBUIPGKqmP38WHkfguWYXhTH7U9WofWBCSICOj6981X"
    "QAzL+KUdhEa9/oAs9sdjqEAiLtsO174JJY+q2Dzkwnh/9FXvI/p2Q0xAV7eAWHzXaSh508DuwQ9ecejLrFeo09t4DBVIvMpKwQ2u"
    "IeRrf5bxcWAv9CbzFWqdkSAioOvfd2W2KpYxpM8MVDjyKbr1oj+GCiQuV63FfhVB5PMjNgP7bus0tHnQE/QgLEFEQNe/78qS27GM"
    "YwNXo+Ssm8h+XDyGCiQSqooxvedNSpJYxts2C9E+zQq02GmAiICu0ZvP4z5no8nDGtZHSY/tQPmfLqG3e4WnIqBAokJZitc88yR3"
    "AlhG8/C1KMH6KrqflCAioOvfd2VLl7IM8x556O7nU8goLB5DBRL3597FIZ1dSNOnrmwm4P39aEXkafRmqpiALti6SiQZ+4pRkO9R"
    "NM9C3O5C4s2YH9jGsQ2ZOJBl/Kq6iEoM9qGG6jgRAV2wDZZIej9NpyNKFJzWb6PChOWB/FDPCBqnoSlfMyuIz1b3oCkXNOSrhPIc"
    "ofx3VeBMjRg67IMuPn9yTaHqkgO/ePk5nOvWQCze2PA9+Dv49orfRFsozxbKf4kbU+NUCzwHYPPrv7i1k9oH5TgSwpTwGmFknoL+"
    "lKskripFe0Je+TFCNnCWii6fjHvQFA4qkKgjWVz4Dky61DFimPlybl7/NOx019gn4uFI6pTtR8KH1JGDR/rRmbf9SYVtHXn+YCR1"
    "F7b/3Ssv1yncEcvJ2HWRpgoqkFiy0ZEO+ywlvUaz1XStjvTn+qxJx61y9ThIQBfcQ6E3+OXNHXmXie2GziyBCiTulj7nvKSIOBew"
    "dYSdVt9RpczNxiv39Q2CBHSJj1zZvYrbtHQYPu3o5ystPkzrMlz+EHOF8lOhLHf/TvyCN9IVhh5k9J/VdA/VUm4hNwqbXpmtggR0"
    "ietKM4rn+m0eheNdFojqChIaarNpwxNvMuY2WxW44+JtXMrJ8XjN4bOFkIAueJ4kkig7M7o/LhKHUhufc941NLHAkixS/0kSKx/T"
    "NTtbEd/rP8hDYXuMsP3vXt2L0qdjUqNxTpVjCVQg4XTnIv35wp7sasHW383VbEKd9sbiyiODVJCALlgjQl978BfHbR+AN5ebl0AF"
    "EgvfFtDUZGeyvhdbR9ih4SUXnJ+EPxba+0ACuuC5kUgsznjRdSG++Mrma4VWB/X4nB1af4gPeXq8UigHlP8iiYFa/H61ZmROJJvL"
    "2WlSO+qykuBzlVoqSECXuK6yC9vTLvEYuyS4io4cEsdPfqUL95iQz8vYvL5ejtb0olk3/GDeah9IQBc8T0K769qbzm9vhKtDdhTA"
    "1sBrX2v+zcD7ePrE/7YMwb270/lSS6xlPVcJFUiYPzLjkxs+4BaUzU9MNutCl7yxxVdbN1NBArpgjUgkfVbJqZnCCd/balcCFUjU"
    "DW/OV55SJ1t0WMb72wHUxMAD+53q5Q0J6ILnRiIZszqRLiv/hr49UFfBNhHuoZOfK/+l4DB2ec1m6e3oMYA2zatHhpPzSqACiehz"
    "7vx9t22NddX8RjJNm/8YRZbO9IEEdCUI5UKh/MmDzR2MDh5Lb/Q+jNo3nCtJvBTIW6Luf1xFB3x5WfI0LDsmkYsz3BLG0LYHi5HN"
    "FZsSqECixV1PPu3NWvwpmmVcWjyCttldjj5JDX0gAV3ivTL1zableR9kTp09CyvzCP/53QY0S6Iu16vFfEH7a+jOdTU5275S2P53"
    "r8oGT6Um9i4o6JpTCVQgcf+EjB+5wArH/vkPuINWZtL73kFo142DIgK6YI1IJCY3JlNfbiy6Nc0nECqQwNsD+VdLI3CIGcs4bTeR"
    "LjZYjwpfhhZDArpgvUkk900VtNvXAzKVsr4AHjncw9GBcr69b2/k6MZmTS55p6BPHVYG6a3pVwIVSHySy/nK+50b/49Jn8sKyhdI"
    "ZF9zT4oI6Dq5T87L9mVKh89jGYfeZdC1ixO4dmlWhbDXrz0o43d9t6RW2/87AlgdOpU2vdqBsyq/o4QKJB7WYD5efoUbHcJmNOba"
    "ZdGB+ebcDIOlJZCALvFxnD6YTVsorqps35cVQQUS/aXCduPu3M9n7DiG3VXQ7nebqiwrSwIgAV3iI8e1E2h0VC4X69SxBI594B6G"
    "rvHlZ/pMo4okNqOxZ98JNOreJs7EZ0wJVCAxek1HXu/Gysa6ar1vDF3oXcQNeDLEGxLQNU4of7q+kl7OZxkDFbF0ppY27TV7bIHX"
    "SXs+cdpleneNlrz+igOf+uQs3TxVS64hbP8kbP+b4e2cSJ/e/cGFNx+vhAokPNu78n7Bh2lpGza7LaR0MP008Q3XzTetBBLQJT4O"
    "xw7DaPj7u5xp3s9iqEDiTqknv2bXWnr3FDuOtf1TqN6oMm5B4GlvSECX+Mi3ccFUy9mRfoyO7nhupCFvHCThGaEUyjZC+fGUJnLr"
    "d2Z8jucHerIjm9cXXRtOX5ZY0nut5CWQgC5xXSkcu9PdqZZ0uqOv6Mgh4XOyNX9j0j165BarqxWVUbQTbk5rp3X1gQR0wfMkkbw4"
    "0o6GLSE04lQT5f6krzRvigmf3lNbrm2pxRde1OPD3jeRhwd9pNjJjP+7V12T3WnxuEDaNK1PCVQgAY9PeP6Y4kN9crzpM692SqhA"
    "Qm9Acx5PUedvLGV1dexbEF2c70pTfIIKIAFdsKYlku9bJVSzbwKds6qs43E1FbV97sTv795Ubj/5Iu181J7vathU3l/YLhO2/92r"
    "dpubUfoimnYOa1ICFUhkjn5Myye14o8cZrP0stWb09U/o2gG8RAR0CWuq98nLCgq7E6LBn3JhwokkoTtPsL2z0ksI2VPG1ocGUrL"
    "lq0qgAR0wfMkkQyNK+fmrR9BH970Lfm5aQZ998P7D/EwYCPV49z5rxf+e+QV/D1O9+dQ+kRrihIqkMjJK6Bads786jFsDmS19kcu"
    "dM0g2qVK1wcS0AVrXRghc3IufGAm3XR2jrfbMB2a2lTGPzfWlffNdqT5W6V8xAMdue9wHZokbP+7V1tjJ3GfMibTIb5lSqhAIts9"
    "lnpl+vNbp7FZrLaPp3HjuXTqdc2uBBLQBWtEGO/WbuBcDk6ga7v5BkIFErtDZtO8Gd58KweWUdVFxfW6P5qmHxlUDAnogvUmkTTp"
    "ka/Cagoa1t2mpMrMRpVYgf8Qx7dmcJ5RmF+5Ufc/R/595R1V2qJsarcjR3TkkNBbVs3Fvpbx02VstuEsYsNtfDKVenfcXAAJ6IK1"
    "LpG02NEMvV+eRdn/+qt2v4zuPpbxW8v05IXNOVTfFvE9SvTk/7b/3aulkguyZD6bbl87vxgqkCib7IIyUjG/O4HNNnx3ZLHMfpCC"
    "fi39pIQEdMEaEa5dzW9BXx4raNOV949DRUSUWKlGC9ur6tlxONe2Uj27qqBmug/8IAFdsN4kkt5j3qCuVwfj7+c6F656lo/fVbcj"
    "U5WG8tkL92K/XBfSq9pQniWUpUJ5Yip7o1ggW4x0Wkz6U1dVlgSrhQfwSWFu8m7+cTg6xY9vtTFc/m+79cZQ9v784grU3CKNksIi"
    "JVQgEXenDw55/rcskawLiEXZNlPowfotQZCALp8TX5HUUMa3s2UZS+4moS0rMuhmj0tSqIiIqzWoLFHWmNHugzka6yyc87OPiiEB"
    "XdVcISoLRfyA513YfX7aCA3un0XVp6wuhAokkk8XokJh+9+MoqHlsnl7sunN1VN9IQFdYR59kDwY82FbWcZbg+0ybVcF3aPsGAQV"
    "SKxYmSNbVoIbMy7KNGRWwojpiZp9CSSg683OVaqyq5g3smEZLl33KVv+VtBOv49JoQIJP31rbv7efxna1X50tXlHuujHUWnsfWPe"
    "fM03yhTjpVp8RrweH2IdLD9E1fm6Ov1/Rz7dlbo6yqhLYc9iqEBCOkvCP/xqwJtGBrPf9Lc40ye3Ed1yfa4XJKBLJpTvC+W/GQUz"
    "7ems752oP//ICyqQiPz+js7VM+dbbGEZl3Vb0z6Dwui+jbpBkICuh00e0jcR1o0ZmvomdGhlT3p4IaeECiRCyq7T0mG2/HK7EIEI"
    "HtqMrjTsSw+80ZJCArq091+iHaLsGzP2dWpKvx/vR/svC/GCCiRChO1WwvbzQSxDdeEX93HTAJrviApFBHA9/VhAPxk4N2Z4Wf/i"
    "Wl0bQCcvtSuGCiRCv+TTh72cedPtLMPf5hZ3Yv5w2rO0fyAkoOvijOU0pd6zMSNv9C1uY/pwmnRscyBUIBFTu4IuK/DkJW06sXcs"
    "T45zE2rH0F4/7xdBArpCP8+lKVrejRnPFu3jyhLH0RVrrymhAomvW5PpnaV+vEsuyzDYt4yzS06jgTOHBEECusYs9aSZWtJ/LYPn"
    "NC7sdjp9dzdMCRVI/E5vR7fOkfLyZp3Z+/NLCZzP6wzqNnWCJySgq8vkdnTjnH8ZLXb05tLnTKFHtdS8oQKJORVtaMwbKR9tyTJo"
    "uDWX92UqTXkzXQoJ6Lp4YwuX//Ff61Pb1YYLfTyVbkMFUqhA4u6EAk7nKOLdN7CM2bcWq+SDFdTxW6ISEtAlbhk6fFmvsu+koIu0"
    "swqgAglzQ2tutrB95neWMdPybUnPZwr66trzQkhAl7i9CnHoT1tFaVITlbXUIaw9r/Gx+E/rY7DHkdczPEP3bCPytJV2fI1TOf27"
    "V1fyo2nPj81oTvBqJVQgkaFmzWvEP6aTreVs9GobSd1TzejJQ6elkICu0mbmvPuL940Zx33DafcjVjQgQaMQKpDYKGzPEbbrJrGM"
    "by06U+lQe/o+4a43JKALtq7COb8UQmNr29LZEenFUIHE448t+Hytenonl2V0TPani1d40qsHp4laauiCbbBE0mpJJl1YL0NOmlHe"
    "0YUy3vKqFR6/K0heVIP4wInquPxmkJwK5X0T1PHfvdo6JYvOijNAyZUTCqACiZOZhI/K3Y/MHWQCsQBnU+73W9nOF6ukkICu0s5y"
    "fm9aKPqb4ZmmoBu0Z8t6Xh2qhAokZFvl/I7EqbIfm1mG/IGC9gnTkF3ddCYQEtD151eD4nbSvxk3fymod6Bt0Fe+dQFU/hdR5SRd"
    "UcwyooQMrzAN1ZLOaj6QgC6Wbe4RzP3NKL+poDM2m6hGPE0rhgokzJ3lfMy0/tx0a8S+1CPZdFrDW9WIGcpASEAXq0NfO7XGq+RY"
    "x2xavuSj6pVFv0CoQALrY75735/csE0sY9y1THpgpD/nvXJsESSgK7YN4jc5GjVmnCdT6OziGM59aX8lVCAREyblmxwKofq2mPUG"
    "m9Lps/vTuSld1YIgAV30iR9v1m9cY8b4jROp/6/VXLijhRIqkDDN9+XNPBX0xHKWsaTDeBr8dSe3hHh7QwK6WghlJJT/ZgRUjaUb"
    "pudx4ZXfvKACifoaHx5LZtEz21mGZcIomr3rDHcj2EoKCejqsNuNd+q6qzHj7rcUumnOWc4mr18gVCAxu96N3/9wB61sS9iXeq5J"
    "tHfT19wQbFgMCeiCLZ9E8npEEi2xquV25M/yhgokXITt7z4U0xlZLGPKqQTa+XIDp399qRckoAu2j8LTtnCV/Brpj87GtCqGdy07"
    "m7qTjf+UYYshkUzfkk6rH0xHB6OaSqECCXaepuwd39iWOGtMpitOZSGToUtEBHRd7RbAO6sPwk/asox5wjl/9GUn6vvwRjFUIMHO"
    "U7R8WmPGkPYTaJXlFnRa7uANCegyFso9hPLAF1I2ImufSss2HkNPNB97QQUSFp28+Puy5Vh3GyPy4kdR+11nkM+GZVKoQIKd2fvv"
    "dzXu1UC94VSBb6PI48FKSEBXXb4Lf/nAUbzZhmWMMBlEjV9/QnmWXaVQgUSAcDbT1ivx7R+B7Hsc4bqKbvoaHWnl7QMVSLBroVDY"
    "/nevRkr70zPumrh3txbekIAufNyO35hcjntuZhnpQu/cNkoTZ1/57Q8VSLAedeO18saMsFY9aZapKY7VcSuCBHRlTWjJ79R/iwvs"
    "WEasXSR9lGqGR6/gAqECCdajVi/90Jjx1ror7brbBvf2MPSGBHSVCeX7Qrm5MctoY9SZ6gy1x+4/3nlBBRKsR72MvzdmHNhG6J71"
    "7fD9pt+LIQFdyz4342mkJum9O4CtsSU8R+0274jXhh+SQgUS7NmnT/fm5G/G4eGetGGJP7Ypf14MCegydpLwGhsNyWsnllEgPEfl"
    "3EZY3irjBFQgwZ59pOGGjRlO2Tb0GOqK43N2BEACutz7PaN3qRV5v9Of3bXNWlODpDBccqCJFCqQYM8+4dutGzP8UXPqdzsKjw/b"
    "UgwJ6NouPIv032NP3stYho/wHHXWsC/2e0d8oAIJ9uyzUNj+N8OkjSZ90Kk/1l7UwgsS0LUm/iz9tMSBNLNnGYeF56iaTQPwtFVb"
    "AqECCfbsEznEuTFDGveO29pjMB461lkJCejSprto5ssO5MMWP7aCmd8lbgQ/Eme22yaFCiSezlxOc3p1JKN6MWK48OSVP3843vB+"
    "kQ9UIMGeli4K2//u1eUFx7iwDqk4MGV4ISSgy+bNbJp5wpuE27KMM4+Pc8trx+D2Y8YXQQUS7GnpXKx3Y8aNe2u4O1Mm4ms/nAIh"
    "AV2/j3Slx98FkB07fQWiV94y7tnINJzcfLAUKpBgT0s3YqWNGbE9R3NntTPwecdHRZCArohJ7ajxXSlZlcIyuOsJXFVtBj5a1q0Q"
    "KpBgT0s/q/5lJMZgrjgrE9tnTsuHBHQdvKhBU9bJyID2LMNKePI692Uqtpk8VgoVSLCnJb1Q3Jjxue17VZk0Gw/R/lIMCeiqXDSR"
    "G3YQk9C9Puy6ur1YlTtYgbs/7REIFUiwp6Wa+n8ZezyHqzauVuDQigsFkICu9CbWXK1QzpzOMnL3O5Ts+qXAzTao+0AFEo5xjjK9"
    "1oR8cfT5M4d+n9KyQYH13ToGQgUS7FejWkPSuFf9zy6SfRuiwHkJycWQgK7kM9tR/yeImO3wZt9NtNgue+auwLX35wRCRUScLkTG"
    "G1BjxhDrb7JQ62y8tmu7AkhAl09jefkKlmFVaoT69s/CN8xDC6AiIq7WIPsCWWNGXhMXlDRsKj61rrIYEtC1b0hLnCoJIol2LEN6"
    "LwklrszA2d2nS6ECCfZr5OZA/8aM35LpaIMqHW+Mm1kMCeiKa5qAXeb5kbTtXmw9mY9VaNiIYbhH1YviHgv34pBcl7/1MzcHxyzz"
    "JBPbecl7WK7FSUr3xoxIu4Poa8lYPJH3kkIFEuIMnRdHUdW9VPxo44sASEAX++X2EPVrzFh9ZQVSWaThalnYCahAQnzkPzc2x9pr"
    "o3BO3pvAHmqPMZ5n+UeJDriC7+rbkrnOHeWLi09jp7i2jUSvJWr44cV4LHH4VAwVSPRQHMLHjZyJdH9H9v7D8RsKfp2I7ZxnB0IC"
    "umAdSiRGU16h7SuSsOlNXS+oQGJ042/hbqdZRlRkBcoqGo61Ik/nQwK6YE0LPY6VK94+Q4YvDe0mzZE3JYklWn+IJHsNEn5Dl3g4"
    "eMq1zF7j013MGvfqLmmHu34gOFItpQgqkKgPrcX5a83Ip91sxV77j1b4h2Y4jgg+5A8J6IK1LjyfH7DCCYHhOPehkTdUIJEsbPcT"
    "tvtXsozn2kZ4Q0hv7DbQ2QsS0AXPjUSyzKY3LpQa4VdVkYE1w6xJRXwlviXxkGsnW5JSjUf4hoOHPMa7JdFSe944vlpf1xXfW9ka"
    "f7u3tRgqkEhKNSD3L/3E77azlYf5N8HY9KMDTrdLkUICumCtSyS7fGT43FhX3PPY3ADR+QDExY9NSZKmFpn6kmW4/fLGJ/R9cHKU"
    "fxEkoAueG4lkftIQvCG8BnUqvFb8KawDqVZs+rNX4Z/syc61p7DOfnd55BYHcv90SeORH13dD4/LaIrDf28OhAokYB1KJHanYrFq"
    "XRNsdrJ/ISSgy2m4NbEWyn8z9A/3xIldTPDZsbbeUIGE+HzMXjoRt+y1Bg37rl50XN+fBKaH/H0esPcnVR2CcZmrm9xP4kW0eszA"
    "R/ezmcvNv4zH+dFb0Xw7JIUEdOn18CCrxixtzHCSj8Zje/LodcX+YqiIiG4dyGyhDn9bsFneE6NS8PDFZWhgv0RvSEAXrHWJ5NfC"
    "4TjT9BYq1NDoCBVITPBwJfVdtuMPrixj/vLBeG/0WzTqw+ZASEAXPDfCVVKRjveHT0MeObW+sH5gLVh19ifr7Qh+247VVWpoJp5G"
    "Q9CJi68DoAKJ4yeDyM2S0sbfyCZun4K3TOiJ6mknqYgArrm1UvK5xWcUu4vNjk60yMajLb/Ltl6eXwwVSNjskJGb62aix5gRXouy"
    "8eXKOzJJxyJvqEDCXdg+ceXMxr262lmBp3ZaLzu5+0gBJKAr95WMjHjaHW1zYBmvzyjw05sdZImx0wOhAgkcjcj//+Xu/EcFNnDd"
    "EdQz61AxJKBrZidEDhrkqobtYbOju69XYOeGJNVZ6yeBUIGEi5A39eM0bnksIz4Le/XiZgfVKJ+DBVCBBNvDDR+mNf7WN/1wNlZ8"
    "vaJyW/AxHxLQZaUuI6OuHOWGdnBtrN31lXdUFRMWBkAFEqymX1ucbszouXIqtrjlyK1MdyuGBHS5tw4ktwbZ0GkH2bcZbsJ1hWgI"
    "t8pDKoUKJNg1dsUhuPG3JR2bDDzzfApn1GWKv4gALgPhmjZ7SKjPWJaR0WoSfvFmEbd3YcYJqEAicbUPyc4aQi+4MsJIaBkKo7dy"
    "Izv7S6ECCXY315TmNO6VbNZYbBR/iMst8ymGBHT1meBOztWsoK/3sq85EoWW4dziMi7wzZQAqECC3c3ulRsbM5qrRuLKbpe4DeNc"
    "CyABXTVCOVEoD5zBMg4XJWP6/jFHFfuPQgUSOeediJe0gK53YsQKoTfYFV7DLS5fEggVSLAW3N6qpHGv6m3jcbeD6nTLyTXFkICu"
    "NfmtyfHy63TabvZtRnuhN8hb14RW/rAKhAokWJufkn+rMePQ1yicZ9icRvlrFEACuryEcohQfrSaZegERuCqPHN6uPe0AqhAQhFn"
    "Qvb3ekd9XBjx7FBPPKKLCe06820xVCDBepzwftWNe6W9jOA1B9vRW24BUkhA1zmh39U/rMlPOsK+5rB4G4x7fnSg3uh5AFQgwXpt"
    "jeFajW+wbAr8sVuwJ13qN9wPEtBFTzclLR5r8ssP/flyUhjDPZgho9MiCougAgk27kr+aPrvbXhLD4yvBtDSZ8lSSEBXKa3DTy1b"
    "8O/cWUZzYQz3QDOcmr/VVEIFEmzcVe1l+e9N9WsbrFkTSvtrTSyABHR1EMpvhHKzs+yrlMhxZjjZNpLqJBkVQAUSs7fdxU5Orfhb"
    "eYyw3NQc662NomFLBgVCBRJsrH1Zq23jXqWd18VPrWNo8ojxxZCALtkcFTa978B/cGYZSx9/QsvNB9FbK7ICoQKJZGF8Xd3FhXe/"
    "zb67q3P4hvq9TqT3jad6QwUSbHT+Utj+d68Kjz1AkplDKdH2EBHQlXB1I1a0cuO/7GEZo4Qnr+wRw+joBSUBUIEEe1rSHubemLHb"
    "7STSMxlNp5n0KRYRwOV8OwM7XfXmF7RnGWbCk9eRe6l0wgldKVQgAefMSCTbpm9BE1pOoO+/BxyFhGgujlAOE8rH3rIvWfXRYvTL"
    "cBKt83AugMr/NXuHzeqRSIa3X4DOTJtEya5dxZCAruJ1vrjiZQDvcJBl9PQbgHSfZ9BfsS5SqIhmC6lLcId7QfytCjYCMPoegaqO"
    "TaGPDiiUkICuCounqDpdxi/xZBlfDlqiJwZZdNKh8kCoQGJn45yZ3ctZxibPFujBiCya9flCASSgy+dUIVIK5RlNWcYNnQeyo1nZ"
    "9K7dUW+oQKKsdQaKNcD8+QEsY4PyjOzItWz6cZ67EhLQtdfbBdFUzMuPsK9+d1oHyfyKFTS9LkcKFUgUfFxYkluBeUU1GzPoh60J"
    "uvVJQTfz+UpIQFcH0+eqzJOYv+3GMowvbStRF4gAnS2BUIHEcQNrbu5ezJftZBl3b7VQjb+loKpT+oWQgK41+n/LO61YxoYF01Vn"
    "pipo7K3MQqhAYv/wJdx3J8xHp7CM4i67VYPaKmizomVKSECXcuR57vEwxDfsZ9+Ga35Q58yqs+jvpP1SqEAie6IOva8t4w98YKOM"
    "Yw4u3PshU+mn3WeVkICu7I3OtHy4lB/tzDJ8DUI4tZ6ZdPjRoiLoMktvR/PmSPl5J/5LlI8dwy3+OpmWrMoPgAokIgZ3ow3ZAfyT"
    "DLZXT97O5LbFptMk/dNKSEDXHPNU+vKmL1+63+7Pd/RrOPcpE+k7rZ1SqEDi9M5Z9Ocmb76Tlsufr2UPcOO+jaU3mk1TQgK60mcs"
    "p1n1nvz4UJYx70ght7VvKk39eN0bKpCYKWzPELavKmcjmazHpzht5Sga57BORECXYvJaOvq0B//Yg2UEaV7gXgSmUH2rokCoQML4"
    "9zZaO8GNn7OcZXQxvsd9sx9GXZ33KyEBXecSTtA37drzA/LZGhDWn15wXeqS6MiV86VQgURMGk+t3jny3VuxjG41v7kRmgOo+Rp7"
    "JSSgy2v/JWobZc+/GsAyLrmq02Nj4v/MgYTK/0U0f8nGPgkHdWj19Zj/RUBXZP0tmqTThp/SkWVc3a1HTRb3pVf9bwRCBRJrjt+j"
    "i61a81nbWcb8cjN6viqC2kdlKCEBXeavPlFFpil/8xBbW2SCtiX9kdGdBi+xl0IFEorRdXSrvgk/qj3LuHy2Lc2uDaHLi5YUQwK6"
    "/GZJ+KdfDXjfcSyj42cHOuN1MP26/Yc3VCDhJWyvFrb3/8nGPmdOdqADJEHU620LH0hAl99Abf7DZh2+dQeWERvuRsunSamPY2gg"
    "VCBx2r4pb/u4KZ/9ZwznuSaQRnR2p9r3jxZDAroCVhnzTuQ7bXrA5s/7WilNKnOjkTpORVCBhGKaMb9m7Hfawo9lqJ50om0229NR"
    "beP9IQFdmc3M+ZoX72mH2SzDsKITXXHInlZvfOoNFUisE7avEbb3NGAZj3y6U53BllQ2vG0hJKCrbFxr3qnffertxjL4feG0p4UV"
    "rfm2qRi6wo5Y8w8nPqSTTzr9h3AN7EsfOzajDa6nA6ECiS+7HfkkwzP0XQQbwynmxNBYB12qUAtUQgK6amuc+MjLlCbls9WT3M4k"
    "0L7nGrjDGrqBUIEEe6Os/bGYlrVnGR9XDKCTP/zifuYtPwoJ6LIWyjZCeddmlpHuNpqW7eE517GblPUtfHibyfPo4EGO8uknffk5"
    "i7Pp5nxr+ZpmHvzVuC20iQ8jkOsQes/hBfcl7HgB/FswQ0xY/B5MN514zYW1m6+ECiSsprjxN9R30y132KjvYosUOvbkBU6Cx0gh"
    "AV1wb4XnqIix9JziMGcTMesEVKzyfflbHgr6G4mPSSIxfT2Bbhiey10+aRMAFUgM6hvIN5/Vi86tYWOfEVZpdFfJCi6kWYESEtB1"
    "56WU7/IhgF7zYBlqxhmUmz2Kq3y0VQoVSET7IN43zZCOGs0yYjOn0Adj+3BB2yOUkICu/BrE97VXo+/OshWauPuZ1CXUj6uqOOAF"
    "FUgohe3Zdmq0RS+WMebwVFro1JZrissLIAFdReMxHzSnhos4yDK6b8miFZZ6XLMXraVQgcSbHYTvrrGRm/jnv74VLcymb7beUdkv"
    "LVVCArpaRMn5mBIvrqwDy6hZoKDdr05QzWmzXwoVSGzdLufjd3RR1WWxjFlPFDTe7ktJ0U1NJSSg68+cMst20sJ7bCW2LfUKmjtH"
    "r6TJegNvqPwvYl876e2hLCOmTkFtXWcH6RjOL4AEdJ1bKuev/7gkqzrMMlbcVlCHFH3Z5Tl9pVCBRL2fnH85Lgrp6LGMFQEKurxi"
    "k2z62uNKSEDXaE/Ce4dSdMSHZRwamk3Dop/Jphqul0IFEhuHYP6z5hukWs1GZBNwFn2lMkVtdx8shgR0HRLOpnOaOv74la32Nn3X"
    "VDrMygE1M0gugAokdgvbfwjbTaazjJWyTHpwfifULSqjEBLQVe8u47utdsALjrEMww1TqKZaL5TYIlIKFUiMsA/iL2z1w842LMNB"
    "mk4db81C8zqsU0ICul4u8OenrBuJj3qzDHIsjW7Ly0Hr9w2RQgUS59L8eGdlOt6wk43IZm0fT3vh7ahpSptiSECXltBK7JRPw9N0"
    "WUbI03F03M7daJwi0QcqkGCz6WTC9l0rWUZ4zhi6mitC6xbViAjo2h7ekU9+vBpfPcK+MYn4NZo67itBnbvpSKECieRkTz6raS5O"
    "dWEZc3OH0i+RD5DxBg8lJKAraY4zX9HyOF7jzjJerkqm56c/QePtdgVCBRLGms68rO4EbnKUjcikfQbSdke+otSqhhOQgK4OQju/"
    "cb0S/2jFMoJ/JlLL93VobcshXlCBhFzYHi1st9nNMhwS4+jo9VpYvX6SDySgKybWll+1qAIXHmIr470bGUfbztXCGwe3LIIKJIxT"
    "bPm0mApcEvjnP+S5RFB60hyb6ngEQAK6bGvNeOtnH3CJF8tYlGhAm5pGYaPSpdLI6ZdoYqE9mf6ytTyJPKKZPtakuNBMLvV6QUP7"
    "WpKdSWzM8PJHK7rArxs+aLhZCRVIKGb9og3YiLz3Y6tT3u5iS5tf7YJDdqZKIQFd+XpqfM4NA3LpHssYucWJlkyV4y9GvQOgAgkn"
    "YQQYGW5IFvdgGeu/etLOTfzxlcUTiiEBXXc+N+MnRGqSDX3YyBLHeNBfKwLwi8i+UqhAIjxIj6+0aEIuHWcZFXsJNV/eDreojVdC"
    "ArrqhHFX8tIPuC9lGUeHY/rpd3ucPnFVAFQgIT4fB7aG0kXBbfC4JYePQwK6fhaZ8wmP3+E7Z1mG06kI+uaTGT6V/KwYKpAQXyVv"
    "JOWcwdER2Oz1XunT70updEtHcqrOWh7qvY2GfnUjPw+byut6HqI1N10In8rGPrNWv+RuXUrCiixeCRVIPNU4RY2vO5LKjmx90Xf0"
    "G1fIJ+JHG7ZKIQFd8HoTeufD6vROm3j8dI/vCahAomHfJZqzx54YDGQZq641o/cuRONnOcf8IQFd8KoUxnDXdsnOOCjwmasZSp9j"
    "x5HeSkRe5RvJjXO3y+bqEVLsayxvb6yDIp9hsn4366M23nEM8v6lwPXayVKoQCKmnzrn3pyQjbZsBDC/yyTl+AYFtvC6XwwVSPg1"
    "+zvLZst2tj51WbWVatY1Bd7ul1YICejy0/k7q+fUn1HGqoweqqw8BTa1cCuECiSOz+vOKSsxCShiGU0Ndqm+OSlw3LCOUkhAV//f"
    "pVx+KSLB61lG+8m3VMWrs/Glj3lKqEDC5f0nzrxeRooC2JrLuT6OnOf6qbh8fK4UEtD1O6AtzTcJIn6GbGT5qNafy76QicNODy+G"
    "CiTcGudiFS9mGZteRHFlw6Zg/typAkhAF2osPzRnGTOfDuX6Dc/ARYE3CqACiTnOmF5cEEi2HGMZM75mc5PepeNXZ+dLIQFdjkeS"
    "6HFdf1Ixg2Wce7GM6zEoDd/JpkqoQMKPTKcLF/mQK55sleb+P3ZzuTfG4dEb90ohAV3w3hTGohn53LaTqdhhtW4xVCDRMGM5pb06"
    "kgUTWEbZoDLuXEIKHr7fMhAS0AXvYOG6On5C9vRzNv7dc3ERvNodSguR3gZEKrGVHN43EsmDwqaod2EWtnrp6Q8VSGhtLkPpXRDJ"
    "7cDuKK3WHdHxllPx/Bp30T0IXRec7HBtupQoOrKM5l2kaOfBTJxhvTMQKpDQ7eaIF0qlRK2QjWTKO81EI8el4+nDlhRDArrifONw"
    "JfUj1y+wte6dim4hPHQ4HnN+SCH8Klb0teyhZdi8tSeZd4mNAPocnYWOknS8rXifD/y7P/zi8HHh736K+m+G0b116LnzRNxt4uBC"
    "qECiW30y7n/dl9hgdhxOautRc4eJ2C/g1XFIQJdu+lCsOO9LLApYxtOhR9Hzz6m4qNY+ACqQEB/HF9MCFLwjFauPvl4MCeiabbQS"
    "4w0eJCyAZXSMv40+ag7HsoH7AqEiIkC9SSTrRr9Cl1cn4V1DlhXD2nXIPoQ1jJ3JnBgLOfxGWRhT/5Tgh7YJ2MXDQwoVSHzxu4Qf"
    "5tuSzIes56xJ0MRfW/fHKw/PUEICuqxHXMc39tuQlECWMTO1BX54oDeWuztIoQKJjWqPsf08S5I1k2VUDjXGrhG9cOxMtUJIQFe0"
    "UJYK5bjv7L9gfB9miQd7dscfslYXQgUSs2fW4FCjliQ/mWW0r2uFo6XdsFWz88WQgK7ZXu9wfy1Tcuw4y/CKdsBrx4fgsrtLpVCB"
    "hP1cCVGE6pOltWwkM2WnM/52HeFzt/KVkICuzPea5KGxDtH3YRlL+nlhizxf7H2kgxQqkGDvWIdpapHTq1iGqYsvfn/PC8d8n5MP"
    "CehSCuV0obxFj2WkNJdi27NuuFVZfgFUILE7tBlZM0GNTBjPMuZ0Qjihswt+kOehhAR09WnegqSpf8MOBew/hvTa2Ak7f7DHm/L3"
    "SKECCfdqM7Jq8ktc+JONGVq/6oY9jFvhiTNOKSEBXfnlVsT6112c68sy6MNIfHCEKd6q/yoQKpAwHm5NouMrsWUey2jerA/eXG2I"
    "h30/XQAJ6NIWymlC+asdyxin0xcnjWuGPRqMCqECCZewNiRv1RW8YB7LcE2KxWodtXEzswwlJKCrxt2B3O/J4WIl+z8/w44k4GXq"
    "Emym3CGFCiTcZ7Yjo9scxUtNWMYcyRBML71Ao78VKyEBXU+lHUi9ahNuKWMZ+tpTcff9Xlz3MqTcnR9E4qec5b7KdOX9WweSJQNs"
    "6KU4I3n+ygBy1rE9Xc6xlSkGWGfgj09TOJ8jawOhAgkne39y9j6h2a1Y/7FXORmnkvFcZw83b0hAl71Qbv6A0H7LWcZA96F4s8Ej"
    "dKrguT/cd/tuHYipYhMOOWv6n+OovzISR327iI7bZZ+ACiSGLXYnO41XYr+NrK/NuDQaz12tQiG/DiohAV03KrzIhTaZeL6S/U+k"
    "70ljcS+dwyj26kIpVCAR0t2HvJoyApfas4wLWmn4SORKdHPRaCUkoMtLOPIpbsH4TUSzP/9FKQ1nt1+CjrS77wMVSPQXtju7BmP9"
    "O2y0ZIom456uU9DWRfJCSEDX3Mf+5MJAX3zUn2WQy5PxuNbjUEuf3oFQgYTN/gBS/KodXreXZSwKzsS6lp1QUrcMJSSg60b3ILIS"
    "PUJdjrE1OZb9zsQaKd6oNtdOChVI+G0MIp+TriAjD5axMDwbz/9QKztw50YxJKCLzXozWTcTqQ/W+zNCzsa7Nj2Uzb+e6gMVSLDZ"
    "Yt6rZiL712wUnjJEgTV0FstWV5wohAR0pRoi8tLWAX32YRk3xyrwjPC5sqNj1AKhAomf1oiM6GyCck6wjE6/Fdgm8pV00LmDxZCA"
    "Lm0PRNxOv1RFFbGVQiKEp5VJB1ZL1c87FEEFEiGebHu1ql8nljF8hgLfTctStX1/1B8S0OUk7OGiz9O4/EyWUTpTgZHpVFX2SLNC"
    "qECCHZPrp2lcpRbLGDErG8dZ3VMltTnsDQnogi2GRLJ8QzZWNdxU2W5JKoYKJD7dDyLNbEu4+HLWMpwYOxWrOTtz8++eDYQEdMF2"
    "RbhKklKx4YhC7sLUzcrQeA+yYkoOPTishbxhkht5OHctLShqKk+57k26GI6ha4NYW1K9Iw3/dFzKFfw28IGtDGx9xMSeuEn4h89C"
    "7nenOCVUIPH0vQ+Z9CqRXnjMRmSGXcdhecv9XBOXcVJIQBfcW4nk9ZrBeLD8LcfeWmaaO5Gay8dotzJD+b9yS9xUviK1PWl4kkcr"
    "37DRkof3UHz620Mub/FKJVQgAWtBIrl1aSj+PuM+dwq5iAjoqg3rQPpUbqS73dhene+fgutGlnFuKUsCoQIJ8XFo9WjJfT82lXo6"
    "jFHBlX/gikC5fDVna4b4vD//mXTrgbdc7O9BdH67MSq4dhNc02nhzQKaFurMn7Jn52O02VD6esoDLkx3jAqujAbXVdsb4cprjzhM"
    "P1aw1cWsueOciZ4OfaAKoXN1JPzPoZb8aqonnzlCjc8ybcXLvJvJJ9zQ48s+G/EGN9l9fgdd4DrGq9O3XAg911eXH53Ygh+eqCdy"
    "3Vhqyoe31+HXT2SE+t27nG+Tr5z3yRDa67sxX3tQm//UoCtymS9vzVcuqqdzzRhRmfqa+9LyOad+JoSWPm7F9yn/QR9t1RW5ci84"
    "8rmnamh6Masrz9M/uZuuFVy7cyF0u4YDbxNSTa911hW5yrzd+Bzjcjp0ICNMNmvScR5nuIVCRlKsK7/m+hXK1eqIXB2eePMa4UV0"
    "kSYjlCPtqLnpC1lL4cit1IP5kaV98eDZWvIKi058sUUs1vmhJR/xDvOLP87BGutZ7aY2b0MrnNsgTqhdl6cyfqNiNo53ELu2Pwjk"
    "9Uu24KIARkx+2YoOrglHBUJG/0f+vKn6Zmxcqily3X3vzWspi/DdO2ydu6P1Lena2knoGB9Cq9W9+A4lx7FPsqbIldLRjTc9U45N"
    "MhmR09OEPhy3FGmdDqF6Ma58/YyreFQTsSv1qCOvf/gFbtKaERvqLLiHKW1wlZBxN/UdZ3ClMxmx/DfJrf7Azf0cSo5lNhDpqFmc"
    "1dgwcp1j/8F+reS+ynyPHR7L6qrtTG5h51Ayq6Je5Irr566y+hVGJjWwdVLph50l2S/a4lyhrsqy3FHkyFCyJ/oXeXnYE4WsCiN1"
    "qJ44mJ1DSmlXcjCbrZO6NeVcUOT9ttiPClfJpTMo06QLSVz1U+TS1bTEBp86k6+UrSk7YPBi2THNtjj6VAjtFtYSm18PIXtv/RC5"
    "9qVHYqtTwcROkxEunxej7LcmuETIKMwtw14zXcixwDqy+NZFnD6wA9Fo+43MbvYUH3/iQCyS2crDXVwL0exqHXxSOA6fWV9x7XMr"
    "kqr8QkyDvuNDa62JasdXYtBam8xdakK6PWOrNHvtPI0S25SjBz5RFH9qQfxWN/mzQuwwA0uSs1BCpg3/TK6mtSE+TT42ri86d99L"
    "NNhRimffUaOFx15gv0et/hCr1B/i3BqbP+XOI+9hG2tbsrsnI67cOo9u/PbCMyrMKVQgEf2Gxw/D2zWudNv/13FUktsFh5Zq0ujv"
    "W7FGuvsfJcsvD09Y1YEkLfsvcTFvJaroNQxPk2/ldnrMwMOG+vxRnD+lY+Ohvn/KC+ZOxn7XfMngw3/WEW7fFX3YOR4nPJ/GrfcJ"
    "wT8NA/+41v9ogmtdZH/Kr44b4dy6IOJ9nhGDcx1QlK8B3WrdkxY6z0fb24Xz+RcN5bMnnUfTH4fyxlsM5VXTtfG7F135PBlrd8f9"
    "dEMB9U3oeaNoChVIjJykhic86cLnV7L+I6eoBaq/qkkvXIoRZbzM9UHVQWH8aLk4TyKJaWuCRp9pQ9sI9wdUIJHc/izqVdyZH+XC"
    "iInnvVDvnja0XVcxAV3ivUpa4IZ6ZdnRGx8JhQokfNw/o9CRnfj3fozY598OlWwZR7W55dwXnkOnLyK+Y1t9uc/Za+hQJuKfe+vL"
    "Z2+kyHY95vWvs2eD2mFd0D398XTlx9kcVCBRUXQdDbqKeLNFjBi/syNq5zOWjr+3VkRAVyl/A6X+RLwinxFaCz/JetAsutRpjCpZ"
    "yqEbEYjPGNdMtM5d8porqEVrxPfNY6PwSV1M0NrNU+nbwJUqqPxfK+OxFfMkkoLSA8jnWSzOeXyZ+zJgFY508iKzw74QeB1XVC7H"
    "Dyd1bLx2g8+8QDuCtPHhlX6ie7DB0IAsbKHzp1yZaEDq4nXIJSkjNIwfoc4ReviNzI9CBRKbR2oS6bYWjRmHnjxCr7PrUXENpvDe"
    "hnlXPxkS87u6xMKBtQwJhrPR7Gla+Lt+T6oy/YIfSu1I+L46UYujCr6D7dVcSd8/q7FXJcSg0xW/UHlDDIUKJGDbJZF46ySggBBd"
    "fAD1FBHQlaxXgl0WeRPPDLbC+KjSXlxzfz38K7onHYOjKT3emXxQSuTPXxjTq6FhpF0PiXzoJTdam9OZjLFkaxXrLczi4rdp4YBP"
    "PWn+ogW09hYhbs5qckiPGZtEI8ODyeGJjNg6MJ9LzNDFPkK7665eQus6eJLX5mryHE2ONlh6kRWL1OTudjtpomEAyerAVlCeOH0P"
    "Zzz+GzIfFEmhAom7+Dx11/cicwzYir3Kd9s57tUTdLBfXxEBXT8f7KXDcgOJKpdllDwVek7d10HjWvek3xPC+QKuAXWobyKv1uvK"
    "/3AMxkULmsjvxoTyuun22CaWrXpqn2pM453Wl9gF9qIbw3vwL/3S0N5R2nJIX9wVxt/kqtDmY4zY99CObk8sV8ULvXPW/a58es8o"
    "zjJKWx7ZNJz3292XO3leWz4sK5yXvVJI3Uex9UVvnTGmLlaVqj6RkRQqkJig04OPb72MGx7OxrsmtCm90u+lKnJcXxEBXdOrevAn"
    "ZuwrSaliGd5vZ3FT87Tokq+RVGPBQ0ovufBugfryYYN/0s16dnxeaTN56IXX1GdKWz59JbtrNY7GcrOjdKjCpBdNijhFE/p486Z5"
    "+nJIxxRW0GQTV97gMyOWpDtykjhdqt63Dz2nvoPq5Ej5QOvmckiH8CqaersjH9/7z/+Q7vBM5f6mKbUd2ZdOeDiLLs6U8xcXNJdD"
    "OsViJ32n8udLDjLibMQNdKbVbzRwTgiF9xq8B8X3ueap86hAQxOf0hQT0OWyU4tsrzMiP38wQmX8Aj37bIgNgjwoVCAhbhmejnmE"
    "ZrmZ4IYmYgK6akZrkM2DjBqJX2UuKGNwM9y8qBd9c2ojTrkkJStjf4ju1MVn8zFt4k2cH7H7PLKXHxo6Xx1vSI6hUBERopZhbL8J"
    "6H4/C6wmjNshAV36V45gF/OO5N5XNvYJGzURvW1riWt1QyhUIAFHUcK43Wc5wlNc8IJJ7iICukx1D2Npfw9y9y37vxkrt5/iYutb"
    "4yyBGOZTTEMnupPXKyRy2EokDdlOa438yK0TrC0JGljAPXDWw52bCCN9oEBC3JbkHNjMnU8wxPNP/ocArj7bF9I6W0Tqr7IM16fL"
    "ueSYOnSytA+FCiTEbUmYxQpu6YjvaG8bMQFdsK2USMKL/GnlnnOq/MnuNO11F97cvzdnea2JHLYSfXqF8TJdhXRuHWtL7hyyp80v"
    "XldFGIRQqEBC3JYs79qW5s8epTpzVkxAV7R2OL/3Zjx63YIRz8ubU8nI+Sp8ug+FCiTEbUmPRQa0YMFc1fMwMQFdsK2USPos9kMX"
    "jvvRF51dqU/718jTKIS3umggGu8UWpxBiy+F8KN2s1/o7a8FoZeXvemmH24UKpAQj8g+PjJB33f70l3CdQUJ6NIZ4IXqWoTypZdY"
    "RpyRKXq6ypZqNw2hUIEEHAFKJNN0y2Xja+xoJCcmoKsKtVa12BPGb3nMMn6PvSUbEGpGPWf0oFCBBByjSiRlFu9kRkeaULUdMSIC"
    "ugYEdpZe1ezO58cwYs9Riiw3tcE3ytxETyylJp9xn8GWZEz+Z2Ia+wAbT7cjFyb8+b8yv97Lhug2wx1do6hllyzcXyUn+d4/CWyJ"
    "Ouvl4hWXA0j3tWzMwN+0QJsWaeP1JdEUKpAQt1eeEd3QLw1r/EPoByEBXdV912HzK37k90FGnLUPR1+uWWPNFsKTMFAgIW6vzIMm"
    "IeuP7hgLdxQkoOvL1TX4qYYvqd/FCNvySShjrge+c9ONQgUS4vZKbVEOWpZB8JIzLUUEdF3OXI1d0rzJnZmMaPCg3J7kahT6MZLS"
    "uGqaI3UmA2api8Ylfaxu0RVhrmTda9YyHDp2kCvjK9DLtTEUKpCA4yCJ5LrdWa7jOw1cIzylQgK6Vty6QfukOpOP6YxICDrHJa3T"
    "xK00QihURCMy0KIKo3DH29zLp+b4yUR3EQFdfa6U08yz7ciHT6wVLf98m/MY0BJ/vOBGoQIJ2OZLJA52NZxxZXt85mRLEQFd23Wu"
    "0XNRTiRxMCOOCK3PppYO3NoXkXRueTd+zBk9WsU1FY190raH8b8e3ua8nNhoKeWrJnW2MOa8dsVQqEACjrUkkg7729Dll025rcLz"
    "ICSgK2NqKH9pzi1u4VFGNJtqSwtVZtxzoS2BCiRgqy2RbF7iS10vmnEPhPYKEtD1dEln3nXUTW6hGyN0HP3oBoU5p3/VjUIFErBf"
    "kUheNITRp5NNuaOnWooI6Ep6HMIvWnOd+7GBEaMMO6HcnE7UcFYrmsZXo5gGOc8PEdpd0GqvijiFHrcO5qtMWQt3IdUf9RjdlU4f"
    "15JCBRLitv17lDG617Ib/XJKTECXTrwnutOmM3+mKyN2rjRFs4kfPXHZjUJFRIjadjrirKz/KX96Tbh2IQFdVYetVfWZofz3UYxI"
    "n3BdVsTZ0+7COBEqIkLUttcuS5Vdi2hLb6jEBHTVzprBBbQJ4+OmM+L87AWyvhcM6ZHhvSlUICFu2/3JMtne5s3pfM8oEQFdevPn"
    "cDWTwvnLT1jGw03bUMRiQ3xfPYTC36xEPcOyR9jKsi25mMnaq3VtKVqt3wZ/EeoKKqJfv0T9R48Re5HZSUesJTwlQgK6Ejacw4cq"
    "25OCjixjYOlJ1NDWB5cK5xwqIuJhKd6e1I4sM2AZS+32ohZ7pFjDT0xA1+VpB3HNbTdy4iIjUqtnyBKMdPDgNTF0yqkgXDeqC0k0"
    "/UVgD/eldDq+eBSRMd3ZfwAzivglO1Cnj4ce7E2hAglxP/iroA06+8MGlwjjK0hAlyxmGr6xM4jYJjHiVHdbNPRsG3zdPIRCBRLi"
    "ftCiTygauMELL5/iLiKgK846Gy+8Gkhs+jNikjIUjfP0xnpVbhQqkBD3gwNmpKA9lzrh0tKWIgK61j/OxOG+AaTejxFKPgV19eiM"
    "DXBLChVIiPvBGYPmoLzuffCr2gYOEtBVpT4F737oR/bUszPoFlvOcZE30eRWPWnyWAl/OqgNMfiuLoe9aG7AG2qwuy153J39BuAY"
    "XsLFvj2HLur3o1CBhLiv7V5eyQXkfkdLhTEcJKDLqfAVrXxsR6S3GUE17nCWD36gXsIdBRVIiPvam3Nfc1GWhrh2gruIgK7KCS9o"
    "ZbgtCYxixL6hb7g1wl27UBjDQQUS4r5225t67la2Le4t3FGQgK7MrOd04SsbsucUI3Tn/OaCLtriy54tKVQgIe5ra55o0RMqD9zi"
    "VQMHCei6e/sZVZ5qTbIdGLFlgB514aK4t3o96bmOoXxfEkFXe+nIYU89okco3+S9HX08h/XOfeLU6JAcP+5uy34UKpAQ9+dnD1tT"
    "NcNgLlc4g5CArvuunfkuHWxpoBEj5ila0/GBIVyx0LZDBRLi/nznLC/qXNeVeyG0iZCALr3OIfykdTY0YAkjPlt4U0lFGLf3ohuF"
    "CiTE/Xne+y607ePuXLRwBiEBXYs3yHmzwNZ0968//+EoKpSmT+3B2Xi1pFCBhLg/35IXQ2dwPbgpwhmEBHTZBhD+gbE1zU5kxJyU"
    "APTNsi/1naRJ01R3UV0vwvvnNpfD0YDpFR7ZHCf84clshlD/OY7I6E4s7Xi0gYMKJMRjhs3TDVDUlTi69aWYgK69G9xRyNgQ3us4"
    "y7hw3RitzOpGi31aUqhAQjxmeL7ghOx2m+5CTyAmoKvK01pVOb8z//0Fy+iTeU7WbUAA7SCcQaiICNGYYUaPYJmjViBlVwkkoEsv"
    "eDq37ksX/mgzRhROGidzdHagi4W2BCqQEI8ZxjcdEbT8Y1valBMT0GW19T1XtzOUD7VlxJ0qdVl+ZTPaalM0hQokxGOG/esOBZ36"
    "akQXLOglIqDryvUmVKEI4wPHMGJfh+NomF08/plSzMFf5eGv9fBNk0SSRbahF+sj8EiLBg4qkBD35z/mK9HZt13xridiArrEb7Cm"
    "h/GI8+6G7YO+cVCBhHiU8XzRddTtAMID5jShkIAu8Zu4D0anUME8HzxPuAehAgnxaOlgWgX6vNodbzwkJqALvgWUSEw+PULTl3ri"
    "CHsj0ftBSMCne4mkk28Vis1vhd/MchYR0CX+BbJ84g00fqkFVhvjTqECCTgClEiKPlWiZbstcQ+zDiICusS/pA7SP4aWbtfFn4Sr"
    "HSqQEL9LnXz+HPKP0MASKiagS/yOJXT3DnR82gg8wnGG6K0lfFMpfle0wWYlSm+ZiJ+VXuCgAgnxuGTbvNVo+tlEfORDqYiALngd"
    "C2PRsXPQobl98Nk2DaI3WJAQj5ZM2m1DMQMi8NHXYgK6xPfHgOIcVHmf4E+BLSlUICH+LWP3sz3oXogU9z8tJqBLPG5PXbMcjTZ0"
    "xcevuInH7YAQ/yK85sMe5OXmiJcIbSIkoEv8/FGwaQlCxaa4TuidoQIJ8Tv69be3Iq/zBniySkxAF3z2kUgu109BRhZfUcyCGNFT"
    "kehNHHhDJ4x9Wm9GKSa/0c45kSICusTX7qIbi5H2vg8oMrgvhQokcnK1Ce1jTjJ4tlf6lbtQF/dXyK28j4iALvHV7tSwB50aVouu"
    "NusjepsBCfMjxiR8qB7pfpsRrT0Oo8/vbqMqRV8RAV3wbaZEopZzEklsH6GeFT1F7zkhcehgayJzrccOnxmhd1KJjI0vol+pMSIC"
    "usQzIGoMb6AL/a6gQtdeFCqQeJrVjqQZP8HYjBETvI+gERf2I6fwgSICuvbbtier7B41ZsSNf8h5feNQ2IZe/4+r846KYnne/iIK"
    "AiKCgqggJkCRIJLDTu+CGQHFgCgYvqioCGYRMSfMCcM155xzgO1qUVSCOQf0mkXMOfNOc37vOVX3X5/nYy07Vd3VOz09UNzSUjAP"
    "W13fwcZ6vLJ4s9JIJOkddGJ3+TtAlxbw1Ngc5fzgWMAKJuj6Y0+Xlzwn+pUyXJ2dMYFdycEaEZ1VW1crUBLeK0p4+phS5aqa7VjB"
    "BF1/tN1SxnMOmLJUtaIwgV2t//wBC5taOvvD5euPthowd6zMjAo8ASuYoOuPzwfN4Mwwe7ZW7ZYwgV37bv2Cc7k1dTMaSGKZsTnU"
    "OG7PuqvzIFYwQdcfb7ZZQzMPV3b4ZRnHBHZNtfgJ1Xfa6eKnl99Fvm0NI7q4sobVyjhWMEHXHzZZNaHVLh/2v/MFhMCusrXf4VCh"
    "rW6kQb572aZrRXgSNolHze0I4BsmwrdnQv/tZnq8eqlVuYVYe7Yb1HshVxM/i/7w55t68MjhsYAVTNA1jv57LXBxTuGb1fEKE9i1"
    "6L1eTBjSFdKHS+JQbm34OTOVr1VnTqxggq5xtqz3gje/0rnZKC9CYNe1ajpxsWtnSH8r1x9ffZpBTKUM3kldc2IFE3SNE/UhDPYu"
    "n8yfn7InBHb1GKKIi1Nj4GW8JPrGhMPVj5N5i+b2gBVM0DVOzIZOYNZ+GrdXVyyYwK5L1lrBf3cAA0iiz91OEDF9Gm9hVcaxggm6"
    "xuk8sg8k20znpmcLCIFdpb9DxN+z0VC7liTujXRQFq0eCM9DcjneD4NXSHQvTn5/DyXRNglqzS8gO2swQddRE9PMlCWzB8Dks5TA"
    "LjMXT8XaJExUri2J31etlHNmPWCYTRnHCiboOkqzept2VE48eJVQArvu5joYetwOF0mxkvCIPqG9OLM9DFfrHCuEIOuo2JbW2pDg"
    "SAjLpQR2FdabxPMqthQHZ0piQV64dvrmYDikZiJWMEHXUbUeumW7DgqGH+qYiAnsKvR8y5MnthTrd8sYH24ODjW95AwNjcMBK5ig"
    "6yjfRj9yuhU1gjCgBHYt2+UJkdqWokaujHE3Jzn7imIOP0bFAlYwQddRd1q8zyn4UQOGW3YgBHad9WkLO1xaCfdfMsbPCiX8266t"
    "Sm/3zmBWrZZY5Wmm8yk21uMZbtgXC+HTpLpuloV83/YP27u8896Dyof9XQArmKDz4Jll3/h+h7tKnvqXYwK7Bo4xF15LrHWPl0mi"
    "Zel3vqXpPeWyaThgBRN0Htx3sDKsHftHcRvtRQjsqt7QTMQ2qaZ7ZCOJZs3MYJTyV6l6wROwggk6Dz48Uh3Ona7KTqmZiAnsMvtp"
    "Kta9qaqLniwJc/Ma0MrYim3yswesYILOg/d2OsDT5w4sSB2vMIFdXYxMRfgzS53zU035G8AcYLmFIztsXcaxggk6D44Z1hD0Hxuz"
    "dHVkwAR2dQw1EfeqW+qmaCXxbE5D6GjchHkFFnCsYILOg9YfXCHyeHNmfnsxIbBrx55KImBcFV2kkyRGHWoHhzPfKpuDC3jD/Hoi"
    "IeFftvGr+o0+cBJdbB4yTQcj/YKqrsKvVj6z3CO/qy9FX/hAryyubdoZQp6HCGPnbWDnYK7H8+7D20yUnZ8BLVvLHfF/fH7xYa0m"
    "8aVbuwBWMEFnZ7e5tnC5zxx+QZ1rMYFdxUVacazzdFhzVRKPo+2gzHMuL1HnWqxggs7O1d65QWbuEl5VnWsxgV0jvoWIANNpsCZK"
    "EnvGNYVO3ZfyKLUjwwom6OycZqGAhWY1r6jmLiaw60fPYGH8bApUMUjCe6ACsQNW817qXIsVTNDZuf+KKDjxZz1PU3MXE9j1qXKQ"
    "MP44GR45SaLf5SjIVTbwMepcixVM0NlZkxAP9XZu4ivV3MUEdhn/DBCZ3pNBSZdEozHxsPrCJp7tU8Cxggk6OxfXT4LCP5t4p1uL"
    "CYFdN/wChOvWSZBYKPfp14wxUo7WHgHvb9O9tXjeHfjHXWn4Qif6j5Dz+bEtZkrxtgFQW60orGCCzs59H2Rpp3cdBObnKYFd3fs7"
    "GJJSwoT2ZHkMx+3a4h/xMFP9drGCCTo7Tws7GXpvawIEllACuwLaTeDJncNF/W8yhr67jbbq5kjYomYJVjBBZ+c5QRtyliVEwtxc"
    "SmBX4Z9SHrQ4XKxrLAn7qLrZy81D4KOcz5FCCDI799zVzXC3NAgy1YoiBHLtve8O/RzDRUqkJKbU/JHTapszNDIJB6xggs7OtQpW"
    "GH7cbgjzTlECu45+ToRZb/RiQF9J6HSNDFWuVIYa9bsBVjBBZ+ejiRsM6z9UB+3HaEJgF97pqNF4fRyhTI0ewy6kttXiPfR43/zY"
    "7JYsuiTo/36/mn07XOHJQ1lW7cUcK5gwX9WKZRwO1tkOkL8BOPUdrCTXTGUBPSmBXeahrdmIK/8/xtDbdkpnQ3fWzraMu0W2Zbtc"
    "tbp9777pahe1ZsfyQ3Tdj3zVrQyrwZKKFZ3XsPLfS0Z6KtV/92dZ5wo4VjCxM6E6W3daq3vVUP76calKsbbVgoHM358S2LUlgitO"
    "n5lu/WNJzFhgpBy2H8EOqFWLFUxMH2pQsp2Z7tUM+ZcX5aVr+xWOZHEzKYFdJQMaK1lDdDqf1jJGoeVb7nZkrtJlRCyYZTcULU9/"
    "Zw/bVdTjXityta2IGGamWzZA9leFXUq5666dyrbsGMAKJmhHNiy3Ari75ivncsMJgV27KtYQFt9Mde8+yd4nfoQxvK9VoIy0DAes"
    "YIJ2ZPZ3q8Gxza8UrzFehMCuycttRMBmE927IZI40sMaTsWUKilXPQErmKAd2byPDtBrdkUWddqeENgFcdaix/hKuoQHsgOY0dYR"
    "tudWZNmB9oAVTNCOrGqxCzSoYMPavi7jmMCuPdHVRMaMijofvSSCbVwho4EN61SzjGMFE7QjC03zhIWzHJm5mruYwK7ScVbiRa6x"
    "buFKSVxb7Amr/nFkDkEFHCuYoB1Z6WYfCP/swnQ3FxMCu6KfVhXRfsa6QXdkf/Vtnw/Y/nBhHrMXc6xggnZk0zr7Q1dHT+Z4wZsQ"
    "2PUis6pY8LCC7vsI+ZzXr2txsGr+IyVGrY81Re5ievQB9jOB9m1L412Es/48a14m/45PcztCtWt/lR3qXIsVTOAOUKP5+09H8Lj9"
    "V/k8ixLYVejjJLY0eMCcN5Z/VyMe8gqjN/JtM2PhQryvSGudB2Pnmetxzxh7Plh4jV0PG7bKPrHZu598ztksXjQ/BrCCCdpZ8vRq"
    "8KzTOv6dhxMCuyIKAoUTrIWf3pKI9bUG4+D1/J9K4YAVTNDO0jDOGc5t2MUj1VkNE9jVyyhA+DRfAz/2SKKVsQv4RezmfYo8ASuY"
    "oJ2lR/tAcJxwhKerszMmsOvcCD9x6fYqSHKQRLstgdDr4xFu6msPWMEE7Sz/3dgG9p7O4f5qn4gJ7Lrn4ivWHVsJ2omSuHSzDYyw"
    "MPC36hoHK5igneWSFl3hXuwpPkutQUxgV0MnH5F5dQWsvC27PqVnV3gy4RRf66euP5CCCdpZDvrbG/a7n+Z2au5iAru8ejcX29xX"
    "gHCTxAnTPjBNe5ovy1zMsYIJ2ln+2DoAprBcPkatQUxg14LX3iLg/D9gOkYSVk98lSFhabDCKozj56PwU1v4SSuNpsKTusq3r2Pg"
    "svDmWMEE7mo1mvej3mo/x46F6QWUwK5ZLu5KYk2dmJMnY7wcYKR4uYyAO+pfjhVM0A75QvsMrSUfCb9vUgK77jo4GJ5E6sXK6pKY"
    "7b5Ee3zUIKjgW8CxggnaIf/YUjvUvWoy7M+jBHYd2zyOJ7/Si69xkigT2aHLnyVA+6plHCuYoB3ytKV2Bt/MBBhUQgnsWmX7ils+"
    "0wvL5ZL4+HVdzqrzkbBM7amxQrpl0iHfzlhhmJfZvrynxgR2mShNwdVfLwbnyxgr5nczRM8JhlrqyIAVTNAOub/tNUP0zEA4PdqL"
    "ENj1d3EfOHWTiVPvZIyegSsNpvsbQX+LcMAKJmiH3PzAZ8MS+wZw+gwlsKtXyRwwPqUVjytLIuvHesO8gZXB6EAsYAUTtEMuebRa"
    "+3hIBrM+48Vx37Z02QFliDnThT79/J8eLu/2Ku3xHhlsSr43xwom2pa4Kuc+MN2pR7LfnW5VLbTQYRzbNJcS2HW3qrvhUCedTr9R"
    "dpZrv/zUpqdEsEv+9ur6MoKty1d0V21+6HC3PDvRltXU63TTdsldevZqT/13Qnd2UB1FsYIJ2lOHTjys7Xg1nrlaUwK7Wo4FpaG1"
    "XvfcS8aIb1ys3TVkIKurrraxggnaU4d5B2pXvRzETvpQArt2hDRRejC9rmSj/FQuP9K1CoxktdUuHCuYoNfDzW51dqV2o9iWTEpg"
    "190gdwNc0ekOmcoYi0ZWC/1eaxwbXuTNsUIIcj1KGg81ZO/OYEYLKYFdx4aP54kXmW5tH/mp6iblaT3/F8QmXPaEnU0i2bsdOt21"
    "2j91+GqezLFjpSV63baLci9n7+KfWteKEaxA7Xexggl6zRubzNa2cIxk83wpgV1+34XybkyYLmSQjFF53WFtaFY8O66OPljBBL3m"
    "D76XhE64m8AOV6UEdpX0dFMieobpvN5Lonh2oPbi+UHstzqKYgUT9JoP1i/JaeiczKb5UAK77k5yN7zboNcNTJQxFlZbmW2jjGKH"
    "1bkWK4Qg1/zO2wWGLRtGsmOZlMCuWNMJvE57na7aOUlUshxqsN2Zwfpd9OZYwQS95hvGa3hN67Fs8WJKYNeqL895WV9FN6WujNEy"
    "d572SnEjNss8HPDZAjhj8FkEaifjmaftezaQ1VXHXaxgguZVjcxQ7ZSdwaxloSchsGu6yFW2ubTQJcyTMSo4z9aaHWrPHqrzB1Yw"
    "QfPq2csWobZXI9mN5pTAroEXmyqZ58N1U91kjBOa0lDbVQnskZqJWMEEzatE8Senwo0E9rAqJbCr+2N3Q9qpMN3e/fJTObXKyulf"
    "KZmtVrs+rGCC5lWb6VsMt1oNYtb+lMCumn8m8Ow6el1eAxmj6NwCQ6VlI9k2NROxggmaV4E9zLnXreHs5ExKYFePaS/4uUeK7vNU"
    "+aliR2t4TtWxrFgdr7CCCZpXHZ6G8/yOaazbYkpg11HhAvscQ3U7bkmixOlcaNoxZ2YwCQd84gXOGHyOhkbz4mSodr95MKurrj+w"
    "ggmaVzZHF2b3Mg9hM/I9CYFdA6d7KA3TW+q2RsoYsTtah+5NimQ11UzECiFIXtm+bWZoOzeStW5OCey6m+BhSHJvoatYKonZzX/n"
    "vFmWwF69KONYwQTNq6iRxw1/8+LZzKqUwK6QxpN4WnCYrspQGWNUwBZDYeNBrIo6JmIFEzSv9N42/GvnAWymHyWwq+nQl/zePqbb"
    "+VAStVqa89giNa9uLOZYwQTNK5OVEfzmpyGsx0xKYNfRJq7w7Z9QXS2tjOF5P5zPi05jpur6AyuEIHnV9NUUfjF9BPucRQnsuvmw"
    "G9QxCtK5z5Wf6tSb2vx+aH22u3I44BNh8Ekx+JwZjcYosw5/EO3PjNQxESuY2BXyhpf+G65Lmi3Pk3mwoj2f/q8Pi7jmSQjscunZ"
    "FApn6nXzw2WMTR06cO+jrZjjGXvACiZMvjSBS/8y3aB6MkbcrCn8uFc4m6VQArtMbBMg4nCo7t11SYxvMZ0fSO/Egl+Xcaxg4m9m"
    "D2gaG6JbuVKechNSvIEv3BPFTB0ogV1DTs2AX50CdD4dZQyTxZu58I5nt9QeDiuYCC+bDj1a+uteG8sYm8fkcjvnrqxFICWwy3jo"
    "Wkgb6K17wyXh2PYMTxK92XV5xwQpmKiTvwaydzbTBSbKOn+09zGvMyuO9Z9JCezymn0E1v100yXWlzEm5T/mH5v2YXnqmhMrmMiy"
    "PQIPZ7vpPmTLGvy6WAP8YTfWdj4lsCukUhF8q9JI9ydDfqqP7Vpyl7Z12TarcMCnGeGMqfvHHUyHhusWRMjfyGyzI/j9aB92L80L"
    "sIIJmleBQzJ459rN2JY7noTALv93PSG8i6Kz+S6Jds2mcHYjjIXl2QNWSI6RvHqVs5rfjlZYTCglsCvraCas2hGoy5wjYzxYs4Eb"
    "j41it9XVBFYwQfPqw0MD37mpDattSwnsmtp1HTwc2lznW0XG+NIxlztX6coeqZmIFUzQvMob9JC3+RbFvvtRArug3VEIOdRUV2u8"
    "/FQTVz/mHSbFsR/qagIrmKB59dJIAw+0HdnSmZTArocziyBtTCPdkEeS6LxQA7oH3dgHdT2IFUzQvBrmYgVFs6OZwzxKYFdE5cfw"
    "65yDbn6ojLH4ZT8o/HxRCVVz94JRc/Gn6grmZGGkx7+qbol3F4Z7+5l+l/yV06hFT+j2842yU60PrGCC/vb6qlVPqK8S8xZRAruu"
    "vHcWCfwcG9teEoPWdYG7jyuxYHU2wAom6G+vKRu7QIlKrFpMCew6VlRXTF9UzO48kBVlUVQLppqNUezU2QCfQYbPJsMnm2k0aeZN"
    "YRhbotRUZwOsYCKpjbeY/vEI830k75iIhGbg6pSubCvwJAR2BdUMEB6j1zAbvYyR4K+Dzb8XKg3VvgQrmBgyy09scVzNJu+TMbo3"
    "bgkV9g9W6jWnBHYVjwwWfjZTWYFV+dlt7p1gqWemMkntkLGCiX11g4RjvSls/XAZ48y8WJj/p5Pia0UJ7CppoBXmcR3ZlquS6N0l"
    "ESY0G6IwtUPGCiEsQ8XORh1YBXdJFGmSwGRvM2WXPyWwa2kTJtxOOjD7OZKw9RwKTXq0UirJ3/SRgok9CYpws3Fg2mJ556ey2QgQ"
    "eRWVvJmUwK68RTrx+cFlhQfLGDwyHfrXslPs1GzHCiaKa+iEb+xlpdJMGWNqqwyY1GCLdtpCSmBXZl+92JEYo8Q8kcR2gyNEXmqv"
    "7KsYDvj8PJwx+FQ+jeZ2rhdUGDdG+XekFzmvDxM0rzK0vhD6rbUSr3bImMCuWer3luAzjcVvkMRw3gIW9xusNFIzESuYoHn1xtAG"
    "nD38lbvNKYFdWZMU0e5BDLs0RBKto2JheUknZbyaiVjBBM2ritu7w8179so+a0pgl0+4TtTe6Miyvcs/1b/94fXBZsovdTbACiZo"
    "XsWOGgjRW55oSwMpgV3WvfWiM1xRVryUxLHfw+HApYpKfXU2wAomaF5lHx0JvkkztAfmUAK7Ih/rRUlpjGKxTBL7wzPgm8cW7SF1"
    "TMQKJmhefa45Di4tTg09sYQS2PXlul5oCzJClmhlDKMX9aDLnXrK0wrhgM9+xBmDT5RUv921PjB1fGvlg5qJWMEEzavUkAC46W2n"
    "bFTHRExgl3cDnXDb15n1MZIxenZqA101/kqsmolYwQTNq5kJEXAt7a/2ki8lsOvQVr24e7Yue35REiUDusPXO/ZKsZqJWMEEzatv"
    "J+Phmn22tsSWEtj1Y1yYqPHlqhK6QBK2XQfCmFNPtBbqmIgVTNC8sr05COp2aK9NC6UEdlU6GCaaXOikPA+XMRx3jYStk2do96hj"
    "IlYwQfOqSrtRkH3geLDvXEpgV6VOYUL7MyOk/XtJxNmOg53fUkM7X/LmWMEEzat2ZzJgcH4XQ+WllMCutH56EaBvz11XSmJly4Yw"
    "78dLbbJxOOBzS3HG4NNQNZr81f7w56mtMkrNRKxgguZV57ggqJdwXptU5EkI7GobHS5mN6rH0npLIuNTOyjq/ld7T81ErGCC5lV2"
    "5UjYmrlQaxNICexa9zRc+I67rvR3L6+ocfHQLChbu1/tkLGCCZpX+woSoOszM+3zOpTArieXw0WJcRdl1itJ3Dw2CEx2t9e2UjMR"
    "K5igeZXTJBnuRCo5tgolsMuvYbjQdh8X4rpWEteVUdDsXxHso2YiVjBB86ofjIQ7M6cYzs76D4FcIU/04tv59vzf9jJGpdwMOLu/"
    "iyFWnZ2xggmaVyEtx0Ky0WdDznxKYNcBa514nXqR//NdEo3vNoK19Rdq95iEAz5zF2eMT0BLMehofTbmaflpuicDwdHxvLbfKC/A"
    "CiZoXnn9Ewx657bavMuehMCuJotbihrRN5XvBkkkrm8Pv7cu1J4+bQ9YwQTNq01nIqG/z7zQFaGUwC7jkJaiydyuyqFMSSTNT4Cw"
    "webaz6VlHCuYoHnV6UECzCs9m+PoRAnsyg5rIbR3x4UUtJAx2lVJht/dQ3PaqZmIFUzQvPrfoEEQZPePoXYwJbDri5pjNXdE8pM/"
    "JfH10EiY3meKIUzumkQKJmhe+ViNgLCqFXm7WZTArqXzdSL020XecZckisLGwryPnwzH1EzECiZoXjX4Jw3SWiq803xKYJf+tlY8"
    "qFMHWncr/3b7xsHcxDLeQZ3PV3F38e3+ftg504ScrV39k7MIqXoOCr3lPgDHS27QcfszPiTEHkyDvUXS5CPw1MJMX/OElzj08RDE"
    "jK2sLw1tIt5ZFILHTbnLop9bMDx68J4nqdccK5jYYNJY9MjKhwpBkgh/4Q1tj1eE1k6UwK5h/9YTicMfQvUsSTRdqMDj9WZge76A"
    "YwUTPl+cRLbrAxj2Wu6y2HrdF7x72QGEUAK78qvbCyeLTzC5jYzxskiBITVqwxB19MEKJt4MqylCKn2ErStljA53feBcoQvkzqQE"
    "dsXdqSoMryuI498l8dQrBN48agzzC705VjDxa1xV8WNZBaFpJYmz3l4AUX7QcQElsKvUv5JIe2UhRm2RxJPKtWDF+5s87IYn9Pnc"
    "XCyIOAbPFpjp8dWcus9NHLtQBIYkud/n+GQ3MKn3jLfPswesYIJec8/LDaD3uV/8GKMEdg00ayDOVX8E2mYyhp57Q825FaHZmzKO"
    "FUzQa34vtTGsnl8NsmtTAruiP9mLwpGfoeE7SXjl+kJEKztYoY4MWMEEvea16rjB5QENoFkgJejVtBJJY41F1lZJ9LzuA9uEC0xS"
    "RwasYIJe89C/rhCQ0xx2z6QEdvnNqyR6tKoiPLvJGJXVa54X4Qer1SzBCiboNT/RrQEsfqaDJ/MpgV11VnyFuFU1xKZKMkbjIZ4K"
    "1Eli4epfjneu4p2ydBdrq5fhimfUUNZDrQ+sYIKegb1/upES7jyCrcikBHbRXazXv9oqTQLGsoW2DmQHBCbwmdsaTUv4pe2fkcbe"
    "nOhHCOzCuyE0mjoTNEov3zHsZPdYjhVMHImZrdSMZP8Xo+a0NdpamyYwj9FzDZjArv/ssngVqX1RmsFOr/fkWMHEP6ObhC5w0f1f"
    "jCMDroWuujyR/ch7moMJ7KL7AP73PSa7cOFEttkl1YAVQmjcDROb6HSvAmSM2DOhhkURE9m9TymEwC56F/nz5VBDX5UYWjvVgBVM"
    "fNON5xGbma7VNxljy7wSg9Gz8axrWQohsIveH3TMKjFceDqe9a2fasAKJu7lPec+IYrO7bD8y9snB/EqnTPYERNKYBe98xOnEhYq"
    "0dU01YAVTMxf4wJJn0N0HVPkX95o9zjec1Ma2/8mhRDYRe8V3dgzjnuoxBPjVANWMLH3QDeYejtQd6O+/FTfvy7h1dJHsr9WlMCu"
    "qIeDwHVCgC6iryR22m/P6XTGmTmqaxz89gB8BxO/k0CjMd47Kzt/YDC7pa5xsIIJep9zxoRehm7Tg1l2vichsKv7Bw/Dk+KWOueq"
    "Msajs14GQ/1IZq92lljBBL3PeSrpvMEquj0b70sJ7OrxdxIfsjlc13un/FQ/Xx8zdJ0Zz9apq22sYILe57S5VZM/PdidxVSnBHYV"
    "HinhE4t0unfuMoa7xoYL/wHMKL+AYwUT9D7n5P4d+N+u/ViPUEpgl8stV1jeV6u79I/8VJcnRnDHkiFsjTqKYgUT9D7n3R3TeWqF"
    "wazhXEpgFx8YB73GBunWfpDEzGdT+Ja0Eez1ZW+OFUz85z7n8E284pRU1nI5JbBrquN0yDb3050NkzFaHV7D08eNYMcjjuVgBRM0"
    "dw/23cJbXxnGihqnGjCBXcZG06Hssa8u9bYkXv2dZjhZ0ZnFVAgH/HYNnJV3V3oaTC+31rnayXssZ94nGKxeBLGK8pwipGCC5q5V"
    "gxuGag2C2PwCT0JgV9O/kzl0bqmbckESJ1adMwx+EcH6qtmOFUzQ3O3hX4dXb9Su/IQ/TGBXYYdSXugTpmuRJGPsmlqT30vrzk6q"
    "2Y4VQpDcNfKO4fHbYtnnmpTArr1nG8Ol8YrO7rkkcrw68MSQfixD7Zawggmau0WZM3ivHn3YMIUS2DU6sjusCwvWdS4fSy6tms75"
    "92TWTs12rGCC5u7zkC2885f+7PVsSmDXtuHTIXGyn85/u/xUQ1I3ce2kVNb1gjfHCiZo7o6eeJqf6T+A+S+mBHZZ9V0DLKCZ7uwf"
    "SVx4D7x+8WA27U+KASuYoLmb+gH42/uDWbQ6tmMCuwLC1kBWtWa6lPI3Ilwoeshnn+nHmnxOMWAF3xOmnyrn4mO+1aMPGzPPm2MF"
    "E/Te9tOxp3mNfgPY2nxKYBf9dovizvDk/N4sVL0eWMEEvUcf6r6FXy/tz5JuUwK7aJbUPbKZD4qIZzvU9TlWMEH3GtQdOIPP1/dh"
    "B/MogV0025+Nm87/7u3EdHXLSO5igu6ZCLrYkX9JjWVLX1ECu2jVXirtwM3sWrNbQfaAFUzQvR9bj9TmI0RbVu80JbCLjj6MOfAn"
    "z/1Zu4ueZCzBBN5rotEMML5uKJoeyErl7+2IwC46is5Nf2AQExqyZfKEWKRggr4T6f2vqYYZTRqxkwZKYBcewdXZ4NQ9Ptg+iT2r"
    "8CkHZ3vmyf3wJL2pTu/14z97JvqvfM1nz/ofM/FKNWAFE3PeHoYh/dx0KzvK+ijL+csdFyWwI79SCIFd9G74AcNffm1hAhtgnWrA"
    "CiZc7xTCr5cNdVuty+sjvCp0j+7M7n9JIQR20fvnDVpUhcoqUWKRasAKJnrdegTLtzjo/K/KGJ10NeGXJoqlOVACu875voBeh2vr"
    "5laQf0f3PlOVnK8Dmai4geO3GuFnH+kbjnp9mqIM3TWYGZ9cyLGCCfqspaFLirIoK5GNCSmgBHLR08XudUpR5oxMZEPUGQcrmMBr"
    "UY3Gc3WM0nx9LKtRu4wQ5OlMcnrrmrkxyrf/xbIH/zmLFRN4H7pG0y/CT7E804atC6HnvWIXPYX2gbOfEtGzDdOeoWfKkudH0U5p"
    "jSbvsq3yyS+ALb1Bz63FLnqabso8W2X6an+WlE7PxsUE3mer0TgElmhTfRqy0db0/F3soqcCP055qY3q04C1OEPP+MUEfcvYyPm5"
    "2v9ts2MWcyIpgVz4RGKNZnFFa+2cUDO24xU9qxgT9N1n7MX30NPRtkx7IZoQ2LX0wmcls6CtbvAvGWO1ee3sKt3NWO/K3QArmKBv"
    "ZNtVuC6Hb6/BDnfvQAjsyk/poVw7G6Gb91SOV13eOBri55uzfmaxgBVM0BGu4dh5hh8VrNnFoBhCYNfd+zGGXXHtdXEX5S6kgcH/"
    "GJ5/q8LW3+oMWMEEHXdtO70xVNptzlo26EII7Cot28CTp0To+h2Ve1hMKj4xrDlZjfmzjoAVTNA35L3cVp/beldga/d1IwR24Tcq"
    "aTSjvtrzKWW27PyzCMAKJvAeNo2m/ptAXvaPEdv8bywhsIu+qemeUwt+f5Iji1JzFyuYoPvh6nmlctv9tZnOnhLYVbdaHxjiq9OZ"
    "aWSM38lj+YiFXiwswwuwggm6H25x36V82uCm7PstT0JgV6d7M2GTPli3a6/8VK1jV/MF37RsrDqWYAUTdD/cnjVHecUxgWxTACWw"
    "a2L6ekgy+OhmtJIxmi438KdD2rC9b8o4VjBB98M9tbjDLTbo2cIalMCuY52PQcOD7rpeBZIo0j3kox9GsfVqR4YVTND9cMe7/eKj"
    "i1qxUT6UwK7o/10AUzdnnbP2b/nqrozf8+vIMtXVBFYwQffDXa5WFf792prVy6QEdiWufAzHPB11mo3yU01taAX/mxXN2qmrCaxg"
    "gs7nzU0doaKuJTuxkBLYFfLtK/jk19C1/12+i/VPHQi71461MH+RgxVM0Pl8QUBdMD/chg1qovYliMCuY6e+wpztNXSfF5XvYm3V"
    "nXeL/6Ms3RFL3n2GM5++yezJrcE89HMttvVsOGCF1AqpD837Ofx7Gzs2tzolsOt009kwxy5U17WHJBpeWcJtX7ixHHVWwwomaH1s"
    "KdrNI+47s+FXPAmBXcY3NkBmOz/dDV8Z46DbUR5cP5CV5NoDVjBB6yN+xyX+KNubVfalBHYN2XwcPn3y0HWvIGO8NNzm6UP17K26"
    "PscKJmh9jG/+ibc+HMSMrSiBXVnzL0KIk4tu4Gz5qWa7/eJjjrQqf1YfK5ig9dHaxAJGH9KyUb6UwK5tc55A4m1H3dE/klhnUhWS"
    "37Vm4WpFYQUTtD4OJdeBoDxteUVhArtMl3+DfW62Ot5Hxhhd0RHeKi3ZkgJvjhVM0PqYUdcNflUPZuvmU4LUSmwlkVSviq74hPxU"
    "PUqbwMdnCptspHbISMEErY9hKnFLJX6bUgK7egVXEruMquhmRMtPVTtyAg968V0ZOb4rfTcgynz6rq0c1zncfoEte5oXTt6chQla"
    "H80XrOfe1a2ZqEIJ7KLvDItqtJuP6+bMpqV5kTeAYYLWx/jep/m78U7sl1rXmMAu+u6aEY0vcbMkb7ZbrSisYILWR5e9L/gGVzd2"
    "pjklsIuewH/y3kf+d1oQ+6iutrGCCVofFtYmsK6kGTNYUQK76JmZJm/Noc9aLat8toBjBRO0Pnz31ISv3IcF+1ICu+jpYsZ96sAk"
    "rmXN1YrCCiZofYT8doVg3pxZzqQEdtHTL9LruEFltT6C1DkKK5ig9TE61h80dT3Ln8HCBHbR8zJmTvSHDiXNWcu3KQasYILWx7Xv"
    "PtDN3J8tv+GRgwns+rDHQmRvrqQLulJeUS5h8MrbhY2rnWr4NqCquJVbQbfe7I+u5r92ol/ZB2YNf3TPNDXFdN+PbGCT8h7uSXu4"
    "m2vPZmtSDVjBBN2zbV21PRRXr8GeqbMzJrDr3v9qCo9rH1lqa5klb83bwyaVmKd+u1jBBN1JviO1DYT0t2QZcxcTAru2VLQX2juf"
    "WJsvknBMbAM1Ey3ZPjVLsIIJeraISfUwmHGzIuunLSAEdtV8ai8cw7+w0vL39tX4qofThRXZvPMFHCuYwKfZqas7myBItvqilDmU"
    "EQK7XP/WEl8svjHbILlftJV6Peap12NmtVQDvgY+O+uKN72L2eSRf/9zPQJOxcDp+dXY8wapBqxgotYbJxEp7rDbWeVPpWzsCoWB"
    "FuyVXQ1CYBd9FkA7Nxaso83YmxqpBqxgwlDkLOYtPsdWecpPdXh/L4j3/aZU/pBCCOyizzR8VIk3zb8pPrapBqxgwjXAXXw5vJ81"
    "fS1jzFqXBJnGt5UL31MIgV34eQq1bz/fD1ocfqTU13YKwQomEs55iSOeG9mnZvJTNbszEFY0v6hsa5xqwAR2Wd/zFqPe/MM+dZFE"
    "0jwPqKEvVtZo7cE0uo5Y6vGDbSuoQK7zmw/1hbbsEbuQJa/5o7uBcOrhZ2VNaRnHCiZoXvWpooe59vcUsKMEdsVVbCyWhhew/Z1k"
    "jIVL20HKqLfKbbX3wQom6ImL+QNiwNn1qtIzgBLYNWe6h8irepDdsJAxJp2Lg3uzHynBtxdzrGACP6Gi0Ty07ANn6p1W6sykBHal"
    "j2ouPEasYLcNkhj/rB/0/3JRcS/05ljBBL3mPdMGQ3bpXkU3nxLYNfW6v+g3eRIbmCyJ1xmpsMxwTGn9LcWAFUzQa/5HJZ7nHFP+"
    "qr0PJrDrxG5/oe03iWmPSmLSHicoWZGrvLvtCa5XHcSW9b/Y9ihjPc6YxM4NReTHJ6yns9yrttrbA76U3leuqOtarGCC5lXgWV9w"
    "u35GWRlICexaF9xEaHMK2d33kii9ooPtb+8qoWomYgUTNK/MGrQBT2OhFNpQArs+TPMUz+wOsTEHJWHZLgZG2F9Vuqo9A1YwQfOq"
    "rEEc9M8+rLTxpQR2Tff1EVvsV7JDyZIYaNQH1tU9raSoswFWMEHz6lhgElw6s0l5P4MS2BUXESBG3ZjEGtSVMaJGDgb+eq8yQu48"
    "QwomaF7FvxgG52vNV4rmUwK7SgqDRTCPYkMKJbEocCTsXr1MqfQmxYAVTNC82qMSb1cuUz7bpRICu9imYPFqYRQLt5Mx+m+2gkbp"
    "W5T/2YZD5JS6Yl78XxZ92liPs/JEaSNxw+s567VDZuL5Rk7gbpureI71AqxgguZuoKULvLDYrUy/6kkI7PLe4yYsJ1xgg6dIYng/"
    "X9gz84wy57Q9YAUTNHfbO4dAm4G7lCp+lMCuWHXU7tL3MNsULWOsfdYaYv8FxU3tkLGCCZq7C1tGgUazWZlsRQnsSgj1FR5/VrKu"
    "NjKGlXEcpO4/rBir4y5WMEFzd9/1npCbvkxJ86UEdm2wChRdek9mvwslYWiaBNFq7kbeWcyxggmau/3bDgbnw1OVzzMpgV1xLUNE"
    "95bRrPEESQx+Ogy86sxXWqprTqxgguZuZe/RcHREnJI2nxLY5fdYK8bursOmuckYs4rGQJ+jA5WAXykGrGCC5u4ilbA5PFC5oGY7"
    "JrCr+LhWDJpdh8WNkoSh+Th4MdxZeaPGwAp+Mox+qgEd0sHC1k75uMibYwUT9Am3Mo/RsDwtTjG/QAns+s+3GzwUKndppYSr1wMr"
    "mKBP6n0PHQxJR6YqL25RArtolpSMSoQbvkOUSz4F5Jpjgj5xmHu4J7iNWKYU51ECu2i2X0nuBH30mUpO1TKSu5igT062Mo2C0083"
    "KSavKIFdtGqbr9XBVa9Fyjt1JYwVTNAnQMeIYPBrskvZkUsJ7KKjj/2GppC1eYnS/oInGUswgZ841Wimj3cGr2W7lKQ0L0JgFx1F"
    "99vZQrH9IqWDZTgZEzEx5KCLsNz/kpnUlTEyS6rCMb5Zyc2jBHbhEVyjyVGzvWios2Kl9tQ42y1KmTjc5LJy56rRf56cHPJ9PJzx"
    "fKqtUkclkIKJW3t04vO71co0jSRiDkwA91MF2nVGG3IwgV30mbje+ROg7fZ12it1Uw1YwURKsF408Y9RXDwl0W7MRGgQ9Dh0ibqa"
    "wAR20aedfFXiifPj0A1VUw1YwcSpneq/78wIGVD+l3snTIQcn4aGcR9TCIFd9DkWc5XQsIaGEnVVhBVM9AjRi1vV2/NfT2UMhxoT"
    "YEOf+4b2P1IIgV30CYX31SdAZP/7hlh1hMMKJh6+YCJef5GnhJc/w7siA94P9OHOP1MIgV30mYZlKhEw2Ifb1Ew1YAUTpXu1YuuP"
    "2lBnU/lf3igdul9I5F71KYFdy6eFigkVmkFygSRidgbD9fmezNUj1YB/s8C/UtDfS/Kdw2BUcxc2/Df9vQQT9LeMmxv0sC2tPruf"
    "5c0xgV30nFSLdXoIV4nIAnrqKSbobxnf0hTYsaA2G/Wfk1Wxi573GjZYgdVzarMOt+nprZigv2XUOxQI/1tuzXRaekIsdtFza72W"
    "B0LhbGsW/59TaDFBf8v4MqAZfDtowr7XpSfdYhc9f3e3TzPIWW7CBpfS03QxQX/L6HLcGe7V+qyYa+mJvdhFzxE27eUMH499Uurn"
    "0VOBMYHXOxpNrOo8uOmW4nOHnjyMXfQ85GV6e7C1vKX4jaWnG5O1OupkNZomwgyMko8rN2zpCcrYRc91HlDFDOL/OaYU5tFTmglB"
    "RmptYhl3ydysZFeLIgR24TOl1Tpf+okPqz1R2fuJnjaNCTp/nE6sBIsPzVC+3I8mBHZt6OUhtnQtZgtOSqLPgV88/VwPxbpqN8AK"
    "JvC5DRpN1YrmcHFYgrK2TwdCYJfHGz9h6y6Yi4d8+oydqgC9JoUo5uaxgBVM4CfyNZpbty1g4trGipESQwjsqtVaK1rO3MCmbJAx"
    "uuZVhg1THZW3+Z0BK5jAz1prNKF3zSG37xPtOK8uhMCuPV3DhceJyWyInXzOq71HNdD91Sie1h0BK5jAT9FqNCdbm0Jz+1Tt5mvd"
    "CIFdzyzaiJ8uYezEbBlDF1ULuloVaAePigCsYAI/H6nRTHY3g/T71bWvP8YSArvuxbYW5mkNmVOcjBFV1hBOH1+gtRThgBVM0Gct"
    "7293hkvah6HrqlACu85NbC2uJ91WfuhljK2/giA2rq3WTO2WsIIJ+qzlqb/BUP9u9+B7Nz0JgV2TS1uJkt7dlJblb3YY3CsSbq6Y"
    "H3r4jDqWIAUT9FnL5BWR4Gpua0hSKIFdB/a0FNpB40O+PJLEkE0J0L1HXs6p12UcK5igz1oeexMPpzx2GUxrUQK7rl0JF8sfRPGe"
    "5bn7qP0gmHt+uSHmbAHHCibos5YBCwdAUpMqvJc/JbDrYbxetL99ibvHyRj1K44A0+/GfLe6msAKJuizlnZBQ2HZ0FZcnriICfIU"
    "ZSdFmEypAxoLGaNgaRr00io8pNCbYwUTtC8ZDCPg2qNJvN98SmBXpexg8aBnFMw4LgmRNQau/RjB5w9dn4MVTNC+5INZGox7P4W/"
    "apRqwAR2JSwOFv29o6C7sYwR/MYMOjuMDT68MxZ+JESIw7xM8fhjQqqocGtbcZ3fVdYdlZm480ojGDHzYeiU3HDACiZofcw+4Qx5"
    "78fmtK9BCeyafr+NGJjRXWm5RhKV+gfDrkuzgjemewFWMEHrQ780GDYvDzc0v+tJCOxq2qu10LpNCJkxQhJ9/SOhtKS64ZFaUVjB"
    "BK2PiePaQ+nYbENcECWw64taK7H9OvCZiowx5GA8JO7caRiudhlYwQStj6Xvu0PjpjZ8T3VKYNep9DDhbnWFXyqTxPrhAyDopwVP"
    "VSsKK5ig9RG3qh9czo3gB3wpgV1ZTkxcdHOAu8clUcVzKNzt2oofVbs+rGCC1scPNhgmfJ/KlZmUwK5k3xCx93kUsGRJuBhGQPfi"
    "SbzFBW+OFUzQ+hh8KhUOaDbyjIWUwC5L8BfQcRLsspcxptcaAeGH1vB/vqUYsIIJWh9RKmFzeA0faZlKCOxqvdxfTPWbBBMTJTHy"
    "sAXMLatksO3RFdZERIqSgFHKjsGmpIq6mEaIHdfjldfW8unMjS8bgemW0Tnxan+FFUzQ+vjX1hny01MNfWtSArs6dWwrtOYTQzK/"
    "lb8bUBMMg2zCDIFqn4gVTND6qNwxCICfNwy/5kkI7Br1upWoGRjDa1+WxIOa7cH+8EnDt9P2gBVM0PoI6dsONn6z5U/8KIFd9D3u"
    "jke6w7+3rXljtaKwgglaH41fxsKnelH8STVKYBd9K2LYhH4wf04EH69WFFYwQetjzMI+8Nx7Ov/sQwnsom9qWuI3GNJeTeVX1DkK"
    "K5ig9ZHfNAnaWm7mozMpgV30BP4kSIV6vzfw+UXeHCuYoPVxb/sAGNkilycspAR20TP7dQ1SYMRKzud/SDFgBRO0Pv7nlQq7n57k"
    "8b1NCYFdw5Y3F5+uLoELhyRRq3JPGOH4h7d8n2LAJxN4N3EXAWH7Ia/ef08p+Me0J+ys+4cb26UasIKJPxedxZDHZ2HduPIr2KIb"
    "VHevDJ0bUQK7fE41FL0mXYB7yyXx7GJHuO78l7vMWcwz0jzEiNUHYJq/qR6fo3Cjp4swXnQOpj2Vn8okMQ4O9SzjS/LVbxcpmKB/"
    "R37XDrDltyVsXUgJ7DI8qSt6bbsPxXMkcfJCFzDdXAWq5FzPwQom6N/RLasTLOxuBUMcUw2YwC6/U3XFtdH34cBNSexOag3T+v3g"
    "LYMLeP5oT/Fk80FoXGyqx9/CjWqu6nU6D70WyxGu9rmOsMvmL3+nzh9YIQT5rpJvtoHkq1Vg+TxKYNfDdk6iU2AxLFNkjFldOkDh"
    "D0uYo2Y7VjBBv6uEsFbQX9SBPospgV1vrGqKXf0/wJsXknAxjoCFSh3w/pJiwAom6He1o0IEGLM6YGKbSgjscnxnJxZ4f4BTzWUM"
    "29hg8Gv+gU+sXcbxGRn4m6bnZVSOaQ02QT94c3W8wgom6PX4sUmB9ONmkKilBHbR8zL4pTZw5XwVKLu5mGMFE/R6xFxToKRubTCb"
    "TQnsoudlROtbwVJDHdijXkGsEIJcj/PNQiDvaWMIW0QJ7KLnZRwuY3Bud2Mo/ZFiwAom6PWYHxEGP/5xgb7NDuRgJXtQNeEUqhGP"
    "xv43xoqpIRC1xQOO+KSSGJiw6FlVsLEVxLWFMsZEU19w6ecHNkaUwC56okNXlQhTiXbmqQasYMK0diVxpNBCtH0vY4zxcIWHkXrw"
    "e5tCCOyiZ0AUubtCqyg9nKueasAKJnYlfoU9Y2uItA7yU4VbOUEbszbQwZkS2JUY+hH8XO3E50RJZOkrwVclj7+2DgePx77COOIE"
    "zK1orscnkyTGuYvlVy8CL5UnhezLsofoJjf5rDFegBVM0PNLYpdbQ8Ptr3hDdW2ACeyyHtxQhJs8gUunJFFvdgMwCvrFG+TZA1Yw"
    "Qc8vaXWlFrw9VRlmBVMCuzIsa4tE7VeImiuJum0aQ3SvanBZ7WSwggl6fkmP2nXBsagOPK5BCexa06KaMFMqCv9IGaOyuRusimoA"
    "WXkFHCuYoOeXKHPrQt1jHuDiSwnsyq5jIuo/qCLMTGSMr99d4cD+5vBLHduxggl6fklMpzrw7LYWls+kBHbtC/wGH37XEPHHy99l"
    "2q0BTHusg+rqyIAVTNDcNc+pAYezIiBgASWwK3rtI2ArHERxP0mMi6oNM2u1h7QDFQ1YwQTN3Uq17WFk70iwUmdOTGBXRsojuDLa"
    "QRzYL4mFb3/zpxE3uZl9OOT7eooF1a9A/97mJMM3GTsLp/BncLmluTwfrqk1HL5ewrupfTtWMEFzN6GZGZxv/JcXXfckBHaN71lH"
    "7Or5HR46yhi359UCn5GVoa66EsYKJmju9japBg6W1WGKPyWwa0WUtTDyqyT6vJLE+S+OEL2iDvip2Y4VTNDcPaqpDrU6ukCiNSWw"
    "a8G/JuLYPkuxe7ckBo6rC9arPOCzmu1YwQTN3fMhNnDKJxDG+lACu0J038Fpra0I6C+J+1F1oNkFLVRXsx0rmKC5G/HeEu5btoFD"
    "mZTALqdmj6G6xlEss5cxDmXXgB0LI2BVoTfHCiZo7t4daQIPW3WBBgsogV1Omwsh4mZDMTJPEjvcLcA/riv4qythrGCC5m4rleit"
    "EmEWqYTAroZjCqHlwYaiTTUZw2z+G27c8QWvr47tqwpcxKrcF5B20pxkeN4jB9Hpyk/4d4PMxID8yuAQ/odvUcd2rGCC5u4haw0U"
    "tqsMUy95EgK7wufaiC89TMTHDEkcOWsFi07YQDV1lYoVTNDc9Z5VCX5ucYATPpTArkp3TEXE8ariZlsZo/lDG1hcxwXOl5RxrGCC"
    "5m4Pf1PQmTeDtVUpgV0Bu3/AiXF24m6V8r/cwwaG2QXCWbXrwwomaO4+01WCQUV6iPGlBHZ9qvcESnc4iqFnJbHutSVcMGoDch8y"
    "VjBBc3fU/TJepV1HgExKYFemaxE81DcSHmMkcVLNXR7eBQ6pYztWMEFzd5H2Hbd+nwANF/2HQK451w/DqNZuIrehjHFi5Hf+IrYX"
    "dFZXkFjBBM3d3Ss0cK57AlxdseMkJrDrmJEB6j93Fbval1fUq/u8OPYbNzcPh5qL64pbc/9App0FyfCOP6qL0r2m4lOZvILZvct4"
    "/CVTSBvtBVjBBM3d5btf8+Rb1WBqoSchsCvPyEy0/azOvfck8TWyEvD2DlBXzXasYILm7qO7n7ky1hlsfSiBXfvSfsGxpTWF8U5J"
    "fK9pCjuveMG5V2UcK5iguavZ+IX3eR4I96wogV2ZKU8hfUldUSNFEiW+laDHXj08VbMdK5iguTt54DveYHg7yPKjBHbN0VyAeZ8a"
    "icouMsb1m2X8oLYjVJU7fpGCCZq7Ey4/5oGT4qDJLEpg17c2R0B/zE1k3JREvpq7rm8SoFmBN8cKJmjudt1zmd+b1g+uLqAEdh3q"
    "sQaOPfUS9SdJYtk/d/geXRJ4f08xYAUTC/YchkoN3MSyVJm7icvv8JsqcU1dpWICux4GrQEL7iW+FkhiTnAhz7EyhsxK4XBtoa2I"
    "aGImVo60IBl+rqu5SOllLQb0spD3vL6V8sudqoH7KDVTkEIyn+Rulfq3+dud9rA435MQ2DVi9R+IfmYvlobIGN7DPnPu6AzilD1g"
    "BRM0d+2zinnqeA/QNKcEdvWyfg6LcpyEYi5jXEn5wtfvDoTa6tiOFUzQ3F1+/R5vfEcHH6wogV3M/SJ8eOksdhVJwqrrO76xUzvI"
    "ULMdK5iguZuWeI3PrxUDngGUwK7WZkehdEhT0XWaJM4WPeZPR8SBkZrtWMEEzd0jX89wo229IXc2JbArW6wBn27NxN3mMobl3sv8"
    "xuR+8EnNdqxgguZuxKADvJFmMGgWUwK7AnpPh347fUWbu+VrtV8n+PYqqZDwO8WAFUzQ3G328wQXKuGjrmsxgV3bwqfDnim+wsFZ"
    "xijbeJy3P28GtyuEw4hrFiL/s42wum5BMjzTTCN+9a8tloHMkvrjb/GF9exh3EgvwAomaO4+2pXLPx13grFqtmMCuy6ZvATvuvXF"
    "pVWSKPYt5iYOHvAy1x6wggmau++S8ni/Db4w1pcS2LV86yU4VNdV3BwoiTnb7/GsNTpYq2Y7VjBBc/eF3yn+/FZr2FedEth1z+YY"
    "fEh1F9/dZIyUzte4/mdH4OcLOFYwQXO3ybajvP7JbpAcSgnsWp60Fj7ZeYsj/0riw+cz/MHK3pCmdjJYwQTN3c4ZW3ledn+oOZcS"
    "2JV5ZDoY1/cTmnmSSE8+wEP+JEN9tW/HCiZo7v6v8SL+c/gw8FhECew6mxAHhZsCxUU/GaN4/Aq+O28EbFbHdqxggubulHEr+GmV"
    "aFsrlRDYNcErDnwyAsWG8hpsGLGFfy2wguNqtk8daCTG2zoIrW8VkuEWrV9B1uEG4rKTfEdu5zq5PKaJE/RQsx0rmKC5O23Mbl78"
    "3RlqqZ0MJrBryKAr6jqosUj6JQlWK49bMl+IVLMdK5iguRs1bzcPfRQMXv6UwK46/zsOD/d7iAbnJVGp+imevao1eKudDFYwQXP3"
    "5s8t3Kc4El7bUwK7LKLWQULd5qJbpiS6rjnKn67qBofUsR0rmKC5+2/CCt6qc0/I11ICu5LCZsCbp37iXrCMMUrN3WP7+sNpNdux"
    "ggmau6ufzeAbbyRDmzmUwK6/L+LA2DFIzHgpiY9NFvFKQ4dBgtq3YwUTNHebferFN10bBW6LKIFdoze4wK+CEDE2SxJvnYfyvoPG"
    "wIU/KQasYILm7rBGQ/kglVhmlUoI7Oo6wQUObQgRUQ8k8aXdIJjWtIh/cU414PtOd/K8xfKt/8C93Ir/ued1yK4/NB37gFf9TO95"
    "YQLfp9Jobk/tAy1GP+Im6qyGCeyi79tuOqUP2Ax7xJMv0rdnYwLfN1L7q8dxENflEV80k76hG7voe8Pt78aBa/gj/uU/bwHHBL5D"
    "o+ZVTDT8qfGA3wukbxrHLvr+85oh0XCktJjn59G3mWMC36eQp1/oYQjc4h629I3p2EXf4251QQ8Jw27xmf95Kzsm8J0UjSbLrjm8"
    "GnCR//Gnb37HLvo++te53vBvyQU+8zR9uzwm8HnYGk2FW04Q1TyXX7xE32CPXREFgcIJ1sJPb0mM7OYEG8ec4pPV9SBWMIF/5dZo"
    "Bk20gIOtD/HZ6poTE9gVez5YeI1dDxu2lq+EL5lDQMRBPvBUOGAFE/h3eI0mofIffqtsO7d8EkkI7LoQ7yvSWufB2PKx5Nytm7zx"
    "kd3cODsWsIIJ/OunRuPU8RnvvcTAI7p2IAR2tT7UVGQUPoI5vySxYXQB//j5BO/7PRawggn8m5NG02nOdb5t+yU+Pb0DIbDr1sP6"
    "Yt/D3zBnkBxFnScAb9gqnw82iwWsYAKv9NVPdcPAP54v5q+jYgiBXeEP7EQTrYXYdl8SPOsot5p2l2ee6gxYwQReX6lZsncT17i+"
    "4JfCuhACu6rnmYvWrjXF6Q5ydvaYuo8Xur7lbd93AKxgAne1Go3p4ky+b24p//S5GyGwK+l/v2CdRQOxJ0/GsGi2k/8zowK8rRsB"
    "WMEE7iU0mkuzx3P//E98eYVuhMCu1gWvwW9sI5G2RBLvJm3m802sYJ4hHLCCCdqXBMcv4qutbWF7RUpg16Fh1+BCkJsYMFESN37v"
    "4q79nEGvrlKxggnalxw+spRX7tsU3l/0JAR2Tfx4Anp4e4nDcTJGl8jdvPH4YChQOxmsYIL2JXe8s3jtAB3cDKIEdn0buh5eDPIR"
    "UxvJGB0fbeEVNkRCQmkZxwomaF/ysvVsPqgkBlo4UQK7flXMhPGf/MWER5LY2W0Ff+vXE76qnQxWMEH7Eqe8UbxexUSYHUIJ7GpV"
    "1B20z4JEn2WS0L6YwXvmJ8MOdZWKFUzQvmTQhfbc48kQ6DObEtjV39wVWrcKFT6tyru+b734rsujoKY612IFE7QvGdvcgbetkQ73"
    "FlECu1aJZ7y+nSL2fJQEFDblN95mgL/aM2AFE7Qvaf8zjBtHZsClhT6hmMAuzyQzGFJZK55XlzEq2Cfw70t+84ZHY8F49kOAoqbC"
    "M9iSVFHskRvQr4a7sPoss+T9noX8Uqsa0BHU2QApmKD1kf83nb9fVgvemVECu9bxbPArbSaOFEtCdFjKV190g1HqrIYVTND6CGow"
    "nl/67gVu1z0JgV3JRRvA6ruvqH5UEmWaLG50lUHJGXvACiZofXx4MZw/2dwChjJKYNfyn5lg0TZQ7JggiX0Bs/n5PTFw9bW6rkUK"
    "Jmh9KBu683NOsfCpDiWwa4ZpPMCPYFFRK2O0yB3FOz/7H4xWKwormKD1EWcWwLsd6A8bAiiBXXuPuUKptVZYfpbE8GvtedVbQ2C2"
    "2vVhBRO0PsZnmfM2N4aD2UxKYNecqOf83WJF9N8iiXv+DjzNOh3kXk6sYILWx7rK+wyHmmbAgoWUwK5jV9N5xAQmRIyMIU4VGfq1"
    "mQBt1IrCCiYsFj3jca+1YrJWxnDPKTLEqsQu21RCYNexDencuzMTS9ZIwns/4y1mGMOsrl0hMSoXEjr5Cts9lqSKwoUBhtxuLuJj"
    "LOUdrMdj+PMCe1glwgErmKD1UT23A38U7wiPrSiBXft6bIJRwl/UCJYxns4YxxMSvaD6GC/ACiZofUwKi+KHsn3gxx1PQmDXJ6dZ"
    "8OXfIBFcTcbw3DqcP9K3gKl59oAVTND6aFcYyjVd2oBVKCWwa/TSBLjQNVR43ZXEgwXdefSTruClzlFYwQStDytjJ57XuzvY2FIC"
    "u0y2NQbnpoo4sFISZlUD+KZF/UE+sY4VTND6iE5/a8hpNxDe+FECu34FvuBWfZjQd5Ixzq4258Xnh0M1dY7CCiZofRytv8AwddNI"
    "KMqkBHbV7DeWG/9mYkwlGWOazT6DSZMM2F7gzbGCCVofFrWzcpbWGAe35lECu7qfq2PYVMaEySFJnJ1iZEgfOhFW/EgxYAUTtD42"
    "ZRgZBqqEg7raJgRy3c2pY0i5wcTdP5IwJDXiNmfMYNOVTnCuwmYwWxAigh2rkipKrrUF3hkCRc5emYmzn0Tz9AUOcOh0OGAFE7Q+"
    "ch1def+kenCgJiWwy2rYbDhxRI29RBLJ1yP5RhcfODvWC7CCCVofIw448D23/eHMTU9CYNfZob1g3zetEMmSiNgYygPftYYL6hyF"
    "FUzQ+hhTqxJnThFwPIAS2OVyowm4zle/3QAZY6HGiZs36A4X1YrCCiZofWwsO2PIWBEPk20ogV2F417yI+N14ukPSWxd/NZQu+lA"
    "kCt6rGCC1odO6WGYWzAIJvhQArtudc3gOwp1otOh8ooKXmDwWT4SEtWKwgomaH1E/s7MbtJuFHzOpAR23X1Rx7BPjQ39JLGoXVbO"
    "Jetx4FnkzbGCCVofTQraaddfyIANCyiBXQM3N1WWr2Diqo2MUeOKnfZi34mw51OKASuYoPVx7Z6ddodKjK+RSgjsyh/TVEkfwsS2"
    "BPmpTsdY8KM3rEGZGA0jHk6DeRl6UTi7KqmiXiVzwPiUVjyuXLV8XevCDauc4OPZcMAKJmh9XJv5xTCgpAE8saEEdv1d3AdO3WTi"
    "1DtJLBrowB/p/OG3OkdhBRO0Plzirhn2NwqCYZc9CYFdJkpTcPXXi8H5krhqVolfO9oOMk/bA1YwQetjXd8Vho0f2pff/8AEdq2y"
    "fcUtn+mF5XJJVKiTZ9B3j4dktaKwgglaH5YOdgbrswnQpxolsOvY5nE8+ZVefI2TMVpl9TDs3zkILsizcZGCCVofz6c6hK7xSIYI"
    "H0pg110HB8OTSL1YWV3GaPh9VnY1ZRScUisKK4Qg9TF1eYZ2XP5I2DmTEtg1y8VdSaypE3PKfwPw2tdOW6EwAz6oFYUVTND6sJ72"
    "Vtuu+1houogS2NUvhCvXohSRPkwSg8/c1HZ1nQBT1TkKK5ig9VEx/6a2qUpY2KUSAruOVOXKn0aKiMyRxMbGoby3TwYYHFMNdmmN"
    "Yc+MEDHzeFP9hJFmUGyqFbs/NNUri8xghLdW3N7qLseruIO88uQhENY01TB1ymJI/+Mtll5x05/eMg1+rfUVLSo11fvkToPss75i"
    "2Mmm8hmTyRq49jIe3tVNNfjsKoL6nRuKqiVN9LGjBNR55yLaO7jpS9cKuFHdVYxR/yd1Pdi7ETzbHw4tG6jENI149tVK9PjVWD8x"
    "5RtssKwhBjdponfd9A38PGuIfx40ke9eTg2HC/sagYtKrKhSUyx/+R46WKnEpOpi+dAfYB3QWL9gfXWRse0HaF83lic6LIiH17WN"
    "YL1bqsG57f8j68zjat6+/38qCUmTVNJcmtRRpPHstU+DkGSOzEMIZcyUecpMEZeu4UpcY8hc573fplCZh8yZp8wkLur33r7/rP35"
    "/fd53Nfr+VnnnPfaa++dvd7bSzb6fIJd8PLQVu1oLg8xO8M+dPLQhpQ1l1eHnWF2dTgR13kMu9i/QOrET/wWtJFvtZzFakhz7W/z"
    "QNlxyiI2eFBzbUpIoKxeu4itaOLB3+nknM5ebtFIwc6pusKXRJ7posfMu7hrewQSuU2aGRud4q4925/ITbLN2F8uzXmv5eJZbG72"
    "xKLVfqm6/3sbhWfY7WFu2n9ytXLfbW111TPctOUXlf99ra3OtZU7v3Ny+nTWU+tAarxSdTuUGP+l6UPjOa7ajUNB/lrnHdGtddV2"
    "U0bvoeB35HWs258T2ONZ9+bbCL8tzUr5HhrtbNi+xkV7Li1I9i6cDH/nuWh1G4PkaZ8mw/lEV37KO3kgy878StKU30qr/FY9NhSC"
    "4w5nrWUdb1lTfQzqHnTWWnt5yzcdj0PAcBfeDRjXjvU67gBH1Km6auV5JK36BD2Zk/bncWu53+MPcKfYSfvjrrVs0uQjGE535ivk"
    "F65sYrwVtKmqlZbeaiSPsalLa0xdtfcemMpgYUQ997pq9Q4byNXXLWjvNvxT2c9twu6VucChb7VS4Bl9ecAZc6pe7yK4En6+ZRUr"
    "7GkrHf9ULZ97S/WJI1t+K5JVlC1mPtfD5KET1drhkUvZ2Yca2fi1WuvhtZtVDg6S4yap+YxztyPxPdEMDt+IZBs3rwO1TzD9N8xB"
    "q4lfD/k+obTTfgdt3LZj0OdMAO2o/HeVCo5uDPsZ2YjNu96d3fN8LhWGd5CtxvhrV5wyZynG7eUWIf7aYe5m7MLhtvKEmy35KqO8"
    "Vgq3z5bW3erMCkeFyz6XtrEoZdxd7hshrzyzkNWf56PdDUS+PHkl84zmI0rzypg1G9+WpGV2Zs+Hhcgmsw5CKnho00v85RnVl2Do"
    "1ebaH1sC5BnJp6Asm+cVbbicPNmkD6MUIrvnc1j3w4NWVNlrqxbVQo61A22zwF7bL+MLXC93pNPa2/MzXrctofWd7eF+7zqz+N/t"
    "adCVZMmhv402Vt2O/mpfJcmfrbWjNral4dfOSi6Hrfnu7vVgMJ38VvLaWkfXysmDdnt+hBX7mWvTrT3oy4tHWIcLZtrVY7xo7ZO9"
    "rPydGe/NGGHJCm9+I54NvNgCdT3ZOMecRhm4abtFG8pLcyzoiJWu2h425vK68Hr0BOG5+9XBnLWPM4O5pbYMuzDtMe8/Nvy2La3b"
    "n2fJycArUpt6jeGEWSDbEX+JnXPyobdNXLXq8GMs/4A/Db/sok1Pv8YSMj3plhs8S55/vykFhNhA2U01wwomXFMOsd3vW9KKRE6Q"
    "vGdS9TZveF9qIxDYFXv4CrNTfpVGkZyQXzdgvoUW8KulPcOfV+1VzRKc7Ghx7P/mbh+1MZt8xxk84k0YVjCRv+Mxu5fmSsvr8W/u"
    "MFufbY3fQ4bt78CCxtjKX2rr0KTh7to+Bo1lg9f16ODPbtrjh+xlw5Qf8COQ15LCpe+l3V4TiHVgIuu3zkuO0zyCeQ7NtctdveTs"
    "H69hWlJzbfp4Zznw7xroZ8bz6nXjQdA89qP0bOMO4Znj5zzcR/nvBkdZn8Hm/N3qOxvAy7HtpOCYLmyehZrW+pcx9sZKW1nHlwYd"
    "KGYLkq206S1a0x3jj7OUVk0UYsfZuuCqbSn5uvdgWMFERssAysqOsI1Xrfje4FJ9+NyoqeQS010gsCuyQRgt2J3DrufyGKOCGsGV"
    "zEe6F6purOIApW2OTGWrGlsLri+TQ6jprbVsYiwnBrSzhMRYuWhJXBeGx8QHq2haNyeUrZpvrb1+PJLOXOHBVhM+PnbdbQhWFzZq"
    "Su92Z30WdKDtNh4P/3zORus4sAN9n/9VV77URmup3476Xfikc/C04W+aetUQwlSDNCOjejCsYAKPTZVqeDML8D32TNNV25ldfxdD"
    "Xx+zIz3+ttFGFren3WE5udLaVotjq1T92QdSWRFF9p5TZuj+UdR7TwzMb9xUu+54DG2aZgSG2xSid1t64/FtctvSViHGbn5Hlpen"
    "EI/riaxPEdC4rvMgZEFTLabzaSRNXOgPA5ZzIiP1NUmlS0nI514s/mEIffD4HzCtaqrF9Op/CQ0dmgbLjJry04Z/3yXhtgfJwb09"
    "WKzkTc+63IPKi3Zau/IA+iCcQdVgO61xsD81CSmEnt85YbTtMvm38Ayp6NqdnfvLmSatrwL94GZaTMdmeVJD1zvQZbQdz13LU+TU"
    "2HJy51dXVtjDml4fbETb5DXTYrpbgQO1GlYF6RWcIEu3kGsm38la8y4MV87qug0p+FvSrY3ttfEtjWjBrMa05+Vm/G0kp0eSVt9V"
    "sCmwB4u7dQtWVntR7Wl77bukO3C9yof+19xBi+uxUhPLokh6k4bQZ2lnhmeWvB97oKJXMHW4rsw4xy/AU9aSZiTxGcfzYF2Wcmgs"
    "2RDUheGRikcwnhmUVd+zb1Lft4s1fjkD2B2faHlD/9Fwzd5Tm/IE5I2X18DafR7aL4ND5bzPWyHQlK9k2s1qwLrXNSCppd0ZVjBh"
    "vCJc7ndvG3wYz4lbc+uxksvWpLxND4HALjx3qVRnk1Ss4RQTzenYfmx3UHt55FVfaLzMU4s/ITtF5eXquTBk8R9ieh12eeTd468a"
    "9mGTVR3lry4PSOJ3Ty2md++NlkNrKHzU52u4kpVG7Ptta53f117s+cI4eefjcLJvkJcW0+m27eUblj/IvGmcqPKqz0Zc2agLogls"
    "/ZU4ed+2ubqcEi8tps/WiZV3+g4gV97/WSd+rs/S4r7pfo3rwWrvdJQbntwirW7jrcX0u7RYuW+vLjrdIL56nb+wPrvQ0FOqKO3G"
    "Dm/sIE/qbsa2b/PWYtp/ZAe5oX2eFHqbE4HHjdi7su7S6rFd2aBmMTLJjmdXLX20mD5wN0a+9NiaBXTha+qUuXXYXZgtFY7twvDK"
    "AtPGFyLl4qi+LK6UE6ZXn0tzz+yQHigrmVl9AmWD3JNsRr8W2rgJIbJj7gHm5NxCm9IlSM7IymfDdXxdcv3FG2lQ2iapcUgPhhVM"
    "4BWOSrXY/YXkFnJCinvQmd2xUcvrml1ihwNaaKMjfeWfhg+YXNxCi2OrVNHDCyTTy4elpQ/7MezC9FIXNznDuJrp1L78b0vDd0rt"
    "rp6T4Gsf1v6trZzw3Eg+leMruM7tcZevv3zDSB6PcVq7Sbq5544Ufr43m3WwkfxjlqX8oL6fFtMZ35rK7+wM5PKmPEb1xznSiFM/"
    "pAnXlDnKt5Jlv/eQI175abOX6cuFbRxk46l+2sAqPfnBVju5lYkfPxdeM0h68ZcBy/TvziyfXGYxmS3ltJ5qLaYLbr1kU1s3lyMz"
    "OOFhqJGy29RnQ591ZbXTC1itSbC85ZRai+kElxL2T7patlDx1evtPCvpzV8mrKy6i0DgNe7umLXsZG8iX/Pha9ETmre6xH/qsN3f"
    "ejGsYAKvllWqN83Kdf9ONmf93ncWCOyqGTyWecyIlCvW8Bhb2kdpPHN+SkM39RdWyHhVvC6yneSqi5WjH/rzfrUt1uTXRCfIUdbt"
    "d23Gw25vSl+4OAqr8JGjxkCuLaGwj9fEsOU25NYEZ/D5EcGwggm8nldqYpCG+JDWcDhDLRDYNdIwBY5COCXenHhhPFFXdteS5aZ0"
    "ZvvaBDDDqTHyJ5W/8G03JXVn/9REyDv78W8OZKluwCpDNrGgN8MKJsRfN/f9c11NHxc2Rdl/YAK7iv26stfPqKz/h+g3+KUuc7Ar"
    "K/ocwbCCCbz3UZ55m8bSf/+0Yc8XqAUCu2oCOrNAA5D1kjjRO0Cn+ejrCj2UT9XBVQ05F6Poub8ctfjZJPr5Qml+BHV2c+R7tVRJ"
    "0zDUDV6+j2BYwYT4BJfc/U+jKQiCD/PVAoFdu1J8YEwJpU5bOLHt+E/NjInBcOGQH8MKJsQneOh6UxJ2tD0MvWgjEsjl/dILrN2A"
    "rmjEia7jx0qPF9oCKJn4rTaVVY/X0pxhLtoV7Vso68Zo+vuLs/bWrNFsVH+gXz7xfa3Rl3HSzalNwUbJRKxggszxZpszI2nCLE6c"
    "Wj5TcnZXwyAlEzGBXf0jRrKEORr6OYUTOf/Okl7dVMOMIj+GFUykvvJkpru0tOdPJ36KNSNLGn/EElKUJ1gb/BdbfTKMLrrnosXf"
    "6fSmtaygKIQ+Hsb3H8lpq6WT2xtD0qcIhhVMiN/8fuBG6cU3T7ih5BUmsCtGnc12vwuij55wYtTTjZK0zQuOHfFjWMGE+M3X3lxS"
    "lLnGhP3Q9GB4h43Ho7jb7tR/d1FUz7rs493eDCuYEEdt8z1DdU/burG5VyMFArs27WrErmdGyaUDOTFBO0xn0sudtX4dwbCCCXHU"
    "Lny5XTejZQh7M08tENjVKcGEfdkeIZfc50T+pB26wm8hbG++H8MKJsRRe+7UHV1ydixbo2Q7JrCrRt2Qlf6kcmgsJ8wyLTT9t7vB"
    "z8uRrMemG2SIqh0dZO6kxWP+rPoaKb0TTU/8zcf5rVxLzZmj7qD3KoJhBRNiZdi1bJzGmYXAcGWcYwK7rPSvkIy3kfSEDSfS4sdr"
    "wheFwqq9fgwrmBArg0HLHZpd3TuCvfLNMYFdN5tdIvEQQT0zONFy5A5N57sd4aSNDcMKJsTKEP/0uuaeU1/Q+1orYQK70haWkQ/l"
    "lNa85iv9veOLpcGprSGiqQ0rf3WQWY5S07gL4phI/7CascQ2tFMXnu2RuXnSo69h0OSSDcMKJsTxEWGzXaodHg6+TiKBXT3jR7BW"
    "T8Lo4Pu8MgxPny8ljYyAgMs2DCuYEGvJmXvzJd9HEfDYVSSw68h8D1aqR+mZZE5AWL7mRLqKBfTsy5pnjtIYV8XKU+MChFnfxyBb"
    "KvzUTraL5yuAK6pXYdnL7Fnds+0ZVjAhjvPQ0/1DO71yY12U3MUEdsUuXy1tPtdWnniXE+t8e4Z617izX08jGFaEMS+M87HemUXb"
    "O4WyWcqoxQR2jSJZUlh5lDyxJyc6x2cWTbUNY/67/RhWMCGO8zNljXUhLeNYXJmNQGCXsV2mFOMRKT85w4lZChF5JI7tsLZhWBHG"
    "vDDOZzoO1O2K7sceKLmLCewy9lgl5ei08jEPTjSZv6uo2XU32Hopkl2YYE6GFLSnA5c6aXGVWLzelNgtiqHHm/BnPrvT7qLGb9yh"
    "45MIhhVMiLWkZufGwti+ofB6rlogsGvnRxOyY200PZbFiRyPLYU9m4fBAOXXxQomxFoyrJ4mfP7AOFil/LqYwK76sxqSc88jqYce"
    "J2bph4eHv4yDN01sGFYwIdaSwBHPw2PX94PmVbUSJrArub0x6ZYeQX8N4cSHn8/C/3ndD5Y8rJGwggmxlhz8O1BTt2QkvC0pEQjs"
    "8uregAT11dJEHScKFn+U9v8TCqkVNVJt8GX24Y07fZbnrMWVqFDZs61u7kddW/Baoj1wSbLyjIJuSpZgBRNivXpW57LUamQU9Hle"
    "IxDYdfRpFhtSP5C6H+JZUpm/W1o2qiNs+FYrYQUTYr3yqN4tdcnvCDnvagQCuxbuHcbWLQylQcCJoacypG1m3eB6da2EFUyI9ape"
    "TYa0rmc3OP+xRiCw62Fic7ZyE6EbyniW5P2o0azx0Gd3nBJZduImMu55B3lbYYAWV7tD/ouK4N/2cvQFXuHel87RLB9gzSyvxDGs"
    "YEKsiZOuJWsaRbqxXGUMYgK7DhkuLvKZHiNv6s6Jb/6jNJ17u7NwZQxiBRNiTQw4Eab5URPC/lbGICaw69DpxUUGS6LljVc40ZuF"
    "a46dD2Vslx/DCibEmmj0tb7mSlAca6+MQUxg16HkJUUZtyPlhvDnX0z2NdBMk+JYM2UMYgUTYk1s1X9XONvej+1SchcT2HXo65Ki"
    "1SkR8uN/OGHYe3f46G/9GCjjAyuYEGuiw+5PYS6NRrG/SktEArkODV5aZNJJK8NPvqPv5rlR96rQFXyUOcp6u5E0vKI9HWLorMUV"
    "tXxqXSm3IIYWreKZ2Ml+k+7GVTfoqzxBrGBCrLs/ZizV1S4Ngf+UJ4gJ7CofbSidOxlNixpy4krAMt2cHqFwXHmCWMGEWHcLi1J1"
    "Hvc6QpLyBDGBXUfn1pEyzKKodzon+hwfo9MbFAdMeYJYwYRYd8E+Qmc3uB+sVJ4gJrCrXDKQzuVFUNVDXkUPnozQaQ/0A9WjGgkr"
    "mBDrrmmpuS786UgouVAiENi1ztVAGrNQS/sGcSLPx0J3uMEoGGdeImEFE2LdTXHXFf3dIg0yeXcmIrDLukBfSjhC6dzFnGjpacIG"
    "eoaDj1mJVP3lNVs5344mTXXW4qrNjC8xo29ulNbyJ+jQ/rv0LicGrirfAyuYEGv7ymnfJafCGDCxEAnsUm/dz2a5+9LZC3iMt4tv"
    "SDN3d4FoJduxggmxtlsfuSFtLesCyyxFArtyTLOYR00rOteEE0Ft86WH9omgUmY1rGBCrO0Wo/MlCRLB11oksGvF4CQGE0Lomr94"
    "XmWaLZYG3x0Ir8+XSFjBhFjbF6oXS06/BsJve5HArvep7sx1gYZ+c+eEn6UnMT+sz0rNezHvgkYwJrudfNqjlRbPDGkb55E75e3k"
    "FREBvPe1+I2m8x0zlm/UhWEFE+L88fXuc03VIBf2RKklmMAuq0Zzid6+tvLLi5woin2puTXBle19FsGwgglx/ki1eqgxah/Mviq1"
    "RCCQK/rf2aRCFyW/aM+JJm4VmommISx2jx/DCibE+cOVXdP4FsQyquzVBAK56j+ZSZwbRco9jnFizLTrmlNBHdlVZb2LFUyI88ep"
    "X6c1GX36srNKLREI5Np5ezrJ3aaVfew4cXf8GU3uzr5swOMaCSuYEOePQ0YHNTV6I9khJXcFArkWh6WTmIVUXvTn73Bv2x/U3PMc"
    "yToq4wMrmBDnj7p+GzWd0iayezezRAK5ks2mkXdHQN5bzAkYOQaKT/SQlo/Lkp72CqKXtg5iS6ottaWZbWjb/IEsv72ltvJUKC1+"
    "48gOnLLkfSzz6kqWY50h7kokKx17WXJc2I7Wn+msxfOVceJFybJ/WzqoPq8lFn2NpLCZLlD1IoJhBRPirJaUYCjdTAyCuvPVAoFd"
    "ldNKpYwxUXTQn+rjVm0oTXQMhsb7/BhWMCHOav7W+tKsSx3guDJHCQRy/bxzQVKfjKBXvvBRu3i+vqTqEgsmtjYMK5gQZzXbtT90"
    "Pef2gatKXmECuyqnn5cqemlpXk9OJDv+p1t+uQ9ceVIjYQUT4qxWbV6p0w9OhielJQKBXaNGnJNGhVGqv58TjQZU6uoMSIY0pbZj"
    "BRPirAZPb+v6SBNgkZJXmMAuny3FUuFooB76nFhoeEdXVDYB5PFZElYwIc5qwwec1qW8mwYbT/sLBHZVNi+Wcj4QmhrPCc03Jzas"
    "WQhcHZsl9UjXkyd3MaMHopy1eE68/PMVG/CgKV1Syp95z0gz9qVbWzC+lSVhBRPizDmhkxkr6N8Wmo8VCezK8b/ICqLc6LAunGj0"
    "+pc0yrkr+CgxsIIJceYc8fuXZOfbFUzHigR2FbzMZ31GtaB55TxLBg4slw737At7lOeBFUyIM+eQ8eXSq8F94fE4kcAug0mZLDe8"
    "Fd0xgMew7rtf6nd7KKiU74EVTIgz551R+6U3z4bC4YkiIcyJ44eye7uD6fE3PEtWD14kea4eBW2VGFjBhDhzthi7SLLdMgqmThIJ"
    "7Gp0xo0NOB5Om03hMX7t6kyuNNJnrzQ9WdMTHeGyebT8ZFUrLZ53Q1/UhYqMtvLfx/lca9TUnZS4NmDZS7oxrGBCnJ2j872IcS9H"
    "Rq5FCgR2NR1oCElDo+SqKE58OOVNFg1wYrmVEQwrmBBn533TfQnVBLImC9QCgV0n9OtA9dQIuUrmxJYYPxLwO5AlH/BjWMGEODtr"
    "9/iRsIJ2LEmZazGBXRuu6YP/ZSoPUXPicqCaVPu3Z9Ob2TCsYEKcndsF+pIX43qz9lW1Eiawq8ENPXiQDHJIFieqlviSmqLerOJF"
    "jYQVTIizc18nL/IwdDjrpsy1mMCukQ30oLQTkbMr+Vz7pZMXCR44nD2wKpGwgglxdrac60Lm3hvHTiu5iwnsSpyigutzNHKhhhPW"
    "61zI7dfjWD+lJmIFE+LsnDfDlnxqMZXNPOMvENj1xlEFxw01sv5STljMGg7lZ85JT6f4S+psLxpffx8zyDXXjprXkrbasJLdbWah"
    "zTD0pvnp+1hhDwv+N7L04dBUIWYoMbCCidjvLWnO95Vs9WVOpK4cDNm2RVJrpV5hArtMmTfNCc5naw34mqHh7MFQaFEkmd7OkrCC"
    "iT7H/enSNatYygxOXFmaCLR6r7RR2eNgArtimA9N1+xnIbs44ZqUCKFP9krblD0OVjDx4XQAfToqk5m5NeYrsqx48F63Ubql7Acx"
    "gV2F+r70+sIDbGgMJ8KHT4UR1yylpEn+UrmRhu7pUCRlLBRXSDtiQqk0x5H9MOWfqm5MGqwjyZLnSX8JK5jAay1l7dMhDf7WJEsf"
    "JosEdoFtG3rLbiD7tpY/jzpr7WFV/Ayp/3Jg+AxcRbMWNCbyDLNx+t/zcO26NYVTF0dK9rmRDCuYqKYtqc+NQ+xbX07M3OkAq9WR"
    "UszTCIHAroSJQXRlYDa7eIsTUbtbQpNuKVKesjfACibGbA+kY+TVrKwrJy5+DITtS9SS3S4/gcCu9KQwun3tMPa67E+MjW3hw9gu"
    "0lN+zhIpmPhQHEI35QxlvcI4MeV1B9gX11CqtBYJ7GINCJ15xIX1PsSJUad6Qz5rLul/q5WwgonTO8LptwxnprbmxOkbfcGNHtVF"
    "va4RCOy6NxZos/2SJC3nRFlSMpjOr9D5K/UKK5jI6Ebo6DU6ye4lz8STFqPg6CGVbo6dSGDXhJ1A/Va91Fkn8hjxVRMhr0Sj+1Ke"
    "JWEFE8PvEOqX+UIXvofH6OScBpufWmgeTRIJ7DItJtTrbGMy0YnH6NhgOkSMPhl+9qy/hBVMuLYjNDmpMSlM4TGerZ0Gv7o81Iyc"
    "JhLYZXQunDbOvETIc06MbVsXKr0aSYUNEhg+jYmzUjyZGb3FHiY/1ErVlyIZVjAh5u67zi5wzNlYCnwSIRDYdU+roZ0ejGBvOvMY"
    "Ou9A6H/XT5qrZDtWMCHm7p76IdAt7JHuprITxgR2FR4EWuzoxiqjeQy7oR3geYOGUn1ldsYKJsTcndg8DhzqL9c52osEdpneobRj"
    "E1l67c1j7F/YF1Stjuq2V9dKWMGEmLue1f3g964FRaFfagRCyOPzlO778Ep3QsVj1Hs3ElZ/VOlMlWzHCibE3DV+MRJODYjQzLEV"
    "CewyWAv09WArEn+JE80t0+DOXgtNX756RQomxNzdP3ICmPz+rPlnvEhgV3Wkhh6yvkyq13GiZPU0kNs+1FQrOxasYELM3cehk8H+"
    "QjQJniwS2BV/I4TuMvWCs/15jMHLjGDvFMcwf5/ewqlifJJYPHXveMoN8t2vFxldj2RYwcTqtCi6bO9paRrlhDFzh+cZz8M/VUcI"
    "BHaNuhVN9zl90E0u4MS+zqEQt7tv+N4MNcMKJjY/i6T7pLe6SWpOrLEMhar8vzVfjvkJBHadvhJJvdbbkL25nMjZ2RF6ZC7RfFey"
    "HSsC4RhBkztbEzsLTix/2AE8bE3IsaYigV0f1lJ6Y881snkxJy437gPFneuRBsr+HCuYADXQxl5XSdpbnrtzViXAycPdyfqKGoHA"
    "rp8B4XRJSx/4mcRjLLFJgnqLu5JSZV2CFUxMaBpGN7T2hl6Mx5h/fgD8fLWKGJqJBHbVHmxDEyNHwYIQHqNz8kio8VtF1iv7Qaxg"
    "Yt3bQPqm7UjYtZTHoF2HgNPQY6TJWJHArgLPltQqew00M+QxxlWOhM51jpKvp/wlrGCizyE1tW+9BoZ05TE6NB8Meu8ekmGTRQK7"
    "cv71pAtiDkLRBU7M3lMXejbVaHoP7S30mOCsFE/EBx13g6MGz8JLb0YKJ+IxIeZuRoYbvN28WzP6S4RIIFefU9H0tUVTss+Dx7jT"
    "PQSKn+RozBeqGVYwIeZu1a4gGDHelETs9xMI7FoZFUFvpN8g/nY8Rmi/DjBjW0PSQ8l2rGBCzN1Igxi4sqYbWWstEtjlmK2hu1Jb"
    "gLsBj6GJSoC1XbqTY8rOCyuYEHP3kF1XSM5YSbyVFTImsKv2TBBtsGU0eD7iRHruABhxbhU5WVoiYUUghNxN2NELnvkeJRaWIoFd"
    "Fa9a0rjAbKg+yIlG0UNgSbdjhO+8sIIJMXdLFibC8mcPiekEkcCubjZeVFN0ENKmc+KM62CwfPWQLFdqO1YwIebuhPMJEDlcHwZP"
    "EwnsOj3aiRqevgRHNDyGb7E5bFoTQRyljkKnBe6uEPsm3obZQ9nDtiTpciTDCiYcXbS0wWY1HLPhxPQ4W4g8PJO4KysZTGDX7rXh"
    "9M3J8fA8ixNWT30h3GYhKVBWMljBxJfCUHo3aSw8a8SJNBdPiEnaRgyUlQwmsGvI1dY0bfJf0GMRJ9YOCoXP/+whK8psGFYwEaNt"
    "RR94rYMz33juriwKAM9pZWSAnUhg1yjzFrRf+WGwT+UxZg2OgPZtbxJ7Zd2OFUwUXPam0RmH4MsVHuPm42CYfbWKxHyoEQjsCpvq"
    "Qqv6X4V3UTxGy5PRkNW8hrRXVjJYwUTBQmdq5X0FOmziMb7Eh8JfmaYQbvc/BHJ1M7Ohh7WVkGbOY1zuFwXnKy2gXMl2rGDi6Uhr"
    "+i7qDWwYwmM8rW4DJkNdYd8EkcAu4zMN6dNnerTXXU5kdiVg3ssdGsj+ElYwUTGsITVapUc3/6mJ7tFqOKEJhNETRAK7Tueq6Lxh"
    "JrRoCyfmXa0H+w6MIzNOxwtdQjgrxZ6f5+1t4If5DAJKtmMFE2LuNgyyBP1+68m9ZxECgV2tNrahZ7+th54NeQzVGA9ovzeXWMxT"
    "M6xgQszd0+lO4DpbJi+U2o4J7MrN9KUXRxyF/FpOZMcFQN23paRSyXasYELM3SUTveDXi9fE2VkksGvAbld689k1sHnCiZ3bg0Ee"
    "X0XWKLUdK5gQc9eG+cLJVg3A5mONQGBX6VcbenPTW7A5xgnzwFCYP8kUPivZjhVMiLl7wssX7Fs6QlgTkcCun/1MqPU4fdrqz6+b"
    "+b4NfExwhRb8fTJIwYSYu70tPaFsTwDoTxAJ7Ar7oaI+p01oWjceIzVSDbGhgbCo2F/CCibE3F10ywF+lkVCylSRwC7foy8hv5UN"
    "fdSUxzDoeJc0NThIKorFfjXcoyZ2nx3tZQDGPc6RgcpKBiuYCNI1p3sv3oKd1Tx3Fyd+I9tjlFlNWbdjArsm/2hGH5z6DDdG8hhv"
    "h5nA16LP5K6ybscKJnJT7GhV0ke48YLHWHJCH1o9NQQo8BMI7Oozy4zWdjCkWf14DP25FvDpqymUK9mOFUxUEFNq51GH6pXxGIa7"
    "DKFPXjNYZC0S2DULDCiEmlH76D8x3lmAl3Fz2Kms27GCiQHt9ekstSn9soPHaN6wDvjMDIDXD2sEArsO57+BHMemtIkLj7HiWiMI"
    "LgiFd8q6HSuYMOz8GhzDben4dB4jMuoXyV3SFq6aiQR2Pb90EXI+utCQKk6YLa0L843jgN/WjBVM3HxXBmO0LrR/DCf2739FIqoS"
    "oM8EkcCu5033Q+UObzqKcWJLaBVZ3L4vNFSyHSuYmJGXD32CvenBPzXx24JLpJf+MOg8XSSwK/pKJhhE+9NDczjhUFJMtm0/SbY6"
    "J4i9ligrxc7JLje+kq3P75MGtyIZVjAh5q7DrceEhn0h/d9GCISQlR/M6YQNdWnWY054tNaH810NYeUCNcMKJsTcnfLtLRnxwAzm"
    "7/UTCOwak1SH3ptiTvNvcSIvwRCCwprBX0q2YwUTYu5++vyeJB33gIgmIoFdeaPewmliRynjxLrHBnA8NAAiv9RKWMGEmLtJtq/I"
    "p3YaOKdkOyawS2d4GeY9caX3czjRyvkXWTWsLfxUsh0rmBBz94PFHfJyb2cYbykS2HXx/n7wGOhD26bwGBk7XhH7lwkQqOxSsYIJ"
    "MXcbPzpFIhwH/cl2gUAu+4As8DnuT1Na8xj9lNx1qU2CnSf9JaxgQszdyVnbyefvKeA2VSSwK9F/GGT814Z2/Prnm5dmEK9br8ng"
    "wb2Frl/c6Su+O+HWloNk6T8NYPOlSIYVTPhWfIQKRwd6/QbvE17weQP5fMkCAp5GCAR2+c64AUddPen6TjxGh15HyLvFLhCtrGSw"
    "gom8wddg9ezm9K8SHmNu8gYSOcUb9uT7CQR2JV06BMMd1TQvgsfwhANkQ2wI8HU7VjCRF1oApZt9qeUBHmP27EyyfRMFG8f/IZBr"
    "edkaWHmlNbVqzmOM/5JL4lWdwKS6VsIKJm4eXA1Gc1vRykU8Rt6m2WTM9O4Q86VGILDrhDoZjDqE0Lk/ObHJfiXp8moAeCgrGaxg"
    "IvHicJgVHEwrunNixpl4MnpEEnxuIhLYFbrRA7rtCqcn//y6x4YNIw5DUiHtRpaEFUzsetxcqWFh9EUzTngUWZCQZeMhf4xIYFdS"
    "nxJi/Y7Q2dmcaLTEjfxXOAU2nfWXsIKJ6EsXSORYQs894eNj//kNmspB6fD3FJHALq+g+mRCI0qL+/IYz5okkcpmX8nsTb2FN4Xg"
    "rMSd7CqV0Zv15OYdc7BU1u1YEfJYyN17dA7ZW2EDA19FCAR29dt0BOB2S5pXzImpZevJeNkLLs5XM6xgQsxdE/tpZExiS+h51E8g"
    "sOt3s7VgOrAN3XH0z8nMgEwS7Eph/EUbhhVMiLm75eNA0ta0LfR2FQnsavphJCTkhtI9f3Gi9+zZZG5Ad+j6vVbCCibE3E1Z1IZc"
    "ie4N5yprBAK7vLd4woRTGjp0HI8RcTieHNAmQT8l27GCCTF3PUNrNEdNk8HcUiSwKzuqlIQVAu0TyWN81VmQTdPHwxRll4oVTIi5"
    "2+rOJM2HqxNhyliRwK6dW+uTbssonWXKY8iXNmiy+6fDjVP+ElYwIebu5+3uRT+aTYcDaSKBXdZj9KUBwZReuMWJhxcCmPtZfzBQ"
    "xsdUSxN53ug69Hw9Zy0+X3TYQ092/WJKv2fykzV2511YznwKqtP+ElYwIZ5Cci51YfMXUlieJhLYtTTpFfOZ0pReteGE1yRz9uZN"
    "HPxQZjWsYEI8hXR1ijn79jYO1FNFArsy9paxbndc6d5N/GTNmt+/pQUlvSFBWSdiBRPiKaSf+jVSTVlveDdJJLDr3KR8tuM/H/r2"
    "T2/fL99yqVQ1FE4pvxVWMCGeQtoUUC5FGQyFZdNEAruMbDPZ5HMB9P0eft6n9ed9UsaE0bBQ+R5YwYR4Cmntt31S0KTR8CtdJLCr"
    "+PEQ5tgqmKqCOXH15AJpZeMJ4KzEwAomxFNIr84ukKZZT4APU0UCu7b3dWMGJJwOOfsn21/OkewKf0g/b4pvEMBvDRDfB6A5tVVa"
    "mmrKLiurDKxgwm7Qc2Y50k3OseBE2oglUuuHTZjPiwiBwK7VNefY7nW+8qg/50va/sqVMhM9mJNSd7GCiaeWxczxhY88yogTfjMy"
    "pDUpfizykJ9AYNesoh3McVsrOW8GJ/au/1s6/0TDOil1FyuYMO6+nT22DZAt3/K3LdgUTZE+Rkexga4igV2jemewT0nB8tX+PMZ+"
    "ulw64NWV/eZ/HUQKJr4MXcjUZkHyjpM8hjqsi3T1VAL7612NQGCXg1EcM9ULl6Pb8BhLzo6Sdi4fwp4rdRcrmKj7JJYZVYbKW1fy"
    "GMPL7CT378PZwcYigV3vJzZgV6cRefSfX/fh/JZSKBnHFip1FyuYaPKyPtu5VyNn9uYxrpw4qhsYOpGVjxUJ7Cq9s0LKvQxy6HVO"
    "LN15W7dgxzSWodRdrGDCeMEKqX5XkOc4cWLi4Lyi6xbT2bg0kcCuQ0+WFl2uBXn3Bk6U3+oqPfJRsQSSILz9Amel+C4Lz5mLpeKn"
    "VoyfQ8YKJsTcjS8cKO1xb8Z+vIsQCOxiiTuZb3KgvF2Px5jxfaEUftiXOSs7SKxgQszdp5u6Se5prdjHQj+BwK4BMxYxu5oQechH"
    "TlyEKdK9kkgWc8mGYQUTYu5WmrSW3r9pxx46igR2NZnaidUfqJHHXueEr0kXyX9yAuulZDtWMCHm7jB/Q6nt3D5s6fMagcAuKdiY"
    "ua4F2XQfJ/TO2kmfrwxnJ5QdJFYwIebusF1rdKbTR7LLZiKBXYVJKyXbzVS2mvPntzpzVFfPZyIDJduxggkxd8/Pu1z4tmMaCx4r"
    "Eth16MDSogczqDw0jseYMDevqIfpdNb+jL+EFYEQcnf8wwWa6sx0dmuySGBXcp+pZFAIyF8teQzTpUlwYdIjadj76ZrK9r60W/lG"
    "tsNPPKUnvhnPIiYZ3py9Io29l6LDCibweT+VqmrqYAi+9VaKd0sVCOwS38Q2tclguGBXIa2+5C9hBRPi2cGNZwfBv/sfSznmPgKB"
    "XabLPahd/WMsO4QTaxf2hVmbbkkNr2VJWBEI4exgSkZfyF5yRYrvnCMQ2GUd4Ulj3x9nS4w5sTWmO1z6cUFadKJEwgomxLODDYd3"
    "h8GPS6RhnS4IBHadXuJJrQ+cYKM7cOLkvFhYM3K/5LK1VsIKJsSzg+WjO8JkhyLpiuNXgcAuy+1edN6/OubfgBNHto6Cgc/OSsQj"
    "VYezJKZvS7p62kq2b7iYMSrVuynjYOnwHVLyoxQdVjAhnh181GkMRBRtkmYpuYsJ7BJPf/aMHQPNFKKtMj6wggnxRGPLJ8nQpWq1"
    "ZDY+SyCwSzz9aXI9GaI+rZYKlHGOFUzgbhWVqqj9IAiNzJD0lFqCCewST3/+Vn6rlcN2SId/pujw7/P0YyCd9GYAK3n8v79Vy/6T"
    "YOLLDGmLSaoOK5jwcA2mxQ8om/nneew4Pxme5M6W/vI6EYYJ7BLPi/azmgqXy4ZKJr6pOqxgoo9DKF3R35GVJfIYtzpMh9VurtLV"
    "1ykCgV34rKpKdU0h6rq6SrQ2RYcVTHx5EE4bOhdJfa/yGI69ZkJ+8TmdfuNUgcAun20a2uLLbKnckMeYrKeBokH/SKHbbZi1hQ9t"
    "NeUk61koZrjxAj/qYVbAqm7z57FSIQIG/yPV5NkwrGBCHFGtL2ohMnSptLmJSGBXeuPW9HR6Fgs9yYmGbeOhMHmjdL+qVsIKJsQs"
    "CcvrAccOjpMGPaoRCOy6PiqYNvkymPlu4kSAyyCobJ0hLVDmQaxg4n9yN3YYrJgJ0npzkcCupSvCaM+/nNiysTzG7cQx4Hush2RW"
    "niVhBRNi11YTxwnQbZ2+9GiCSGDXh/ka2vBckURDeIydQ6bCyxuWUq4yzrGCCTGv+uSlw+WdU3S16SKBXWP6EPr+23Pd/B+cCPWY"
    "BVM7b9dt18WGYQUTYl4N850FnwsH6b7Yp+owgV2R/oT6nX6u6xXFidhSH7j0fplkHtaS4fPNOCvFs86verQAvVkrpFOD1QwrmBBz"
    "d9dof/CPSZX67fITCOwSzzqHdtTCzDdLpEz+7wZIwYSYuyVOMXD/SRdpfhORELJSOOs8v2cPGDB+nHRWWfVhBRNi7n42S4TmT5tL"
    "4c9qBAK7xLPOlm7DoP9YkAYp2Y4VTIi5W295MryeW6GLthIJ7BLPOrcymwCzNuhLD29mSVjBhJi7dnXSIHG7RleaJhLYJZ51Nt2a"
    "Du+PTdENPqusfZCCCTF3F5hMh7Ksk+Hf00UCu8SzzuOXzwKTilbhR++n6LCCCTF34xXiZ93W4XVVqTqs/LRX6OjGZOWx/y/Gs5kQ"
    "M22NhimVGiuY4GOldfY84vqWx6j5OhO+zjimuWewMAwT2CWeYt17ZwYcXvtWA01SdVjBRNDGcPp1yCVi0ZIT1TQdehuHkVHXUwQC"
    "u8Rzr/8qRHKjMPKf8s2xggnH3SH0xBtPWL+Tx+j1fTLYDptMEmxFArv6KLOod4sIMLnDid1JRuCefkw3pH4v4R2/+MT35h5Ai4eP"
    "Ypln+RmvS+AMw1o0kNpdjmRYwYR4Lvz8fjfoPyJPZ/UiQiCw68t6La2R3NnbP+fIlkcEg//ICl3tXDXDCibEc+GuhaFg+y1CN+6g"
    "n0BgV1hGBP118qQ0tYgT7XM7Qqfny3SVF20YVjAhngtv/jQOGnj+c2Kzq0hg14RWEfT97je6Zxs5kbmnH7glLCz6qsy1WMGEeC58"
    "79x+0HpYqibvXY1AYFfQYUq9NE3Ip4mc+MhGgu1HreZ7aYmEFUyI58K7V42At3X1iXMTkcCuWAtCv1ZdJlf//Lrd+k6AnNufNTql"
    "+mAFE+K58Al3x8DEwjjiMlYksCs+PpR6z/SCGeY8xuqgyfD0ZDS5f95fwopACOOj/+9xsHbxcrI7XSSwK31iIG2wLxk+3f7zqRwn"
    "w6ftC8j9Am0YVjAhjo+ZDdJgi18mqVJGFCawK7JjIH0zLRnOuvIYq/uMAT+3AmJ1J0WHFXziV/xUXu9Hwq56R8lYZf8hxECEeHL5"
    "r//GQeWC5eTSaZHALvHX/TFpJFSGryJLlOeBFUyIJ7AblI2B/3LjyM5bIoFdYpaUaJLgrK4rGWFZIjxzTIgnyf0uj4DlD/WIZ5lI"
    "YJeY7WsH9oGW6+uRoBc1Qu5iQjwRbx3UD9Q7UzQjlBWAMD6QSxy1DbzioJHLUk2ekw0TxiAixJP9G4bGwfRj+SfaXRIJ7BKrT5lZ"
    "GFw3HRC+/4SfUEswIXYozPkWAvlpETrtfLVAYJdYRTtedYc+m28UBb2LEGoiJsS3se/c5ArZkdt07a9ECgR2ibNBu1IjmPZZrZOK"
    "egm1HRP47e/K3mCYOawatFhnp+oqENiFZyKVKlIZUS3cC8j4H+KIGr5cTfMs10DQRqv/OXX/vCgZHAsukWxlBYAVTLh28KVWszZB"
    "ZDEfgwEXh8PJDndIWNi6E5jALvGsc7BpEpzZ94REOqfqsIIJ9TxPmuJ0EFY15kTjlL6Q3kMPhr1IEQjsEk9HXxjdFy4rxNGaFB1W"
    "MOHT3onuzb4ESxbxGK3Od4cVK0wg2C5VILDLcoQ97dG3HJru5cSzhDowrrJQ86Oit/AGftwXgN+ar1J9m+kKIUt2aeJuRgrv08eE"
    "2D0wsp4LbN9kSia+iRAI7IKAKPp15S0SsPnPadxXbaDd+UYkRcl2rGBC7B4wvNEK9gyIJw92+wkEdpmGA13yxheOruHE1XltweFr"
    "V7Kn1IZhBRNi98CYPC2EN1tGkqxEArvuOYRQ716p0G0GJ1KvdYF37VYSv6+1ElYwIXYP6NnGQuyIArJY2W1jArvgsz9dbrEW1vfm"
    "MaT5vaC47lGSUVIiYQUTYveAx/d4yC++RwKtRAK77l3xooYzCqCzN49RNi0RHK49JMuU2QArmBC7B24Fd4bQfXowPk0ksMu63Imm"
    "dLgMYz5yIrY4AXYO1Yd7p/wlrGBCHB+WD2NhY0JjsJ0mEthVWNea3tz9Gh7v58S10i5w9KAFLHReUYgVTIjjo++iTtA5ownMV2oJ"
    "JrBL/bwJzZ7yGg7/5ESVQySUm7jDhtspOqzgc+HipwrpTuB+ojsYKd8DK5gQz7fb3o+Fou6N4cEZkcAu8df9a3gUsG8WkDYpS/it"
    "MCGe06/v1xmst+nB1lsigV1ilkx8GA0GvWrIRdsS4ZljQuw3qC6Ph7ob7pHnF/6HQC4x2+/kRkDi3zeJ68saIXcxIfZNTLjWAU42"
    "KyAXlVU4JrBLHLXHbofCffu9ZJ21DcMKJsT+D31PLRw9tJTElIkEdonVp+tmP7A7sJDU3eUn1BJMiH0svS1bwd5xnQh/96dQfZBL"
    "rKLfohygWNnQbnkWIdRETIj3mBj/doIJRxuRxtcixbqLXOJsMKRbU6BZjchOh/ZibUcEvjdFWS09/UBqWzYj9c70FwjswnezKPsP"
    "ZUQlNHIHQ8NUYUTtiGlI103QoxPGW/9Pb0bU2hCIPqSGmy6pOqxg4tznenR4HUN6OpuPj44zAsFwaWtwm7q7EBPYJZ6I/6/YH3w3"
    "BIEvn2uRggnXDBWdFWNCV1X+GYP/usKnDlHwsSJFILBLPEP/ZocrxMdGwdAGqTqsYGLBvJcQY2FDC5L4pxp1wQbqP+wI171FArs2"
    "6j0G10VN6Yx5f8ZHRC2Z0XAFIaSrcBMN7h5J3xRMD2/Ngd+z+elPG2oBjoP+IlsuRzKsYELsMWnp3BCibx8g/yorAExglzpWWXe1"
    "OQ7753Gi+rojxOxhZKqyAsAKJsQek8qL1uB48i4xPu4nENhlZOtOFxy5Af9O4DEuN/ICXbvXZI+ybscKJsQek31PHWDPB30AV5HA"
    "rlZWTWl2wnuI6MFjOC/yheja+lC/ulbCCibEHpMxZs4w/pINjH9VIxDYlRHQiBYEGNBbfjzGVjNfyLVwhJPnSySsYELsMUne5gAD"
    "d/vCv2YigV3DF+pRdd9GtLMej+Fl7AlkSwAU3cySsIIJscdk7mNrePsPhaIxIoFdPbq8guHrbOhfFzkBNx3g3IVI6K3MaljBhDg+"
    "yoJMQHrQGVZMFgnsyk4qgyHlznT7Gk54J1jCou5dYFFtyyKsYEIcH6MLTSG7SzeodUzVYQK7qoLKoKLAmaZXcOLfGTVkcG4/aP0m"
    "RYcV3D0gfirj8CpiG9cXpivfAyuYELsgStqYQNLdzpBwWiSwS/x1QzLrQrltHHzi7wpDCibEbg7ru9bgvYbCmVsigV1ilkS+bATS"
    "zVAwVfIKK5gQu1KqlznA/SW+kH9BJLBLzPZVzSzhd/vmkP+0RshdTIjdNe3vO0HzNTbQThmDmMAucdS+v2sB53qYQaGdDcMKJsQu"
    "odKFDjB3vT7cvCgS2CVWn9NfTcBG/kKcCv3E6oMIsdvpWGtrGHfrDjm6UC0Q2CVW0f0+dcB47Xny62uEUBMxId4ZlhtiDCsO7yfN"
    "lRUAJrBLnA0eS2/Jhwb/kIah3YXajgl8R5lKNdXqKYmx3kz+apMgENiFZyKVasH0GpKljKhw41RhRLnPzAcDS2+6MMH2fzp4DJxe"
    "kn6fh8D4Fqk6rAjE0p0QluNDJ47h48P22h1itnU4WE7OLMIEdol9E6n9rpPgAyMg0TVVhxVMzMjPBGsHf7qojMcobpBPYuzHQvKn"
    "FJFALrHTQq6fTxIVotYkVYcVTHT4nQR9rrWhjsAJ/bS1JIVMBBe1SGDXf0GJcJQF0S/d//SYND5IPu26QgZ49BJufcM9RqeXWNKn"
    "ZvVoSE9+Rrh08CPSa98nMkXJEqxgQuxEMl9VSoIdDCD9eYRAYBccNaQ/X1jQ/EQe49zvSuIOZuDG/waAFEyInUhDT1wjm/c2BSf+"
    "NwBEYNeDGe+hMLsZvdaZx7gw4D05FeMBR5V1O1YwIXYiTX93haSk+UNPa5HALpMVV+CppTs1CuExGl55Sf7V08Cyr7USVjAhdiLB"
    "1mKyK7MtDH9WIxDYtfHVAVjXvwV9bcljvPt2m1xb1Bk6l5RIWMGE2Ik0cdch8l+L3rDIRiSwK+96FhhPDaDt/q9v4s4pkm82CLoq"
    "KwCsYELsRHrwJIc4rhsBx9NEArt2lQ2DMeODaJ0dnJiXtZ2Mr0oBI2UFgBVMiOOjs800pSZPhMtTRQK7GoxtDruHhlHfP110RYsz"
    "SP8rk2Dku9wirGBCHB/bI+aQdRGT4V6jVB0msKtBh+awNCyM6h3mhG+r1qRyVTrk3kvRYQX3mIifqv4iN5LGpsA65XtgBRNir0yi"
    "7TSSET4RGhSLBHaJv+7S5GHk2bhUiJ6QJfxWmBB7fjpX5JCsRSOg7KZIYJeYJcXeK8l8k4EQ2qxEeOaYEHuXGq89RAqNesPsEpHA"
    "LjHbPzhuI+4dOoHr2xohdzEh9mDZDS8me9q1Bb+qWoHALnHUOm0/QLTFIdDV1oYJoxYRYi9Z+NgrxKO2JRSU/g+BXGL1Mbc5SuaH"
    "u4KNUq+EWoIIsSeu4v5VsrtOU8ieqxYI7BKr6N7rBWT1EmPo+iRCqImYEO/ndAopIZ+i9IG/NRsT2CXOBp/qbiQ1DR+Sei96CbUd"
    "E/g+UJXKs9NBkr7nFdnztItAYBeeiZR61bI1eamMqDC9VGFEGW6+QCa3JTTH1+5/+rzundQjX2fNgFB3ZXZGCibczx4mxn8TWg6c"
    "GG4na05fmAlpMVeKMIFdYndNnU+7ND57ZkJGvVQdVgTCsj6JfwZ0w58xmLG/U5hN5iyoKU8RCOwS+3GyrsSFVa6aBa3qp+qwgomE"
    "XvqSWvl/2uj8pydufxtdcfwssFSLBHYF1beXKn8DPeXLCXIjT+enmgUXv5vqsILfNix+qr0jT+uOfJwGoZP8JawIhPB244OD3Is2"
    "2E6HxadEArvEbqfsDF3Rm7A0OKLsWLCCCfEmgZyvkzSLT02ErFsigV1i11b4hECN3ueRUGVeIvRgYUK8VyawdY3mzMsRMLZUJLBL"
    "7D4r+n1d03FMXzBW5nOsCIRwc1bW4Dak849e8M+3WoHALrGL7kZTO6IL7gDx9jYMK5gQb/pbMG8gGbc6GkwviQR2id2Aix5riPn3"
    "1jC3yE/o7cOEeIPkXd+p5NM/ajBVdiyYwC6xq3GNZyeiOm4Phz9FCD2KmBBvl88bPptYP7WGgKuRAoFdYnemLIeS3O+/SJtNvYVe"
    "S4EQ7hMuPptAIg8awLXS7iKBXPj+YpXq2rUCXcHqmRBmlCqMqD41Z6WCs4RGbGj2P+/y3ljbQpIfp8Pf91N0WMGE2B/VuyBISn01"
    "GayUNQMmsEt8J7luT5A08flkSDolvmEcE2LXVvElkAZkjYWf//MWc+wS361ufAykQfPHQvgt8U3pmBDfaN3FO1pap+xOMm3Et7Fj"
    "l/iO+J/foqTS20kQWia+8R0T4g0V7XbFSA+794Lpr8W3ymOX+K57044x0mTjXjD4f95cjwnxTqSG2hjp+IUYOGcvvh0fu8R39jf6"
    "t61U3jEGDl8U38CPCfFmuUVvI6XUv1rDkUPiW/6xS7x7IKxhpHTyfitYsEC8SQAT4m2bo05opCGGjpDzXrytALvwvQcq1cyMcOmF"
    "ngMcvi7eiIAJfLunSrXqVgA7l9kGLJTxcedrQ3lCfB36dzcnLe44LTDWk1deN6Vl9//cdqMQNKsNlL5M0WEFE2JfqjrJheX2jIb+"
    "ysyJCewKa/WKxfRsSvOG8BiHhrqw0IRoGFGRosMKJsS+1IHbzNiig12hm7IuwQR2xc8pYwMOu9I5r//UxFwzZlnQFYqUFQBWMCH2"
    "pd5f/FPaMK0/fPtPJLCrunM+e3nDh8pjeIzpCnFGITq9S9FhBRNiX6rDr+tSwPIR4GaeKhDY9fTHKha2JYCeqv4z1/53XWIKMfFB"
    "ig4rmBD7Uo9Z7ZZmXh8L7qpUgcCu5geGsKMNgunNuTzG0ca7pVKFOKU8D6xgQuxLjd42V3JrPBlq6qYKBHaRKZ7s590wWmHNYyyZ"
    "P1uavnIyZB1W67CCCbHu5lUnSru2ToVqx1SBwK6aEDdW0DicBplxYq2er7RSqe2PfqTosIIJXOeVlf7sZ5qKKd/JC1V/Jtxzj+ao"
    "30NWgtFxQndq+BOs/B5GPoyxgs1TOzCsYALf9axSWTtv1GwYrYK12X0FQrhD+uIgiH0dSR3+5TEW5BmQmSetIFcVx7CCCXx/sbLz"
    "KrbXDEuqA4FPEgVCuBf5vAvUvo6heVZ8RI2qydQcTGkMXc/FM6xgAt+dqlLpLdpyYn+JEaTU6S0Q2BWYeYb83NmBRvypu8Oc5oe3"
    "N7UA29ZdGVYwgW9hVKksB/jporwawBFNgkBg1+tcA/LBviN9VcWJZT8sdX2fNoKfgd0ZVjCB7yhTqf6tt0/3fIgxzNzUQyCw6+hN"
    "fYnRjnTOMF5FOxzbp6traQwfr/RgWMEEvmNGpZp0Q1+qGmkM4a26CwR2/Xx0Wqq0jKXfbnJiTVZdyaCwLnw3TWBYwYQ4G3zv5Cd9"
    "bNkAdht3EwjsauTtwmI2t6Phkfwm5dP7A6TbP/RgzH8JDCuYEOePM0d7Sdd1RvCXb1eBwK5Olwey9I9RdOheHiPkex9pVIsfZOXZ"
    "XgwrmMA3N6tUrHamZDrKAHZpugoEdhl3X8zSTbS0yMCVn7+aNFda36ySdLvXm2EFE/huaZVq9pJ1kltdA3gyqZNAYNfuhL9Z9YZQ"
    "2uIBJ2z986TlM0whSBvJsIIJ8Z7q2wa7pad5DeDE9GiBwC51+DGWf8Cfhl/mhM+2IokWOIPtZj+GFUyI91QnG0vS6DPN4XCSl0Bg"
    "l2vKIbb7fUtakchjjH95VmrzuxW0U9Y+WMEEvkdT2Z9HPZfum/kAsRYJ7Io9fIXZOXnQRn/yKtfzozRjUCi0VfZRWMEEvgFOpTph"
    "Vo8NGK+G/Y9qBAK7CjpUsjGjmtF6TjzGsIYm7HWDcGih7Aexggl8u45KtfhtM7YqWA2/LEQCu9IM9eWwd2Z02WdOtHvjxM5ahMD7"
    "m1kSVjCB37ahrPpiW7KBWd6QO14ksKsy1USG03XonEJO3CwOYFtO+4PmpLKbQAom8FpLperTWcuM7jlDwRSRwK4fd61lkyYfwXA6"
    "Jxpe1bJ+2c1h34sUHVYwgVeDKtXv1lrWP8cDDFf7CAR2VTe0lpNWfYKejBNT3aqkcm0zeLLEme2Iv8TOOfnQ2yau2vT0aywh05Nu"
    "ueGizd/xmN1Lc6Xl9fio/frgp+RywgU+xdkwrGBCzCuHO/9J/76wgS0rXQQCuxJ+vmUVK+xpKx0nxt0zYpFBapig7Cawggkxr+Si"
    "JqyDgSsselwjENgVeEZfHnDGnKrXc+LSpWYs2EH9518BsIIJMa9GD/Fhv2yc4ZyVSGBXlWEjeWlXQ9o3mcfIIC1Z7WJvOKjs7rCC"
    "CTGvBvsQlvO5KcRPEgnsmqGxkeMKPoLk9+fXjdOya3ecgSm7VKxgQsyr6+M6sV+FZnB0qkhgl/8KZzl64U14/YETuxLi2bJkK4hS"
    "MhErmPh53Fru9/gD3CnmeXVJIcIVYtAPkcAuy1HOclrCTSgK5TFc3NzYkZlW0F7Zc+odNpCrr1vQ3m1chae29FYjeYxNXVpjyjMx"
    "O9KHbddzhmtKLcEKJsTnoU4NZl9+mMPhZiKBXYGPbGSro59g/X1OJDgQJlU2he/KE8QKJsTn0fdEBzasWQNwmyQS2GVZ7Sy7W9yC"
    "f7Zyon9qJ6anPI9jxf4SVjAhPo+7Xons0KlfxDtdJLDL2stbvul4HAKG8xhHUvqwuoYGYKPso7CCCfF5xF5KZPpr68CG76YCgV3a"
    "9l5yjw2F4Ljjz/jwa8kWWRlBu4810r0HprKyXaWee12Fp1Yp28oX7b9A+Dz+BG/HBbP9L8zBRBmDWBGepvA8+tIolr5DD87aigR2"
    "xW1zka1+3ILpnXmMhns7sJNNGoC+MhtgBRPi84h424PtsvlIssaJBHZtXOctW60/DpW2PEZy80RGTv4iTuf8JaxgQnweW+KHsnfv"
    "bhLzaSKBXUbL/OUZ3jmQ84gTd74msd51K8jqhyk6rAjPpo63rKk+BnUP8uehV5XEnA0rSKyy28YEdiUlKf+9Xg6M8eExiifWY8cf"
    "1IGvpj7MY95/bPhtW1q3v6tQnbtFG8pLcyzoiJX8my+VLViHOs0gI7Ahwwom8GhWqSYub8ra1q0HZm42AoFdPWzM5XXh9egJ4sbf"
    "D5fYlC2bZwS89xUrmMD5puwHF7mzlPtfyXIXkcCudfebynlPvsIwJx4j+L2avX9bF+yqayWsYELM3Q9Nw9jomvfkwIcagcCuxatd"
    "Zavg2+BYzYl19lFsyVo9eK/UK6xgQsxdi7OdWDl9RKY0EQns8urkI0cPOgHF5zjx8EEP9rTRR7JSyXasYELM3TPLB7B6/10gMWNF"
    "AruSav1lk1U50H01J8I7DmX6Su62OOMvYQUTYu5myqPZ3SF7iflkkcAu3cYgedqnyXA+kcdofD6VFbc8Qj4q2Y4VTIi5O6tlKlvZ"
    "rpCsqzhahAnssipoI2u0s2H7Gk48uWrMOnx4SHIDglgfg8aywet6dPBnN+0CdT3ZOMecRhm4aQvnWMiTV9enhad4lpyfaMrqNHhP"
    "DKaqGVYwIebum1wb5jn0Nvl4wk8gsGuIupk8o/YbfD/ACVMHd/aj81fS8ZINwwomxNztPFrNJmSXkwHOIoFdGSfd5LMld6D9Gk4s"
    "Lw9l8cfek0XKSh8rmBBzt+uVKHZ2xkUiv6gRCOyK7NBCPptWCMmpPEbVlk6sk9sjsuJCiYQVTIi5a3Iqgc3pX0g+mokEdn3RBcgX"
    "g/4GtZbHkGYOYCM/XyCDlNkZK5gQcxdmDWdSu62k61iRwC5rq2D5xOopMNuEx3hVNJpNVXI3U5mdsYIJMXfjhkxgBhvmkX+nigR2"
    "JXcMlxuUBEHPG5zYUprGttYsJf+Pq/OOy/n7//+lVBoopZAmkdEgSeN6ndfVQLIqFKkoijYaCCHbm4w32bL33uo6z2O/S9l77+yd"
    "FfV7Hb/PH8/z/a+bx+N+e766znmc9Tpdut5J1WIFE+eyvFjb4hyyahPvu7sUouufudK1WpHArpEt/FjZOi/S1u7vmNjPEFqnH5Uy"
    "hgQIvR33ymMHbZhe6k/y09OJn8PVbQJbF9yUime4AVYwIfbd4mgHeDlCK3076ioQ2OXRthU7tOMuuevEa+RVu8Iv65vSS34TECmY"
    "EPsu69AFulodlXSsRQK78me5sIorJWSxMa/RblYg7JArpKZKb8cKJsS++86wF5QN2C49U3YTmMAu6zMeLMtuNblS+bcnroyALt2K"
    "pRNKb8cKJsS+u6dpLFQ3XCJZmIoEdnnf6cJWrB1Hooo5UTcjEQ4ErJcaK70dK5gQ++777alQ82m0tC5DJLDr+lk/1sy/C2k4s+Xf"
    "O15joLvSd++f6UCxggmx71a0GQu3rDpKOeNFArvC5xN2sMs76VUIr5H7fjwsvaGR7t1P1WIFE2LfHb97PLDufaR16wNKBAK5tlRK"
    "7FeWDrGYwokG275QW7+F0mHb/pA72oF5rqoh0aatNF7pTdmX2rry8EQnTf9EO3bd8TdZu533kl//GEGLPgekyEMBgBVMiPnYa2cG"
    "T64USVOr/AUCu/b815pFX7tP7m3jxPqD9rB4T4k0TkkUVjAh5mOIZRuoGFQk/djrKhDYtbKuG9s0hhKn1ZxYc9QL9HcdkTyVRGEF"
    "E2I+FswjoGpVKC20Egns6mXmyaoC1pDf0zjhS3tCVcvtUnVVLcUKJsR85O8Jh3ofp0stH9UIBHaNee3NVpjlkpqhvEbE5xjwqv1X"
    "uqAkCiuYEPNx+NgwOFkQJdUzEwnsMlioZnPqeZNXnXiNrStTIendaGmuslrCCibEfGj0RkNwPXtpxiiRwK7HRjLLvPpOWl/DidGt"
    "xsK+ph2lDac6UKxgQszHdNNc+H3vqNp4vEhgV9M4DXu1tp/kyTgxt+0kuHPzuvrao1QtVjCxehhhX+u+k7RLeT4mKcTFq9fV736L"
    "BHb98VL+fVQ/ydCY17j+5TetypoipX7tJyQK9/zowjasl/oRybdtxb8FqospWF9dK6VdDwCsYELMx6QDVnB55Qzp7Wt/gcCu4cfc"
    "2aEwRpwceI0lQ5xh1tG1kvd0N8AKJsR8jJ3gBjWmUyW601UgsKv+ms7Mc91aMt+S19jWgID5xaVShLL/wAomxHxcSQ6CN8FJkpGl"
    "SGCXnb8v2/5sAmlTy4n8oeHQ9Px06Tn/v7aQggkxH2v3RUKTdI10V5mjMIFdQVslNqeZD5l3lxM3Fg6DvhOipBxlt40VTIj5iF8+"
    "AsZ+N5YuWYgEdq28JbOvV95LE3dyouG3UTDK0F6apiQKK5gQ89FoXibMXrxcnZ4pEth196GGbWvTX3o/mtdoVj8Xjj09ql6rzFFY"
    "wYSYj+O2E+B03wu+LSeKBHbdrNCwwVe6alt48Bo+0/MgvXS137e7qVqsYELMR8jtPGjy00B9aLZZCSaw68R2DVNvd/a9lcCJ6BXV"
    "VK9zoLRw0kDILVN2Kd8vkGGXWwkp+lnUkU0ceZKUL+E98cFxS4gtmS4dvRwAWMGEmI/6ZjYw99wAKf6Zv0Bg15/hXdiSjuvI/BWc"
    "mE1dIf6fKVK3fDfACibEfBhP6QSJN4KkIdtdBQK7Cu75sfGN8sjxBZx49zIQJp4bKd093wSwggkxHxNZMLT50VJ6ZykS2FVaT2ZJ"
    "mb7kyFheozIuEqI1GilLSRRWMCHmo8poMJCct+pIZY+DCew69lXDvnp8lOzCeY3do0bAf5+NpfrlZRQrmBDzMfx4Eqw2HqWWrEUC"
    "uxbu8Wdt6g+QSu15DWlSJoxft1ydpKz6sIIJMR8PQrLglOOd4v7ZIoFdD0P82eCobtp7zzmx3XoC+N6+4LvwZAeKFUyI+bgSlgvf"
    "LhRp7+eIBHa9uiCz5q1W06K/Y7uDKg+eOM/Slj9N1WIFE+s2KD9v7Kr9PpHn43ftJLB3maV10UkTCOx6t1FmPXVX08yvnOgm14E7"
    "LxpL3c8OhOcJ3qx+3n6SRloLKfoS58M2fV5PPBu25jt6o+Zwb0B/6fLFAMAKJsR8BLVzgDb6dlIW/79+EYFdvgcldqZ0Mim24DXW"
    "lnjA5/pB0uKpboAVTIj5ON6sC3RcpC+t3uEqENhVukujjNpqEmzEa8T5BsOgjS2lGcochRWBEPKxcVZPsAqn6hfNRAK7hkYFsH8/"
    "fZKCP3LiXEkUHOz/Vj1FSRRWMCHmowii4d8Z7dWm72sEArtGXghgI7tFSCnnOLHz3ySo7jhKnays+rCCCTEfZ52T4fS6NSWHmokE"
    "dhk2D2CDpe7aI4s5MVGdBe5rbxVvURKFFUyI+Xjvmwk/zI5o944RCewK6alhzeevpgMH8xrz+uTCs1NF2jj+radIwYSYj9j1Y6F5"
    "QGvadqxIYNeZGIlZLjGFZY68RsIiZVZr1JxueZCqxQomxHxMWzsRfnYypv8UlfpgAruKlX3UJMc6YBbKn6rgijW0HNtYOripG9xu"
    "F8RWxKSQKzbOQorgpMzmuU0l8bN5T7SwsQe3jzYSvRAAWMGEmA/v2hZQ3rtCrafMUZjArsKFAazHW4n0mP83teFe0N5UXypUEoUV"
    "TIj5mNfDB866zVf/2uMqENilNQhiB/W+SnencKK0bk9oWp+qPymJwgomxHxUnO8Fs2Mq/Ph3IWECu2Z2CWJtrkVKhcN4DYcx0ZB6"
    "uL26hp/DIQUTYj5O3Y0GOq6O1vFzjUBgV75vIBucE6wd6MNrfNZJhknPV5fUKKs+rGBCzIfz7ZEwa06Z9pKlSGDXUGt/VuK9hnb6"
    "++kudsmE5x8Pa58qqz6sYELMx+OwUWBq7k7LM0QCuwruSCzmqymEXueE69qxsNivNb2hrPqwggkxH9/rZ8Ijx4l0/1iRwK6fk3xY"
    "1/2hcGAVJ657j4XlXcfQn9dStVjBRH9PiXXOMoWUVJ6PqQoxIHgMLa4RCewaOsCHNZgWCjMrOXHzZROYXLVTva99T9jhFcySLrsQ"
    "i3+chRTt2BXEfGpk8lHHmZ8hv3EEzZPz6shLAYAVTIj5GD/fCWbEeqvvKvsoTGDXny9dWaeR36R7erzG13xvaFkyTx0yTVn1IQUT"
    "Yj4Km/iCRVMdP6+jrgKBXbUvu7JXuwZJzt844R7SC66eqfB7UdEEsIIJMR+LC3tBzXt3rX4LkcCu5M1BbLBuiHbaTU58WRANwx+p"
    "tBbfaylWMPF/8hE2GNIf3NFavqoRCOyK9g5g91qtpTf3cqLrgZHQL6BMG6AkCiuYEPOhPpkA1ZGdaWQjkcCuOlsIO7zQDNrnc2JM"
    "4CgY+8eNapQ5CiuYEPPhsjgFTI5PoXKGSGCX9w+lh/qFQUofXuONUSYMsp5II892oFjBhJiPyqJU8J2xlY4aJxLYlertydyWzoL5"
    "lryGZ+0oeBi5kZ5U9lFYwYSYjxq9THhTuIJOO5Dqhwnssj7Qmd1wz4MaiT+Vd0JjWPnsud+ik30gR9WTfXW8Lw364SykKLdpMLtm"
    "/lPKH897u0VeS1jVpIs6VNlHYQUTYj6+VDrByR/mJclf/AUCu/7c7s5eVQyW2vyt4RnhA7pVOn7R/K85kIIJMR9Ll/hAl9+DtUuK"
    "XQUCu25HdGOD7/XUNh7Ja3xq0gvCDN21Ky80AaxgQszHxbshMP5MpfZZc5HAruHrA1n7sCKq05vX2K8/GL7G3NGWK3MUVjAh5uNc"
    "04GgU+VNM5/WCAR2DTwhswbJjeBCm7/tsSoBPrbuTPueL6NYwYSYj8iXQ6Gifj7dZSYS2JXFfFkr+3Do9ocTvaenwNedU+hAfisM"
    "KZgQ83HGKAFWDt5Ol6SLBHZ57fFktR9mQbdSTtRfkwrfp2ylO5REYQUTYj5sRw2HRfUu053jRQK7rIpc2drWW6D879ie9W0k1NtT"
    "Qa/eSdViBRN/zDyZ3dhZEDeU56OpQpjsraC2f0QCu6zHu7KrOlug6DYnvkw1A+9EVnJ8dhg8n9GLbXvsJ+0e2kZI0Zm6IWybS6x0"
    "6T1vQdP7LaG8tlFJ9PUAwIqQFSEfO5o4gf6MqVq7H/4CgV3vgoPZ4OreWst3nHh00xvuFUdpHymJwgomxHxk7ukCYPJJe3i/q0Bg"
    "18LQrmznkXV00UNO3B0UAlXVL7SPlTkKK5gQ89FiXnc4ft2HXmgiEth1ysmfxUw0hx9nOeF0IRImr/Sm+7/WUqxgQszH9C79YE3+"
    "VGrxsEYgsEv3uh97MYjfnuaE1amhoH0/leqXl1GsYELMx4aoKLh7eRuFRiKBXTCqM4uYNhscc5z/fqfscPjUczu9ryQKK5gQ81F1"
    "KRqs8i7TiFEigV3zzNxY7pItMF3Da/ybNhy+6F6mv5R9FFYwIeZjzJoo+Lj9O304XiSwy7u8FVvsexqs6/IaueohkNKpirreS9Vi"
    "BRNiPgK7x0O7QW+o96j9fpjALqfgNszg83EobcOfatmM+jDM719ti2n9YPmlXmz3xqnalWVthBS9ywphgyNDtVolaSrVAPOWcGrv"
    "FG3WjQDAikAI+ahr2gJOLf2mDXnnLxDYZabpzlLCNtDF8bzGvXde8OXlBy1VVn1YwYSYj4ORnnDgaxd6Y6erQGDXqIsBrOa0BcyJ"
    "5DXWmHSH+EAf+p+yj8IKJsR8XDkUAEOtJ9NRliKBXdYdlfX1y/5gruE1Pr4Lh4HBU+kcJVFYwYSYj7HQC4Y/30wrlERhArsSJ3kx"
    "j9A5cMaG18jpEgU1O7dRc2XVhxVMiPnY7BkOT+tfpPw7fjGBXR/K3diHHlthyAdO5J2OBpJ6mXoqqz6sYELMRwuDfvDz6DfqnCkS"
    "2DWvS2uWX3Iarh3mROtVUXBh03f6nicKKZgQ83E/sC/kNWkACyaIBHYtuWrDGm5+CBuzOfHzcz+Y27s+rHqaqsUKJqq2tGLxpqfh"
    "Q2+ej70KcU0h6v4SCewK3mfDHmY+hLEnOHHo33rgM/OH1qz7AKi93ZOZnCiiizu3FVLUIakHM7HZRH1u8RacrucIlsZV2tIrAYAV"
    "TIj5cKV20HhgJ1r93F8gsGvt0SA2Q20Jc+9x4tzSTpBs24XG5bsBVjAh5qPDaneYcyyHDtruKhDYVf+qskY5GQGbrnBii1cADBub"
    "R934+yikYELMh8UINRxcs45usRQJ7Jp7uQu7GD4XPhznxI2cXpCyZjM9ryQKK5gQ8zGrNAjaFZdSy2c1AoFdxy66s5lB20BnKSd0"
    "LcIh5ckF6sJPz5GCCTEfhoXBsCv2M61sKhLYlfWmNctZeAZ2D+M1HleHQ/CmbzROSRRWhKwI+Rh+tjuQDyYwP1sksEvPx5ZVd3kE"
    "0W3+1vDvC6cbN4BTSqKwggkxH2tDAiA5yw6k8SKBXQVF5ix3y09Qv+XEr4bdIcTADr7fTNViBRNiPj6Y9oSfqc1gwITrfpjAruUm"
    "Vqzw5Ufo2/DvUznoQs8F7ajRxgg4tLoHy+5nCps3thVStO9ON3bhsRV0DG3LZ+cDtlDH04M2uhQAWMGEmI/GHazh265kmvHEXyCw"
    "y22/huk/GwibB/AanR+6wYW12XTUVDfACibEfOQvbAuBpivocSVRmMCu5Qk+bMusf2BKT14j+70fnGyzjk5XEoUVTIj5OEk9wWj5"
    "CXqlqUgIPd+yI7s7ZTu4ePAa42cEwZcRpXSGkiisYELMx6OxfvB212u673WNQGDXzCfObPGRsxBmzGu8GBsMbdw/0zPKHIUVTIj5"
    "qFcoQf8bhlDWXCSwy+OpLdvQ7jF0ucmJzJLucOSZCWQrqz6sYELMx5JnvmB40AbCxogEdvVSWbDckF9QtebvKBocAONH28EfJVFY"
    "wYSYD/uTnUA+7QYG40QCu0I19Zimth7b/vc3L/3XG3wOu0GHW6larGAib7I5K8z4CWZevEa0QkxXiLyvIoFdp1rUYw6P67FJezjR"
    "a8kvWvU9gr5eHQlDm3dj0pI+cNm8nZAi49IAdjZwMPQ6z1vwTdtmMK1dEm10MQCwggkxHz8nNIb7/RbQ6Kf+AoFdZl38WOGbeTD1"
    "Eiem32kDz+KW011KorCCCTEf4X1bwM5Th+nO3a4CgV0FqzzYnuodQE9zYnVPT/hieoI+VhKFFUyI+eh/rz3IJQ/pb1uRwK7UZm3Z"
    "1bb/wYStnPjh4wfhoa9p8LdaihVMiPmY+LADNL9VF/Z+rhEI7LpdbsdOjX8CdyZyYnSuBFYlhmCuzFFYwYSYjzU/O0C90qYgNxUJ"
    "7Bq1xoL1GVQNl/5+umZ3fSFsqw3kKXMUVjAh5mNpngsEJLnA3VEigV0rl9dj3gMNWZzV39GHdQLnE8q+WUkUVjAh5sPkfEt4e0mC"
    "OzkigV2tN3wHT1cLtuwBJ/avbQMpbQjYXE7VYgUTYj46/3QF25U+sKjCVo0J7PKYpmLPvzVkUdV/95y93yvrnsl0gN9AuDjYnxWc"
    "ngGG+e2EFO0gEruYUwDOQe14aidbwKmEAvpQSRRWMCHmw17bAHKHbKMHXvoLBHa9G+zJ7u7aBdCd1zDd6AguPw/REmXVhxVMiPnw"
    "rG4Gu/ZfpvsPuQoEdr2b3475viiFBj68xoIx7eFji4c0o6IJYAUTYj52XnSE7Sa/6ZIWIoFdFV/s2UWHZ1DXmteYv6UDHNlUF2y/"
    "11KsYELMR/ABJ6g6aQ5Bb2oEAruujm3MIi79hjFfOPFWyeD4nU0hTJmjsIIJMR+ub1uAap8z+JuLBHYltzNk198ZMvUZTrzMdgFt"
    "tAu48G9VQQomxHxMpTYQfc8XhmeIBHYlBvyA6QUWLHQhJ9aXtoTdFRLMVhKFFUyI+bBbZA6RqT1haY5IYFd85T0YKNmyrZG8xqVB"
    "TeCIey/wUuYorGAiL/U7rKtvwVL+zrWNFMK0Qy+YpZcmENhVeOQezLO2ZRM3cOLa/Mc0qve/tP7MgVCc7MfaXdgIgZ/aCSlKDfVi"
    "MxftgUQt7yVZl+rDmZCt9Jay6sMKJsR8TDU3gMMnGN320V8gsKvWx4Wdf3oeGlJO5A9uBtEXL9Ez090AK5gQ8zFutRl0/vSaTipx"
    "FQnkMuvnyBpav4ClOzlhk+EIE4dX0ykXmgBWMCHm4xCxgq2HjUFtKxLYlf+PJcvfWgNrFnBCPckJ3swxh2H87jlSMCHmo7drE8ja"
    "5gBuyj4KE9h1/qshq19sxB4l8xqqay0gY6EzHFUShRVMiPlov8wCjCM6QzczkcAuq57KGsi9MWtPeI2zh22g5oIvuPP/3wApmBDz"
    "saPCBJo+7A6aDJHALqvs+0A227KhxryG3kJzME/qCWP5d54hBRNiPpb2qAOHx0SCTbZIYNebNQyum7dmYy9zYtQPPdi6YSC4PE3V"
    "YgUTYj6ebTeBkLz+8Ni2jxoT2OWxoxwc+rVgDV5xwinjGnVetpl6Th8IeVGeTHfDCZgY3V5I0e0mbqyw+QU41LE9v7fURR+2zAaa"
    "fS0AsIIJMR/jjf7QoStu0BE//QUCu56+bMH2xL6EQndew6u+GVz48YpGzHQDrGBCzIflVX3YxuqAsTJHYQK7zly3Yp5pKubmyGt8"
    "fWYJ/Qcaw2JljsIKJsR8/BltBN1Sm0DrpiKBXbWfjZgdNWbGhrzG099WoEpxgIFVtRQrmBDzIU80hCn9XcHqUY1AYNfaY7+gQwNL"
    "dvH539FnqgX09OwMw5VEYQUTYj6Ota0Lpxf7Q6mpSGDXxaEP4GGoHfM7xolm50yg0eXuEK4kCiuYEPORdaKKpvXpB8NG/R8Cucyt"
    "T8DcKa1Zh2mcoMF1oEVGJKw604FiBRNiPl4MvEeHnIuDZrkigV3tHDZArxWu7EA3XmNL3HNqFj8MnJQ5CiuYiMhiYP2hFevZnNcY"
    "N/Q59VGIjz9FArvMa9bDmzGubMYiTkQMeEMnTS6nwaYhMNexJZtp/B20bi5Cis7tdGJXK1+DtOlvT5xQTZd2vU4P3wgArGBCzEf7"
    "3q9oSr239PQHf4HALqe+TZn3/jrMfTMn3gXrwwLPOtBDmaOwggkxH5U3q6iVTX1wVvZRmMCulY4mbPYXE7ZqBSd8bI1gkn4T2KXs"
    "o7CCCTEfwe4/afHXFjDeUiSwq+HM3xDfyor9msqJmX0Nwd3cFYiSKKxgQszH6mVf6Pv13mCiJAoT2BWx5SE8lezZw1heQ69JXXDJ"
    "8IdkJVFYwYSYj7Rdz+nMbr3geiORwK7WL0+AtrMzM/k7iloeqaLmmn5QeX0RxQomxHykx16isRYx0GCMSGBX7ewN8MXEjSX/4sSv"
    "yHv0zqk4WH+uA8UKJsR8XH90kM6PTIbWeSKBXR4np0Hx2U5s1HFOTM/V0gtRqbDidqoWK5gQ83E/uZwa9EkC27VRakxgV/7URTDu"
    "Twe25G/Oo/IvUacWd2n53N4Q/LYpi3huwE6udBFSNPNbM/bOWpfdbObCT6MuV1LV7Nc0WpmjsIIJMR/S6qvUhtVSb2UfhQnsmpJX"
    "n1lHNGCrbXmN1je/0kH5JnBc2UdhBRNiPpLc7tFLA61Au91VILCr9e4a0MtqwuZa8BqmhT/o1+nKjkJJFFYwIeaj1aG7tMDFFQwt"
    "RQK7Qvwfg1WSAzP6w4kHPb7Qu4O94aiSKKxgQszHzhVXqH92ACx5WiMQ2BWrewq+u7dhe25x4tP85/SGYy/opCQKK5gQ8xG6+QTd"
    "MXgAzLQUCeyy89oIIWVurOtWTnyJuERP6MVAF2WOwgomxHyU3d9GnRwSIChbJLDLymo6pKo9WZvUv7+5ko+u/ZOhlzJHYQUTYj6i"
    "n82li31Gw5JckcCu3vN6wOUt3qyhG69x3+1fml2YCVtepGqxgolTm6ZB9ZpOLFCP13jn+i+dohAbVWkCgV2943pA7SRv9mQcJwKW"
    "HaLquEoaOycU8vY3YD/zzNl9Q1chRd/rNmR6zxqywMW8Jyb6XqEDm9VQfgsJK5gQ8/Hf4BL6z956sP2pv0BgV/FiFVtS1ZTNXcaJ"
    "uK53afwBS0hUEoUVTIj5sFOdoNuj7KHRDleBwC4rl6eQetGRrZzPCcntLnU86gLeSqKwggkxH8OullA9lRcsbCIS2FU54jTcTWnL"
    "bmfxGpMGXaHXXQKgRkkUVjAh5uNj0l46VBsC+q9rBAK7vFptgtKL7uxVb16jS8EJmuQ1AKKVRGEFE2I+tq1bRe3KokHVXCSwq8+G"
    "6TCmTmdW1/pvm9/eRm83SoDGyhyFFUyI+egHU+jrhSlQPEYksOtC/RA44uDDzj3mxBElHxZeo+Hi2Q4UK5gQ8/FcJ4B+i86Burki"
    "gV3SQkMY00HNbv0d2zOqwmhrs/GQ9SBVixVMiPno9iKT6jQcC3peeWqBQC7LHGfYNcOXzTrKiUmXv2k/7J8IaTdTtZMyDeG+gZrt"
    "/NROYzx9PjUMI2yKvcv/eSqfjbe0z7aPB52xHShWMGFZaQjbdqnZwoG8PabUDaCLB+XA4dMigV3ip1s+zZ0W9hoFKcoqHCuY0H8S"
    "AgZvfNj6Al7DSTuFmuenQPJ1kcAusZecuJVMHxyIh8ymZUKbY+LLsBngZurFtpz4O3MuWkWrNkZDeZlIYJfY2+fGz6N+Y8Jg5qca"
    "oe9iwrjfZnjctCMzf/uX8N5LPTJDIF3JICawS0ztso+raKsYCWxsmgBWMPHU/CzYvWjHkg1c+V5tWAldM6MzTCgXCewSR59dmzbS"
    "vabO8HmXqzCWYMJ66HMwT2rJVjbiNaI9GXXfaQceypiICewSR1HHOxvonlhT2PXEXxgTMeFZVYfdX2/NPOrzGp+aF1PLCgNodTFA"
    "ILBLnA2qwlfSkEmfqOZruDC2Y2LJPzqsuLMtMx7Ha3SzXEiPZr2m6w5FCAR24ZlIpep4/pv2oZKoap00IVE7RsynP1sT1j9ZzIpK"
    "ZT4tUUuc86Bb4zQtVjBxpKENnbmNsNK/O6/Pn5y1hufy4PmCM76YwK6DT+aWXKwlbMcKXmNg0wElBXPzIMU2TYsVgfg8t2TldcLy"
    "nvMa9y5EquM88+A/ZYWMCewaGTVOGupN2Fdz/pvvvhGp9leITVWpWqxgotR2nDSwIWH/xfCn2vnntXrLw4lw3DhNILBr06lD0qFu"
    "EtuyiBNh51rQ82d0YLRfJNROOAC19buwopNumgjHMliX68Yaqdw0rdvsgDdxXqxXthv/W7IesXROa2t4fCUAsIIJGLQNXEZ6ss11"
    "OFH1qR018bOHtj/8BQK7HpbPhnZXfdmwTE50eBBGh5d0hISZboAVTMROnAXWNd4s/iP/rAKKLejeIV6w+IirQGBXTce+4KlLWJ3h"
    "vEbjYx40Ibk7/KpoAljBhOW43mA4RM0yrvIaR63vaD807QkJzUQCu2rcTOB8tcx8QngNY2s9esEjCnS/1VKsYIJ2MYYWSwlruJvX"
    "8DUdou2yJBo6Pa4RCOwybr2ArtRq2NHWvMbaQ/9qK8KT4LQyimIFE8XDC2jTtTJrPIXXCG361Zd0TgZDM5HAroNxc0vq99YwUs2J"
    "tWWXio+rs+CsMhtgRSD2zS25P1Fmw3pxok+v1epO0zIhLkMksGuk6Xjp3WHCdp3lxJ+r09Ur5udCjbKmxopACPm4md9U+uM2DkrG"
    "iwR2vbZTkWN6aqYz9+8Il2IgXYOJUG/lFF+sYELMR4KLg/QoZgL8aJKmxQR29dBREZd7fuzG9b/jbl5faW2sLhwc3R+aHe9JLpoF"
    "sScLPDQ+L/TJw5ld2apjHTU+XXuQ6nP+rI2LBz+Z0MZI2QHNYfsvf8AKJpoN0SPDhwWyqsCO/K9STGKl3u2sIUzZ12ICu8brdyc3"
    "d8ss/ygn7v4cKVkf6gBntK6AFUwc16lLvo/zZ1WsA98PRiZJg1+6g910N4HArjs6XcmOColN7cRrnLk+SvpyIRCiWjYBrGBixRUd"
    "0uGizOLdeI1PXqMlncBAOFwhEthl5B9IvrRVs4/rOXGqU7a0tFd/eKCsALAiENfqkPsjCfNe5M7fef2TLYX+7AdvlRUAJrDLp8yf"
    "RJf7srN6vIadQY4UVRUHzLqMYgUTSUZ1yPneElvyhmfQrkeO9KI0DqzLRAK7VhRpyIbDPswxlj/Vnp6ZUsXiVFig7DmxgolBY1Xk"
    "6hQ1K1bzGs7ZmVLA1FT4cEMksMuoVCaz33mz7vs4EdU4TSqpzYRrygoZK5gQ81HYKk1Kqs4Eo9MigV1zusrk3BhvVlDDCc/Jw6RG"
    "zcZBf2VWwwomxHz8mTpMOtF0HBTppgkEdt1pJpM6IcoYHMxrwAlz+HS7GyyJy6KxZw1ZwesgFnC7kWbuN0O2xb0rG+xmrlmyw47t"
    "ivVkkQWN+Ch6Xp+e/TUBbAYWaW8M0AG7VWmsq5GlRnppCd5PU5nj28aamluWUFuayt6saMxXfTCWFkzPgfaDirStXqeCumAk06Q0"
    "1jysnAwXg0awN70bawruTIZ2LiPYwT8WfAfpcoDKP9PAqHeRdvGB7bChcCjrcdVCU93yIDQtjWU+Ryw0pNFBiN0Xy3QTODFvWiXd"
    "NCYeQkOLtLkd7oH3hQFsva+FRrfrc0jO7McybS005q7P4Wl0P6auMOdrn9uRZMGR2bT4wGtqNTZOPtd1AchmVfLKKYPkFhHFoG/w"
    "Vd6wOVo+MGvL359VqtlLh5M/457QZv+d8z21c6Ds5XQagq9+lW8+C5ULtU//uhLLw+SVjR79j9A2iSIj/uhA4rkV2ry4XvKBelXQ"
    "1/+rvPJADznv4Z+/rqsxIfKR9dX/Ix736VpycM5E2KFXn363bEWnR2awMh9LTWrpam273AyWMUj5uWCdlszMYJcy+P+Yvq1mX0m/"
    "1nkwYkCRViCQ64hTK6o3OoPV+YcTc3wOl7TXzYPjt3dpsYKJd7s2atULMxgUcGJ7h5KSyzfz4EfWrRJMYNe7qZu0zxdnsNjtnDhp"
    "9Lm4XWYuXP5JKH524Qn3Fmq3JGaw4TInHiy6Wjxj1li4kJxFsYKJwudOdLpuBtv3jPerxTvHFm+rzIHpo/IEArt25c3T1u+m1Lbn"
    "NeLtLvixZ3Gw8ORbeue2qdZwVTpzPNlYc2dXjHb6i3RW+LixJudfJzo8J52l/MtrTD2l43fxXQrUfXiCYgUTLjX52rXOGay5Ia+x"
    "f8BYvyZFSdBke7lAYJf4e3h9L/H1KRkDe/9ZRbGCCfH3OPdSV63bJxJG7agH+PfA9Q5eWFOiF5XOonbyGv/G6KhDmw2Czuf1ACuY"
    "uNnbiY6qTWMr4jnR9r2T+nX3vpA/3kIgsOvy+1PFpxzTWc4qTpy+7av+ciwIWrk6AlYwEXG5Jb3ZKo0dd+BEclas2us/CcbZtxUI"
    "7Nqs6aRuGpDGFqZxIqHFFHXhAWcY95AAVjARIbWkVm1SmdNrPjJ4DVykfr3aFl406y4SyLV4+AX1KeVn8568xvvhsnrpHhP4Obs/"
    "+F5fTg2fJjPHfy00Vudb0NC4FDal1OL/1NhSMF89Z5MJXHPuD1jBhJvnL9+ZM1NYPUNe40voIvXk7bagMusuENglPtUfV6064Lc+"
    "mPpGAlYwYUjMpMUhKey8Lyf6bUwitmf/o5PDi7QX30fJiV+LoX3kN3mH2SC5MO80vHb4Jsf+GigXJ52G3LwqZfQZMGcYGdfhKR3c"
    "pUiLFUxAaR85r8U7eNuUE7N1YsmVwXeov/c4ignswiOfSvXyQDS5ffM3DQ0pEsZETIwZ20s+4lgF9BknOjaOInte6sDzviKBXXhE"
    "ValqGg0gtd+NwcDURY0VTKQ/9ZdfPTFi/58w+ZNOru/YRZt5F2kDTsTLyVYLoQi+yYW34+WbrRZCg7jvMv4MVSqz3mNJyy/J1Nin"
    "SHt3RpLcu3kXmP77u1y5Nkl+4dYFvqz5IR/wGi5Dl1kQsey7QlyNnUiqrn/V2rct0up6p8lv05bTtu4/5fSwNHlw3nK67MpPWXdc"
    "skwrncDr2g+FkN5MIraTA9XaXkVar7I0+dXIrlKyZ7VMqtPkK3++qyeoquVTj5Wfn31XN4j5pRCmnnnEcb5uyZBORVqsYOLmpjT5"
    "5qqR9I4eJ4Ke5JLnsS2lUdFF2g93kuW2AbZEP+O3vOHfFLlsozEZ5f1bjs9NkZstNSa6hdUKoXdpInlFr6t9A4q0WMEEflpll+ow"
    "jmyeHy39616kdatOkOdY55CeN37LN80T5e2eOeT42D8yrq1SPWyQQo7qnpRephVpz58bLE9cdJRUvq+Rff+JkXud30PaHa2RczJj"
    "5ENH9xBt4xqFeO0xitwv3yzx3o4VTLy5PFx+VzKNvNvzRyFSlseSFY2+SZruRdqrn/vKVVtekZHmKk1Dt3B5+PDHZPmnWjm/Sbg8"
    "r9dj0qZPrcznwQQyJ+me1NS1SIsVTOCnVal2Z/UlG/3MSeNY5dNd5i/3KTKWbberNAFBQbJbqYH8vkClaeceJF88biAfkVT8/7SI"
    "jSSZEQbEI6hIixVM4KdVqXbMkcjX0jYkIqxIa76hg0xu28vHA+tonp7pJCd3s5FHtamjKdjfST7X2Ub2ucUJ1fVuJJHZkh5KzrGC"
    "Cfy0KlXtok7k7KBOpJ9fkbZ4n4O847m7PDW7jsb4lIOc+MNdPnaujgbXVqnSPM3J7vF9ya0EZUW2uZ5c7Bcka/N1NOnzTeTKdH+5"
    "LFFHE5VnIveJ8pcXWerwb794YEvstd3IXWVkwAomZnrayjnuneTVT3mNTI8qKftGLOkfVaTtdfoJSdweLtc66GqGO7whHgNC5Rn6"
    "uhqnem+IgRwq9znEa+TbGhCH/EgyVy7SYgUT+GlVKtu4E5KDewopjy/Snjm3j7yRY+VhxbqaqunHybnUaPllka6mYtRxEj4gWt7X"
    "R5effqy5K3WISyDxPYq0WMEEflqVasKOzVIDn1HkgptS4+5M8uWfBHnoC13NvNczSdSmBHmZV10Nrq1SrVgSI3UwH0du+xZpx99w"
    "IrofU+QRU+tqyl46ETvDVHnt1bqatjkTCVQnysfC6vK/PvtyU03/m0iWKzVeXYuXCnpnyI8c9DSvPsRLuiMyZKsxepqyy41I9Z1U"
    "eeMHTpxUTdc67pxE7JVxd2XhApofmyE7uulrrJLC6cMtGfLHRvqawgHhNH5+hnzshB7/H3US9Up+d8ojzToXabGCiVIbS+nurgx5"
    "fAEnnnf8od0cNpFc61ikPTvCAewOpsp3YvQ1ruMcIKQiVTbbq6/BtVWqlU6L6LSZmcS+v9JLtsyHHesT5NFxBpqnqdOh+FeivKmb"
    "gcZ6yHRo/SRRTvvGiVW2qdTLbyz5rXxWWMHEjJmdwOpXijz7PCfWB/xHnVkSORahzAYbToBv/2h59m8DzdV1RyHWK1ae/8hAs3L+"
    "USi2i5UjCgz4/ZLRu2h3gwyyWq18VkjBBH5alepwn98U7kSTpMAircG2z9DOKlRuvbKepnXD13B3Urg8dVI9zYFvryB3RLgc4lKP"
    "vyXb8ITCrmFkkDJ/YAUT+GlVKutVRjAiZAC5qvzm4SEmDJ4HymEV9TS6g0zYyl+B8mxbQw2urVKts3KEGw5B5LbSHtUnHFjOfQ+5"
    "b4qhpuqKA8v/6CHP0hpqDgw2ZQFW/nJPX0P+Nry/Fyz+pwM5o/T24D+dGOyyl/0MjDQhpp7sHLWXx0QaafblOLGQInf59m1OXBwf"
    "Bvf7m5IzSr9at7M7+77bQP7PyFiz5UEQm3nYWK7zwUhzvzSIwRZjuWy1Ef87yAY9wPiVNTnmVaTFCiYSu3Vh3Sxs5PIxnNjdZxCM"
    "6FCXXFHao6JrP2YT+IoM8DbWtFD2fxWDX5F5c4w1uLZKFbMyFbJ7H5dsg5Ua1nGs8brd5HdXE00hGcKWvD1CrrQx0eg6D2FOt4+Q"
    "lbc40f1lIsQ3vy7VURKFFUzAsQGsYuUj0mMLJ3R3ZMOb6qmSg7JX+7Eoib3WZpKyFyaaXpqRLMtgGjldaqI56TySTfyZT+aNNeEr"
    "y1mjQffFGklPGXexggn8tMqa4fc48FzVS/JSVjKT7NPZnHAb0siyvma7dzprO8yGBCfW1+DaKhUzzQODkcbqRKW3y2Gj2RXjz+ob"
    "zRpoFtuOZtsudpPSautrmugpPx/vJnntrs//lsxlElidOKLWIUVarGDieXU6W3HckKzK58S01Elwq2WR9vMgJedFo9gEeRWNPdhA"
    "E/97FLs5bwQ9XNhA8/rJKPY9cwTN69qAj6LKnnbIjIMl3fyLtFjBBH5aZT5/PAHCThvSz8pnNWRnGqtZ3wqaPGugmXImjZ092Ar6"
    "ejbU4NrKKiN0DKzQWUE9lPZo+z2BVU9fBDc+N9TMzh7BdlyeBV2vN9SYx4xgLU7NgobTGvI37qE5UPMtlwYq/QormKi9kcoOL/eB"
    "Q2GcOFczAhJ7XaIPBypzlGM0a7j/DGxfaKq53TaW2aWUwORMU81Qc+XnyBIIbmGqEN/mpIFD9iG6RZmjsIIJ/LQqVUVZFJw/XAeu"
    "9lNmtaV92YEHVeDU3kzT1DqcuXV8Bx8bmmkq64Yz3abv4CjlNbZBHEwNeE1XKyMDVjCBn1aZo96FwOcxTUGt9BLtbA1z6W7Gnp40"
    "0xTPDmTFfvXZ+M1mGvOsQAYu9VlAfzN+P7FTPygprQ8GSi/BCibw0yr9qqs3HJzmBiqlRvJDNxZdrxX7FtNIExrlwdJ7ObKpmkaa"
    "3O4ezMvPkYV85ETVW39opG0JzSVllYEUTOCnVamGnDaBL4/7wQpltfQJ9Ni+FsEsZY255k9dI7YnqCtbPNlcOP1S2mNXE1BP7Qln"
    "lURhBRMFV6yZx39dWF4NPyM7cawRzHfrBr6b8ikmsEs8VRvfpCX0zwlQ+kyRFiuY6F9ix96M9mQFjzjR8ZcrtC7zhu4+IoFd+DNU"
    "qayyVdB25mDIV1Z9+FwMfwriGVnx1G+08coB0PjnVIoVTIif1WHND+oYHgHf4rIEArsCHjyDc436sZY5nLjQ6weNHBQBi8szKVYw"
    "gU8mVaoOYU/pCXUv2P+wXCCwa8+gZ/B9aTh72IrXeDg3hrxasYSGNimnM1/HySEFC+DZ6CoZn+Kdbz9QLtx/ClhHvh8c+WIAueVX"
    "QjOel1OsYEI861unP5Ik/3OJvmi3TIsJ7IooiJBXlpX9jzhgm0TfNg4jo830YeamaXBgSYIs2elr4l9MgxDDRNm0r77m/U17OHc9"
    "RZ54lK+Wpq1PpUsc4knnFuUUK5iw7egA7YakyqweX8l0PqJPB7uOIIseiQR2eTUOp+neGXJRMq/RbGu19tXibCJdyqRYwYS46tty"
    "vl/J1mljSZ3hWQKBXXjFqazCtw4r0b+VQ7boTKZYwYS4Tlw9q5v67ctJ5HawuHrFLrySVak0c4Mhfv9maaKJPpS+jGHXLx8myXWM"
    "NaciYlm0yxEidTTW7JoSzhonvSQ/FvE1w9fMCAice1y60KycYgUTQ3+HszOfXhK/p5zwDgmB356vJb/HIoFd86YFsTHZxvK+bpyo"
    "IP1hQlatZHk5k2IFE+La50lOEOi+syTNlU8XE9iF110qVVvfILj9jyVJNplAsYIJcbXkYqCB3V9bkTXx4hoOu/B6TqUK21hBfZaO"
    "hGueyjoRncrjs3fxhN6u6RlqGRgPy7ymUKxgQhx9YsLO0qTKeICYLIHArnNXD0BAXCx73ZDXeB11lpa+jwePK5kUK5gQR58unw5Q"
    "552R8F1pQUxg19WUA3DzYQzbDJzIaXaQdrkcCXPtyylWMCGOPpPvFtFvR3tAywb6gAns2mFxADpkxLCr8zmR4CoR19hIKWGlIzy8"
    "O0w2updJ2m38JcfvGi7/OpZF3raulg84JcvHLxiRTS9/KmPJPE04CSmJkZZl6AFWMJG3Klk2sjAmPXrwcx+L2xGk7aKf6kMN9QUC"
    "uwpVaXJYne/qcDNeI/fhCDJj3Hu1lWM5xQom4J80+cr87+q7+zixc0kSabGgj5/7c5HALt9nqbJfl+X0ez4/8fJaPJYsmedV/EAZ"
    "fbCCCXx2plKZVWYTu59PtW9jswQCu/D5nEq18HI2+b72qXZTRTbFCibEc7h0OZfc7uBBzfuLZ33Yhc/9lPGqVxwtzFQT3VWOkOw+"
    "DQzODJdj7utp8Dh/do49hMSmyDtm8vFqZFgS/Tw6jCwapwdYwYQ4G2xyM6bpIRFknam+QGDXkW1hNH5XujzYmhMxxfo0Y+AI4tK8"
    "nGIFE+JsYDn7RYnZ5CRy5JFIYNer8fHSgZ/p8rnz/NTg1fB+JS7zx5LnZZkUKwIhzAaNP59T/+yWQ/YqawZMYBc+41DWDOPPqB12"
    "ZJPMOXkUK5gQzzK67naStl7LJUP7/5/zEuTCZyfK+sq+CwQ0XyBVKRlMto9h89ofJnPBSIPnkg1Nwtn9qkrSKu7vKPogGHpbbJGe"
    "KhnECibEGWfAQQlSV1+VbisZxAR2hTQKYm5OxnLKd753XpEaAn4jX0tgU06xgglxxpkEflA/0pgYPBIJ7KrUdmIGWfZyi32Gf79h"
    "PAiOf7EktUoGsYIJccZZFe0Bu03ak/vKSI0J7MKnCSqVuokH3MhtR2bvn0Sxggnx1OBYPReYv9yXpPcSTyawC59SqFRyg2X0YNEY"
    "eKkp0uJ3zfiNsvje2eXXAur+IAUyfaZQrGBCnNUKTRbRpEWpkKqMPpjALo/dk8HsbiJbuYUTKywW0bwVqfD7QibFCibEWS14wFT6"
    "eMhQyFRaEBPCDDd8MhwKT2QREZz4ljWVfp4xFEa2LKdYwYQ4q101Hk6NRoXBGWWOwgR25bSaDFcfJrBprXiN86uH04nnwkAnRw+w"
    "gglxVrucp6F9DhMYqYyJmMCuG0l5sLhBAtv4jBNRj+2JRUWI9GKyDMkv4mWjW2OIyvOXjOdE3z5J8opQI/JsGJ8N5t+RyParkVLW"
    "OQfACibEmXOQbQC5W1arHqc8FSawa8OsVDls1jf17j18bB/lF0naLf2ptkxXco4UTIgz54o6g4hl6AU/F2N9gcCunMhUufmDZTTt"
    "KZ+jXtAkcvaf3n6ycznFCibEmdMvdyQZveWI9uczkcCueI8kueaOF4T35TVqPmST0/WfaQPOZ1KsYEKcOf+xH02aJA+hvtFZAoFd"
    "+O2ZSvXnySjS+XQs9ToyjmIFE+Jbsl//ZBLTOovohn7imzjswm/llPXu3HA6Vm1PPufL4LElH+ZeGiaXbtLT4Hk3rdYO4mcny2VB"
    "fMY5VRZHzzSRiM5lB8AKJsTZefIXE1pW4E/WrHAUCOwq7BVGcz3T5dmv+fzx1cuYXt8VQQpG6QFWMCHOzp+6tNQm3xlIquvrCwR2"
    "lb6Ik86npsv5ubzGtXovStruSCLTrcspVjAhzs6b41epdc+PJJZPRQK75ix3IhGrUuQ+7TnxRP8/dYPQHHJd6SVYwYQ4O2ecC5dM"
    "bowm4+OzBAK78FsOZSe8J0xamTSaPLkzgWIFE+LbjMb950qHp2eRud3FNybYhd+eqFQ9Op6mm0a3J4alDlA454gyRkXLrY8qu+3K"
    "w9DQKlrulq2vsbpXCS1yQ2VfC3567vvcFrr2iZdOTJFhl2c0e5d0iFTNNNLg1UDVoDBm07KSBNnzebBpcRdIoQuko8rogxVMiGuG"
    "q9tdobrPMam7MvpgArty9waylQ+N5BVn+axmqEPArtE16exoPcAKJsQ1w/lxHSBk+h9pttKvMIFd6f07sXwre/nhEE70v+8H+8cY"
    "k8xW5RQrmBDXDA7G7eHIFDti+FQksGvkbAf2ZbWH7GXJiUbxHtDAoj0xLs+kWMGEuGYIvmQLFm6E2ChzLSawC7/lUD6rebYwLUki"
    "N3dOpljBhPg2o/VqS1hYrzeZ2l98Y4Jd+O2JSkW7B8Kwzy/UC5V+VXQvka32yyfR64w1rUwSWeOzU8nEWGPNp6oUtuK5Nanzh78F"
    "WOso0+wt4+EXKdLiW3P4bpx4g+5wSCea12MMGAzOp1jBhLiSmUY702m9M+Gw8llhArv0N1tCZVYquxLIa2w735n2iMiEP6WZFCuY"
    "EFcy0rbmNCU0ESYpe2dMYFdNqCUEvUlh879yIuVOc/ptfCKYKPsPrGBCXMn03KtLVcsi4KyyLsEEdlkaWcKSzBRWcooTw+zq0stf"
    "I8BdyQdWMCGuZI40v6w1+RMA/yorfUxglzSrMYSsSWZ3p3Ci2bAr2riNgZBW5gBYwYS4kvnTaa72853WYKKMJZjArlYfLcB3QxIL"
    "6sFrTGroTPoOPavVySeQu22ofPFUAUye91VOPzJEjm1bAP1sv8oNExLlB9s8wTuK38X5vXUgCYz/TdObqym+VRjRp5f8/dPXvz+L"
    "d3HOGscQ581vadk7P4oVTODbjSpV5wbx5EfXt3SyR5EfJrBLvFNkOHgoubvsMp2WmyXcEMIEPlVVqSK6JBHN9M107NlMgcAut4x4"
    "2eDZAkg156uMgvgY0j5zCW2krH2wggl87qtSLSkcTpICA+ljG5HArnPbRsox6V5QtofXcKvtT2Iinel4ZRTFCiaqPUbKruZe0Ko3"
    "JwKPDSSJWwu0bpl6AoFdFx+lyG8XLKNlU/hK5kp4EDmZ0F0bq/RErGDiXL0U+R+9ZdSohteIadmVaIKs1ElXHAQCu6r3pMhXdlWp"
    "37fj68SlxJnEDOutfqyslrCCCbf9ycq/f1WfLOFPteNsK9LyqUqaPpMIBHZ9CR8pG4EhOVrFa1QMbERqsnZKg2YQMB85WLax201W"
    "P62WV06Ikusn7CIZmdVy62595YqwB+TBLn7f58XJbDJt1F31uvnjKL47hO8wibeQNhjkEK8nd9QthitrUaRgwrd1ivxrmDG5/Jqf"
    "eBkOGk0G20dLTsrOCxPYVb01QR5/Ops0a8ufyv98PPGeM0Tqo8xqWMFEukOC/LpTNlk0mz/VZcvBpPWEDdIYa5HArj3ro+V5FntI"
    "nVJe43y7EOK2aI20XhnhsIKJyo7RcmPtbhKdyIl7wRoybON5KUoZ4TCBXb6VofIZo0fkfBG/6fS5hQsp+kGlYKVfYQUTG1qHyi7y"
    "Q2Jsw4nejRxJx5PPpL5Kv8IEdp2PDZC9JunLfUP4TadjdQyIxfgyaexUGbCCiep5/rLHBz25xT1ew7TFd6mH0SupfC4RCOwi3TvK"
    "fRyt5dYN+f2r7/6xRO/HLelb7niK71nh+17ija1ry2NJK4Pb0oy4LIoVTPSpCJPr1zwi39fz36Nd4zAS+bAuqb6SKRDYVfkqUK6c"
    "YyD7XeY1NK0DiddBFempjD5YwYRxdqD8wddAPujOCYdFncgvQ0syqKVIYNddg07yuQ3N5Xsd+P2rlxOdSLpJA1JH6SVYwUTlTg95"
    "TP/mslEdTminWJDdfvZEztATCOyKOmcvW710k8PXcmLVv7qk8l9z0k9Zi2IFE76d7OUP3d3k0dGcOLrmmdS1rSO5ftZBILArysNY"
    "vrhElvP/cGKr5XHJtMyELFN29FgRiNVG8pv/iPz2DCeiuq+QLKOsyIepRCCwq+phJWmR21veNozfClv4JZQculGXvHiZTfFNOdya"
    "4p27gvphpNm9uiQ3IotiBRNim/+5riHf1lqTYWcyBQK7rEd3krvVNpcdpvIadumdiOOXxuTLk3KKFUyIbT4nwpGMXdGGzLcRCey6"
    "2cRBJrK77HSJE8TTgiTU2JEtDfUBK5gQ2/wHqUOGtnAnvkovwQR2xR8wlg8EauR4wj/dQ4efSlWbHUi+MpZgBRNim7sPpdKHRq7k"
    "t7IrEgjkyrr7kkBEH5ms4jVe6iyXIkZYklJlLMEKJsQ2f0TSpRlfbYnePCIQ2DX8/RGSM2KQbFzLiVcFGmIz05q4u42j+K4jbk3x"
    "1uT4Cg3puNKazBqaRbGCCbHN7310JXeWuZPpZZkCgV26Yx1kry3u8kh7/lRTOzuS9Lw2xPxROcUKJsQ23/SlPjHV8SX83TYmsCvk"
    "l7FcsEkje2bwGsd/qciWe26khak+YAUTYpvPvHtL6rNNTWyUGQcT2GWz/xUxtugr2z3gRMIKrRQxzYXUrHAErGBCbPO7QUulaSu8"
    "yLIKB4HArk2Hj5KroVHyus78ZuZkOVUy+G1DqLKmxgomxDavyGstJS9qSZYtJAKBXdd1Z5CrefFy8RJeo6CeDjHxDCcbFk+k+F4o"
    "vp8q3jDtO1aHpM8JJztGZFGsYOL+gdekxbe+cudYTtzZdFWa/nYI+XU9UyCw64zrcdKuXrS87CcnwmYyKeZLf9JWGUuwgglPdoz0"
    "mTlYDt/GCS0USCF5sYQ5iQR2TRw4k4QcGi7XlfmZzPY3E6XJW/oSY2W9ixVM1LeYSeL9h8sdGnIi94uN9PnBALJ0lJ5AYNevBy1J"
    "n1XJcpcdf++9NlJJmuYB5Iwy42AFE9sDWpKG55LkyJGcqBrQVB3Qrisx+M9BILBr9tShEtikyZfq8XOfxBFd/c4edSZmyliCFUwY"
    "Zg+RYu1TZZ/LvIbLn8naZrZtiJ4y42ACu3Ke9aVRsamy+She48uSS7S8uT4ZPplAaJYRK+7hL++YYCCcJ516+QICVvWVN93j9zKq"
    "Zu2hsY6mJFjpu1jBBD6ZUqmejt1LF7QxIwbTiEBgl5vzYbjYbrC8V9L/e7d2B01/MIKYDplA8d1TfAdWvMXap8MO2m7ASNJIWS1h"
    "BRMFvY/Ch0sxsuTNibbVD6ht+xjCzmcKBHa5bXoFF23C5Q43OfFj421661YfcvyhsvNCCiZu2r4CWB8mv5vBCZ+nuvCfnz8ptxIJ"
    "7FpYaswKXQLlr634uU+3j79oVXxHslXpu1jBROo0Y5Z7PkB2/MZr6NibwZ/eLcjkdD2BwK6Qe/Zsw92OssMSXuNMe30w8jUjeco8"
    "iBVM2PS0Zxe9O8qacE5EGFrCp9I6pL8ywmECu6YM8mCVne1kl/ecmH5RB3y9rksNlL6LFUz0Wt2RzZ1nKxce5kR+YQP4lHZU6ruI"
    "CAR2vXMPYFcvGMpOvfj5Vc/LbWD983m+cQsIdLiRxkbaBkkLo02EM6vE6mQ2SLYmKWf4+dXNla1hz55V6p7KU2EFE/j0S6XyPeQM"
    "rufXqD8pfRcT2FVplcCcfKeSytacsLuYDPU6FEp6d6ZQfL8V37MVb8o2W5QCzUcuk37GZlGsYOLrjRGsqiyfZDpyos3RMZC8NkD6"
    "WZopENi1qDyNtW1uQ34CJ/b+lwCf/3OW9JRxFyuY8PVPY3dYc3IonRPVnZPAqP8U9cAWIoFd9i1HsZE63aTbBvymrHPpQNDe6aJu"
    "o6zhsIIJaWcGe7W2q2Rwk9f43WgQ7BzZWzsoR08gsCtgTgY70iKR9knnNTzsguCgabZ2ijLuYgUTb/els5t9Emi6CyeGUH8YNsuK"
    "NixzEAjsejo1hfVu7gSG5zmxY01L8JtmQWuVlT5WMHF1VjK7kNwSRi/mxKbh9nBdZwhtrYyimMCuyj7DWcTnGTDCg9/fvXkxB0Z4"
    "3i1ZOzqP4rvA+E6yeKtYJ3MsOHe+VvJZ6SVYwYT+/FHspsMImvCRP9XgltmQfduIxilrOExg19rINPYisRXUzuM1Ig8nQrCOObV7"
    "Wk6xgok5F1JZmn4rKFY3+Psdv3Fw5HIujbIWCexqOSORXfSfBfvuc6KtTSh0PZ5Dmyi9BCuYMDdPZOk1M+HhTk4stgoGvdLtdKKy"
    "0scEdh26Hs0Sg4uhaU9+qzgipxPoL1lHXZURDiuYCG0QzfLWHgdvI074PW4LaxaW0uByB4HArlrrUFbw/jVs2/SXON0AJnw4QNsr"
    "YwlWMGFD+jKDr6+gURongivrQkzCVbpLGeEwgV3bHmnY7N7GbFVdfnO56aUECKjcTy/PmkrxvWl8f1u8gd38SSLUebOfbldW+ljB"
    "hMOZGJbeuATcK/hTDeo/GLq3eUHHXcgUCOx6czyM2Z15C2tH8Bp2jXrDoO6PaPdn5RQrmPgih7FzPm8hqgknStJlCB6vDw2cRQK7"
    "TtAANmabCXu+mxNVZ9zBc2wtjW6gD1jBxMroAFYVZ8LMJ/19qvEO8K2lOXwfoycQ2LUpuCPzDHdgzZvy+9SwtCFkvzOApspYghVM"
    "7NvWgVUxe+Z3k9d46lxLfT9ZQbmyH8QEdhX62LJjRzxY92xeI7HzZXorpS4sUsYSrGDi8WIb5vajI9svccJC/wAdlGAKJspYggns"
    "Sneux5wWBLBDDzhRNjIKEt88p0e6TqH45jtuTfEO/bOeg+F6ixd01eAsihVMiG0eatUbyG8j2FWRKRDYRdwD2flqE9amlhMVITIc"
    "SdCHA8qMgxVMiG3+Qs8dZg6yhl/2IoFd6vXKp77Rgb0P5r/54bYOEPe+EWiVsQQrmBDb/Oq6hmCkjO/hykofE9j1+D9b5hXViTkf"
    "5USkSw0tH2sFbspYghVMiG2edu0OPTvVCd6ccRAI7CJH67HUoYGspyW/F15VuI+emdIQ0pReghVMiG3+X6+F9PO8ptBPWZdgArui"
    "3J9A6LxQVjiB14DEXpB50QgOxOVR/LcLuDXFv4KIadgbFvwwgnqDsihWMCG2+RQHNUh9HODL2UyBwK4jhh7sqo4j67iC17B56gap"
    "/tbw/HE5xQomxDbv38EG1sW7QqC1SGDXPis7duJQJ/brJSe2RjSEL9Etgd8XxQomxDZvdPc7tXnrAYHKjIMJ7PrT0ZCZWQSx9pH8"
    "013/5TZdVt0SQpVeghVMiG2+Sfcgdb7gDo6lDgKBXVtsn0JBahhzOciJnU0W0LWFTeC9MuNgBRNim8+/OpiOW24PzwqIQGCXQfE+"
    "SDw+mEU35m/7Ip6pyeuGQfRPTkuo/hAtj8ne9Pc919qKGPlp6Zq/P+N3esreWeVMMksa00d5auFtHyai6g6RLz5b/L83cdbbnEjl"
    "o3o0rpUsENiF3xUq+8EJumTvyr1a5zmDACuYOK83VDZ+PfN/NY6fa0mS0rTaprn+AoFd4jvIvXYmZEhlgnbYyf6AFUzcVfahrcw8"
    "4evfbxC4Pbc+WRa+s2SLWiSwq4/1CHnSPXNoOIETDq27kvRuUTR+VhPA39CCP2n8jS4q1aXhhOx/1o2Oy3MErGBCbI8eAwPIsYVG"
    "1F/pV5jAroDYEfKFlM6QUPb/2DrvuCh2r42PItJBLCBYEBARGyoiFnaSFQUFUUCwUERBROkoiFLt2LF3Ra8VGyoqFjYZrwUL9t6x"
    "94YFAZV3sn72955wvX/N5z7P15OdCVOSkxMWI7e8FdounFR9lu8+UIEEf67qFDmgAatpUdN5iCOga6dBNO4ftoI8XMBm+z5eEVF4"
    "vfYqd582FCqQ4M/V6reGKC+2uWvYwQCOgK7oPlE4+MlystKbxaj90huZHP+HHJohULheZUmjYfhRgxN/egm3VuZEgi96U76KZH2p"
    "5NbKQAJW1REEx/MRSDkplzjl5XIEdPHztQvG+6DVHpPJRPmLHiqQ4K/5k8DB6OWt1mSZfPeBBHf9ufnaAQW9kOtlPdJSvvtABRL8"
    "Nbeq7IOSW3uqFly05gjo4udr4ze3RpZ+R4uKpmEKFUjw1zzbzwH9c9Jb8Up+34UEdPHztQ1GG6HytxMUpnf8KVQgwV/z0NcGyLR0"
    "kuKfywEUKpFvo7Df8y+KjLTyGjFaNjRA/z55oPjaIoCLAYkVTaJwl8/bxczGbE64hdQXNVxSrfBe24QjoIufRb6XrovSbhuLBesC"
    "KFQgYZ8zBvfor4fGHWDEr0gdZF5tJxr34gnoersgEt8Ns0H+1YzweD8WTdPdSvZNTyWwvgfMO+AzGgM6RiHT9K3k3bBkLqMREnx2"
    "QoTDONQ1dQSZcSKJI6CLz8xsFxeBPA16k4nPS7g8S0jw2QmDN49FxR8KVV3teAK6+AzT0OBh6KZWjkpH/jaACiT47ITg4ECUa3vB"
    "dRnL+AUEdPGZsgEZfVDRNXPF8nU2XN4rl9vAZSf0PuuGthsI4mb5CxIS0MVn/HaWn4N3Fggi+4KECiT4fvWi2hrlbu4vbp6COAK6"
    "YLaxILj16Yiw6yCxU2UnLg8ZEny/2mVeB82a1FucUxjAEdBl2yocexqOR0e/sN9htlVA1Y8TxPIKfwoVx/Uh2HnCOhR9tbJGqzYX"
    "dkTuCUvFzAIHLgYkYMaFIIyxaoLmz5sjtpV/OSSgC2ZKC0JdPUsUWjpbdJefalCBBMzwEIQDiS4ItV0hppy25gjogquSBGFH/A8x"
    "qe9MMXS2fC8BbQ8/EYib3diF2jpV1fgdnte/iDsPLBRHOgRQqECieNBgrKg6ju4cYcSLGEc0p1ASU9ZZcQR08RkpFTpvxIvh68Qn"
    "2wMoVCAxaMVA/GDlA7QqhhEDE5+JO422iYMH8wR0vVzjjRt9eoYOrGVE/ck6yNr6vDjzF6JQgRkQfKtafdRBSxeeF0csQlwMSPCZ"
    "HO0HmaJZC3aK26dgjoAu/gpW/dseGWdS8an87gMVSPAZKVVnu6Ku55aLY1fbcAR08df8zlwvhOh6sXu8NoUKJPjMmrWlfujbguGi"
    "l3y/ggR08SvcCsrD0YjcEeJo8xICFUjwGUJmh8ag4gkfFP8+5Ano4le4hZmmoIgHdxWVZ5IIt6oNEHyFpkVzJqL0Fl2PKUKSOQK6"
    "+BVur2RisrLrsWNDkglUIMHXdHq/NxNNJVNVm3rzlaagC1adkr+2H94RpTn7xdmnA7iemPtaie2ztPHD1TWzd0KsSsS6TU6JKrMA"
    "ChVIFHTthp0K6+NLg1lmTbMxDdHPtnWQ7QhrjoAuPt8nxJKK+UcuiQeXBVCoQGLuvk542gZL/OQCizGhbqG4J/C22KorT0CX1aS2"
    "OHeRNS7vwWI4P05EqaEhYnRZGoE1qGCGGKxZJQi6vuPQweYhYoPhyQQqkODzyNqkR6Et2lvEbfIXPSSgy8NuOD6Ymo/mjmVnt+G7"
    "IPQ2cpM492kJgQok+DyyT/JbuE/b62IvK56AriBfP/wrtRQl1Gbnqvw9RvXCzou96tWlUIEEn0fm+m8XNNL/m7h1kjZHQNe9+r2x"
    "14+6uN4lFsN4qjWabvVMTJbfqaECCT6PbEjLhujyJy2UL79TQwK6duo6Ya0zTbB/JruCU4Z/E10OvxQd5HdqqECC71cl5K7YsKoW"
    "6jUdcQR0Pcq2wikLOuD7dizLYviN2ijMrgF6t9qWQgUSfL863jxP/Jn7WPy+O4AjoOueYIWjf7bH3bVZjLTypeLdDWWi7Sl/ChWY"
    "6cS36v3iY2JCnhE6k4W4GJDgM7beWNwRjbrWQjvY8xwQ0MWf3Z5mddAHvYZo0Blr7lxBgs88G7GmAWq9QAvtlq85JKCL7yV1S+zQ"
    "O9EYrZXfLKECCT6D7k1cF2RT65vYV+67kIAuvre/7t8beRQL6KRtCYEKJPhMwPr9fBE2vi7uKuUJ6OL/aodtCkVrDe+IPU8mcX+D"
    "kOCr1rUaH4VUtbeIGUOTOQK6+LtP659j0Tm9LWJt93TuXgIJvs7dloXJ6LDOXHGhF199D7pgJT75++PgYlEM/yQeOx/A9cRH9vo4"
    "ujXCnltqZuktaZghBv/+JSY3CqBcfwVERNhPlBbigasrGdGi9glxX1VHFNKhGUdAF5/j1TV6uPhyby2kWBVAubwuQPyyfImCLnrj"
    "uuoadJsXdRVDTtdF6y/5cwR08RlCnXs5iaHJ2iha/hKGCiTm+xainfuG4THqTCeHVl8Vj1/po3/v+XMEdPE5RYOrPyisFuuhzlcC"
    "KFQ4YuEMFH88DDdOZsSBjksVlfMM0S4HnoCuwNIg5PE7AtcpYsTZ5A4oMLQjakDSCazLB7PQYB0/QUh53QFtWtIRWQYlE6hAgs9V"
    "u7bPAt0d7oZS5O9aSECXlbchzjfrhSdJjHh+3QjNftIDfZP/oqACCT5X7c7Kj6Lfm35olCVPQJe2wxs0KN0HfzZmv9w04rb4PViB"
    "esnviVCBBJ+rdq9il6i/ri/yT9LmCOiaMfII0rIIxlMmshiPNi8TF9dxQcq1NhQqkOBz1aR2w8SzZ0V08po1R0CXavlM9HLcKOx7"
    "gRFtKu3E2IW2qJX8VIMKJPh+Rd4dVJz2b42mZSOOgK4d820RujAWH+/EMp2qFtcVF730QM2GNKVQgQTfr3BnG0XH3Yby93MAR0CX"
    "ZbUNWqI3FluZshjHT+sU7fc3RnNO+1OowGwqvlUBi31cPe45oF7yVypUOILLCqt7sEBhgO3RHvkbBxLQxZ/duWcEMeO4G9pTYs2d"
    "K0jw2W3u3YaKtx1FVCZfc0hAF99L9GdkirOqfNAm+akGFUjwWXqbVuwSD3r1RR+N6nIEdPG9fWqBJHo1Hoy+NCshUIEEn23YZtRH"
    "0elMP3T5IU9AF/9X65lVG4mLB6HI40nc3yAk+EqepTss0L6hbkglf7FAArr4u08jewvkrO+GbFwzuXsJJPjanwtrtUHVQ+XrMZiv"
    "SApdsDqp/Pxo17xo1TlDZCc/1WBPzNsUKr4dFoNX7q2ZCdj9wyTV6pZGqFoIoFCBROD4cFXa/Rg8pTHLBDyyKkClZdgbhTRqyRHQ"
    "xecOXn5TpBrnaICaLgigUIFEoZcPyV8ZgxN9GLEq5o0qcKc+muvIE9C1ZucR8vFJNJ41jxHtza+JnbeMQPeLUwmsPAqzTfkapmlr"
    "r4nFz0egvsOSCVQgweekhhlsED2HRiOD80kcAV3LdmSj7J6jcd+FLMaJdTnitGGh6OCTEgIVSPA5qQ/GdRO3OY1Gdi14Arr0ne1Q"
    "ZP0YrH+fEfqpzcTO0wajy/JfFFQgweekzm0brTCqGoYexWlzBHSdjQwTq7/F4b2e7OwabDJXZGf1QRby+y5UIMHnpG5/66Myq+yD"
    "hNPWHAFdQ7b5kurgOJy3XV1VxWWKyqXSHm2Q73BQgQTfr9waG5JpXVuhtzMRR0BXq2AremJBFO5izNaf0wgjsnJ1L5SebUOhAgm+"
    "X51d14Ck1tdFO+VvHEhAl/v95jT+3Fi86D0jJh/LFdNaRqP4vRMJrGjL9RhubXhm7Q3im4HR6GtYMrc2HBJ8v0q+MUjc/XAcmnsx"
    "iSOgi1/jXip2E98YjEZF8j0RKpDg+9W/u9Yq8r6PRc/NeQK6+LX6056NVYxbPQzFye8lUOEIrl95bbZV9XANRK7x2hwBXXzNAcPR"
    "vqpAzz5optwToQIJvl89aGlE3vdwQ/3PWXMEdPG1E6btMyDrLezQSLknQgUSfL/6FetP9npbo8iFiCOgC9ZtEIS8HW5EuVAbvbjt"
    "z1V0gATfr8q+9SJjGtZBqksBHAFdx3pOozqmo7DdDBYjfXsi6e4vIM9mARQqPRtuoNnTQ/G0ezVbpTq5lsR1647sw5pzMSDBZ2D3"
    "fTyfpHhbor0LEEdAF6w5IQgbneaTy70t0IapmKsbBQk+Lzw1YQ3pPr0ranDZmiOgC9aQkt+vjNaQa0+dUbncS7i6g4CAFRLkZ9Sh"
    "TeTtLE/UdJI2R3B1FEANQkGIaJhNGh0vF9+tCaDw/EQuPkjnjg/Cxs1rZqtfurWIqO6XiTFiAIUKJFzCT9Iqz6G4vjcj1ltJpHFi"
    "KzTD2oEjoIvPur9rlUtuHXolFu4P4HLoIWHf5gXNfz8Q1y5ixIFhh0jxlruizyl/joAumPEvCIVfDpCUkluiq/yWARVI0Nr6kv12"
    "JdYLZoStqpjcSj4rfmvCE9BFcxtKaUe641E7GFFd8lPl+TUZtRueSWB1bFg/EVbTlu+7O6tUp+ZMQHPkuyhUIMFXjtw9K5p0mZyI"
    "hl1N4gjosu88g3osjMQBGxihNTeW3P4Rhr7Kd1GoQILvJY9N84iZThB6Z8UT0FX1rJAaDByOK14x4t2sTeRKB0+UaFKXQgUSfN99"
    "d+My0X+BEKsHAAnoOr/zFQ3v7oebDGZnd9+2E0TvWlvEanJABRJ8pZCEIW9Ir6Yt0BX5eQ4J6FqmYyANtHTDvQ4wot+YS2SGtTYq"
    "n4wpVCDB96uije9J1M0yMX8q4gjoct5kJTmld8I7m7C1ACvf6NKNUY1Q+NimFCpcH+P61ZOzV0j9LUVi1oYAjoCul82tpPyXHbFu"
    "FSOaBz4h9VN2iR2v+FOowPUGfKtOLNWiOy7cFI3nIC4GJPh1Ez/QO1Kl91l8IJ8rSEAXf3YfLK1L/y02RVrF1ty5ggS//qN93mvy"
    "YLoVur3ahiOgi+8lxX2ryL2jnZFFgjZ3zSHBr2PZsOgy+TQHoSi570ICuvjebnzyDqmq5YN85bcMqECCX4/T7Nd2YvYoEI2+zxPQ"
    "xf/VPuiykywKHYsqziRxf4OQ4Ovpm86MJqdTEtFp+dsAEtDF333EfdHkddNEZFCYyt1LIMFX4J/p7ExGOaQhpTe/LwB0wT0CBCF+"
    "TCkJarRD1JPfAGBPbKLXWXqq2xx/XVZzrcyL/Z9IdtRysVG9AAoVSLyepZCuta6Hu/xkRMWl5nTR8Fti9xQHjoAufnXNxJ3lZNfU"
    "bPHIwgAKFUjcWdBLmhukh6e0Y8SKFr/JJ7s08aojT0BXzqG+0go3AT+LZsTaSw9J8NgQVGY2mcD6/3A9Fr+TwKFvD8lPm+GoKjyZ"
    "QAUS/Kqteya6NFPXB9UuSeII6AqwNJRcNvTG3VNYjHcXtWjjRr3QE/nrDiqQ4FdtSRYWtPRXJ1S7KU9Al207a8nN2Ql/OcUIz9f1"
    "6IyfNihG/ouCCiT4VVtN5G+bNZWmyCJZmyOgq7rKSUoptsJGHdnZvbe0Ed3oXQt1lp8GUIEEv2rrzSRbGnKwVDx9zZojoOtOtZtU"
    "NVIfH53OYow7bkRX1ysUV0zHFCqQ4PuVlaIxPbNhuVg+G3EEdB1P95UCOrxA+a/UVR0VnegRK5V4e09zChVI8P2q89NaNHhOkOi3"
    "I4AjoGvfRR/pRuxzZHSGEa4PdeiadgPRp9eTCdxXAvYYvkJToKEu7SL4IFVQMlehCRJ8vzK40ZymuCDU6FQSR0AXX2lqbS0LuutO"
    "J+Ql90SoQILvVxdbtaNt/rFCq1rwBHTxFbP6e9rQov2mqL9RXQoVSPD9Kk3Vibao81uckqLNEdDFV/6aVGVDOz96JNZdZ8PV8YIE"
    "36/adHOkW42Pih4XrDkCuvgKZgE+5nRU7DKxjfx1BxVI8P1q6lsr6hocIf6cjDgCumD1NEF4P1eH3i9pL64r9ufqqkGC71cuTnXp"
    "sKltxMYlARwBXRcygiXFtQNoUKS6suo6fdrs7VfFeL0ACpX37cKk2EHL0cli/RqtOj5YSU/WGyBu2mfFxYAEv0YxJ8qOGjyyFOOn"
    "II6ALlj5TRC+Dm1J+w20EMexepZAgQS/crKiGNGPw7zEfPnNEhLQBevLyt8fLREtDPEUrdhoFFAgAeuUCUJJQz+Kf8SLAbHaHAFd"
    "sAa6IMyXv4aUHr/FESaTCdxFBVYYh7uuCELT7gH019hqsfXwZAIVSPC11aeEhdGEIRdEy9NJHAFdI++ESt4rC9HUqep1qQOG0PTh"
    "R8XOz0oIVCDB/46S3SPoF9dZollTnoCuRj5jpD6Z01DHq4wYcsSXVvjHi/byEwcqkODPbvCUIdQ51kRsIn9/QAK6zp+PlY6Oa4qe"
    "iGw9p/5GN9p9xXNFqXwFoQIJvqKcFXan2ffvu467Ys0R0HX2Wrw09kMf0X4Zi3G8qDXdPiO1p7/8xIEKJOBqYEFo/Kg1NU3PUQ1f"
    "iDgCuiYdiJNuDYkgd78xIjG/H23dIkG1+ktTChVIBIbESYfrnC2S5jLCvLYBXeMrqabkBnAEdH1+HyutWDaKdL3BiPGBBrSvR4Fi"
    "wBL5bQn8pS4fGiGFXJyCeuvUXFncd68hPXR4psKmq/yeCBRI6P0TKVV+G4GMXRmR5IrpqJh7ih9XWnEEdPErpF/IMQp2GCoS9gVw"
    "650hYe8SLb0hlujsZkbM7WxMrxUmFk2+5c8R0MVfj9XHDOnn3VOL9l0M4NZtQ2KBSZyUl9Zb/ODKiHMvDKnybIZqmB1PQBd/PU4f"
    "06P1ZpuQjmf9KTzvcEUuf83fHbOjdSsbktczEHcFIcGvLP59xp5empej+jQNcwR08X132uk+NOdisgrJvR0qkOBXSBes7kN9tO66"
    "YvkdDhLQxf8NDmsVSO2/dVcUy++JUIEEv9K72G4I7VZpLIryGwAkoIu/lziUjaaZP1uLTeS7D1Qgwa9YHzBzBH1iMUv8UMoT0MXf"
    "E1NWx1DDcSvFHPnrDiqQ4He1WhQYRrP6XxCbjUjmCOji7+0RBSOpzs/zYtHkKdydGhL8Plhnk0bSqM4fxUVD+N25oAvu1CUIla11"
    "aWiMCdG6EMD1xK8no6QFj23p5XE1V5NP6aFN9Xr1Idbl/hQqkAjaOloSO8fTt88YUXG8CxU2RJOxiW05Arr49efpgbXo/T1hcm+X"
    "7yVAgQRaNErSmTKTnq7PCKsPv8nseROJiy1PQNe1+yOkngPX0WPDGHGpbBz9eUQpTmg8hcB9u2DFArjPl/xOnT+e7lzkJhqPTCZQ"
    "gQRf18B7Rwrd1WCHwvpKEkdAV6u9iZJDsofYfCiLMd44ivazmKLwe1RCoAIJvq7BgvlRtO97G5WjNU9AV4PaidKtlZHEegMjDh4c"
    "Rm/fGaBaz2qSAwUSfF2D9Z2H0Gd5ZmRZojZHQJf/0Fjp9347+tqQnV2X+r3oJW9zclV+1kIFEnxdAz87BVXkxpNE+Y0MEtDl4zZa"
    "qpqaTaujWIwqDyu6UDeUtJff+qACCb5fFVc3pvvzl5BJ8pslJKCrsGWwFH/7CN10lRGq3G60+dlNpI53MwoVSPD9KtLkO9n+bTZJ"
    "3BTAEdB1JDZImuZ6hAr7GVG++y05NzuXTLnoT6ECV97zrTp2woSGPz1Aes9BXAxI8BUEtr0xpzc/LyYf5e8PSEAXf3YzmznT5sI/"
    "pHexNXeuIMFXQug9yZXubxRPouVrDgno4nvJt0xfeulLChkVr81dc0jwFR3GXRlMD6w1I4flvgsJrj4D19s7P4mkRboNSKsmJQQq"
    "kOArU9wKj6IOTW1Vzx/xBHTxf7W30ydSN5PrRQ7y3zlUIMHv9LdkYwr9XGuHYoB8L4EEdPF3n8L6KbTpi22KvoszuXsJJPi9Af0y"
    "02nJzobieT9+x0LogrsXsgrjr8j2cetJsPzuA3ui+eKB0jXH1zTBu2bViI3H7hG3uQUk0SyAQgUStU67S31e1JZKdzHCUbsptVz7"
    "lvR3t+MI6OLrTJRUXCKbThLSe1UAhQokdiKldOSOvlT5lMU4sfEM+WxyhszvwRPQZRTWU1KurC+VNmEx3Nom0377DIglnULgXoaw"
    "Mgnc+1AQLJpMoEfv6pMM+csLKpDg65eMWZFAL9RNJUnylxckoGue4RipYPEs+r09+x19tcJovcNpZObjEgIVSPD1Sy4vGEYnzNhL"
    "8i15Arpsew+Xsrcdo2/TWYynh/vS6ct3kOvyXxRUIMHXL0nqKlLV85vEIUmbI6Br9m1fKfTkWzr7JSMO9GlDb2qdJTfkOwNUIMHX"
    "L9m9rTnVtvlAFlyz5gjoctzTS8p7aiA5uap7yW8terzXVWIsv+9CBRJ8vxolfCLS2E9k0GzEEdDl9aGjtK5RC2lrLiNOLzahFwx1"
    "6agZNhQqkOD7VficYyRuzlUSkh/AEdCVFdRRisixkrSyGLH403ayp8VzYnrGn0IFVtjgW9Xl+lXiJ7+V9ZafalCBBF8p5H7vD6S+"
    "/kfSQX4aQAK6+LN7q1k9+q+/Ll19wZo7V5DgK55oWTanHye8JwvlbwNIQBffS56bd6Iel6vJixRt7ppDgq/cUvVAQffm3iSV8rcB"
    "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"
)

# ── Tinker (Fusion Wheel temel OBJ) embed ────────────────────
_TINKER_OBJ_B64 = (
    "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"
    "W/dunn5LrXtln6nlZkJ/Pn/7bvf0VZAv9PE07TvVTNnLK3T3u8fXxfrdZd69I86nZbezxvmQ6rvHevOxiI83Vt891pdPxvMZ"
    "VDdGvfn0yqD15hHswLu5Gzn4b84n79Tw2cKPozjC0d1HUs83hefTacSx7+6F8Xoevex3fh/lw2fbx5rW+Ok2a3YIL3fGjxrh"
    "h0fWy0/PqR8Zr1d768184Rm95PXyMy/1/+HPuLiQ//jL3/79v/3zX/7tjz/+65//9W9//d//6x/DP17c43oFIP/xx//+t7/8"
    "j3//1z//+a//+te/7eR/+zP88ce//BnDn/9pHfKxXh/XWNehGrt+z/V9/b6WeFGnFK7fa4+g0Lw+rpFcqxzzSr8aWbxkXI2u"
    "tKt8UTo+VqNrNfLVYy6ryiq+DpxVZaHR4qxWd2tp2/pcZVZbq9j6vRKv/lZLeFUt4g4orZGsFVjUN695rB9LDsTHYu8Xkc2o"
    "1vmBwXSObP2uC6h1faEOftU1fzZxlSxr2GsU6yxbH6XrY3VQFmhWl+g62xiaPhYRArcRAcO1lKWrVq9h9bVAvHpe6rPUkGSZ"
    "cYlr+LyqE0wJraLFrkValH+xATVgPvwogM3kB4EYCfQK6ApQ1/RXpZW84IDG8RLnYuQq8lb6WvYreX1evTbrDCF6VyZKYuxX"
    "1Q4ArTMUBfGxBsvSw9ocSAEoAdgrrS286evMRTv4XF+rneZTDSth5eRVA1XX1+qhqhyyrg464LywZw2uW7nFnrT1sZiCVamv"
    "iTeM/foH+E+rtNobGI5aWPQtQrBqwfKmFbwaWwqygomtlR4rQQ2uogNDChzfWCDFj6CP1cBUlUUIFjvfFwiXJLJanspYo0D/"
    "V+mlTh5rCksvs1TwWqxFyEb3z8V/c3XHGt7E2K6mmmUOH9JUTrBWVkLXbFEMm2flbNxYoJ3XRCbmOziuiTEWAh05aKLZ6tcm"
    "zBjNmohakPUD7QHqa6mXcNe5qKtGVh50X5DJG0jKOhEWUs3V5AQ81m4Ka5ArPS2uHpkw+41LOIoBn5gNktZnsS+UXbOA2Kuy"
    "a3bAJrS7+NrVbgwY+/oFJQu/G/B9EbJi/azW1sdaYthGJgxXOaFgz2blDVRbg0GINc0loJeIrvb3mo2GOG3uEWuyiDneTYnY"
    "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"
)

# ── Ayarlar (Editor) ─────────────────────────────────────────
# SETTINGS_FILE, load_settings, save_settings yukarıda tanımlı
_S = load_settings()
_DARK = (_S.get("theme", "dark") == "dark")
_LANG = _S.get("lang", "tr")

# ── Palet (tema duyarlı) ──────────────────────────────────────
if _DARK:
    BG      = QColor("#1e1e1e"); SIDEBAR = QColor("#252526")
    PANEL   = QColor("#2d2d2d"); PHOVER  = QColor("#333333")
    BORDER  = QColor("#3c3c3c"); BLIT    = QColor("#505050")
    ACCENT  = QColor("#0078d4"); TPRI    = QColor("#cccccc")
    TSEC    = QColor("#888888"); TDIM    = QColor("#555555")
    TTITLE  = QColor("#ffffff")
    CANVAS  = QColor("#161616"); GRID    = QColor(255,255,255,7)
else:
    BG      = QColor("#f3f3f3"); SIDEBAR = QColor("#e8e8e8")
    PANEL   = QColor("#ffffff"); PHOVER  = QColor("#ddeeff")
    BORDER  = QColor("#d0d0d0"); BLIT    = QColor("#aaaaaa")
    ACCENT  = QColor("#0067b8"); TPRI    = QColor("#1e1e1e")
    TSEC    = QColor("#555555"); TDIM    = QColor("#aaaaaa")
    TTITLE  = QColor("#000000")
    CANVAS  = QColor("#ececec"); GRID    = QColor(0,0,0,12)

ATK = QColor("#4b8cc8"); DEF = QColor("#4bc87a"); STA = QColor("#c87a3a")

# ── Çeviri ────────────────────────────────────────────────────
_TR = {
    "tr": {
        "diameter":    "Çap",
        "height":      "Yükseklik",
        "symbol":      "Sembol",
        "spiral":      "Spiral desen",
        "export_obj":  "⬇  OBJ Aktar",
        "export_done": "Tamamlandı",
        "export_msg":  "{n} üçgen aktarıldı.\n{p}",
        "save_title":  "OBJ Olarak Kaydet",
        "save_filter": "Wavefront OBJ (*.obj)",
        "sym_tip":     "Herhangi bir Unicode: A-Z, Ğ, İ, 漢, あ, ア, ★ …",
        "view_3d":     "3D GÖRÜNÜM",
        "design_cfg":  "TASARIM AYARLARI",
        "save":           "Kaydet",
        "dont_save":      "Kaydetme",
        "cancel":         "İptal",
        "unsaved_title":  "Kaydedilmemiş Değişiklikler",
        "unsaved_msg":    "\'{name}\' kaydedilmedi.\nÇıkmadan önce kaydetmek istiyor musunuz?",
        "saved_status":   "Kaydedildi",
        "corrupt_title":  "Dosya Sorunu",
        "corrupt_msg":    "Dosyada şu hatalar bulundu:\n{errors}\n\nGeri kalan geçerli verilerle devam etmek için \'Kurtar\'ı seçin.",
        "recover":        "Kurtar",
        "abort":          "Vazgeç",
        "preview":        "ÖNİZLEME",
        "spin_speed":     "DÖNÜŞ HIZI",
        "max_rpm":        "Maks: {rpm} RPM",
        "export_zip":     "⬇  Hepsini Dışa Aktar (ZIP)",
        "total_weight":   "TOPLAM AĞIRLIK",
        "power_stats":    "GÜÇ HESAPLAMA",
        "type_label":     "TÜR",
        "attack":         "Saldırı",
        "defense":        "Savunma",
        "stamina":        "Dayanıklılık",
        "balance":        "Denge",
        "drag_hint":      "sürükle·döndür  tekerlek·zoom",
        "drag_hint2":     "sürükle · döndür   tekerlek · zoom",
        "drag_hint3":     "sürükle·döndür  2x·oto-spin  tekerlek·zoom",
        "body_color":     "GÖVDE RENGİ",
        "pick_color":     "Renk Seç",
        "reset_metal":    "Metalik Gri",
        "load_image":     "Görsel Yükle",
        "remove_image":   "Görseli Kaldır",
        "weight":         "AĞIRLIK",
        "select_ring":    "RING SEÇ",
        "color":          "RENK",
        "calculated":     "Hesaplanan",
        "track_length":   "TRACK UZUNLUĞU",
        "st_number":      "ST Numarası",
        "experimental":   "Deneysel",
        "part_stats":     "PARÇA PUANLARI",
        "shape":          "BİÇİM",
        "tip_length":     "ALT UZUNLUK",
        "semi_flat_r":    "YARI DÜZ r",
        "hole":           "DELİK",
        "radius":         "Yarıçap",
        "depth":          "Derinlik",
        "length":         "Uzunluk",
        "cylinder_r":     "Silindir r",
        "blade_count":    "KANAT SAYISI",
        "count":          "Adet",
        "blade_type":     "KANAT TİPİ",
        "common":         "GENEL",
        "length_mm":      "Uzunluk mm",
        "tip_taper":      "Uç incelme",
        "gap_ratio":      "Kanat boşluğu",
        "wing_settings":  "WING AYARLARI",
        "camber":         "Eğrilik",
        "spike_settings": "SPIKE AYARLARI",
        "base_ratio":     "Taban/boy",
        "flat_settings":  "FLAT AYARLARI",
        "blade_settings": "BLADE AYARLARI",
        "asymmetry":      "Asimetri",
        "fb_3d_view":     "FACE BOLT — 3D GÖRÜNÜM",
        "er_3d_view":     "ENERGY RING — 3D GÖRÜNÜM",
        "fw_3d_view":     "FUSION WHEEL — 3D GÖRÜNÜM",
        "st_3d_view":     "SPIN TRACK — 3D GÖRÜNÜM",
        "pt_3d_view":     "PERFORMANCE TIP — 3D GÖRÜNÜM",
        "png_label":      "⬇ PNG Etiket",
        "export_label":   "Etiketi Dışa Aktar",
        "export_all":     "Tümünü Dışa Aktar",
        "warning":        "Uyarı",
        "no_texture_fb":  "Face Bolt için texture yüklü değil.",
        "done":           "Tamamlandı",
        "select_image":   "Görsel Seç",
        "embedded_img":   "(gömülü görsel)",
        "part_settings":  "PARÇA AYARLARI",
        "fb_color":       "Face Bolt Rengi",
        "st_color":       "Spin Track Rengi",
        "pt_color":       "Performance Tip Rengi",
        "er_color":       "Renk Seç",
        "err_missing":    "Zorunlu alan eksik: \'{k}\'",
        "err_series":     "Geçersiz seri: \'{v}\'",
        "err_spiral":     "\'spiral\' bool olmalı (true/false)",
        "err_symbol":     "\'symbol\' string olmalı",
        "err_blades_range": "\'fusion_wheel_blades\' 0-16 arası olmalı",
        "err_blades_int": "\'fusion_wheel_blades\' tamsayı olmalı",
        "err_blade_type": "\'fusion_wheel_blade_type\' geçersiz",
        "new_proj_title":    "Yeni Proje",
        "proj_name_lbl":     "PROJE ADI",
        "proj_name_ph":      "örn. dragoon_v2",
        "series_lbl":        "SERİ",
        "btn_cancel":        "İptal",
        "btn_create":        "Oluştur",
        "err_name_empty":    "Proje adı boş olamaz.",
        "err_no_series":     "Bir seri seçin.",
        "err_file_exists_t": "Hata",
        "er_folder_empty":   "energy-rings/ klasörü\nbulunamadı veya boş.",
        "shape_sharp":       "Sivri",
        "shape_round":       "Yuvarlak",
        "shape_flat":        "Yarı Düz",
        "shape_sharp_hole":  "Sivri İçi Delik",
        "shape_flat_hole":   "Yarı Düz Delik",
        "export_win_title":  "Dışa Aktar",
        "exported_msg":      "Dışa aktarıldı",
        "hws_title":      "Hybrid Wheel System",
        "hws_sub":        "Yan sanayi standart parça sistemi",
        "bgm_title":      "Beigoma",
        "bgm_sub":        "Metal Fight standart sistemi",
        "tex_info":       "PNG veya JPG yükle.\nHexagonal yüzeye\notomatik uyarlanır.",
    },
    "en": {
        "diameter":    "Diameter",
        "height":      "Height",
        "symbol":      "Symbol",
        "spiral":      "Spiral pattern",
        "export_obj":  "⬇  Export OBJ",
        "export_done": "Done",
        "export_msg":  "{n} triangles exported.\n{p}",
        "save_title":  "Save as OBJ",
        "save_filter": "Wavefront OBJ (*.obj)",
        "sym_tip":     "Any Unicode: A-Z, Ğ, İ, 漢, あ, ア, ★ …",
        "view_3d":     "3D VIEW",
        "design_cfg":  "DESIGN SETTINGS",
        "save":           "Save",
        "dont_save":      "Don\'t Save",
        "cancel":         "Cancel",
        "unsaved_title":  "Unsaved Changes",
        "unsaved_msg":    "\'{name}\' has unsaved changes.\nDo you want to save before closing?",
        "saved_status":   "Saved",
        "corrupt_title":  "File Issue",
        "corrupt_msg":    "The following problems were found:\n{errors}\n\nChoose \'Recover\' to continue with the valid data.",
        "recover":        "Recover",
        "abort":          "Abort",
        "preview":        "PREVIEW",
        "spin_speed":     "SPIN SPEED",
        "max_rpm":        "Max: {rpm} RPM",
        "export_zip":     "⬇  Export All (ZIP)",
        "total_weight":   "TOTAL WEIGHT",
        "power_stats":    "POWER STATS",
        "type_label":     "TYPE",
        "attack":         "Attack",
        "defense":        "Defense",
        "stamina":        "Stamina",
        "balance":        "Balance",
        "drag_hint":      "drag·rotate  wheel·zoom",
        "drag_hint2":     "drag · rotate   wheel · zoom",
        "drag_hint3":     "drag·rotate  dbl·auto-spin  wheel·zoom",
        "body_color":     "BODY COLOR",
        "pick_color":     "Pick Color",
        "reset_metal":    "Reset Metal",
        "load_image":     "Load Image",
        "remove_image":   "Remove Image",
        "weight":         "WEIGHT",
        "select_ring":    "SELECT RING",
        "color":          "COLOR",
        "calculated":     "Calculated",
        "track_length":   "TRACK LENGTH",
        "st_number":      "ST Number",
        "experimental":   "Experimental",
        "part_stats":     "PART STATS",
        "shape":          "SHAPE",
        "tip_length":     "TIP LENGTH",
        "semi_flat_r":    "SEMI-FLAT r",
        "hole":           "HOLE",
        "radius":         "Radius",
        "depth":          "Depth",
        "length":         "Length",
        "cylinder_r":     "Cylinder r",
        "blade_count":    "BLADE COUNT",
        "count":          "Count",
        "blade_type":     "BLADE TYPE",
        "common":         "COMMON",
        "length_mm":      "Length mm",
        "tip_taper":      "Tip taper",
        "gap_ratio":      "Gap ratio",
        "wing_settings":  "WING SETTINGS",
        "camber":         "Camber",
        "spike_settings": "SPIKE SETTINGS",
        "base_ratio":     "Base ratio",
        "flat_settings":  "FLAT SETTINGS",
        "blade_settings": "BLADE SETTINGS",
        "asymmetry":      "Asymmetry",
        "fb_3d_view":     "FACE BOLT — 3D VIEW",
        "er_3d_view":     "ENERGY RING — 3D VIEW",
        "fw_3d_view":     "FUSION WHEEL — 3D VIEW",
        "st_3d_view":     "SPIN TRACK — 3D VIEW",
        "pt_3d_view":     "PERFORMANCE TIP — 3D VIEW",
        "png_label":      "⬇ PNG Label",
        "export_label":   "Export Label",
        "export_all":     "Export All",
        "warning":        "Warning",
        "no_texture_fb":  "No texture loaded for Face Bolt.",
        "done":           "Done",
        "select_image":   "Select Image",
        "embedded_img":   "(embedded image)",
        "part_settings":  "PART SETTINGS",
        "fb_color":       "Face Bolt Color",
        "st_color":       "Spin Track Color",
        "pt_color":       "Tip Color",
        "er_color":       "Pick Color",
        "err_missing":    "Required field missing: \'{k}\'",
        "err_series":     "Invalid series: \'{v}\'",
        "err_spiral":     "\'spiral\' must be bool (true/false)",
        "err_symbol":     "\'symbol\' must be a string",
        "err_blades_range": "\'fusion_wheel_blades\' must be 0-16",
        "err_blades_int": "\'fusion_wheel_blades\' must be an integer",
        "err_blade_type": "\'fusion_wheel_blade_type\' is invalid",
        "new_proj_title":    "New Project",
        "proj_name_lbl":     "PROJECT NAME",
        "proj_name_ph":      "e.g. dragoon_v2",
        "series_lbl":        "SERIES",
        "btn_cancel":        "Cancel",
        "btn_create":        "Create",
        "err_name_empty":    "Project name cannot be empty.",
        "err_no_series":     "Please select a series.",
        "err_file_exists_t": "Error",
        "er_folder_empty":   "energy-rings/ folder\nnot found or empty.",
        "shape_sharp":       "Sharp",
        "shape_round":       "Round",
        "shape_flat":        "Semi-Flat",
        "shape_sharp_hole":  "Sharp Hole",
        "shape_flat_hole":   "Flat Hole",
        "export_win_title":  "Export",
        "exported_msg":      "Exported",
        "hws_title":      "Hybrid Wheel System",
        "hws_sub":        "Third-party standard parts system",
        "bgm_title":      "Beigoma",
        "bgm_sub":        "Metal Fight standard system",
        "tex_info":       "Load a PNG or JPG.\nAuto-fitted to the\nhexagonal face.",
    },
    "ja": {
        "diameter":    "直径",
        "height":      "高さ",
        "symbol":      "シンボル",
        "spiral":      "スパイラル模様",
        "export_obj":  "⬇  OBJエクスポート",
        "export_done": "完了",
        "export_msg":  "{n} 個のトライアングルをエクスポートしました。\n{p}",
        "save_title":  "OBJとして保存",
        "save_filter": "Wavefront OBJ (*.obj)",
        "sym_tip":     "任意のUnicode: A-Z, Ğ, İ, 漢, あ, ア, ★ …",
        "view_3d":     "3Dビュー",
        "design_cfg":  "デザイン設定",
        "save":           "保存",
        "dont_save":      "保存しない",
        "cancel":         "キャンセル",
        "unsaved_title":  "未保存の変更",
        "unsaved_msg":    "\'{name}\' は未保存です。\n閉じる前に保存しますか？",
        "saved_status":   "保存済み",
        "corrupt_title":  "ファイルの問題",
        "corrupt_msg":    "以下の問題が見つかりました:\n{errors}\n\n有効なデータで続行するには「復元」を選択してください。",
        "recover":        "復元",
        "abort":          "中止",
        "preview":        "プレビュー",
        "spin_speed":     "回転速度",
        "max_rpm":        "最大: {rpm} RPM",
        "export_zip":     "⬇  全てエクスポート (ZIP)",
        "total_weight":   "合計重量",
        "power_stats":    "パワー統計",
        "type_label":     "タイプ",
        "attack":         "アタック",
        "defense":        "ディフェンス",
        "stamina":        "スタミナ",
        "balance":        "バランス",
        "drag_hint":      "ドラッグ·回転  ホイール·ズーム",
        "drag_hint2":     "ドラッグ · 回転   ホイール · ズーム",
        "drag_hint3":     "ドラッグ·回転  ダブル·自動スピン  ホイール·ズーム",
        "body_color":     "ボディカラー",
        "pick_color":     "色を選択",
        "reset_metal":    "メタルグレー",
        "load_image":     "画像を読み込む",
        "remove_image":   "画像を削除",
        "weight":         "重量",
        "select_ring":    "リングを選択",
        "color":          "カラー",
        "calculated":     "計算値",
        "track_length":   "トラック長さ",
        "st_number":      "ST番号",
        "experimental":   "実験的",
        "part_stats":     "パーツ評価",
        "shape":          "形状",
        "tip_length":     "チップ長さ",
        "semi_flat_r":    "セミフラット r",
        "hole":           "穴",
        "radius":         "半径",
        "depth":          "深さ",
        "length":         "長さ",
        "cylinder_r":     "シリンダー r",
        "blade_count":    "ブレード数",
        "count":          "個数",
        "blade_type":     "ブレードタイプ",
        "common":         "共通",
        "length_mm":      "長さ mm",
        "tip_taper":      "先端テーパー",
        "gap_ratio":      "ギャップ比",
        "wing_settings":  "ウィング設定",
        "camber":         "キャンバー",
        "spike_settings": "スパイク設定",
        "base_ratio":     "ベース比",
        "flat_settings":  "フラット設定",
        "blade_settings": "ブレード設定",
        "asymmetry":      "非対称",
        "fb_3d_view":     "フェイスボルト — 3Dビュー",
        "er_3d_view":     "エネルギーリング — 3Dビュー",
        "fw_3d_view":     "フュージョンホイール — 3Dビュー",
        "st_3d_view":     "スピントラック — 3Dビュー",
        "pt_3d_view":     "パフォーマンスチップ — 3Dビュー",
        "png_label":      "⬇ PNGラベル",
        "export_label":   "ラベルをエクスポート",
        "export_all":     "全てエクスポート",
        "warning":        "警告",
        "no_texture_fb":  "フェイスボルトにテクスチャが読み込まれていません。",
        "done":           "完了",
        "select_image":   "画像を選択",
        "embedded_img":   "(埋め込み画像)",
        "part_settings":  "パーツ設定",
        "fb_color":       "フェイスボルトの色",
        "st_color":       "スピントラックの色",
        "pt_color":       "チップの色",
        "er_color":       "色を選択",
        "err_missing":    "必須フィールドがありません: \'{k}\'",
        "err_series":     "無効なシリーズ: \'{v}\'",
        "err_spiral":     "\'spiral\' はbool値 (true/false) である必要があります",
        "err_symbol":     "\'symbol\' は文字列である必要があります",
        "err_blades_range": "\'fusion_wheel_blades\' は0〜16の範囲である必要があります",
        "err_blades_int": "\'fusion_wheel_blades\' は整数である必要があります",
        "err_blade_type": "\'fusion_wheel_blade_type\' が無効です",
        "new_proj_title":    "新規プロジェクト",
        "proj_name_lbl":     "プロジェクト名",
        "proj_name_ph":      "例: dragoon_v2",
        "series_lbl":        "シリーズ",
        "btn_cancel":        "キャンセル",
        "btn_create":        "作成",
        "err_name_empty":    "プロジェクト名を入力してください。",
        "err_no_series":     "シリーズを選択してください。",
        "err_file_exists_t": "エラー",
        "er_folder_empty":   "energy-rings/ フォルダが\n見つからないか空です。",
        "shape_sharp":       "シャープ",
        "shape_round":       "ラウンド",
        "shape_flat":        "セミフラット",
        "shape_sharp_hole":  "シャープ (穴あり)",
        "shape_flat_hole":   "セミフラット (穴あり)",
        "export_win_title":  "エクスポート",
        "exported_msg":      "エクスポート完了",
        "hws_title":      "ハイブリッドホイールシステム",
        "hws_sub":        "サードパーティ標準パーツシステム",
        "bgm_title":      "ベイゴマ",
        "bgm_sub":        "メタルファイト標準システム",
        "tex_info":       "PNGまたはJPGを読み込みます。\n六角形の面に\n自動フィットします。",
    },
}

def tr(key: str) -> str:
    return _TR.get(_LANG, _TR["tr"]).get(key, key)

# ══════════════════════════════════════════════════════════════
# .BEI DOSYA ŞEMASI  (minimal TOML — stdlib toml yok, elle parse)
# ══════════════════════════════════════════════════════════════
# Zorunlu alanlar:
#   series   = "beigoma" | "hybrid_wheel"
#   name     = "<proje adı>"
#   created  = "<ISO datetime>"
# Editörün yazdığı alanlar:
#   spiral   = true | false
#   symbol   = "<tek karakter veya boş>"
#   modified = "<ISO datetime>"

REQUIRED_KEYS = {"series", "name", "created"}
EDITABLE_KEYS = {
    "spiral", "symbol", "face_image_data", "face_bolt_color",
    "energy_ring", "energy_ring_color",
    "fusion_wheel_blades", "fusion_wheel_blade_type",
    "fusion_wheel_blade_depth", "fusion_wheel_taper", "fusion_wheel_gap",
    "fw_wing_camber", "fw_wing_sweep", "fw_spike_ratio",
    "fw_flat_bevel", "fw_blade_sweep", "fw_blade_asym",
    "fusion_wheel_color",
}
ALL_VALID_KEYS = REQUIRED_KEYS | EDITABLE_KEYS | {"modified"}

def _toml_parse(text: str) -> dict:
    """Basit satır-bazlı TOML parser (string/bool/int değerler + uzun base64)."""
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, rest = line.partition("=")
        key = key.strip()
        val = rest.strip()
        # String (tırnak içi — base64 = işaretleri dahil tümünü al)
        if val.startswith('"') and val.endswith('"'):
            result[key] = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            result[key] = val[1:-1]
        # Bool
        elif val.lower() == "true":
            result[key] = True
        elif val.lower() == "false":
            result[key] = False
        # Int / float
        else:
            try:
                result[key] = int(val)
            except ValueError:
                try:
                    result[key] = float(val)
                except ValueError:
                    result[key] = val
    return result

def _toml_val(v) -> str:
    """Python değerini TOML değer dizisine çevirir."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return f'"{v}"'
    return str(v)

def bei_read(path: Path) -> dict:
    """Dosyayı okur ve parse edilmiş dict döndürür."""
    try:
        return _toml_parse(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}

def bei_validate(data: dict) -> list[str]:
    """
    Eksik/geçersiz alanları hata listesi olarak döndürür.
    Boş liste → dosya geçerli.
    """
    errors = []
    for k in REQUIRED_KEYS:
        if k not in data:
            errors.append(tr("err_missing").format(k=k))
    if "series" in data and data["series"] not in ("beigoma", "hybrid_wheel"):
        errors.append(tr("err_series").format(v=data["series"]))
    if "spiral" in data and not isinstance(data["spiral"], bool):
        errors.append(tr("err_spiral"))
    if "symbol" in data and not isinstance(data["symbol"], str):
        errors.append(tr("err_symbol"))
    if "fusion_wheel_blades" in data:
        try:
            v = int(data["fusion_wheel_blades"])
            if not (0 <= v <= 16):
                errors.append(tr("err_blades_range"))
        except (TypeError, ValueError):
            errors.append(tr("err_blades_int"))
    if "fusion_wheel_blade_type" in data and data["fusion_wheel_blade_type"] not in ("wing","spike","flat","blade"):
        errors.append(tr("err_blade_type"))
    return errors

def bei_write(path: Path, data: dict):
    """
    dict'i .bei dosyasına yazar. Mevcut dosyadaki bilinmeyen alanları korur,
    bilinen alanları günceller, yoksa ekler.
    Sıra: series, name, created, modified, spiral, symbol, diğerleri
    """
    from datetime import datetime
    data = dict(data)
    data["modified"] = datetime.now().isoformat(timespec="seconds")

    # Önce mevcut dosyayı oku (bilinmeyen satırları korumak için ham metin)
    existing_lines = []
    if path.exists():
        existing_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    # Hangi anahtarları zaten yazdık takip et
    written = set()
    out_lines = []

    for line in existing_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out_lines.append(line)
            continue
        if "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            if k in data:
                out_lines.append(f'{k} = {_toml_val(data[k])}')
                written.add(k)
                continue
        out_lines.append(line)

    # Yazılmamış anahtarları sona ekle (sıralı)
    for k in ("series", "name", "created", "modified", "spiral", "symbol"):
        if k in data and k not in written:
            out_lines.append(f'{k} = {_toml_val(data[k])}')
            written.add(k)
    # Geri kalan
    for k, v in data.items():
        if k not in written:
            out_lines.append(f'{k} = {_toml_val(v)}')

    path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")


def sec_header(text):
    w = QWidget(); w.setFixedHeight(30)
    w.setStyleSheet(f"background:{SIDEBAR.name()};border-bottom:1px solid {BORDER.name()};")
    lay = QHBoxLayout(w); lay.setContentsMargins(12,0,12,0)
    lb  = QLabel(text)
    lb.setStyleSheet(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:9px;"
                     "font-weight:700;letter-spacing:2px;background:transparent;")
    lay.addWidget(lb); lay.addStretch(); return w

def hdiv():
    f = QFrame(); f.setFixedHeight(1)
    f.setStyleSheet(f"background:{BORDER.name()};"); return f

def stat_bar(label, val, color):
    w = QWidget(); w.setFixedHeight(26); w.setStyleSheet("background:transparent;")
    row = QHBoxLayout(w); row.setContentsMargins(12,0,12,0); row.setSpacing(8)
    lb  = QLabel(label); lb.setFixedWidth(82)
    lb.setStyleSheet(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:9px;background:transparent;")
    class Bar(QWidget):
        def __init__(self): super().__init__(); self.setFixedHeight(5); self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        def paintEvent(self,_): p=QPainter(self); p.fillRect(0,0,self.width(),self.height(),BORDER); p.end()
    vl = QLabel(str(val)); vl.setFixedWidth(22); vl.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
    vl.setStyleSheet(f"color:{color.name()};font-family:'Segoe UI';font-size:9px;font-weight:700;background:transparent;")
    row.addWidget(lb); row.addWidget(Bar()); row.addWidget(vl); return w


def stat_bar_live(label, color, max_val=6):
    """Değeri sonradan güncellenebilen stat_bar. (widget, update_fn) döndürür.
    max_val: çubuğun %100'e karşılık gelen değer (ER=5, ST=3). Dışarıdan
    set edilen değer max_val'e indirgenir."""
    w = QWidget(); w.setFixedHeight(26); w.setStyleSheet("background:transparent;")
    row = QHBoxLayout(w); row.setContentsMargins(12,0,12,0); row.setSpacing(8)
    lb  = QLabel(label); lb.setFixedWidth(82)
    lb.setStyleSheet(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:9px;background:transparent;")
    class Bar(QWidget):
        def __init__(self):
            super().__init__()
            self._val = 0; self._max = max_val
            self.setFixedHeight(5)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        def set_val(self, v):
            self._val = max(0, min(int(v), self._max)); self.update()
        def paintEvent(self, _):
            p = QPainter(self)
            p.fillRect(0, 0, self.width(), self.height(), BORDER)
            if self._max > 0 and self._val > 0:
                fill_w = int(self.width() * self._val / self._max)
                p.fillRect(0, 0, fill_w, self.height(), color)
            p.end()
    bar = Bar()
    vl = QLabel("0"); vl.setFixedWidth(22); vl.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
    vl.setStyleSheet(f"color:{color.name()};font-family:'Segoe UI';font-size:9px;font-weight:700;background:transparent;")
    row.addWidget(lb); row.addWidget(bar); row.addWidget(vl)
    def update_fn(v):
        clamped = max(0, min(int(v), max_val))
        bar.set_val(clamped); vl.setText(str(clamped))
    return w, update_fn


def weight_label_widget(prefix=""):
    """Güncellenebilir ağırlık etiketi. (widget, update_fn) döndürür."""
    w = QWidget(); w.setFixedHeight(28); w.setStyleSheet("background:transparent;")
    row = QHBoxLayout(w); row.setContentsMargins(12,0,12,0); row.setSpacing(6)
    if prefix:
        pl = QLabel(prefix); pl.setStyleSheet(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;background:transparent;")
        row.addWidget(pl)
    row.addStretch()
    vl = QLabel("—")
    vl.setStyleSheet(f"color:{TPRI.name()};font-family:'Segoe UI';font-size:11px;font-weight:700;background:transparent;")
    row.addWidget(vl)
    unit = QLabel("g"); unit.setStyleSheet(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:9px;background:transparent;")
    row.addWidget(unit)
    return w, lambda v: vl.setText(f"{v:.1f}" if isinstance(v, float) else str(v))


# ══════════════════════════════════════════════════════════════
# BEIGOMA GEOMETRİ MOTORU
# ══════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════
# FONT OUTLINE → 3D MESH  (herhangi bir Unicode karakter)
# Qt QPainterPath.addText() ile outline alınır, ear-clipping ile
# triangulate edilir. PySide6 zaten mevcut olduğundan ekstra
# bağımlılık yoktur.
# ══════════════════════════════════════════════════════════════

def _outline_char(char: str, size: float = 200.0):
    """
    Verilen Unicode karakteri QPainterPath outline'ına çevirir.
    toSubpathPolygons() ile bezier eğrileri Qt tarafından tessellate edilir.
    Döner: list of contours, her contour [(x,y), ...] kapalı çokgen.
    Koordinatlar merkezi (0,0) olacak şekilde normalize, Y yukarı (+).
    """
    from PySide6.QtGui import QPainterPath, QFont

    path = QPainterPath()
    for family in ("Noto Sans CJK JP", "Noto Sans", "Arial Unicode MS",
                   "DejaVu Sans", "FreeSans", "Unifont", "Arial", ""):
        font = QFont(family, 200)
        font.setStyleStrategy(QFont.StyleStrategy.PreferOutline)
        path = QPainterPath()
        path.addText(0, 0, font, char)
        if path.elementCount() > 2:
            break

    if path.elementCount() < 3:
        return []

    br = path.boundingRect()
    if br.width() < 1 or br.height() < 1:
        return []

    # Manuel normalize: önce ham polygon'ları al, sonra her noktayı dönüştür
    raw_polys = path.toSubpathPolygons()

    scale = size / max(br.width(), br.height())
    cx    = br.x() + br.width()  / 2.0
    cy    = br.y() + br.height() / 2.0

    contours = []
    for poly in raw_polys:
        pts = []
        for pt in poly:
            nx =  (pt.x() - cx) * scale   # X: sol→sağ
            ny = -(pt.y() - cy) * scale   # Y: Qt'de aşağı pozitif, biz çeviriyoruz
            pts.append((nx, ny))
        # Son nokta == ilk nokta ise çıkar (kapalı çokgen tekrarı)
        if len(pts) > 1 and abs(pts[-1][0]-pts[0][0]) < 1e-6 and abs(pts[-1][1]-pts[0][1]) < 1e-6:
            pts = pts[:-1]
        if len(pts) >= 3:
            contours.append(pts)

    return contours

def _signed_area(poly):
    """Shoelace ile işaretli alan. Pozitif → CCW."""
    n = len(poly)
    s = 0.0
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i+1) % n]
        s += x0 * y1 - x1 * y0
    return s * 0.5


def _ear_clip(poly):
    """
    Basit ear-clipping triangulation.
    poly: [(x,y), ...] CCW sıralamalı kapalı çokgen (son nokta ≠ ilk nokta).
    Döner: [(i0,i1,i2), ...] index üçlüleri.
    """
    verts = list(poly)
    n0    = len(verts)
    if n0 < 3:
        return []
    if n0 == 3:
        return [(0, 1, 2)]

    idx = list(range(n0))
    tris = []

    def cross2(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    def point_in_tri(p, a, b, c):
        d1 = cross2(p, a, b)
        d2 = cross2(p, b, c)
        d3 = cross2(p, c, a)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    max_iter = n0 * n0 * 2
    iteration = 0
    while len(idx) > 3 and iteration < max_iter:
        iteration += 1
        found_ear = False
        n = len(idx)
        for i in range(n):
            prev_i = idx[(i - 1) % n]
            curr_i = idx[i]
            next_i = idx[(i + 1) % n]
            a, b, c = verts[prev_i], verts[curr_i], verts[next_i]
            cv = cross2(a, b, c)
            if cv <= 0:   # reflex veya degenerate — sıfırı da geç
                continue
            ear = True
            for j in range(n):
                if idx[j] in (prev_i, curr_i, next_i):
                    continue
                if point_in_tri(verts[idx[j]], a, b, c):
                    ear = False
                    break
            if ear:
                tris.append((prev_i, curr_i, next_i))
                idx.pop(i)
                found_ear = True
                break
        if not found_ear:
            # Sıkışma: en küçük cross2'li kulağı zorla al
            n = len(idx)
            best = None; best_cv = -1e18
            for i in range(n):
                prev_i = idx[(i-1)%n]; curr_i = idx[i]; next_i = idx[(i+1)%n]
                a,b,c = verts[prev_i],verts[curr_i],verts[next_i]
                cv = cross2(a,b,c)
                if cv > best_cv:
                    best_cv = cv; best = i
            if best is not None and best_cv > -1e-6:
                i = best
                prev_i = idx[(i-1)%n]; curr_i = idx[i]; next_i = idx[(i+1)%n]
                tris.append((prev_i, curr_i, next_i))
                idx.pop(i)
            else:
                break

    if len(idx) == 3:
        tris.append((idx[0], idx[1], idx[2]))
    return tris


def _merge_polygon_with_holes(outer, holes):
    """
    Dış kontur (CCW) ve delik listesini (CW→CCW reversed) bridge edge
    yöntemiyle tek düz poligona birleştirir.
    Döner: [(x,y), ...] birleşik poligon (ear_clip'e verilebilir).
    """
    # Her deliği: en sağdaki noktadan bridge açarak dış kontüre bağla
    result = list(outer)
    remaining = [list(h) for h in holes]

    while remaining:
        # Kalan delikler arasından en sağdaki noktaya sahip olanı seç
        best_hole_i = 0
        best_hx = -1e18
        best_hp = 0
        for hi, hole in enumerate(remaining):
            for pi, (hx, hy) in enumerate(hole):
                if hx > best_hx:
                    best_hx = hx; best_hole_i = hi; best_hp = pi

        hole = remaining.pop(best_hole_i)
        # Deliği bridge noktasından başlayacak şekilde döndür
        hole = hole[best_hp:] + hole[:best_hp]
        hx, hy = hole[0]

        # Dış konturda bu noktaya görünür olan en yakın vertex'i bul
        # (basit yaklaşım: en sağdaki x≥hx olan vertex)
        best_ri = 0; best_rx = -1e18
        for ri, (rx, ry) in enumerate(result):
            if rx >= hx and rx > best_rx:
                best_rx = rx; best_ri = ri

        # Bridge: result[best_ri] → hole[0] → ... → hole[-1] → hole[0] → result[best_ri] → devam
        bridge = (result[:best_ri+1]
                  + hole
                  + [hole[0]]
                  + result[best_ri:])
        result = bridge

    return result


def glyph_to_mesh_tris(char: str, flat_r: float, base_y: float, lift: float):
    """
    Herhangi bir Unicode karakteri için 3D kabartma üçgenleri üretir.
    Dış konturlar: üst+alt yüzey + yan duvarlar (dolu).
    Delik konturları: sadece yan duvarlar (üst yüzey yok = görsel delik).
    """
    size = flat_r * 2.0 * 0.88

    contours = _outline_char(char, size)
    if not contours:
        return []

    top_y = base_y + lift
    result = []

    for contour in contours:
        nv = len(contour)
        if nv < 3:
            continue

        area = _signed_area(contour)
        if area == 0:
            continue

        # area > 0 → CCW → dış kontur (dolu)
        # area < 0 → CW  → delik (sadece yan duvar)
        is_hole = (area < 0)

        if not is_hole:
            # Üst yüzey
            tri_idx = _ear_clip(contour)
            for i0, i1, i2 in tri_idx:
                x0,z0 = contour[i0]; x1,z1 = contour[i1]; x2,z2 = contour[i2]
                # X aynası: 3D'de ters görünümü düzeltir
                result.append(((-x0,top_y,z0),(-x1,top_y,z1),(-x2,top_y,z2)))
                result.append(((-x0,top_y,z0),(-x2,top_y,z2),(-x1,top_y,z1)))
                # Alt yüzey
                result.append(((-x0,base_y,z0),(-x2,base_y,z2),(-x1,base_y,z1)))
                result.append(((-x0,base_y,z0),(-x1,base_y,z1),(-x2,base_y,z2)))

        # Yan duvarlar — hem dış hem delik için
        for i in range(nv):
            xa,za = contour[i]; xb,zb = contour[(i+1)%nv]
            xa=-xa; xb=-xb  # X aynası
            result += [
                ((xa,base_y,za),(xb,base_y,zb),(xb,top_y,zb)),
                ((xa,base_y,za),(xb,top_y, zb),(xa,top_y,za)),
                ((xa,base_y,za),(xb,top_y,zb),(xb,base_y,zb)),
                ((xa,base_y,za),(xa,top_y,za),(xb,top_y,zb)),
            ]

    return result


def build_beigoma_mesh(diam_mm: float, height_mm: float,
                       spiral: bool, letter: str,
                       body_segs: int = 48) -> list[tuple]:
    """
    Tüm beigoma geometrisini üçgen listesi olarak döndürür.
    Koordinatlar mm cinsinden, +Y yukarı.
    Dönen değer: [(v0,v1,v2), ...] — her vi (x,y,z) tuple.
    """
    R, H = diam_mm / 2.0, height_mm

    # ── Profil (r, y) — Y aşağı pozitif, döndürünce +Y'ye çevrilecek
    profile = [
        (0.0,       0.0      ),
        (R*0.50,    0.0      ),
        (R*0.88,    H*0.10   ),
        (R*1.00,    H*0.24   ),
        (R*0.82,    H*0.44   ),
        (R*0.48,    H*0.68   ),
        (R*0.14,    H*0.88   ),
        (R*0.04,    H*0.97   ),
        (0.0,       H        ),
    ]

    def prof_r(y_target: float) -> float:
        """Belirli bir Y yüksekliği için profil yarıçapı (interpolasyon)."""
        y_target = max(0.0, min(H, y_target))
        for j in range(len(profile)-1):
            r0,y0 = profile[j]; r1,y1 = profile[j+1]
            if y0 <= y_target <= y1:
                f = (y_target-y0)/(y1-y0) if y1!=y0 else 0.0
                return r0 + f*(r1-r0)
        return profile[-1][0]

    tris = []

    # ── 1. ANA GÖVDE (revolve) ─────────────────────────────────
    for i in range(body_segs):
        a0 = math.tau * i      / body_segs
        a1 = math.tau * (i+1) / body_segs
        for j in range(len(profile)-1):
            r0,y0 = profile[j]; r1,y1 = profile[j+1]
            # +Y yukarı koordinat sistemine çevir
            p00 = ( r0*math.cos(a0),  H-y0,  r0*math.sin(a0))
            p10 = ( r1*math.cos(a0),  H-y1,  r1*math.sin(a0))
            p01 = ( r0*math.cos(a1),  H-y0,  r0*math.sin(a1))
            p11 = ( r1*math.cos(a1),  H-y1,  r1*math.sin(a1))
            tris += [(p00,p01,p10),(p01,p11,p10)]

    # ── 2. SPİRAL KANAL ────────────────────────────────────────
    # Gerçek beigoma spirali: gövdenin yan yüzeyinde üstten alta sarılan
    # kabartmalı şerit. Spiral gövde yüzeyine yapışık, dışa doğru kabarık.
    if spiral:
        turns    = 5              # tur sayısı
        seg_turn = 80             # her tur segment sayısı
        steps    = turns * seg_turn
        sw       = R * 0.055      # şerit yarı-genişliği (yüzey boyunca)
        sh       = R * 0.030      # kabartma yüksekliği (dışa doğru)

        # Spiral sadece gövdenin yan kısmında: y_start → y_end (profil koordinatı)
        y_start = H * 0.08   # üst düzlüğün hemen altından başla
        y_end   = H * 0.92   # uca yakın nerede biter

        def spiral_surface_pt(t, offset_along_normal=0.0, offset_along_tangent=0.0):
            """
            t ∈ [0,1]: spiraldeki ilerleme parametresi.
            offset_along_normal: yüzeyden dışa doğru uzaklık (kabartma için).
            offset_along_tangent: spiral eksenine dik, yüzey boyunca kayma (şerit genişliği).
            Döner: (x, y, z)
            """
            y_c   = y_start + (y_end - y_start) * t          # profil Y koordinatı
            angle = math.tau * t * turns                       # açısal ilerleme

            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            # Yüzey yarıçapı ve komşu noktadan profil normali hesapla
            r_c = prof_r(y_c)
            eps = (y_end - y_start) / (steps * 10)
            r_next = prof_r(min(H, y_c + eps))
            # Profil eğim açısı: dr/dy → normal yönü
            dr = r_next - r_c
            # Yüzey normali (radyal-dışarı bileşeni n_r, yukarı bileşeni n_y)
            slope = math.atan2(dr, eps)          # eğim açısı
            n_r   =  math.cos(slope)             # radyal normal bileşeni
            n_y   = -math.sin(slope)             # Y normal bileşeni

            # Merkez nokta (yüzeyde)
            cx = r_c * cos_a
            cy = H - y_c
            cz = r_c * sin_a

            # Yüzey teğet yönü (spiral ilerleyişine dik, yüzey üzerinde)
            # Spiral teğeti: açısal yön (−sin, 0, cos) + eksenel yön
            # Sadece açısal tanjantı kullan (gövde etrafında şerit genişliği)
            tx = -sin_a
            tz =  cos_a

            # Normal yönünde dışa it (kabartma)
            nx = cos_a * n_r
            ny = n_y
            nz = sin_a * n_r

            x = cx + nx * offset_along_normal + tx * offset_along_tangent
            y = cy + ny * offset_along_normal
            z = cz + nz * offset_along_normal + tz * offset_along_tangent
            return (x, y, z)

        for i in range(steps):
            t0 = i       / steps
            t1 = (i + 1) / steps

            # Her segment: şeridin 4 kenarı (2 yan × 2 uç = dörtgen → 2 üçgen)
            # Yüzeyde (normal=0) sol/sağ kenar, kabartmada (normal=sh) sol/sağ kenar
            s0_base_l = spiral_surface_pt(t0, 0,   -sw)
            s0_base_r = spiral_surface_pt(t0, 0,    sw)
            s0_top_l  = spiral_surface_pt(t0, sh,  -sw)
            s0_top_r  = spiral_surface_pt(t0, sh,   sw)

            s1_base_l = spiral_surface_pt(t1, 0,   -sw)
            s1_base_r = spiral_surface_pt(t1, 0,    sw)
            s1_top_l  = spiral_surface_pt(t1, sh,  -sw)
            s1_top_r  = spiral_surface_pt(t1, sh,   sw)

            # Üst yüzey (dışa bakan)
            tris += [(s0_top_l, s0_top_r, s1_top_l),
                     (s0_top_r, s1_top_r, s1_top_l)]
            # Sol yan duvar
            tris += [(s0_base_l, s0_top_l, s1_base_l),
                     (s0_top_l,  s1_top_l, s1_base_l)]
            # Sağ yan duvar
            tris += [(s0_top_r, s0_base_r, s1_top_r),
                     (s0_base_r, s1_base_r, s1_top_r)]

    # ── 3. HARF KABARTMA ───────────────────────────────────────
    # Qt QPainterPath.addText() → outline → ear-clip triangulation.
    # Herhangi bir Unicode karakter desteklenir:
    # ASCII, TR (Ğ,İ,Ş,Ç,Ö,Ü…), Japonca (漢,あ,ア…), Arapça, vb.
    if letter:
        ch     = letter[0]                  # ilk karakter (büyük/küçük korunur)
        flat_r = R * 0.50 * 0.82            # üst düzlüğe sığacak yarıçap
        lift   = H * 0.08                  # kabartma yüksekliği
        base_y = H                          # üst yüzey Y koordinatı
        tris  += glyph_to_mesh_tris(ch, flat_r, base_y, lift)

    return tris


def export_obj(tris: list, path: str, diam: float, height: float,
               spiral: bool, letter: str):
    """Üçgen listesini .obj dosyasına yazar."""
    lines = [
        "# BeiDesignCAD OBJ Export",
        f"# diam={diam}mm  height={height}mm"
        f"  spiral={'yes' if spiral else 'no'}  letter='{letter}'",
        "o beigoma",
        "",
    ]
    for v0,v1,v2 in tris:
        for v in (v0,v1,v2):
            lines.append(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}")
    lines.append("")
    n = len(tris)
    for i in range(n):
        b = i*3 + 1
        lines.append(f"f {b} {b+1} {b+2}")
    Path(path).write_text("\n".join(lines), encoding="utf-8")


# ══════════════════════════════════════════════════════════════
# 3D GÖRÜNTÜLEYICI
# ══════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════
# OPENGL SHARED BASE — tüm 3D view'lar bu sınıftan türer
# ══════════════════════════════════════════════════════════════

_GL_VERT_SRC = """
#version 330 core
layout(location=0) in vec3 aPos;
layout(location=1) in vec3 aNorm;

uniform mat4 uMVP;
uniform mat3 uNormMat;
uniform vec3 uLightDir;
uniform vec3 uBaseColor;
uniform float uAmbient;
uniform float uDiffuse;

out vec3 vColor;

void main() {
    vec3 n = normalize(uNormMat * aNorm);
    float diff = max(dot(n, uLightDir), 0.0);
    float light = uAmbient + uDiffuse * diff;
    vColor = clamp(uBaseColor * light, 0.0, 1.0);
    gl_Position = uMVP * vec4(aPos, 1.0);
}
"""

_GL_FRAG_SRC = """
#version 330 core
in vec3 vColor;
out vec4 FragColor;
void main() {
    FragColor = vec4(vColor, 1.0);
}
"""

# Texture destekli shader (FaceBoltView hexagon üstü için)
_GL_TEX_VERT_SRC = """
#version 330 core
layout(location=0) in vec3 aPos;
layout(location=1) in vec3 aNorm;
layout(location=2) in vec2 aUV;

uniform mat4 uMVP;
uniform mat3 uNormMat;
uniform vec3 uLightDir;
uniform float uAmbient;
uniform float uDiffuse;

out vec2 vUV;
out float vLight;

void main() {
    vec3 n = normalize(uNormMat * aNorm);
    float diff = max(dot(n, uLightDir), 0.0);
    vLight = uAmbient + uDiffuse * diff;
    vUV = aUV;
    gl_Position = uMVP * vec4(aPos, 1.0);
}
"""

_GL_TEX_FRAG_SRC = """
#version 330 core
in vec2 vUV;
in float vLight;
uniform sampler2D uTex;
out vec4 FragColor;
void main() {
    vec3 texColor = texture(uTex, vUV).rgb;
    FragColor = vec4(clamp(texColor * vLight, 0.0, 1.0), 1.0);
}
"""


def _make_mvp(rx_deg, ry_deg, spin_deg, zoom, aspect,
              center_offset=(0.0, 0.0, 0.0),
              z_flip=False, pre_spin_z=False):
    """
    Döndürme + projeksiyon matrisini numpy ile hesapla.
    Döner: (mvp 4x4, norm_mat 3x3) — her ikisi de column-major float32.
    """
    def Rx(a):
        c, s = np.cos(a), np.sin(a)
        return np.array([[1,0,0,0],[0,c,-s,0],[0,s,c,0],[0,0,0,1]], dtype=np.float32)
    def Ry(a):
        c, s = np.cos(a), np.sin(a)
        return np.array([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]], dtype=np.float32)
    def Rz(a):
        c, s = np.cos(a), np.sin(a)
        return np.array([[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.float32)
    def T(tx, ty, tz):
        m = np.eye(4, dtype=np.float32)
        m[0,3]=tx; m[1,3]=ty; m[2,3]=tz
        return m
    def S(s):
        m = np.eye(4, dtype=np.float32); m[0,0]=m[1,1]=m[2,2]=s; return m

    rx = math.radians(rx_deg); ry = math.radians(ry_deg); sp = math.radians(spin_deg)
    cx, cy, cz = center_offset

    # model: merkeze taşı, spin, yaw, pitch
    model = T(-cx, -cy, -cz)
    if z_flip:
        # FaceBolt: Z eksenini çevir (hexagon öne gelsin)
        model = np.array([[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]], dtype=np.float32) @ model
    if pre_spin_z:
        model = Rz(sp) @ model
        model = Ry(ry) @ Rx(rx) @ model
    else:
        model = Ry(sp) @ model          # auto-spin Y etrafında
        model = Ry(ry) @ Rx(rx) @ model

    # Ortografik projeksiyon — aspect ratio düzeltmesi:
    # NDC'de X: [-1,1] = ekran genişliği, Y: [-1,1] = ekran yüksekliği
    # Geniş ekranda (aspect>1): X aralığı daha geniş, zoom'u aspect'e böl
    sx = zoom / max(aspect, 0.01)
    sy = zoom
    proj = np.array([
        [sx,  0,    0,     0],
        [0,   sy,   0,     0],
        [0,   0,   -0.005, 0],
        [0,   0,    0,     1],
    ], dtype=np.float32)

    mvp = proj @ model
    norm_mat = np.linalg.inv(model[:3, :3]).T.astype(np.float32)
    return mvp, norm_mat


def norm_tris(raw_list):
    """(v0,v1,v2) listesini (normal, v0, v1, v2) listesine çevir (normal hesapla)."""
    result = []
    for v0, v1, v2 in raw_list:
        ax=v1[0]-v0[0]; ay=v1[1]-v0[1]; az=v1[2]-v0[2]
        bx=v2[0]-v0[0]; by=v2[1]-v0[1]; bz=v2[2]-v0[2]
        nx=ay*bz-az*by; ny=az*bx-ax*bz; nz=ax*by-ay*bx
        nl=math.sqrt(nx*nx+ny*ny+nz*nz)
        if nl>1e-9: nx,ny,nz=nx/nl,ny/nl,nz/nl
        result.append(((nx,ny,nz), v0, v1, v2))
    return result


def _tris_to_vbo(tris):
    """
    [(normal, v1, v2, v3), ...] listesini interleaved float32 array'e çevir.
    Format: [x,y,z, nx,ny,nz] × 3vertex × N tris  →  shape (N*3, 6)
    """
    N = len(tris)
    if N == 0:
        return np.zeros((0, 6), dtype=np.float32)
    arr = np.empty((N * 3, 6), dtype=np.float32)
    for i, (n, v1, v2, v3) in enumerate(tris):
        base = i * 3
        arr[base,   :3] = v1;  arr[base,   3:] = n
        arr[base+1, :3] = v2;  arr[base+1, 3:] = n
        arr[base+2, :3] = v3;  arr[base+2, 3:] = n
    return arr


class GLMeshView(QOpenGLWidget):
    """
    Tüm 3D view sınıflarının ortak OpenGL tabanı.
    Alt sınıflar _build_mesh() → [(normal,v1,v2,v3),...] döndürür,
    ve _draw_scene() içinde upload_mesh() + draw_group() çağırır.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rx = 20.0; self._ry = 30.0; self._zoom = 1.0
        self._spin_angle = 0.0
        self._auto = True
        self._drag = False; self._last = QPoint()
        self.setCursor(QCursor(Qt.OpenHandCursor))

        self._prog    = None
        self._vao     = None
        self._vbo     = None
        self._n_verts = 0
        self._dirty_mesh = True
        self._groups  = []
        print(f"[GL] __init__: {self.__class__.__name__}")

        # Hint text — GL context'ini bozmayan ayrı QLabel
        from PySide6.QtWidgets import QLabel as _QL
        self._hint_lbl = _QL(self)
        self._hint_lbl.setStyleSheet(
            f"color:{TDIM.name()};font-family:'Segoe UI';font-size:7px;"
            "background:transparent;")
        self._hint_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    # ── Alt sınıf API ────────────────────────────────────────
    def _get_groups(self):
        """
        [(tris, (r,g,b), ambient, diffuse), ...]
        Alt sınıf override eder.
        """
        raise NotImplementedError

    def _view_scale(self):
        """Ortografik scale faktörü — alt sınıf override eder."""
        return 0.05

    def _center_offset(self):
        return (0.0, 0.0, 0.0)

    def _z_flip(self):
        return False

    def _pre_spin_z(self):
        """True ise spin Z etrafında (FaceBolt), False ise Y etrafında."""
        return False

    # ── OpenGL init ──────────────────────────────────────────
    def initializeGL(self):
        try:
            print(f"[GL] initializeGL: {self.__class__.__name__}")
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glDepthFunc(gl.GL_LESS)
            gl.glEnable(gl.GL_CULL_FACE)
            gl.glCullFace(gl.GL_BACK)
            gl.glClearColor(*[c/255.0 for c in CANVAS.getRgb()[:3]], 1.0)

            self._prog = QOpenGLShaderProgram(self)
            ok1 = self._prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex,   _GL_VERT_SRC)
            ok2 = self._prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, _GL_FRAG_SRC)
            ok3 = self._prog.link()
            print(f"[GL] shader compile: vert={ok1} frag={ok2} link={ok3}")
            if not ok3:
                print(f"[GL] shader log: {self._prog.log()}")

            self._vao = QOpenGLVertexArrayObject(self)
            self._vao.create()
            self._vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
            self._vbo.create()
            self._vbo.setUsagePattern(QOpenGLBuffer.UsagePattern.DynamicDraw)

            self._upload_mesh()
            print(f"[GL] initializeGL done: {self._n_verts} verts")
        except Exception as e:
            import traceback
            print(f"[GL ERROR] initializeGL failed: {e}")
            traceback.print_exc()

    def _upload_mesh(self):
        """Tüm grupları tek VBO'ya yükle, offset bilgisini sakla."""
        if self._prog is None or self._vao is None or self._vbo is None:
            # initializeGL henüz çağrılmadı — dirty flag'i koru, sonra çizilince yapılacak
            self._dirty_mesh = True
            return
        try:
            self.makeCurrent()
            groups = self._get_groups()
            all_verts = []
            self._group_offsets = []
            offset = 0
            for tris, color_rgb, amb, dif in groups:
                data = _tris_to_vbo(tris)
                cnt  = len(data)
                self._group_offsets.append((offset, cnt, color_rgb, amb, dif))
                all_verts.append(data)
                offset += cnt
            if all_verts:
                combined = np.concatenate(all_verts, axis=0).astype(np.float32)
            else:
                combined = np.zeros((0, 6), dtype=np.float32)
            self._n_verts = len(combined)
            raw = combined.tobytes()
            self._vao.bind()
            self._vbo.bind()
            self._vbo.allocate(raw, len(raw))
            stride = 6 * 4
            self._prog.bind()
            self._prog.enableAttributeArray(0)
            self._prog.setAttributeBuffer(0, gl.GL_FLOAT, 0,   3, stride)
            self._prog.enableAttributeArray(1)
            self._prog.setAttributeBuffer(1, gl.GL_FLOAT, 3*4, 3, stride)
            self._prog.release()
            self._vbo.release()
            self._vao.release()
            self._dirty_mesh = False
        except Exception as e:
            import traceback
            print(f"[GL ERROR] _upload_mesh failed in {self.__class__.__name__}: {e}")
            traceback.print_exc()
            self._group_offsets = []
            self._n_verts = 0
            self._dirty_mesh = False

    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        if hasattr(self, '_hint_lbl'):
            self._hint_lbl.setText(self._hint_text())
            self._hint_lbl.adjustSize()
            self._hint_lbl.move(4, h - self._hint_lbl.height() - 2)

    def paintGL(self):
        try:
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            if self._dirty_mesh:
                self._upload_mesh()

            if self._n_verts == 0:
                return

            w, h = self.width(), self.height()
            aspect = w / max(h, 1)
            scale  = self._view_scale() * self._zoom

            mvp, norm_mat = _make_mvp(
                self._rx, self._ry, self._spin_angle, scale, aspect,
                center_offset=self._center_offset(),
                z_flip=self._z_flip(),
                pre_spin_z=self._pre_spin_z(),
            )

            LX, LY, LZ = 0.45, 0.75, 0.55
            ll = math.sqrt(LX*LX+LY*LY+LZ*LZ)
            light_dir = np.array([LX/ll, LY/ll, LZ/ll], dtype=np.float32)

            self._prog.bind()
            self._vao.bind()

            # uniformLocation tabanlı — PySide6 6.x'te QMatrix4x4 üzerinden
            # setUniformValue çalışmıyor; raw GL uniform calls kullan
            prog_id = self._prog.programId()
            mvp_flat = mvp.flatten().astype(np.float32)
            nm_flat  = norm_mat.flatten().astype(np.float32)

            loc_mvp   = gl.glGetUniformLocation(prog_id, b"uMVP")
            loc_nm    = gl.glGetUniformLocation(prog_id, b"uNormMat")
            loc_light = gl.glGetUniformLocation(prog_id, b"uLightDir")
            loc_col   = gl.glGetUniformLocation(prog_id, b"uBaseColor")
            loc_amb   = gl.glGetUniformLocation(prog_id, b"uAmbient")
            loc_dif   = gl.glGetUniformLocation(prog_id, b"uDiffuse")

            gl.glUniformMatrix4fv(loc_mvp,  1, gl.GL_TRUE, mvp_flat)
            gl.glUniformMatrix3fv(loc_nm,   1, gl.GL_TRUE, nm_flat)
            gl.glUniform3f(loc_light, float(light_dir[0]), float(light_dir[1]), float(light_dir[2]))

            for start, count, color_rgb, amb, dif in self._group_offsets:
                if count == 0:
                    continue
                r, g, b = color_rgb
                gl.glUniform3f(loc_col, float(r), float(g), float(b))
                gl.glUniform1f(loc_amb, float(amb))
                gl.glUniform1f(loc_dif, float(dif))
                gl.glDrawArrays(gl.GL_TRIANGLES, start, count)

            self._vao.release()
            self._prog.release()
        except Exception as e:
            import traceback
            print(f"[GL ERROR] paintGL failed in {self.__class__.__name__}: {e}")
            traceback.print_exc()

    def _hint_text(self):
        return tr("drag_hint")

    def _to_qt_mat4(self, m):
        from PySide6.QtGui import QMatrix4x4
        vals = m.flatten().tolist()
        return QMatrix4x4(*vals)

    def _to_qt_mat3(self, m):
        from PySide6.QtGui import QMatrix3x3
        vals = m.flatten().tolist()
        return QMatrix3x3(vals)

    # ── Mouse / wheel ─────────────────────────────────────────
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag = True; self._auto = False
            self._last = e.position().toPoint()
            self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, e):
        self._drag = False
        self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseDoubleClickEvent(self, e):
        self._auto = True

    def mouseMoveEvent(self, e):
        if self._drag:
            d = e.position().toPoint() - self._last
            self._ry += d.x() * 0.5
            self._rx = max(-89, min(89, self._rx + d.y() * 0.5))
            self._last = e.position().toPoint()
            self.update()

    def wheelEvent(self, e):
        self._zoom *= 1.12 if e.angleDelta().y() > 0 else 0.88
        self._zoom = max(0.2, min(8.0, self._zoom))
        self.update()

    def invalidate_mesh(self):
        self._dirty_mesh = True
        self.update()


class BeigomaView(GLMeshView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bei_diam   = 25.0
        self.bei_height = 15.0
        self.spiral     = False
        self.letter     = ""
        self._rx = 25.0; self._ry = -35.0
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(200, 200)
        self._mesh_key = None

    def _spin(self):
        if self._auto:
            self._ry = (self._ry + 0.5) % 360
            self.update()

    def _view_scale(self):
        return 0.04 / max(self.bei_diam / 25.0, 0.1)

    def _get_groups(self):
        key = (self.bei_diam, self.bei_height, self.spiral, self.letter)
        if key != self._mesh_key:
            self._mesh_key = key
        raw = build_beigoma_mesh(self.bei_diam, self.bei_height, self.spiral, self.letter)
        # (v1,v2,v3) → (normal, v1, v2, v3) dönüştür
        tris = norm_tris(raw)
        if _DARK:
            color = (175/255, 178/255, 187/255)
            return [(tris, color, 0.20, 0.78)]
        else:
            color = (220/255, 220/255, 228/255)
            return [(tris, color, 0.55, 0.45)]

    def _hint_text(self):
        return tr("drag_hint2")


# ══════════════════════════════════════════════════════════════
# SAĞ PANEL
# ══════════════════════════════════════════════════════════════

class BeigomaPanel(QWidget):
    def __init__(self, view=None, parent=None):
        super().__init__(parent)
        self._view = view
        # Kendi state — view olmasa da export çalışsın
        self._bei_diam   = 25.0
        self._bei_height = 15.0
        self._bei_spiral = False
        self._bei_letter = ""
        self.setStyleSheet("background:transparent;")
        self._build()

    def _build(self):
        v = QVBoxLayout(self)
        v.setContentsMargins(12,12,12,12); v.setSpacing(10)

        ss_lbl = (f"color:{TSEC.name()};font-family:'Segoe UI';"
                  "font-size:9px;background:transparent;")
        ss_inp = (
            f"QSpinBox, QLineEdit {{"
            f"  color:{TPRI.name()};font-family:'Segoe UI';font-size:10px;"
            f"  background:{PANEL.name()};border:1px solid {BORDER.name()};"
            f"  padding:3px 6px; selection-background-color:{ACCENT.name()};"
            f"  selection-color:#ffffff;}}"
            f"QSpinBox::up-button, QSpinBox::down-button {{"
            f"  background:{PANEL.name()};border:none;width:16px;}}"
            f"QSpinBox::up-arrow   {{ width:7px;height:7px; }}"
            f"QSpinBox::down-arrow {{ width:7px;height:7px; }}"
        )
        ss_btn = (
            f"QPushButton {{"
            f"  color:{TPRI.name()};font-family:'Segoe UI';font-size:9px;"
            f"  background:{PANEL.name()};border:1px solid {BLIT.name()};"
            f"  padding:6px 10px;text-align:left;}}"
            f"QPushButton:hover {{"
            f"  background:{PHOVER.name()};border-color:{ACCENT.name()};}}"
        )

        def row(lbl_text, widget):
            r=QWidget(); r.setStyleSheet("background:transparent;")
            rl=QHBoxLayout(r); rl.setContentsMargins(0,0,0,0); rl.setSpacing(8)
            lb=QLabel(lbl_text); lb.setFixedWidth(76); lb.setStyleSheet(ss_lbl)
            rl.addWidget(lb); rl.addWidget(widget); return r

        self._diam = QSpinBox()
        self._diam.setRange(10,60); self._diam.setValue(25); self._diam.setSuffix(" mm")
        self._diam.setStyleSheet(ss_inp); self._diam.valueChanged.connect(self._update)
        v.addWidget(row(tr("diameter"), self._diam))

        self._h = QSpinBox()
        self._h.setRange(5,40); self._h.setValue(15); self._h.setSuffix(" mm")
        self._h.setStyleSheet(ss_inp); self._h.valueChanged.connect(self._update)
        v.addWidget(row(tr("height"), self._h))

        v.addWidget(hdiv())

        self._ltr = QLineEdit()
        self._ltr.setMaxLength(1); self._ltr.setPlaceholderText("—")
        self._ltr.setToolTip(tr("sym_tip"))
        self._ltr.setStyleSheet(ss_inp); self._ltr.textChanged.connect(self._update)
        v.addWidget(row(tr("symbol"), self._ltr))

        v.addWidget(hdiv())

        self._spiral_cb = QCheckBox(tr("spiral"))
        self._spiral_cb.setStyleSheet(
            f"color:{TPRI.name()};font-family:'Segoe UI';font-size:9px;background:transparent;")
        self._spiral_cb.stateChanged.connect(self._update)
        v.addWidget(self._spiral_cb)

        v.addWidget(hdiv())

        btn = QPushButton(tr("export_obj"))
        btn.setStyleSheet(ss_btn)
        btn.clicked.connect(self._export_obj)
        v.addWidget(btn)

        v.addStretch()

    def set_dirty_callback(self, cb):
        """EditorWindow tarafından set edilir — her değişiklikte çağrılır."""
        self._dirty_cb = cb

    def _update(self):
        self._bei_diam   = float(self._diam.value())
        self._bei_height = float(self._h.value())
        self._bei_spiral = self._spiral_cb.isChecked()
        self._bei_letter = self._ltr.text()
        if self._view is not None:
            self._view.bei_diam   = self._bei_diam
            self._view.bei_height = self._bei_height
            self._view.spiral     = self._bei_spiral
            self._view.letter     = self._bei_letter
            self._view.invalidate_mesh()
        if hasattr(self, "_dirty_cb") and self._dirty_cb:
            self._dirty_cb()

    def load_from(self, data: dict):
        self._spiral_cb.blockSignals(True)
        self._ltr.blockSignals(True)
        self._spiral_cb.setChecked(bool(data.get("spiral", False)))
        self._ltr.setText(str(data.get("symbol", ""))[:1])
        self._spiral_cb.blockSignals(False)
        self._ltr.blockSignals(False)
        self._bei_spiral = self._spiral_cb.isChecked()
        self._bei_letter = self._ltr.text()
        if self._view is not None:
            self._view.spiral = self._bei_spiral
            self._view.letter = self._bei_letter
            self._view.invalidate_mesh()

    def get_data(self) -> dict:
        """Mevcut panel değerlerini dict olarak döndürür."""
        return {
            "spiral": self._spiral_cb.isChecked(),
            "symbol": self._ltr.text(),
        }

    def _export_obj(self):
        path, _ = QFileDialog.getSaveFileName(
            self, tr("save_title"), "beigoma.obj", tr("save_filter"))
        if not path:
            return
        diam   = self._bei_diam
        height = self._bei_height
        spiral = self._bei_spiral
        letter = self._bei_letter
        if self._view is not None:
            diam = self._view.bei_diam; height = self._view.bei_height
            spiral = self._view.spiral; letter = self._view.letter
            tris = build_beigoma_mesh(diam, height, spiral, letter)
        else:
            tris = build_beigoma_mesh(diam, height, spiral, letter)  # ham (v0,v1,v2)
        export_obj(tris, path, diam, height, spiral, letter)
        QMessageBox.information(self, tr("export_done"),
                                tr("export_msg").format(n=len(tris), p=path))


# ══════════════════════════════════════════════════════════════
# DİĞER PANELLER
# ══════════════════════════════════════════════════════════════

class PartSlot(QWidget):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        self._label=label; self._hover=False
        self.setFixedHeight(52); self.setCursor(Qt.PointingHandCursor)
    def enterEvent(self,e): self._hover=True;  self.update()
    def leaveEvent(self,e): self._hover=False; self.update()
    def paintEvent(self,_):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        w,h=self.width(),self.height()
        p.fillRect(0,0,w,h,PHOVER if self._hover else PANEL)
        p.setPen(QPen(ACCENT if self._hover else BORDER,1,Qt.DashLine))
        p.drawRect(1,1,w-2,h-2)
        p.setFont(QFont("Segoe UI",9,QFont.DemiBold))
        p.setPen(TTITLE if self._hover else TSEC)
        p.drawText(QRect(12,0,w-60,h),Qt.AlignVCenter|Qt.AlignLeft,self._label)
        p.setFont(QFont("Segoe UI",8)); p.setPen(TDIM)
        p.drawText(QRect(12,0,w-16,h),Qt.AlignVCenter|Qt.AlignRight,"+ Ekle")
        p.end()


class EditorTopBar(QWidget):
    def __init__(self, name, series_label, parent=None):
        super().__init__(parent)
        self._name=name; self._label=series_label; self.setFixedHeight(36)
    def paintEvent(self,_):
        p=QPainter(self); w,h=self.width(),self.height()
        # Ana bar rengi
        topbar_bg   = SIDEBAR.darker(110) if _DARK else SIDEBAR.lighter(97)
        topbar_logo = SIDEBAR.darker(130) if _DARK else SIDEBAR.darker(103)
        p.fillRect(0,0,w,h, topbar_bg)
        p.setPen(QPen(BORDER,1)); p.drawLine(0,h-1,w,h-1)
        p.fillRect(0,0,170,h, topbar_logo)
        p.setPen(QPen(BORDER,1)); p.drawLine(170,0,170,h)
        p.setFont(QFont("Segoe UI",10,QFont.Bold))
        p.setPen(ACCENT); p.drawText(QRect(14,0,40,h),Qt.AlignVCenter,"Bei")
        p.setPen(TSEC);   p.drawText(QRect(46,0,120,h),Qt.AlignVCenter,"DesignCAD")
        p.setFont(QFont("Segoe UI",9))
        p.setPen(TSEC); p.drawText(QRect(186,0,20,h),Qt.AlignVCenter,"›")
        p.setPen(TPRI); p.drawText(QRect(202,0,400,h),Qt.AlignVCenter,self._name)
        tw=120; tx=w-tw-12
        p.fillRect(tx,8,tw,20,QColor(ACCENT.red(),ACCENT.green(),ACCENT.blue(),30))
        p.setPen(QPen(QColor(ACCENT.red(),ACCENT.green(),ACCENT.blue(),80),1))
        p.drawRect(tx,8,tw,20)
        p.setFont(QFont("Segoe UI",7,QFont.Bold)); p.setPen(ACCENT)
        p.drawText(QRect(tx,8,tw,20),Qt.AlignCenter,self._label.upper())
        p.end()



# ══════════════════════════════════════════════════════════════
# BEYBLADE PREVIEW VIEW — 5 parçayı birleşik Z stack'te gösterir
# ══════════════════════════════════════════════════════════════
def _tris_z_max(tris):
    """Verilen triangle listesinin (normal,v1,v2,v3) maksimum Z değerini döndürür."""
    if not tris:
        return 0.0
    return max(max(v1[2], v2[2], v3[2]) for _, v1, v2, v3 in tris)

def _tris_z_min(tris):
    """Verilen triangle listesinin (normal,v1,v2,v3) minimum Z değerini döndürür."""
    if not tris:
        return 0.0
    return min(min(v1[2], v2[2], v3[2]) for _, v1, v2, v3 in tris)


class BeybladePreviewView(GLMeshView):
    """
    Sol panel önizleme: FaceBolt + EnergyRing + FusionWheel + SpinTrack + PerformanceTip
    tek OpenGL sahnesinde, Z ekseninde hizalanmış, dönen beyblade.

    Dizilim mantığı (ALTTAN ÜSTE, +Z = yukarı):
    ─────────────────────────────────────────────────────────────
    1. PerformanceTip  → en altta, flip sonrası üst yüzü Z=0 referans.
                         PT orijinalinde üst yüz Z=z_max → _flip_z_tris → üst Z=0, uç aşağı.
    2. SpinTrack       → PT'nin üst bitişinden 3mm ALTA (yani PT_üst−3mm):
                         ST_Z_OFF = PT_TOP_Z − 3.0
                         (ST orijinalinde alt yüzü Z=0 → ST en alttaki vertex Z=0)
    3. FusionWheel     → ST'nin üst bitişinden 3mm ALTA:
                         FW_Z_OFF = ST_TOP_Z − 3.0
                         (Tinker orijinali Z=0 alt, Z≈6.5 üst)
    4. EnergyRing      → FW'nin üst bitişinden 3mm ALTA:
                         ER_Z_OFF = FW_TOP_Z − 3.0
                         (ER orijinali kendi Z min/max'ına göre)
    5. FaceBolt        → ER'nin üst bitişinden 3mm ÜSTE:
                         FB_Z_OFF = ER_TOP_Z + 3.0
                         (FB flip sonrası: hexagon üst Z=0, vida ucu Z=−FB_TOTAL_H.
                          Z_OFF = ER_TOP + 3 → hexagon üstü ER_TOP+3 konumuna gelir)
    ─────────────────────────────────────────────────────────────
    Her parça Z offseti update_from_panels() içinde gerçek mesh
    boyutlarından dinamik olarak hesaplanır.
    """

    # Overlap miktarı (mm) — her parça bir öncekinin üst bitişinden bu kadar aşağıda başlar
    _OVERLAP = 3.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._rx = 15.0   # hafif eğik bakış
        self._ry = 0.0

        # Her parça için mesh + renk — dışarıdan set edilir
        self._groups : list = []   # [(tris, rgb, amb, dif), ...]
        self._fb_tex  = None       # FaceBolt texture (QImage)
        self._fb_tex_groups : list = []  # texture VBO için ayrı list

        # Dinamik kamera framing
        self._stack_z_center = 0.0
        self._stack_z_range  = 40.0
        self._stack_r_max    = 20.0   # radyal (X/Y) maksimum

        # Texture nesneleri (FaceBolt top face)
        self._tex_prog  = None
        self._tex_vao   = None
        self._tex_vbo   = None
        self._tex_id    = None
        self._tex_n     = 0
        self._tex_dirty = False

        # ── RPM takibi ───────────────────────────────────────
        # Timer aralığı 33ms → saniyede ~30.3 tick
        # Her tick 1.2° döner → RPM = 1.2 * (1000/33) * (60/360) ≈ 60.6
        self._RPM_MAX        = 1250.0          # üst sınır
        self._rpm_deg_tick   = 1.2            # her tick kaç derece döner
        self._rpm_timer_ms   = 33             # timer aralığı (ms)
        self._rpm_current    = self._rpm_deg_tick * (1000.0 / self._rpm_timer_ms) * (60.0 / 360.0)

        # RPM overlay etiketi
        from PySide6.QtWidgets import QLabel as _QL2
        self._rpm_lbl = _QL2(self)
        self._rpm_lbl.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self._rpm_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._rpm_lbl.setStyleSheet(
            "color:#e8e8e8; font-family:'Segoe UI'; font-size:9px; font-weight:600;"
            "background: rgba(0,0,0,120); border-radius:3px; padding:2px 5px;"
        )
        self._rpm_lbl.raise_()
        self._update_rpm_label()

    def _update_rpm_label(self):
        """RPM etiketini güncelle — değer ve maks sınırını göster."""
        rpm = self._rpm_current
        capped = min(rpm, self._RPM_MAX)
        pct = capped / self._RPM_MAX * 100.0
        # Renge göre dolu bar karakteri (▓)
        bar_len = 8
        filled  = int(round(pct / 100.0 * bar_len))
        bar     = "▓" * filled + "░" * (bar_len - filled)
        self._rpm_lbl.setText(f"⟳ {int(capped):>5} RPM\n{bar} max {int(self._RPM_MAX)}")
        self._rpm_lbl.adjustSize()
        # Sağ üst köşeye yerleştir
        margin = 6
        self._rpm_lbl.move(self.width() - self._rpm_lbl.width() - margin, margin)

    # ── GLMeshView overrides ──────────────────────────────────
    def _view_scale(self):
        # Tüm stack'i sığdırmak için Z ve radyal boyutların büyüğünü kullan
        half_z  = max(self._stack_z_range / 2.0, 1.0)
        half_r  = max(self._stack_r_max, 1.0)
        biggest = max(half_z, half_r)
        return (1.0 / 2.2) / biggest

    def _center_offset(self):
        return (0.0, 0.0, self._stack_z_center)

    def _z_flip(self):      return False
    def _pre_spin_z(self):  return True   # Z ekseni etrafında spin (Beyblade gibi)
    def _hint_text(self):   return ""

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, '_rpm_lbl'):
            self._update_rpm_label()

    def _on_tick(self):
        self._spin_angle += self._rpm_deg_tick
        self.update()

    def _get_groups(self):
        return self._groups

    # ── Dışarıdan mesh güncelleme ─────────────────────────────
    def update_from_panels(self,
                           fb_view=None, er_view=None, fw_view=None,
                           st_view=None, pt_view=None):
        """
        Panel view'larından mesh'leri toplayıp birleşik sahneyi güncelle.

        Dizilim: alttan başla (PT referans Z=0), her parçanın üst bitişinin
        3mm altından bir sonraki parça başlar. FaceBolt ise ER üst bitişinin
        3mm üstüne yerleştirilir (vida aşağı iner, hexagon üstte).
        """
        groups   = []
        all_z    = []
        amb_d, dif_d = (0.22, 0.78) if _DARK else (0.42, 0.58)

        # ════════════════════════════════════════════════════════
        # 1. PERFORMANCE TIP  (en alt — referans: üst yüzü Z=0)
        # ════════════════════════════════════════════════════════
        pt_top_z = 0.0   # PT üst bitişi = Z=0 (flip sonrası sabit referans)

        if pt_view is not None:
            pt_raw  = _pt_tris(pt_view.tip_shape, pt_view.tip_length,
                               pt_view.tip_flat_r, pt_view.tip_hole_r,
                               pt_view.tip_hole_d)
            # PT orijinali: üst bağlantı yüzü Z≈0 (z_min), uç Z=büyük pozitif (z_max).
            # _flip_z_tris (z→-z) sonrası: bağlantı yüzü Z≈0 kalır, uç Z=negatif.
            # Flip sonrası z_max (bağlantı yüzü) = -z_min_orig ≈ 0.
            # Bağlantı yüzünü tam Z=0'a hizalamak için: offset = -z_max_after_flip
            pt_flip     = _flip_z_tris(pt_raw)
            pt_flip_zmax = _tris_z_max(pt_flip)   # bağlantı yüzü (en üst)
            # Bağlantı yüzü Z=0 olacak şekilde kaydır
            pt_tris_placed = _z_offset_tris(pt_flip, -pt_flip_zmax)
            r = pt_view._color.redF()
            g = pt_view._color.greenF()
            b = pt_view._color.blueF()
            groups.append((pt_tris_placed, (r, g, b), amb_d, dif_d))
            all_z.extend([v[2] for _, v1, v2, v3 in pt_tris_placed
                          for v in (v1, v2, v3)])
            pt_top_z = 0.0  # bağlantı yüzü = Z=0 referansı

        # ════════════════════════════════════════════════════════
        # 2. SPIN TRACK  (PT üst bitişinin 3mm altından başlar)
        # ════════════════════════════════════════════════════════
        # ST orijinalinde alt yüzü genellikle Z=0.
        # ST_alt → pt_top_z − OVERLAP
        # → ST_Z_OFF = (pt_top_z − OVERLAP) − st_z_bot
        st_top_z = pt_top_z   # ST yoksa bu değeri kullan

        if st_view is not None:
            st_raw   = _st_tris(st_view.conn_h)
            st_z_bot = _tris_z_min(st_raw)
            st_z_top = _tris_z_max(st_raw)
            st_z_off = (pt_top_z - self._OVERLAP) - st_z_bot - 1.0
            st_tris_placed = _z_offset_tris(st_raw, st_z_off)
            r = st_view._color.redF()
            g = st_view._color.greenF()
            b = st_view._color.blueF()
            groups.append((st_tris_placed, (r, g, b), amb_d, dif_d))
            all_z.extend([v[2] for _, v1, v2, v3 in st_tris_placed
                          for v in (v1, v2, v3)])
            st_top_z = st_z_off + st_z_top

        # ════════════════════════════════════════════════════════
        # 3. FUSION WHEEL  (ST üst bitişinin 3mm altından başlar)
        # ════════════════════════════════════════════════════════
        # Tinker (FW tabanı): Z=0 alt, Z≈6.5 üst.
        # FW_alt (tinker Z=0) → st_top_z − OVERLAP
        fw_top_z = st_top_z   # FW yoksa ST üstünden devam

        if fw_view is not None:
            tinker_raw = _tinker_tris()
            fw_z_bot   = _tris_z_min(tinker_raw)
            fw_z_top   = _tris_z_max(tinker_raw)   # sadece tinker gövdesi (blade hariç)
            fw_z_off   = (st_top_z - self._OVERLAP) - fw_z_bot
            zamak      = fw_view._ZAMAK_DARK if _DARK else fw_view._ZAMAK_LIGHT
            tinker_placed = _z_offset_tris(tinker_raw, fw_z_off)
            groups.append((tinker_placed, zamak, amb_d, dif_d))
            all_z.extend([v[2] for _, v1, v2, v3 in tinker_placed
                          for v in (v1, v2, v3)])
            # Blade cache — fw_top_z hesabına dahil etme
            if fw_view._blade_cache is None:
                fw_view._get_groups()
            if fw_view._blade_cache:
                blade_placed = _z_offset_tris(fw_view._blade_cache, fw_z_off)
                groups.append((blade_placed,
                               zamak,
                               amb_d, dif_d))
                all_z.extend([v[2] for _, v1, v2, v3 in blade_placed
                              for v in (v1, v2, v3)])
            # fw_top_z = tinker gövdesinin üstü (blade Z'si değil)
            fw_top_z = fw_z_off + fw_z_top

        # ════════════════════════════════════════════════════════
        # 4. ENERGY RING  (FW üst bitişinin 3mm altından başlar)
        # ════════════════════════════════════════════════════════
        er_top_z = fw_top_z   # ER yoksa FW üstünden devam

        if er_view is not None and er_view._raw_tris:
            er_raw   = er_view._raw_tris   # gerçek mm boyutları
            er_z_bot = _tris_z_min(er_raw)
            er_z_top = _tris_z_max(er_raw)
            er_z_off = (fw_top_z - self._OVERLAP) - er_z_bot - 1.0
            er_tris_placed = _z_offset_tris(er_raw, er_z_off)
            r = er_view._color.redF()
            g = er_view._color.greenF()
            b = er_view._color.blueF()
            groups.append((er_tris_placed, (r, g, b), amb_d, dif_d))
            all_z.extend([v[2] for _, v1, v2, v3 in er_tris_placed
                          for v in (v1, v2, v3)])
            er_top_z = er_z_off + er_z_top

        # ════════════════════════════════════════════════════════
        # 5. FACE BOLT  (ER üst bitişinin 3mm ÜSTÜNE yerleşir)
        # ════════════════════════════════════════════════════════
        # FB flip sonrası: hexagon üst yüzü = Z=0, vida ucu = Z=−FB_TOTAL_H
        # İstenen: hexagon üst yüzü = er_top_z + OVERLAP
        # → FB_Z_OFF = er_top_z + OVERLAP
        # (flip sonrası Z=0 olan hexagon, fb_z_off kadar yukarı taşınır)

        if fb_view is not None:
            all_tris = _face_bolt_tris()
            _FB_SINK = 2.5   # FB'yi ER içine 2.5mm göm
            fb_z_off = er_top_z + self._OVERLAP - _FB_SINK

            # Gövde (hexagon üst yüz hariç)
            other = [t for t in all_tris
                     if not (t[0][2] < -_FB_HEX_NZ
                             and (t[1][2]+t[2][2]+t[3][2])/3 < _FB_HEX_Z_MAX)]
            other_flip   = _flip_z_tris(other)
            other_placed = _z_offset_tris(other_flip, fb_z_off)
            if fb_view._body_color:
                bc = fb_view._body_color
                body_col = (bc.redF(), bc.greenF(), bc.blueF())
            else:
                body_col = (175/255, 177/255, 187/255) if _DARK else (210/255, 210/255, 218/255)
            groups.append((other_placed, body_col, amb_d, dif_d))
            all_z.extend([v[2] for _, v1, v2, v3 in other_placed
                          for v in (v1, v2, v3)])

            # Top face (texture için ayrı)
            top = [t for t in all_tris
                   if t[0][2] < -_FB_HEX_NZ
                   and (t[1][2]+t[2][2]+t[3][2])/3 < _FB_HEX_Z_MAX]
            top_flip   = _flip_z_tris(top)
            top_placed = _z_offset_tris(top_flip, fb_z_off)
            self._fb_tex_groups = top_placed
            self._fb_tex        = fb_view._texture
            all_z.extend([v[2] for _, v1, v2, v3 in top_placed
                          for v in (v1, v2, v3)])

        # ── Kamera framing güncellemesi ───────────────────────
        print(f"[PREVIEW] pt_top={pt_top_z:.2f}  st_top={st_top_z:.2f}  fw_top={fw_top_z:.2f}  er_top={er_top_z:.2f}  fb_z_off={er_top_z+self._OVERLAP:.2f}")
        print(f"[PREVIEW] groups={len(groups)}  all_z={'[' + (f'{min(all_z):.1f}..{max(all_z):.1f}' if all_z else 'EMPTY') + ']'}")
        if all_z:
            z_lo = min(all_z)
            z_hi = max(all_z)
            self._stack_z_center = (z_lo + z_hi) / 2.0
            self._stack_z_range  = max(z_hi - z_lo, 1.0)
        else:
            self._stack_z_center = 0.0
            self._stack_z_range  = 40.0

        # Radyal (X/Y) maksimum — sadece tinker + ST + FB gibi "gövde" parçalar
        # blade kanatlarını hariç tutmak için groups'tan tinker ve diğerlerini kullan
        r_max = 20.0
        for grp_tris, _, _, _ in groups:
            for _, v1, v2, v3 in grp_tris:
                for v in (v1, v2, v3):
                    r = math.sqrt(v[0]*v[0] + v[1]*v[1])
                    if r > r_max:
                        r_max = r
        self._stack_r_max = r_max

        self._groups = groups
        self._tex_dirty = True
        if hasattr(self, '_tex_id') and self._tex_id is not None:
            try:
                self.makeCurrent()
                gl.glDeleteTextures(1, [self._tex_id])
            except Exception:
                pass
            self._tex_id = None
        self.invalidate_mesh()

    # ── Texture GL işlemleri ──────────────────────────────────
    def initializeGL(self):
        super().initializeGL()
        if not _HAS_OPENGL:
            return
        try:
            self._tex_prog = QOpenGLShaderProgram(self)
            self._tex_prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex,   _GL_TEX_VERT_SRC)
            self._tex_prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, _GL_TEX_FRAG_SRC)
            self._tex_prog.link()
            self._tex_vao = QOpenGLVertexArrayObject(self)
            self._tex_vao.create()
            self._tex_vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
            self._tex_vbo.create()
            self._tex_vbo.setUsagePattern(QOpenGLBuffer.UsagePattern.DynamicDraw)
        except Exception as e:
            print(f"[GL ERROR] BeybladePreviewView tex init: {e}")

    def _upload_tex_mesh(self):
        if not self._fb_tex_groups or self._tex_prog is None:
            self._tex_n = 0
            self._tex_dirty = False
            return
        try:
            self.makeCurrent()
            tris = self._fb_tex_groups
            arr = np.empty((len(tris)*3, 8), dtype=np.float32)
            for i, (n, v1, v2, v3) in enumerate(tris):
                base = i * 3
                for j, v in enumerate([v1, v2, v3]):
                    # UV: XY pozisyonundan (Z offset sonrası XY değişmedi)
                    u, uv = _fb_uv(v[0], v[1])
                    arr[base+j, :3] = v
                    arr[base+j, 3:6] = n
                    arr[base+j, 6] = u
                    arr[base+j, 7] = uv
            raw = arr.tobytes(); stride = 8 * 4
            self._tex_vao.bind()
            self._tex_vbo.bind()
            self._tex_vbo.allocate(raw, len(raw))
            self._tex_prog.bind()
            self._tex_prog.enableAttributeArray(0)
            self._tex_prog.setAttributeBuffer(0, gl.GL_FLOAT, 0,   3, stride)
            self._tex_prog.enableAttributeArray(1)
            self._tex_prog.setAttributeBuffer(1, gl.GL_FLOAT, 3*4, 3, stride)
            self._tex_prog.enableAttributeArray(2)
            self._tex_prog.setAttributeBuffer(2, gl.GL_FLOAT, 6*4, 2, stride)
            self._tex_prog.release()
            self._tex_vbo.release()
            self._tex_vao.release()
            self._tex_n = len(tris) * 3
            self._tex_dirty = False
        except Exception as e:
            print(f"[GL ERROR] BeybladePreview _upload_tex_mesh: {e}")
            import traceback; traceback.print_exc()

    def _upload_gl_texture(self):
        if self._fb_tex is None:
            return
        img = self._fb_tex.convertToFormat(self._fb_tex.Format.Format_RGBA8888)
        w, h = img.width(), img.height()
        tex_ids = gl.glGenTextures(1)
        self._tex_id = int(tex_ids) if not hasattr(tex_ids, '__len__') else int(tex_ids[0])
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        ptr = img.bits()
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0,
                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, ptr)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def paintGL(self):
        super().paintGL()   # ana gövde grupları

        if self._tex_prog is None:
            return
        try:
            if self._tex_dirty:
                self._upload_tex_mesh()
            if self._tex_n == 0:
                return
            if self._fb_tex is not None and self._tex_id is None:
                self._upload_gl_texture()
            if self._tex_id is None:
                return

            w, h = self.width(), self.height()
            aspect = w / max(h, 1)
            scale  = self._view_scale() * self._zoom
            mvp, norm_mat = _make_mvp(
                self._rx, self._ry, self._spin_angle, scale, aspect,
                center_offset=self._center_offset(),
                z_flip=False, pre_spin_z=True,
            )
            LX, LY, LZ = 0.45, 0.75, 0.55
            ll = math.sqrt(LX*LX+LY*LY+LZ*LZ)
            light_dir = np.array([LX/ll, LY/ll, LZ/ll], dtype=np.float32)
            self._tex_prog.bind()
            self._tex_vao.bind()
            pid = self._tex_prog.programId()
            gl.glUniformMatrix4fv(gl.glGetUniformLocation(pid, b"uMVP"),     1, gl.GL_TRUE, mvp.flatten().astype(np.float32))
            gl.glUniformMatrix3fv(gl.glGetUniformLocation(pid, b"uNormMat"), 1, gl.GL_TRUE, norm_mat.flatten().astype(np.float32))
            gl.glUniform3f(gl.glGetUniformLocation(pid, b"uLightDir"), float(light_dir[0]), float(light_dir[1]), float(light_dir[2]))
            amb, dif = (0.22, 0.78) if _DARK else (0.42, 0.58)
            gl.glUniform1f(gl.glGetUniformLocation(pid, b"uAmbient"), amb)
            gl.glUniform1f(gl.glGetUniformLocation(pid, b"uDiffuse"), dif)
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)
            gl.glUniform1i(gl.glGetUniformLocation(pid, b"uTex"), 0)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, self._tex_n)
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
            self._tex_vao.release()
            self._tex_prog.release()
        except Exception as e:
            import traceback
            print(f"[GL ERROR] BeybladePreview paintGL tex: {e}")
            traceback.print_exc()


# ── Mesh dönüşüm yardımcıları ─────────────────────────────────
def _z_offset_tris(tris, z_off):
    """Tüm vertex'lere Z offset ekle. (normal, v1, v2, v3) listesi."""
    if z_off == 0.0:
        return tris
    result = []
    for n, v1, v2, v3 in tris:
        result.append((n,
                       (v1[0], v1[1], v1[2]+z_off),
                       (v2[0], v2[1], v2[2]+z_off),
                       (v3[0], v3[1], v3[2]+z_off)))
    return result

def _double_sided(tris):
    """Her üçgeni ters kopyasıyla çift taraflı yap.
    Procedural ince yüzeyler (blade, ST connector, PT ucu) için."""
    result = list(tris)
    for n, v1, v2, v3 in tris:
        result.append(((-n[0], -n[1], -n[2]), v3, v2, v1))
    return result

def _flip_z_tris(tris):
    """Z eksenini çevir. Vertex Z'leri negatife alınır, winding order (v1↔v3)
    ters çevrilerek normalin yönü korunur — back-face culling bozulmaz."""
    result = []
    for n, v1, v2, v3 in tris:
        fv1 = (v1[0], v1[1], -v1[2])
        fv2 = (v2[0], v2[1], -v2[2])
        fv3 = (v3[0], v3[1], -v3[2])
        fn  = (n[0], n[1], -n[2])
        result.append((fn, fv3, fv2, fv1))
    return result


def make_left(series_id, preview_view=None, export_all_cb=None):
    w=QWidget(); w.setMinimumWidth(180)
    w.setStyleSheet(f"background:{SIDEBAR.name()};border-right:1px solid {BORDER.name()};")
    v=QVBoxLayout(w); v.setContentsMargins(0,0,0,0); v.setSpacing(0)

    if series_id != "beigoma":
        v.addWidget(sec_header(tr("preview")))
        if preview_view is not None:
            v.addWidget(preview_view, 2)
            # ── RPM bölümü ─────────────────────────────────
            v.addWidget(hdiv())
            v.addWidget(sec_header(tr("spin_speed")))
            rpm_container = QWidget()
            rpm_container.setStyleSheet("background:transparent;")
            rpm_v = QVBoxLayout(rpm_container)
            rpm_v.setContentsMargins(8, 4, 8, 6)
            rpm_v.setSpacing(4)

            # Hız göstergesi etiketi
            rpm_val_lbl = QLabel()
            rpm_val_lbl.setAlignment(Qt.AlignCenter)
            _rpm_val = preview_view._rpm_deg_tick * (1000.0 / preview_view._rpm_timer_ms) * (60.0 / 360.0)
            rpm_val_lbl.setText(f"{int(_rpm_val)} RPM")
            rpm_val_lbl.setStyleSheet(
                f"color:{TPRI.name()};font-family:'Segoe UI';font-size:13px;"
                f"font-weight:700;background:transparent;"
            )
            rpm_v.addWidget(rpm_val_lbl)

            # Maks bilgisi
            rpm_max_lbl = QLabel(tr("max_rpm").format(rpm=int(preview_view._RPM_MAX)))
            rpm_max_lbl.setAlignment(Qt.AlignCenter)
            rpm_max_lbl.setStyleSheet(
                f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;"
                f"background:transparent;"
            )
            rpm_v.addWidget(rpm_max_lbl)

            # Hız slider'ı
            from PySide6.QtWidgets import QSlider
            rpm_slider = QSlider(Qt.Horizontal)
            # Slider değeri 0-100 arasında, RPM 0..1250 arası
            _rpm_to_slider = lambda rpm: int(rpm / preview_view._RPM_MAX * 100)
            _slider_to_rpm = lambda v: v / 100.0 * preview_view._RPM_MAX
            rpm_slider.setRange(0, 100)
            rpm_slider.setValue(_rpm_to_slider(_rpm_val))
            rpm_slider.setStyleSheet(
                f"QSlider::groove:horizontal {{height:4px;background:{BORDER.name()};border-radius:2px;}}"
                f"QSlider::handle:horizontal {{background:{ACCENT.name()};border:none;"
                f"width:12px;height:12px;margin:-4px 0;border-radius:6px;}}"
                f"QSlider::sub-page:horizontal {{background:{ACCENT.name()};border-radius:2px;}}"
            )

            def _on_rpm_change(val):
                new_rpm   = _slider_to_rpm(val)
                # Her tick'te dönecek derece: rpm * 360 / 60 / (1000/timer_ms)
                new_deg   = new_rpm * (360.0 / 60.0) / (1000.0 / preview_view._rpm_timer_ms)
                preview_view._rpm_deg_tick = new_deg
                preview_view._rpm_current  = new_rpm
                rpm_val_lbl.setText(f"{int(new_rpm)} RPM")
                preview_view._update_rpm_label()

            rpm_slider.valueChanged.connect(_on_rpm_change)
            rpm_v.addWidget(rpm_slider)
            v.addWidget(rpm_container)
        else:
            ph=QWidget(); ph.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            ph.setMinimumHeight(160); ph.setStyleSheet(f"background:{CANVAS.name()};")
            v.addWidget(ph,2)

    # "Hepsini Dışa Aktar" butonu — sadece hybrid_wheel ve callback varsa
    if series_id == "hybrid_wheel" and export_all_cb is not None:
        v.addWidget(hdiv())
        zip_btn = QPushButton(tr("export_zip"))
        zip_btn.setFixedHeight(28)
        zip_btn.setStyleSheet(
            f"QPushButton{{background:{ACCENT.name()};color:#ffffff;"
            f"border:none;border-radius:3px;"
            f"font-family:'Segoe UI';font-size:8px;font-weight:600;padding:0 8px;margin:4px 6px;}}"
            f"QPushButton:hover{{background:{ACCENT.lighter(115).name()};}}"
        )
        zip_btn.clicked.connect(export_all_cb)
        v.addWidget(zip_btn)

    update_weight = None
    update_power  = None
    if series_id != "beigoma":
        # ── TOPLAM AĞIRLIK ────────────────────────────────────
        v.addWidget(hdiv())
        v.addWidget(sec_header(tr("total_weight")))
        ww, update_weight = weight_label_widget()
        v.addWidget(ww)
        # ── GÜÇ HESAPLAMA ─────────────────────────────────────
        v.addWidget(hdiv()); v.addWidget(sec_header(tr("power_stats")))
        sw=QWidget(); sw.setStyleSheet("background:transparent;")
        sv=QVBoxLayout(sw); sv.setContentsMargins(0,4,0,4); sv.setSpacing(2)
        sb_atk, upd_atk = stat_bar_live(tr("attack"),  ATK, max_val=20)
        sb_def, upd_def = stat_bar_live(tr("defense"), DEF, max_val=20)
        sb_sta, upd_sta = stat_bar_live(tr("stamina"), STA, max_val=20)
        sv.addWidget(sb_atk); sv.addWidget(sb_def); sv.addWidget(sb_sta)
        v.addWidget(sw)

        # ── TÜR BELİRLEYİCİ ──────────────────────────────────
        v.addWidget(hdiv())
        v.addWidget(sec_header(tr("type_label")))

        # Gömülü PNG ikonları (base64)
        _TYPE_INFO = [
            ("attack",   tr("attack"),   _ATTACK_PNG_B64),
            ("defense",  tr("defense"),  _DEFENSE_PNG_B64),
            ("stamina",  tr("stamina"),  _STAMINA_PNG_B64),
            ("balance",  tr("balance"),  _BALANCE_PNG_B64),
        ]

        type_container = QWidget()
        type_container.setStyleSheet("background:transparent;")
        type_layout = QHBoxLayout(type_container)
        type_layout.setContentsMargins(6, 6, 6, 6)
        type_layout.setSpacing(6)

        # Her tür için (ikon QLabel, ad QLabel) çiftleri
        _type_widgets = {}  # key → (icon_lbl, name_lbl, col_widget)
        for key, label_text, png_b64 in _TYPE_INFO:
            col = QWidget(); col.setStyleSheet("background:transparent;")
            cl  = QVBoxLayout(col); cl.setContentsMargins(0,0,0,0); cl.setSpacing(2)

            icon_lbl = QLabel()
            icon_lbl.setFixedSize(36, 36)
            icon_lbl.setAlignment(Qt.AlignCenter)
            icon_lbl.setStyleSheet("background:transparent;")

            # Gömülü base64'ten yükle
            _pix = _load_type_pixmap(png_b64)
            if not _pix.isNull():
                icon_lbl.setPixmap(_pix.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                _fallback = {"attack":"⚔️","defense":"🛡️","stamina":"🌀","balance":"⚖️"}
                icon_lbl.setText(_fallback.get(key,"?"))
                icon_lbl.setStyleSheet(f"background:transparent;font-size:20px;")

            name_lbl = QLabel(label_text)
            name_lbl.setAlignment(Qt.AlignCenter)
            name_lbl.setStyleSheet(
                f"color:{TSEC.name()};font-family:'Segoe UI';font-size:7px;"
                f"font-weight:600;background:transparent;"
            )

            cl.addWidget(icon_lbl, 0, Qt.AlignCenter)
            cl.addWidget(name_lbl, 0, Qt.AlignCenter)
            type_layout.addWidget(col)
            _type_widgets[key] = (icon_lbl, name_lbl, col, _pix)

        v.addWidget(type_container)

        # Aktif tür adı etiketi (büyük, renkli)
        type_name_lbl = QLabel("—")
        type_name_lbl.setAlignment(Qt.AlignCenter)
        type_name_lbl.setStyleSheet(
            f"color:{TPRI.name()};font-family:'Segoe UI';font-size:11px;"
            f"font-weight:700;background:transparent;padding:2px 0 6px 0;"
        )
        v.addWidget(type_name_lbl)

        _TYPE_BALANCE_THRESH = 3  # eşik: tüm çiftlerin farkı bu değerden az ise denge

        def _detect_type(atk, def_, sta):
            """Tür tespiti: 3 kombinasyonun hepsinin farkı < eşik → denge, değilse max."""
            if (abs(atk - def_) < _TYPE_BALANCE_THRESH and
                abs(def_ - sta) < _TYPE_BALANCE_THRESH and
                abs(atk - sta)  < _TYPE_BALANCE_THRESH):
                return "balance"
            mx = max(atk, def_, sta)
            if mx == atk:   return "attack"
            if mx == def_:  return "defense"
            return "stamina"

        def _refresh_type(atk, def_, sta):
            active = _detect_type(atk, def_, sta)
            _TYPE_LABELS = {
                "attack":  tr("attack"),
                "defense": tr("defense"),
                "stamina": tr("stamina"),
                "balance": tr("balance"),
            }
            _TYPE_COLORS = {
                "attack":  ATK.name(),
                "defense": DEF.name(),
                "stamina": STA.name(),
                "balance": "#c84b4b",
            }
            type_name_lbl.setText(_TYPE_LABELS[active])
            type_name_lbl.setStyleSheet(
                f"color:{_TYPE_COLORS[active]};font-family:'Segoe UI';font-size:11px;"
                f"font-weight:700;background:transparent;padding:2px 0 6px 0;"
            )
            for key, (icon_lbl, name_lbl, col, orig_pix) in _type_widgets.items():
                is_active = (key == active)
                # Parlak / soluk geçişi — opacity efekti için grafik efekt
                from PySide6.QtWidgets import QGraphicsOpacityEffect
                eff = QGraphicsOpacityEffect(icon_lbl)
                eff.setOpacity(1.0 if is_active else 0.25)
                icon_lbl.setGraphicsEffect(eff)
                # İsim rengi
                name_lbl.setStyleSheet(
                    f"color:{'#ffffff' if is_active else TDIM.name()};"
                    f"font-family:'Segoe UI';font-size:7px;font-weight:{'700' if is_active else '400'};"
                    f"background:transparent;"
                )
                # Arka plan highlight
                col.setStyleSheet(
                    f"background:{'rgba(255,255,255,18)' if is_active else 'transparent'};"
                    f"border-radius:4px;"
                )

        def update_power(atk, def_, sta):
            upd_atk(max(0, min(20, atk)))
            upd_def(max(0, min(20, def_)))
            upd_sta(max(0, min(20, sta)))
            _refresh_type(atk, def_, sta)

        # Başlangıç durumu (0,0,0)
        _refresh_type(0, 0, 0)

    v.addStretch()
    return w, update_weight, update_power



# ══════════════════════════════════════════════════════════════
# FACE BOLT  — STL embed + 3D görünüm + texture panel
# ══════════════════════════════════════════════════════════════
import zlib, base64 as _b64

def _load_face_bolt_tris():
    """Gömülü STL'yi çözer, (normal, v1, v2, v3) listesi döndürür."""
    import struct
    raw = zlib.decompress(_b64.b64decode(_FACE_BOLT_B64))
    count = struct.unpack_from('<I', raw, 80)[0]
    tris  = []
    off   = 84
    for _ in range(count):
        n  = struct.unpack_from('<fff', raw, off);     off += 12
        v1 = struct.unpack_from('<fff', raw, off);     off += 12
        v2 = struct.unpack_from('<fff', raw, off);     off += 12
        v3 = struct.unpack_from('<fff', raw, off);     off += 12
        off += 2
        tris.append((n, v1, v2, v3))
    return tris

_FB_TRIS_CACHE = None
def _face_bolt_tris():
    global _FB_TRIS_CACHE
    if _FB_TRIS_CACHE is None:
        _FB_TRIS_CACHE = _load_face_bolt_tris()
    return _FB_TRIS_CACHE

# ── Top-face hexagon UV mapping yardımcıları ─────────────────
# STL: Z=0 tabanında nz=-1 (dışa bakan hexagon yüzeyi).
# Render'da parça Z ekseni çevrilerek hexagon öne/yukarı gelir.
_FB_HEX_Z_MAX = 0.5    # hexagon üçgenlerinin max z_avg eşiği (Z=0 tabanı)
_FB_HEX_NZ    = 0.95   # hexagon normal |Z| minimum (nz<-0.95)
_FB_HEX_CX   =  0.0    # hexagon merkez X
_FB_HEX_CY   =  0.0    # hexagon merkez Y
_FB_HEX_R    =  7.16   # hexagon circumradius (mm)
_FB_TEX_PAD  =  0.04   # kenar boşluğu oranı
_FB_TOTAL_H  = 13.226  # parça toplam yüksekliği

def _fb_uv(vx: float, vy: float) -> tuple[float, float]:
    """Hexagon vertex'ini [0,1] UV'ye çevirir."""
    half = _FB_HEX_R * (1.0 + _FB_TEX_PAD)
    u = (vx - _FB_HEX_CX + half) / (2.0 * half)
    v = (vy - _FB_HEX_CY + half) / (2.0 * half)
    return u, v


# ── FaceBoltView ─────────────────────────────────────────────
class FaceBoltView(GLMeshView):
    """Face Bolt 3D görünümü — STL render + üst yüze texture. OpenGL backend."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(260, 260)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._rx, self._ry = 20.0, 30.0
        self._texture    = None   # QImage (panel tarafından set edilir)
        self._body_color = None   # None = metalik gri
        # Texture shader + GL objeler
        self._tex_prog   = None
        self._tex_vao    = None
        self._tex_vbo    = None
        self._tex_id     = None   # OpenGL texture ID
        self._tex_n_verts = 0

    def _on_tick(self):
        self._spin_angle += 0.6
        self.update()

    def set_texture(self, qimage):
        self._texture = qimage
        self._tex_dirty = True
        # Eski texture ID'yi sil — paintGL'de yeniden oluşturulacak
        if self._tex_id is not None:
            try:
                self.makeCurrent()
                gl.glDeleteTextures(1, [self._tex_id])
            except Exception:
                pass
            self._tex_id = None
        self.invalidate_mesh()
        self.update()

    def set_body_color(self, color):
        self._body_color = color
        self.invalidate_mesh()

    def _z_flip(self):
        return True   # hexagon öne gelsin

    def _pre_spin_z(self):
        return True   # Z ekseni etrafında spin

    def _view_scale(self):
        return 1.0 / (_FB_HEX_R * 2.8)

    def _center_offset(self):
        return (0.0, 0.0, _FB_TOTAL_H / 2.0)

    def initializeGL(self):
        """Ana + texture shader'larını başlat."""
        super().initializeGL()
        if not _HAS_OPENGL:
            return
        try:
            # Texture shader programı
            self._tex_prog = QOpenGLShaderProgram(self)
            self._tex_prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Vertex,   _GL_TEX_VERT_SRC)
            self._tex_prog.addShaderFromSourceCode(QOpenGLShader.ShaderTypeBit.Fragment, _GL_TEX_FRAG_SRC)
            self._tex_prog.link()
            self._tex_vao = QOpenGLVertexArrayObject(self)
            self._tex_vao.create()
            self._tex_vbo = QOpenGLBuffer(QOpenGLBuffer.Type.VertexBuffer)
            self._tex_vbo.create()
            self._tex_vbo.setUsagePattern(QOpenGLBuffer.UsagePattern.DynamicDraw)
            self._tex_dirty = True
        except Exception as e:
            print(f"[GL ERROR] FaceBoltView tex init: {e}")

    def _get_groups(self):
        """Sadece gövde (non-top) triangles — texture grubunu ayrı VBO'da tutuyoruz."""
        tris = _face_bolt_tris()
        other_tris = []
        for t in tris:
            if not (t[0][2] < -_FB_HEX_NZ and (t[1][2]+t[2][2]+t[3][2])/3 < _FB_HEX_Z_MAX):
                other_tris.append(t)
        amb, dif = (0.22, 0.78) if _DARK else (0.42, 0.58)
        if self._body_color is not None:
            body_col = (self._body_color.redF(), self._body_color.greenF(), self._body_color.blueF())
        else:
            body_col = (175/255, 177/255, 187/255) if _DARK else (210/255, 210/255, 218/255)
        return [(other_tris, body_col, amb, dif)]

    def _upload_tex_mesh(self):
        """Top face üçgenlerini UV coords ile texture VBO'ya yükle."""
        if self._tex_prog is None:
            return
        try:
            self.makeCurrent()
            tris = _face_bolt_tris()
            top_tris = [t for t in tris
                        if t[0][2] < -_FB_HEX_NZ and (t[1][2]+t[2][2]+t[3][2])/3 < _FB_HEX_Z_MAX]
            if not top_tris:
                self._tex_n_verts = 0
                return
            # Format: [x,y,z, nx,ny,nz, u,v] × 3 verts × N tris
            arr = np.empty((len(top_tris)*3, 8), dtype=np.float32)
            for i, (n, v1, v2, v3) in enumerate(top_tris):
                base = i * 3
                for j, v in enumerate([v1, v2, v3]):
                    u, uv = _fb_uv(v[0], v[1])
                    arr[base+j, :3] = v
                    arr[base+j, 3:6] = n
                    arr[base+j, 6] = u
                    arr[base+j, 7] = uv
            raw = arr.tobytes()
            stride = 8 * 4
            self._tex_vao.bind()
            self._tex_vbo.bind()
            self._tex_vbo.allocate(raw, len(raw))
            self._tex_prog.bind()
            self._tex_prog.enableAttributeArray(0)
            self._tex_prog.setAttributeBuffer(0, gl.GL_FLOAT, 0,   3, stride)  # pos
            self._tex_prog.enableAttributeArray(1)
            self._tex_prog.setAttributeBuffer(1, gl.GL_FLOAT, 3*4, 3, stride)  # norm
            self._tex_prog.enableAttributeArray(2)
            self._tex_prog.setAttributeBuffer(2, gl.GL_FLOAT, 6*4, 2, stride)  # uv
            self._tex_prog.release()
            self._tex_vbo.release()
            self._tex_vao.release()
            self._tex_n_verts = len(top_tris) * 3
            self._tex_dirty = False
        except Exception as e:
            print(f"[GL ERROR] _upload_tex_mesh: {e}")
            import traceback; traceback.print_exc()

    def _upload_gl_texture(self):
        """QImage'i OpenGL texture'a yükle."""
        if self._texture is None:
            return
        img = self._texture.convertToFormat(self._texture.Format.Format_RGBA8888)
        w, h = img.width(), img.height()
        if self._tex_id is not None:
            gl.glDeleteTextures(1, [self._tex_id])
        tex_ids = gl.glGenTextures(1)
        self._tex_id = int(tex_ids) if not hasattr(tex_ids, '__len__') else int(tex_ids[0])
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        import ctypes
        ptr = img.bits()
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, w, h, 0,
                        gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, ptr)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def paintGL(self):
        """Ana gövde + texture hexagon çiz."""
        # Önce gövdeyi normal shader ile çiz
        super().paintGL()

        # Texture yoksa sadece metalik renk göster
        if self._tex_prog is None or self._tex_n_verts == 0 and not getattr(self, '_tex_dirty', False):
            return

        try:
            if getattr(self, '_tex_dirty', True):
                self._upload_tex_mesh()

            if self._tex_n_verts == 0:
                # Top face yok — metalik rengi ana shader zaten çizdi
                return

            # Texture yükle/güncelle
            if self._texture is not None and self._tex_id is None:
                self._upload_gl_texture()

            w, h = self.width(), self.height()
            aspect = w / max(h, 1)
            scale = self._view_scale() * self._zoom
            mvp, norm_mat = _make_mvp(
                self._rx, self._ry, self._spin_angle, scale, aspect,
                center_offset=self._center_offset(),
                z_flip=self._z_flip(), pre_spin_z=self._pre_spin_z(),
            )
            LX, LY, LZ = 0.45, 0.75, 0.55
            ll = math.sqrt(LX*LX+LY*LY+LZ*LZ)
            light_dir = np.array([LX/ll, LY/ll, LZ/ll], dtype=np.float32)

            self._tex_prog.bind()
            self._tex_vao.bind()
            prog_id = self._tex_prog.programId()
            mvp_flat = mvp.flatten().astype(np.float32)
            nm_flat  = norm_mat.flatten().astype(np.float32)
            gl.glUniformMatrix4fv(gl.glGetUniformLocation(prog_id, b"uMVP"),     1, gl.GL_TRUE, mvp_flat)
            gl.glUniformMatrix3fv(gl.glGetUniformLocation(prog_id, b"uNormMat"), 1, gl.GL_TRUE, nm_flat)
            gl.glUniform3f(gl.glGetUniformLocation(prog_id, b"uLightDir"),
                           float(light_dir[0]), float(light_dir[1]), float(light_dir[2]))
            amb, dif = (0.22, 0.78) if _DARK else (0.42, 0.58)
            gl.glUniform1f(gl.glGetUniformLocation(prog_id, b"uAmbient"), amb)
            gl.glUniform1f(gl.glGetUniformLocation(prog_id, b"uDiffuse"), dif)

            if self._texture is not None and self._tex_id is not None:
                gl.glActiveTexture(gl.GL_TEXTURE0)
                gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)
                gl.glUniform1i(gl.glGetUniformLocation(prog_id, b"uTex"), 0)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, self._tex_n_verts)
                gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
            else:
                # Texture yok — metalik gri düz renk
                self._tex_vao.release()
                self._tex_prog.release()
                return

            self._tex_vao.release()
            self._tex_prog.release()
        except Exception as e:
            import traceback
            print(f"[GL ERROR] FaceBoltView.paintGL tex: {e}")
            traceback.print_exc()

    def _hint_text(self):
        return tr("drag_hint2")
# ── QImage ↔ base64 PNG yardımcıları ────────────────────────
def _qimage_to_b64(img) -> str:
    """QImage'i PNG olarak base64 string'e çevirir."""
    from PySide6.QtCore import QBuffer, QIODevice
    import base64
    buf = QBuffer()
    buf.open(QIODevice.OpenModeFlag.WriteOnly)
    img.save(buf, "PNG")
    buf.close()
    return base64.b64encode(buf.data().data()).decode("ascii")

def _b64_to_qimage(b64: str):
    """base64 string'ten QImage döndürür."""
    from PySide6.QtGui import QImage
    import base64
    try:
        raw = base64.b64decode(b64)
        img = QImage()
        img.loadFromData(bytes(raw), "PNG")
        return img
    except Exception:
        return None


# ── FaceBoltPanel ─────────────────────────────────────────────
class FaceBoltPanel(QWidget):
    """Sağ panel: Face Bolt görsel (texture) yükleme + renk."""

    def __init__(self, view: FaceBoltView, parent=None):
        super().__init__(parent)
        self._view      = view
        self._dirty_cb  = None
        self._img_data  = ""   # base64 PNG string
        self._color     = None # None = metalik gri varsayılan

        ss_btn = (
            f"QPushButton{{background:{PANEL.name()};color:{TPRI.name()};"
            f"border:1px solid {BORDER.name()};border-radius:3px;"
            f"font-family:'Segoe UI';font-size:9px;padding:4px 8px;}}"
            f"QPushButton:hover{{background:{PHOVER.name()};border-color:{ACCENT.name()};}}"
        )
        ss_lbl = f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;background:transparent;"
        ss_val = f"color:{TPRI.name()};font-family:'Segoe UI';font-size:9px;background:transparent;"

        v = QVBoxLayout(self)
        v.setContentsMargins(10, 10, 10, 10)
        v.setSpacing(8)

        # ── Gövde rengi ───────────────────────────────────────
        clbl = QLabel(tr("body_color"))
        clbl.setStyleSheet(ss_lbl); v.addWidget(clbl)

        color_row = QHBoxLayout(); color_row.setSpacing(5)
        self._color_btn = QPushButton("🎨 " + (tr("pick_color")))
        self._color_btn.setFixedHeight(28)
        self._color_btn.setStyleSheet(self._color_btn_ss())
        self._color_btn.clicked.connect(self._pick_color)
        color_row.addWidget(self._color_btn, 1)
        self._hex_input = QLineEdit("")
        self._hex_input.setFixedWidth(72); self._hex_input.setMaxLength(7)
        self._hex_input.setPlaceholderText("#rrggbb")
        self._hex_input.setStyleSheet(
            f"QLineEdit{{background:{PANEL.name()};color:{TPRI.name()};"
            f"border:1px solid {BORDER.name()};border-radius:3px;"
            f"font-family:'Consolas','Courier New';font-size:9px;padding:2px 4px;}}"
            f"QLineEdit:focus{{border-color:{ACCENT.name()};}}"
        )
        self._hex_input.editingFinished.connect(self._hex_changed)
        color_row.addWidget(self._hex_input)
        v.addLayout(color_row)

        reset_btn = QPushButton("↺  " + (tr("reset_metal")))
        reset_btn.setStyleSheet(ss_btn); reset_btn.clicked.connect(self._reset_color)
        v.addWidget(reset_btn)

        presets_fb = ["#cc2222","#cc7722","#2255cc","#22aa44","#8822cc","#111111","#dddddd","#c8922a"]
        pgrid = QGridLayout(); pgrid.setSpacing(4)
        for i, hx in enumerate(presets_fb):
            pb = QPushButton(); pb.setFixedSize(20,20); pb.setToolTip(hx)
            pb.setStyleSheet(f"background:{hx};border:1px solid {BORDER.name()};border-radius:3px;")
            pb.clicked.connect(lambda _=False, c=hx: self._set_color(QColor(c)))
            pgrid.addWidget(pb, i//4, i%4)
        v.addLayout(pgrid)

        v.addWidget(hdiv())

        # Önizleme kutusu
        self._preview = QLabel()
        self._preview.setFixedSize(160, 160)
        self._preview.setAlignment(Qt.AlignCenter)
        self._preview.setStyleSheet(
            f"background:{CANVAS.name()};"
            f"border:1px solid {BORDER.name()};"
            f"border-radius:4px;"
        )
        self._preview.setText("—")
        self._preview.setStyleSheet(
            self._preview.styleSheet() +
            f"color:{TDIM.name()};font-size:11px;"
        )

        ph_row = QHBoxLayout()
        ph_row.addStretch()
        ph_row.addWidget(self._preview)
        ph_row.addStretch()
        v.addLayout(ph_row)

        # Yükle butonu
        load_btn = QPushButton(
            tr("load_image") if "load_image" in _TR.get(_LANG,{}) else
            (tr("load_image"))
        )
        load_btn.setStyleSheet(ss_btn)
        load_btn.clicked.connect(self._load_image)
        v.addWidget(load_btn)

        # Temizle butonu
        clear_btn = QPushButton(
            tr("remove_image")
        )
        clear_btn.setStyleSheet(ss_btn)
        clear_btn.clicked.connect(self._clear_image)
        v.addWidget(clear_btn)

        v.addWidget(hdiv())

        # Bilgi etiketi
        info = QLabel(tr("tex_info"))
        info.setStyleSheet(ss_lbl)
        info.setWordWrap(True)
        v.addWidget(info)

        # Dosya adı
        self._fname_lbl = QLabel("")
        self._fname_lbl.setStyleSheet(ss_val)
        self._fname_lbl.setWordWrap(True)
        v.addWidget(self._fname_lbl)

        v.addWidget(hdiv())
        # ── Ağırlık (sabit) ───────────────────────────────────
        wrow = QWidget(); wrow.setStyleSheet("background:transparent;")
        wlay = QHBoxLayout(wrow); wlay.setContentsMargins(0,2,0,2); wlay.setSpacing(4)
        wlbl = QLabel(tr("weight"))
        wlbl.setStyleSheet(ss_lbl)
        wval = QLabel("1.0 g")
        wval.setStyleSheet(f"color:{TPRI.name()};font-family:'Segoe UI';font-size:10px;font-weight:700;background:transparent;")
        wlay.addWidget(wlbl); wlay.addStretch(); wlay.addWidget(wval)
        v.addWidget(wrow)

        self._weight     = 1.0   # sabit Face Bolt ağırlığı (g)
        self._weight_cb  = None   # EditorWindow tarafından set edilir

        v.addStretch()

    def set_weight_callback(self, cb):
        """Toplam ağırlık güncellemesi için callback."""
        self._weight_cb = cb

    def get_weight(self) -> float:
        return self._weight

    def set_dirty_callback(self, cb):
        self._dirty_cb = cb

    # ── renk yardımcıları ────────────────────────────────────
    def _color_btn_ss(self) -> str:
        c = self._color
        left = c.name() if c else "#888888"
        return (f"background:{PANEL.name()};color:{TPRI.name()};"
                f"border:1px solid {BORDER.name()};"
                f"border-left:5px solid {left};"
                f"border-radius:4px;font-family:'Segoe UI';font-size:9px;"
                f"text-align:left;padding-left:6px;")

    def _pick_color(self):
        init = self._color if self._color else QColor("#aaaaaa")
        c = QColorDialog.getColor(init, self, tr("fb_color"))
        if c.isValid(): self._set_color(c)

    def _set_color(self, c: QColor):
        self._color = c
        self._color_btn.setStyleSheet(self._color_btn_ss())
        self._hex_input.setText(c.name())
        self._view.set_body_color(c)
        if self._dirty_cb: self._dirty_cb()

    def _reset_color(self):
        self._color = None
        self._color_btn.setStyleSheet(self._color_btn_ss())
        self._hex_input.setText("")
        self._view.set_body_color(None)
        if self._dirty_cb: self._dirty_cb()

    def _hex_changed(self):
        txt = self._hex_input.text().strip()
        if not txt: self._reset_color(); return
        if not txt.startswith("#"): txt = "#" + txt
        c = QColor(txt)
        if c.isValid(): self._set_color(c)
        else: self._hex_input.setText(self._color.name() if self._color else "")

    def _load_image(self):
        from PySide6.QtGui import QImage
        path, _ = QFileDialog.getOpenFileName(
            self,
            tr("select_image"),
            "",
            "Görseller (*.png *.jpg *.jpeg *.bmp *.webp);;Tüm Dosyalar (*)"
        )
        if not path:
            return
        img = QImage(path)
        if img.isNull():
            return
        self._fname_lbl.setText(Path(path).name)

        # Format dönüştür + kare crop
        img = img.convertToFormat(QImage.Format.Format_ARGB32)
        sz = min(img.width(), img.height())
        img = img.copy((img.width()-sz)//2, (img.height()-sz)//2, sz, sz)

        # 512×512'ye düşür — hem texture hem kayıt için
        img = img.scaled(512, 512, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self._img_data = _qimage_to_b64(img)   # base64 string olarak sakla

        # Önizleme
        from PySide6.QtGui import QPixmap
        pm = QPixmap.fromImage(img.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self._preview.setPixmap(pm)
        self._preview.setText("")

        # View'e aktar
        self._view.set_texture(img)

        if self._dirty_cb:
            self._dirty_cb()

    def _clear_image(self):
        from PySide6.QtGui import QPixmap
        self._img_data = ""
        self._fname_lbl.setText("")
        self._preview.setPixmap(QPixmap())
        self._preview.setText("—")
        self._view.set_texture(None)
        if self._dirty_cb:
            self._dirty_cb()

    def load_from(self, data: dict):
        """Dosyadan face_image_data (base64) ve face_bolt_color alanlarını yükle."""
        b64 = data.get("face_image_data", "")
        if b64:
            img = _b64_to_qimage(b64)
            if img and not img.isNull():
                self._img_data = b64
                from PySide6.QtGui import QPixmap
                pm = QPixmap.fromImage(img.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self._preview.setPixmap(pm)
                self._preview.setText("")
                self._fname_lbl.setText(tr("embedded_img"))
                self._view.set_texture(img)
        co = data.get("face_bolt_color", "")
        if co:
            c = QColor(co)
            if c.isValid():
                self._color = c
                self._color_btn.setStyleSheet(self._color_btn_ss())
                self._hex_input.setText(c.name())
                self._view.set_body_color(c)

    def get_data(self) -> dict:
        d = {"face_image_data": self._img_data}
        if self._color:
            d["face_bolt_color"] = self._color.name()
        return d


# ══════════════════════════════════════════════════════════════
# ENERGY RING — klasör tarama + OBJ yükleme + 3D görünüm
# ══════════════════════════════════════════════════════════════

def _scan_energy_rings() -> list[dict]:
    """
    <proje_kökü>/energy-rings/ altındaki geçerli ring klasörlerini tarar.
    Geçerli klasör: ring.obj VE icon.png VE performancedata.toml içermeli.
    [{"name", "obj", "icon", "toml", "weight", "attack", "defense", "stamina"}, ...]
    """
    base = Path(__file__).parent / "energy-rings"
    if not base.exists():
        return []
    rings = []
    for d in sorted(base.iterdir()):
        if not d.is_dir():
            continue
        obj_f  = d / "ring.obj"
        icon_f = d / "icon.png"
        toml_f = d / "performancedata.toml"
        if obj_f.exists() and icon_f.exists() and toml_f.exists():
            try:
                pdata = _toml_parse(toml_f.read_text(encoding="utf-8", errors="replace"))
            except Exception:
                pdata = {}
            rings.append({
                "name":    d.name,
                "obj":     obj_f,
                "icon":    icon_f,
                "toml":    toml_f,
                "weight":  float(pdata.get("weight",  0.0)),
                "attack":  int(pdata.get("attack",    0)),
                "defense": int(pdata.get("defense",   0)),
                "stamina": int(pdata.get("stamina",   0)),
            })
    return rings

def _load_obj(path: Path) -> list[tuple]:
    """
    Minimal OBJ parser — sadece v ve f satırları.
    [(v1,v2,v3), ...] üçgen listesi döndürür (her v: (x,y,z) tuple).
    Quad'ları iki üçgene böler. Negatif indeksleri destekler.
    """
    verts = []
    tris  = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("v "):
                parts = line.split()
                verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith("f "):
                parts = line.split()[1:]
                # "v/vt/vn" → sadece vertex index
                idx = []
                for p in parts:
                    i = int(p.split("/")[0])
                    idx.append(i - 1 if i > 0 else len(verts) + i)
                # Fan triangulation
                for k in range(1, len(idx) - 1):
                    tris.append((verts[idx[0]], verts[idx[k]], verts[idx[k+1]]))
    except Exception:
        pass
    return tris

def _obj_yup_to_zup(tris: list[tuple]) -> list[tuple]:
    """OBJ Y-up koordinatlarını Z-up'a çevir: (x,y,z) → (x,-z,y).
    Winding order da ters çevrilir (v1↔v3) ki normaller doğru kalsın.
    Dönüşüm sonrası X,Y merkezi sıfırlanır."""
    def cv(v): return (v[0], -v[2], v[1])
    converted = [(cv(a), cv(c), cv(b)) for a,b,c in tris]   # v1↔v3 swap
    # XY merkezini sıfırla
    all_v = [v for t in converted for v in t]
    cx = (min(v[0] for v in all_v) + max(v[0] for v in all_v)) / 2
    cy = (min(v[1] for v in all_v) + max(v[1] for v in all_v)) / 2
    return [((a[0]-cx, a[1]-cy, a[2]),
             (b[0]-cx, b[1]-cy, b[2]),
             (c[0]-cx, c[1]-cy, c[2])) for a,b,c in converted]

def _normalize_obj_tris(tris: list[tuple]) -> list[tuple]:
    """OBJ üçgenlerini merkeze al ve normalize et (max extent = 1)."""
    if not tris:
        return tris
    all_v = [v for t in tris for v in t]
    xs = [v[0] for v in all_v]
    ys = [v[1] for v in all_v]
    zs = [v[2] for v in all_v]
    cx = (min(xs)+max(xs))/2
    cy = (min(ys)+max(ys))/2
    cz = (min(zs)+max(zs))/2
    ext = max(max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)) or 1.0
    scale = 2.0 / ext
    def n(v): return ((v[0]-cx)*scale, (v[1]-cy)*scale, (v[2]-cz)*scale)
    return [(n(a), n(b), n(c)) for a,b,c in tris]

def _compute_normals(tris):
    """Her üçgen için yüzey normalini hesapla."""
    import math
    result = []
    for v1,v2,v3 in tris:
        e1 = (v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2])
        e2 = (v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2])
        nx = e1[1]*e2[2] - e1[2]*e2[1]
        ny = e1[2]*e2[0] - e1[0]*e2[2]
        nz = e1[0]*e2[1] - e1[1]*e2[0]
        ln = math.sqrt(nx*nx+ny*ny+nz*nz)
        if ln > 1e-9:
            result.append(((nx/ln, ny/ln, nz/ln), v1, v2, v3))
    return result


# ── EnergyRingView ────────────────────────────────────────────
class EnergyRingView(GLMeshView):
    """Energy Ring 3D görünümü — OBJ render + renk. OpenGL backend."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._rx, self._ry = 20.0, 30.0
        self._tris     = []
        self._raw_tris = []   # gerçek mm boyutları (preview için)
        self._color = QColor("#4488cc")

    def set_ring(self, tris_with_normals: list, raw_mm_tris: list = None):
        self._tris    = tris_with_normals   # normalize [-1,+1] — kendi view için
        self._raw_tris = raw_mm_tris or []  # gerçek mm — preview için
        self.invalidate_mesh()

    def set_color(self, color: QColor):
        self._color = color
        self.invalidate_mesh()

    def _tick(self):
        self._spin_angle += 0.5
        self.update()

    def _view_scale(self):
        return 1.0 / 2.6

    def _get_groups(self):
        if not self._tris:
            return []
        r = self._color.redF()
        g = self._color.greenF()
        b = self._color.blueF()
        amb, dif = (0.25, 0.75) if _DARK else (0.45, 0.55)
        return [(self._tris, (r, g, b), amb, dif)]
# ── EnergyRingPanel ───────────────────────────────────────────
class EnergyRingPanel(QWidget):
    """Sağ panel: Energy Ring seçimi + renk."""

    def __init__(self, view: EnergyRingView, parent=None):
        super().__init__(parent)
        self._view      = view
        self._dirty_cb  = None
        self._rings     = _scan_energy_rings()   # [{"name","obj","icon"}, ...]
        self._selected  = ""    # seçili ring klasör adı
        self._color     = QColor("#4488cc")
        self._obj_cache : dict[str, list] = {}   # name → tris_with_normals

        v = QVBoxLayout(self)
        v.setContentsMargins(8, 8, 8, 8)
        v.setSpacing(6)

        ss_lbl = f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;background:transparent;"

        # ── Ring listesi ──────────────────────────────────────
        lbl = QLabel(tr("select_ring"))
        lbl.setStyleSheet(ss_lbl)
        v.addWidget(lbl)

        # Scroll alanı — icon grid
        sc = QScrollArea(); sc.setWidgetResizable(True); sc.setFixedHeight(180)
        sc.setStyleSheet(
            f"QScrollArea{{border:1px solid {BORDER.name()};background:{BG.name()};border-radius:3px;}}"
            f"QScrollBar:vertical{{background:{BG.name()};width:5px;}}"
            f"QScrollBar::handle:vertical{{background:{BORDER.name()};border-radius:2px;min-height:20px;}}"
            f"QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}"
        )
        grid_w = QWidget(); grid_w.setStyleSheet(f"background:{BG.name()};")
        self._grid = QGridLayout(grid_w)
        self._grid.setContentsMargins(4,4,4,4); self._grid.setSpacing(4)
        self._icon_btns: dict[str, QPushButton] = {}
        self._populate_grid()
        sc.setWidget(grid_w)
        v.addWidget(sc)

        # Seçili ring adı
        self._sel_lbl = QLabel("—")
        self._sel_lbl.setStyleSheet(f"color:{TPRI.name()};font-family:'Segoe UI';font-size:9px;background:transparent;")
        v.addWidget(self._sel_lbl)

        v.addWidget(hdiv())

        # ── Renk seçici ──────────────────────────────────────
        clbl = QLabel(tr("color"))
        clbl.setStyleSheet(ss_lbl)
        v.addWidget(clbl)

        color_row = QHBoxLayout(); color_row.setSpacing(5)

        # Renk önizleme + tıklayınca dialog
        self._color_btn = QPushButton()
        self._color_btn.setFixedSize(32, 32)
        self._color_btn.setStyleSheet(self._color_btn_ss())
        self._color_btn.clicked.connect(self._pick_color)
        color_row.addWidget(self._color_btn)

        # Hazır renk presetleri
        presets = [
            ("#cc2222",""), ("#cc7722",""), ("#cccc22",""),
            ("#22aa44",""), ("#2255cc",""), ("#8822cc",""),
            ("#cccccc",""), ("#333333",""),
        ]
        preset_grid = QGridLayout(); preset_grid.setSpacing(3)
        for i,(hex_c,_) in enumerate(presets):
            pb = QPushButton()
            pb.setFixedSize(16,16)
            pb.setStyleSheet(f"background:{hex_c};border:1px solid {BORDER.name()};border-radius:2px;")
            pb.clicked.connect(lambda _=False, c=hex_c: self._set_color(QColor(c)))
            preset_grid.addWidget(pb, i//4, i%4)
        color_row.addLayout(preset_grid)
        color_row.addStretch()
        v.addLayout(color_row)

        v.addWidget(hdiv())

        # ── Ağırlık + performans (TOML'dan) ──────────────────
        ss_stat_lbl = f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;background:transparent;"
        wrow = QWidget(); wrow.setStyleSheet("background:transparent;")
        wlay = QHBoxLayout(wrow); wlay.setContentsMargins(0,2,0,2); wlay.setSpacing(4)
        wlbl = QLabel(tr("weight")); wlbl.setStyleSheet(ss_stat_lbl)
        self._er_weight_lbl = QLabel("—")
        self._er_weight_lbl.setStyleSheet(f"color:{TPRI.name()};font-family:'Segoe UI';font-size:10px;font-weight:700;background:transparent;")
        wlay.addWidget(wlbl); wlay.addStretch(); wlay.addWidget(self._er_weight_lbl)
        v.addWidget(wrow)

        sb_atk, self._upd_atk = stat_bar_live(tr("attack"),    ATK, max_val=5)
        sb_def, self._upd_def = stat_bar_live(tr("defense"),   DEF, max_val=5)
        sb_sta, self._upd_sta = stat_bar_live(tr("stamina"), STA, max_val=5)
        v.addWidget(sb_atk); v.addWidget(sb_def); v.addWidget(sb_sta)

        self._weight_cb = None   # EditorWindow tarafından set edilir

        v.addStretch()

        # Boş mesaj
        if not self._rings:
            empty = QLabel(
                tr("er_folder_empty")
            )
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet(f"color:{TDIM.name()};font-family:'Segoe UI';font-size:8px;background:transparent;")
            v.insertWidget(1, empty)

    def _color_btn_ss(self) -> str:
        return (f"background:{self._color.name()};"
                f"border:2px solid {BORDER.name()};border-radius:4px;")

    def _populate_grid(self):
        from PySide6.QtGui import QPixmap, QImage
        for i, ring in enumerate(self._rings):
            btn = QPushButton()
            btn.setFixedSize(52, 52)
            btn.setToolTip(ring["name"])
            # icon.png yükle — kare fill (aspect ignored, sığdır)
            img = QImage(str(ring["icon"]))
            if not img.isNull():
                img = img.scaled(48, 48, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                pm = QPixmap.fromImage(img)
                btn.setIcon(pm)
                btn.setIconSize(pm.size())
            btn.setStyleSheet(self._btn_ss(False))
            btn.clicked.connect(lambda _=False, name=ring["name"]: self._select(name))
            self._grid.addWidget(btn, i//3, i%3)
            self._icon_btns[ring["name"]] = btn

    def _btn_ss(self, selected: bool) -> str:
        if selected:
            return (f"background:{ACCENT.name()};border:2px solid {ACCENT.name()};"
                    f"border-radius:4px;padding:1px;")
        return (f"background:{PANEL.name()};border:1px solid {BORDER.name()};"
                f"border-radius:4px;padding:1px;"
                f"QPushButton:hover{{border-color:{ACCENT.name()};}}")

    def _select(self, name: str):
        # Eski seçimi temizle
        if self._selected and self._selected in self._icon_btns:
            self._icon_btns[self._selected].setStyleSheet(self._btn_ss(False))
        self._selected = name
        if name in self._icon_btns:
            self._icon_btns[name].setStyleSheet(self._btn_ss(True))
        self._sel_lbl.setText(name)
        # OBJ yükle (cache)
        if name not in self._obj_cache:
            ring = next((r for r in self._rings if r["name"]==name), None)
            if ring:
                raw = _load_obj(ring["obj"])
                norm = _normalize_obj_tris(raw)
                raw_zup = _obj_yup_to_zup(raw)
                self._obj_cache[name] = {
                    "norm": _compute_normals(norm),
                    "raw":  _compute_normals(raw_zup),
                }
        cached = self._obj_cache.get(name, {})
        self._view.set_ring(cached.get("norm", []), cached.get("raw", []))
        # Performans verilerini güncelle
        ring_data = next((r for r in self._rings if r["name"]==name), None)
        if ring_data:
            w = ring_data.get("weight", 0.0)
            self._er_weight_lbl.setText(f"{w:.1f} g")
            self._cached_atk = ring_data.get("attack",  0)
            self._cached_def = ring_data.get("defense", 0)
            self._cached_sta = ring_data.get("stamina", 0)
            self._upd_atk(self._cached_atk)
            self._upd_def(self._cached_def)
            self._upd_sta(self._cached_sta)
        if self._weight_cb:
            self._weight_cb()
        if self._dirty_cb:
            self._dirty_cb()

    def set_weight_callback(self, cb):
        self._weight_cb = cb

    def get_weight(self) -> float:
        ring_data = next((r for r in self._rings if r["name"]==self._selected), None)
        return ring_data["weight"] if ring_data else 0.0

    def _pick_color(self):
        c = QColorDialog.getColor(self._color, self, tr("pick_color"))
        if c.isValid():
            self._set_color(c)

    def _set_color(self, c: QColor):
        self._color = c
        self._color_btn.setStyleSheet(self._color_btn_ss())
        self._view.set_color(c)
        if self._dirty_cb:
            self._dirty_cb()

    def set_dirty_callback(self, cb):
        self._dirty_cb = cb

    def load_from(self, data: dict):
        ring_name = data.get("energy_ring", "")
        color_hex = data.get("energy_ring_color", "")
        if color_hex:
            self._set_color(QColor(color_hex))
        if ring_name:
            self._select(ring_name)

    def get_data(self) -> dict:
        return {
            "energy_ring":       self._selected,
            "energy_ring_color": self._color.name(),
        }


# ══════════════════════════════════════════════════════════════
# FUSION WHEEL — hibrit: tinker.obj temel + prosedürel kanatlar
# ══════════════════════════════════════════════════════════════

# ── Sabitler (tinker.obj'den ölçülen) ────────────────────────
_FW_OBJ_R      = 17.0045   # dış yarıçap (mm)
_FW_OBJ_H_BOT  = 0.0       # alt Z
_FW_OBJ_H_TOP  = 6.5       # üst Z
_FW_BLADE_R    = _FW_OBJ_R - 0.5   # kanat iç çemberi = 16.5045 mm
_FW_OBJ_CX     = 0.004     # merkez X offset
_FW_OBJ_CY     = -0.004    # merkez Y offset


def _load_tinker_tris():
    """
    Gömülü tinker.obj'yi çözer.
    Döner: [(normal, v1, v2, v3), ...] — EnergyRingView formatı.
    Koordinatlar mm, merkez ~(0,0), Z=0 alt Z=6.5 üst.
    """
    import zlib, base64 as _b64, math

    raw  = zlib.decompress(_b64.b64decode("".join(_TINKER_OBJ_B64)))
    text = raw.decode("utf-8", errors="replace")

    verts = []
    tris  = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("v "):
            p = line.split()
            verts.append((float(p[1]) - _FW_OBJ_CX,
                          float(p[2]) - _FW_OBJ_CY,
                          float(p[3])))
        elif line.startswith("f "):
            idx = [int(p.split("/")[0]) - 1 for p in line.split()[1:]]
            # fan triangulation (n-gon → n-2 üçgen)
            for i in range(1, len(idx) - 1):
                tris.append((idx[0], idx[i], idx[i + 1]))

    result = []
    for i0, i1, i2 in tris:
        v0, v1, v2 = verts[i0], verts[i1], verts[i2]
        ax = v1[0]-v0[0]; ay = v1[1]-v0[1]; az = v1[2]-v0[2]
        bx = v2[0]-v0[0]; by = v2[1]-v0[1]; bz = v2[2]-v0[2]
        nx = ay*bz - az*by
        ny = az*bx - ax*bz
        nz = ax*by - ay*bx
        nl = math.sqrt(nx*nx + ny*ny + nz*nz)
        if nl > 1e-9:
            nx, ny, nz = nx/nl, ny/nl, nz/nl
        result.append(((nx, ny, nz), v0, v1, v2))
    return result


_FW_BASE_CACHE = None

def _tinker_tris():
    global _FW_BASE_CACHE
    if _FW_BASE_CACHE is None:
        _FW_BASE_CACHE = _load_tinker_tris()
    return _FW_BASE_CACHE



def build_blade_tris(
    blade_count:   int   = 3,
    blade_type:    str   = "wing",
    blade_depth:   float = 6.0,    # radyal uzanma (mm)
    taper:         float = 0.0,    # uç incelme 0=sabit, 1=tam sivri
    gap_frac:      float = 0.25,   # kanatlar arası boşluk oranı [0–0.6]
    # wing
    wing_camber:   float = 0.10,
    wing_sweep:    float = 10.0,   # derece
    # spike
    spike_ratio:   float = 0.5,    # taban genişliği / yükseklik oranı
    # flat
    flat_bevel:    float = 0.15,
    # blade
    blade_sweep:   float = 20.0,
    blade_asym:    float = 0.35,   # ön/arka asimetri 0=simetrik
    # ring (blade_count==1)
    ring_taper:    float = None,   # None → taper kullan
    RSEG: int = 22,
    ASEG: int = 10,
) -> list:
    """
    blade_count adet kanat — normal+vertex formatı döner.
    blade_count == 1 → dairesel halka.
    """
    import math

    if blade_count < 1:
        return []

    R_IN   = _FW_BLADE_R
    R_OUT  = _FW_BLADE_R + blade_depth
    Z_BOT  = _FW_OBJ_H_BOT
    Z_TOP  = _FW_OBJ_H_TOP
    Z_H    = Z_TOP - Z_BOT

    tris_raw = []

    def quad(a, b, c, d):
        return [(a, b, c), (a, c, d)]

    def norm_tris(raw_list):
        result = []
        for v0, v1, v2 in raw_list:
            ax=v1[0]-v0[0]; ay=v1[1]-v0[1]; az=v1[2]-v0[2]
            bx=v2[0]-v0[0]; by=v2[1]-v0[1]; bz=v2[2]-v0[2]
            nx=ay*bz-az*by; ny=az*bx-ax*bz; nz=ax*by-ay*bx
            nl=math.sqrt(nx*nx+ny*ny+nz*nz)
            if nl>1e-9: nx,ny,nz=nx/nl,ny/nl,nz/nl
            result.append(((nx,ny,nz), v0, v1, v2))
        return result

    # ── 1 kanat = tam dairesel halka ─────────────────────────
    if blade_count == 1:
        tp = ring_taper if ring_taper is not None else taper
        for i in range(64):
            a0 = math.tau * i     / 64
            a1 = math.tau * (i+1) / 64
            for ri in range(RSEG):
                t0 = ri     / RSEG
                t1 = (ri+1) / RSEG
                r0 = R_IN + t0*(R_OUT-R_IN)
                r1 = R_IN + t1*(R_OUT-R_IN)
                # uç incelme: dışa doğru Z aralığı daralır
                hw0 = Z_H/2 * max(0.02, 1.0 - tp*t0)
                hw1 = Z_H/2 * max(0.02, 1.0 - tp*t1)
                zmid = (Z_BOT+Z_TOP)/2
                def p(r, a, hw): return (r*math.cos(a), r*math.sin(a), zmid+hw)
                def q(r, a, hw): return (r*math.cos(a), r*math.sin(a), zmid-hw)
                # üst yüzey
                tris_raw += quad(p(r0,a0,hw0), p(r0,a1,hw0), p(r1,a1,hw1), p(r1,a0,hw1))
                # alt yüzey
                tris_raw += quad(q(r0,a0,hw0), q(r1,a0,hw1), q(r1,a1,hw1), q(r0,a1,hw0))
                # ön/arka kenar (her segment aynı a için)
                if ri == 0:        # iç kenar kapak
                    tris_raw += quad(p(r0,a0,hw0), q(r0,a0,hw0), q(r0,a1,hw0), p(r0,a1,hw0))
                if ri == RSEG-1:   # dış kenar kapak
                    tris_raw += quad(p(r1,a0,hw1), p(r1,a1,hw1), q(r1,a1,hw1), q(r1,a0,hw1))
        # yan kapak (a0 tarafı — küçük, ama temiz olsun)
        # halka sürekli olduğundan yan kapak yok
        return norm_tris(tris_raw)

    # ── çok kanatlı yapı ─────────────────────────────────────
    gap_frac   = max(0.05, min(0.70, gap_frac))
    span_frac  = 1.0 - gap_frac               # her kanada düşen açı oranı
    ang_each   = math.tau / blade_count
    half_span  = ang_each * span_frac / 2.0   # kanat yarı-açısı

    sweep_rad  = math.radians(wing_sweep  if blade_type=="wing"  else
                              blade_sweep if blade_type=="blade" else 5.0)

    for bi in range(blade_count):
        base_a = bi * ang_each

        # ── nokta üret ───────────────────────────────────────
        pts_top = []
        pts_bot = []

        for ri in range(RSEG+1):
            t = ri / RSEG
            r = R_IN + t*(R_OUT-R_IN)
            ang_off = base_a + t*sweep_rad

            # uç incelme: dışa gittikçe Z aralığı daralır
            hw = Z_H/2 * max(0.02, 1.0 - taper*t)
            zmid = (Z_BOT+Z_TOP)/2

            # Açısal genişlik profili (tip'e göre)
            if blade_type == "spike":
                # üçgen profil: içte geniş, dışta nokta
                w = half_span * (1.0 - t) * spike_ratio * 2
                row_angs = [ang_off - w, ang_off + w]
                row_top = [(r*math.cos(a), r*math.sin(a), zmid+hw) for a in row_angs]
                row_bot = [(r*math.cos(a), r*math.sin(a), zmid-hw) for a in row_angs]
                # Dış uca doğru tamamen kapanır
                if t > 0.98:
                    tip = (r*math.cos(ang_off), r*math.sin(ang_off), zmid)
                    row_top = [tip, tip]; row_bot = [tip, tip]

            elif blade_type == "blade":
                # Asimetrik: ön dar, arka geniş
                w_front = half_span * (1.0 - blade_asym) * max(0.1, 1.0-t*0.4)
                w_back  = half_span * (1.0 + blade_asym) * max(0.1, 1.0-t*0.5)
                row_angs_top = [ang_off - w_front, ang_off + w_back]
                row_angs_bot = [ang_off - w_front, ang_off + w_back]
                row_top = [(r*math.cos(a), r*math.sin(a), zmid+hw) for a in row_angs_top]
                row_bot = [(r*math.cos(a), r*math.sin(a), zmid-hw) for a in row_angs_bot]

            elif blade_type == "flat":
                # Sabit genişlik, bevel uçlarda
                bv = flat_bevel
                if t < bv:
                    ww = half_span * (t/bv)
                elif t > 1.0-bv:
                    ww = half_span * ((1.0-t)/bv)
                else:
                    ww = half_span
                row_angs = [ang_off-ww, ang_off+ww]
                row_top = [(r*math.cos(a), r*math.sin(a), zmid+hw) for a in row_angs]
                row_bot = [(r*math.cos(a), r*math.sin(a), zmid-hw) for a in row_angs]

            else:  # wing
                # Sinüs eğrisi genişlik + camber
                w = half_span * math.sin(math.pi * t)
                camber = wing_camber * math.sin(math.pi * t * 0.85) * Z_H
                # Açısal dağılım ASEG noktası
                row_top = []; row_bot = []
                for ai in range(ASEG+1):
                    frac = ai/ASEG
                    a = ang_off + (-w + frac*2*w)
                    row_top.append((r*math.cos(a), r*math.sin(a), zmid+hw+camber*0.3))
                    row_bot.append((r*math.cos(a), r*math.sin(a), zmid-hw))
                pts_top.append(row_top); pts_bot.append(row_bot)
                continue

            # spike / flat / blade: 2 noktalı satır → sadece 1 açısal bölüm
            pts_top.append(row_top)
            pts_bot.append(row_bot)

        # ── yüzey dörtgenleri ────────────────────────────────
        cols = len(pts_top[0]) - 1  # açısal segment sayısı

        for ri in range(RSEG):
            for ai in range(cols):
                tris_raw += quad(pts_top[ri][ai],   pts_top[ri][ai+1],
                                 pts_top[ri+1][ai+1], pts_top[ri+1][ai])
                tris_raw += quad(pts_bot[ri][ai],   pts_bot[ri+1][ai],
                                 pts_bot[ri+1][ai+1], pts_bot[ri][ai+1])

        # ── kenar kapakları ──────────────────────────────────
        for ri in range(RSEG):  # ön
            tris_raw += quad(pts_top[ri][0], pts_bot[ri][0],
                             pts_bot[ri+1][0], pts_top[ri+1][0])
        for ri in range(RSEG):  # arka
            tris_raw += quad(pts_top[ri][-1],    pts_top[ri+1][-1],
                             pts_bot[ri+1][-1],  pts_bot[ri][-1])
        for ai in range(cols):  # dış
            tris_raw += quad(pts_top[-1][ai], pts_top[-1][ai+1],
                             pts_bot[-1][ai+1], pts_bot[-1][ai])
        for ai in range(cols):  # iç
            tris_raw += quad(pts_top[0][ai],  pts_bot[0][ai],
                             pts_bot[0][ai+1], pts_top[0][ai+1])

    return norm_tris(tris_raw)


# ── FusionWheelView ───────────────────────────────────────────
class FusionWheelView(GLMeshView):
    """Fusion Wheel 3D görünümü — tinker.obj + prosedürel kanatlar. OpenGL backend."""

    _ZAMAK_DARK  = (0x8a/255, 0x8a/255, 0x94/255)
    _ZAMAK_LIGHT = (0xb0/255, 0xb0/255, 0xb8/255)
    _BLADE_DEF   = QColor("#c0a060")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCursor(QCursor(Qt.OpenHandCursor))

        self.blade_count  = 3;  self.blade_type   = "wing"
        self.blade_depth  = 6.0; self.taper        = 0.0
        self.gap_frac     = 0.25; self.wing_camber  = 0.10
        self.wing_sweep   = 10.0; self.spike_ratio  = 0.5
        self.flat_bevel   = 0.15; self.blade_sweep  = 20.0
        self.blade_asym   = 0.35
        self._color_blade = QColor(self._BLADE_DEF)

        self._rx = 65.0; self._ry = 0.0
        self._blade_cache = None; self._blade_mesh_dirty = True

    def set_color_blade(self, c: QColor):
        self._color_blade = c
        self.invalidate_mesh()

    def rebuild(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)
        self._blade_mesh_dirty = True
        self.invalidate_mesh()

    def _tick(self):
        if self._auto:
            self._spin_angle = (self._spin_angle + 0.35) % 360
        self.update()

    def _view_scale(self):
        r_total = _FW_BLADE_R + self.blade_depth + 1.0
        return (1.0 / 2.1) / r_total

    def _get_groups(self):
        if self._blade_mesh_dirty or self._blade_cache is None:
            self._blade_cache = _double_sided(build_blade_tris(
                blade_count=self.blade_count, blade_type=self.blade_type,
                blade_depth=self.blade_depth, taper=self.taper,
                gap_frac=self.gap_frac, wing_camber=self.wing_camber,
                wing_sweep=self.wing_sweep, spike_ratio=self.spike_ratio,
                flat_bevel=self.flat_bevel, blade_sweep=self.blade_sweep,
                blade_asym=self.blade_asym,
            ))
            self._blade_mesh_dirty = False

        zamak = self._ZAMAK_DARK if _DARK else self._ZAMAK_LIGHT
        blade_c = (self._color_blade.redF(), self._color_blade.greenF(), self._color_blade.blueF())
        amb, dif = (0.22, 0.78) if _DARK else (0.42, 0.58)
        return [
            (_tinker_tris(),       zamak,   amb, dif),
            (self._blade_cache,    blade_c, amb, dif),
        ]

    def _hint_text(self):
        return tr("drag_hint3")


# ══════════════════════════════════════════════════════════════
# SPIN TRACK — embed OBJ
# ══════════════════════════════════════════════════════════════
_ST_TOP_B64 = (
    "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"
)

_ST_BOT_B64 = (
    "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"
    "2x++fvuj/d+Lf/k/rfSVYw=="
)

# ══════════════════════════════════════════════════════════════
# SPIN TRACK
# ══════════════════════════════════════════════════════════════

_ST_TOP_CACHE   = None
_ST_BOT_CACHE   = None
_ST_TRIS_CACHE  = None
_ST_CONN_H_LAST = None

def _load_st_obj(b64_tuple):
    raw = zlib.decompress(_b64.b64decode("".join(b64_tuple)))
    verts, faces = [], []
    for line in raw.decode("utf-8").splitlines():
        p = line.split()
        if not p: continue
        if p[0] == "v":
            verts.append((float(p[1]), float(p[2]), float(p[3])))
        elif p[0] == "f":
            idx = [int(x.split("/")[0])-1 for x in p[1:]]
            for i in range(1, len(idx)-1):
                faces.append((idx[0], idx[i], idx[i+1]))
    return verts, faces

def _st_top_data():
    global _ST_TOP_CACHE
    if _ST_TOP_CACHE is None: _ST_TOP_CACHE = _load_st_obj(_ST_TOP_B64)
    return _ST_TOP_CACHE

def _st_bot_data():
    global _ST_BOT_CACHE
    if _ST_BOT_CACHE is None: _ST_BOT_CACHE = _load_st_obj(_ST_BOT_B64)
    return _ST_BOT_CACHE

def _st_obj_to_tris(verts, faces, z_offset=0.0):
    result = []
    for fi,fj,fk in faces:
        v1,v2,v3 = verts[fi],verts[fj],verts[fk]
        if z_offset:
            v1=(v1[0],v1[1],v1[2]+z_offset)
            v2=(v2[0],v2[1],v2[2]+z_offset)
            v3=(v3[0],v3[1],v3[2]+z_offset)
        ax,ay,az=v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]
        bx,by,bz=v3[0]-v1[0],v3[1]-v1[1],v3[2]-v1[2]
        nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
        ll=math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
        result.append(((nx/ll,ny/ll,nz/ll),v1,v2,v3))
    return result

def _build_st_connector(r_top,r_bot,r_hole,height,z_base,seg=48):
    tris=[]; z_b=z_base; z_t=z_base+height
    def pt(r,a,z): return (r*math.cos(a),r*math.sin(a),z)
    def nrm(pa,pb,pc):
        ax,ay,az=pb[0]-pa[0],pb[1]-pa[1],pb[2]-pa[2]
        bx,by,bz=pc[0]-pa[0],pc[1]-pa[1],pc[2]-pa[2]
        nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
        ll=math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
        return (nx/ll,ny/ll,nz/ll)
    for i in range(seg):
        a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
        p0,p1=pt(r_bot,a0,z_b),pt(r_bot,a1,z_b)
        p2,p3=pt(r_top,a0,z_t),pt(r_top,a1,z_t)
        tris+=[(nrm(p0,p2,p1),p0,p2,p1),(nrm(p1,p2,p3),p1,p2,p3)]
        q0,q1=pt(r_hole,a0,z_b),pt(r_hole,a1,z_b)
        q2,q3=pt(r_hole,a0,z_t),pt(r_hole,a1,z_t)
        tris+=[(nrm(q0,q1,q2),q0,q1,q2),(nrm(q1,q3,q2),q1,q3,q2)]
        d0,d1=pt(r_hole,a0,z_b),pt(r_hole,a1,z_b)
        d2,d3=pt(r_bot,a0,z_b),pt(r_bot,a1,z_b)
        tris+=[((0,0,-1),d0,d2,d1),((0,0,-1),d1,d2,d3)]
        u0,u1=pt(r_hole,a0,z_t),pt(r_hole,a1,z_t)
        u2,u3=pt(r_top,a0,z_t),pt(r_top,a1,z_t)
        tris+=[((0,0,1),u0,u1,u2),((0,0,1),u1,u3,u2)]
    return tris

def _st_tris(conn_h=4.0):
    global _ST_TRIS_CACHE,_ST_CONN_H_LAST
    if _ST_TRIS_CACHE is not None and _ST_CONN_H_LAST==conn_h:
        return _ST_TRIS_CACHE
    vu,fu=_st_top_data(); va,fa=_st_bot_data()
    ust_z_min=min(v[2] for v in vu); alt_z_max=max(v[2] for v in va)
    alt_tris=_st_obj_to_tris(va,fa,z_offset=0.0)
    ust_bot_rs=[math.sqrt(v[0]**2+v[1]**2) for v in vu if abs(v[2]-ust_z_min)<0.2]
    alt_top_rs=[math.sqrt(v[0]**2+v[1]**2) for v in va if abs(v[2]-alt_z_max)<0.2]
    r_top=max(ust_bot_rs); r_bot=max(alt_top_rs); r_hole=min(ust_bot_rs)
    conn_tris=_build_st_connector(r_top,r_bot,r_hole,conn_h,z_base=alt_z_max,seg=48)
    ust_tris=_st_obj_to_tris(vu,fu,z_offset=alt_z_max+conn_h)
    _ST_TRIS_CACHE=alt_tris+_double_sided(conn_tris)+ust_tris; _ST_CONN_H_LAST=conn_h
    return _ST_TRIS_CACHE

# ══════════════════════════════════════════════════════════════
# PERFORMANCE TIP — embed OBJ
# ══════════════════════════════════════════════════════════════
_PT_TOP_B64 = (
    "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"
)

# ══════════════════════════════════════════════════════════════
# PERFORMANCE TIP — OBJ Z=0 üst flanş, Z=6 serbest uç
# Tip mesh Z=6'dan +Z yönünde (aşağıya) uzanır
# ══════════════════════════════════════════════════════════════
_PT_OBJ_Z_TIP  = 5.998   # OBJ uç Z = tip mesh başlangıcı
_PT_TIP_R_BASE = 5.976   # OBJ Z=6 yarıçapı

_PT_TOP_CACHE   = None
_PT_TRIS_CACHE  = None
_PT_PARAMS_LAST = None

def _pt_top_data():
    global _PT_TOP_CACHE
    if _PT_TOP_CACHE is None:
        raw=zlib.decompress(_b64.b64decode("".join(_PT_TOP_B64)))
        verts,faces=[],[]
        for line in raw.decode("utf-8").splitlines():
            p=line.split()
            if not p: continue
            if p[0]=="v": verts.append((float(p[1]),float(p[2]),float(p[3])))
            elif p[0]=="f":
                idx=[int(x.split("/")[0])-1 for x in p[1:]]
                for i in range(1,len(idx)-1): faces.append((idx[0],idx[i],idx[i+1]))
        _PT_TOP_CACHE=verts,faces
    return _PT_TOP_CACHE

def _pt_obj_to_tris(verts,faces):
    result=[]
    for fi,fj,fk in faces:
        v1,v2,v3=verts[fi],verts[fj],verts[fk]
        ax,ay,az=v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]
        bx,by,bz=v3[0]-v1[0],v3[1]-v1[1],v3[2]-v1[2]
        nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
        ll=math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
        result.append(((nx/ll,ny/ll,nz/ll),v1,v2,v3))
    return result

def _build_pt_tip(shape="sharp",length=3.0,flat_r=1.5,hole_r=0.6,hole_d=0.8,seg=48):
    r_base=_PT_TIP_R_BASE
    z0=_PT_OBJ_Z_TIP       # OBJ'nin DAR UCU
    z_end=z0+length         # +Z yönünde uzanır
    tris=[]
    def pt(r,a,z): return (r*math.cos(a),r*math.sin(a),z)
    def nrm(pa,pb,pc):
        ax,ay,az=pb[0]-pa[0],pb[1]-pa[1],pb[2]-pa[2]
        bx,by,bz=pc[0]-pa[0],pc[1]-pa[1],pc[2]-pa[2]
        nx,ny,nz=ay*bz-az*by,az*bx-ax*bz,ax*by-ay*bx
        ll=math.sqrt(nx*nx+ny*ny+nz*nz) or 1.0
        return (nx/ll,ny/ll,nz/ll)

    # z0'da üst kapak (OBJ iç boşluğunu kapatır, -Z bakıyor)
    for i in range(seg):
        a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
        tris.append(((0,0,-1),(0,0,z0),pt(r_base,a0,z0),pt(r_base,a1,z0)))

    if shape in ("sharp","sharp_hole"):
        r_tip=hole_r if shape=="sharp_hole" else 0.0
        for vi in range(20):
            t0=vi/20; t1=(vi+1)/20
            za=z0+(z_end-z0)*t0; zb=z0+(z_end-z0)*t1
            ra=r_base+(r_tip-r_base)*t0; rb=r_base+(r_tip-r_base)*t1
            for i in range(seg):
                a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
                p0=pt(ra,a0,za); p1=pt(ra,a1,za)
                p2=pt(rb,a0,zb); p3=pt(rb,a1,zb)
                tris+=[(nrm(p0,p1,p2),p0,p1,p2),(nrm(p1,p3,p2),p1,p3,p2)]
        if shape=="sharp":
            apex=(0.0,0.0,z_end)
            for i in range(seg):
                a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
                p0=pt(0.01,a0,z_end-0.01); p1=pt(0.01,a1,z_end-0.01)
                tris.append((nrm(apex,p1,p0),apex,p1,p0))
        else:
            for i in range(seg):
                a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
                tris.append(((0,0,1),(0,0,z_end),pt(hole_r,a1,z_end),pt(hole_r,a0,z_end)))
                q0=pt(hole_r,a0,z_end); q1=pt(hole_r,a1,z_end)
                q2=pt(hole_r,a0,z_end-hole_d); q3=pt(hole_r,a1,z_end-hole_d)
                tris+=[(nrm(q0,q2,q1),q0,q2,q1),(nrm(q1,q2,q3),q1,q2,q3)]
                bot=(0,0,z_end-hole_d)
                tris.append((nrm(bot,q2,q3),bot,q2,q3))

    elif shape=="round":
        cyl_h=length*0.3; z_cyl=z0+cyl_h; r_sph=r_base; z_cen=z_cyl
        for i in range(seg):
            a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
            p0=pt(r_base,a0,z0); p1=pt(r_base,a1,z0)
            p2=pt(r_base,a0,z_cyl); p3=pt(r_base,a1,z_cyl)
            tris+=[(nrm(p0,p1,p2),p0,p1,p2),(nrm(p1,p3,p2),p1,p3,p2)]
        for vi in range(11):
            th0=math.pi/2*vi/10; th1=math.pi/2*(vi+1)/10
            ra=r_sph*math.cos(th0); rb=r_sph*math.cos(th1)
            za=z_cen+r_sph*math.sin(th0); zb=z_cen+r_sph*math.sin(th1)
            for i in range(seg):
                a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
                p0=pt(ra,a0,za); p1=pt(ra,a1,za)
                if rb<0.01:
                    apex=(0,0,zb); tris.append((nrm(apex,p0,p1),apex,p0,p1))
                else:
                    p2=pt(rb,a0,zb); p3=pt(rb,a1,zb)
                    tris+=[(nrm(p0,p1,p2),p0,p1,p2),(nrm(p1,p3,p2),p1,p3,p2)]

    elif shape in ("flat","flat_hole"):
        cone_h=length*0.4; z_cone_end=z0+cone_h; z_cyl_end=z0+length
        for vi in range(12):
            t0=vi/12; t1=(vi+1)/12
            za=z0+(z_cone_end-z0)*t0; zb=z0+(z_cone_end-z0)*t1
            ra=r_base+(flat_r-r_base)*t0; rb=r_base+(flat_r-r_base)*t1
            for i in range(seg):
                a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
                p0=pt(ra,a0,za); p1=pt(ra,a1,za)
                p2=pt(rb,a0,zb); p3=pt(rb,a1,zb)
                tris+=[(nrm(p0,p1,p2),p0,p1,p2),(nrm(p1,p3,p2),p1,p3,p2)]
        for i in range(seg):
            a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
            p0=pt(flat_r,a0,z_cone_end); p1=pt(flat_r,a1,z_cone_end)
            p2=pt(flat_r,a0,z_cyl_end); p3=pt(flat_r,a1,z_cyl_end)
            tris+=[(nrm(p0,p1,p2),p0,p1,p2),(nrm(p1,p3,p2),p1,p3,p2)]
        if shape=="flat":
            for i in range(seg):
                a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
                tris.append(((0,0,1),(0,0,z_cyl_end),pt(flat_r,a1,z_cyl_end),pt(flat_r,a0,z_cyl_end)))
        else:
            z_dt=z_cyl_end; z_db=z_cyl_end-hole_d
            for i in range(seg):
                a0=2*math.pi*i/seg; a1=2*math.pi*(i+1)/seg
                pi0=pt(hole_r,a0,z_dt); pi1=pt(hole_r,a1,z_dt)
                po0=pt(flat_r,a0,z_dt); po1=pt(flat_r,a1,z_dt)
                tris+=[(nrm(pi0,pi1,po0),pi0,pi1,po0),(nrm(pi1,po1,po0),pi1,po1,po0)]
                q0=pt(hole_r,a0,z_dt); q1=pt(hole_r,a1,z_dt)
                q2=pt(hole_r,a0,z_db); q3=pt(hole_r,a1,z_db)
                tris+=[(nrm(q0,q2,q1),q0,q2,q1),(nrm(q1,q2,q3),q1,q2,q3)]
                bot=(0,0,z_db); tris.append((nrm(bot,q2,q3),bot,q2,q3))
    return tris

def _pt_tris(shape="sharp",length=3.0,flat_r=1.5,hole_r=0.6,hole_d=0.8):
    global _PT_TRIS_CACHE,_PT_PARAMS_LAST
    params=(shape,length,flat_r,hole_r,hole_d)
    if _PT_TRIS_CACHE is not None and _PT_PARAMS_LAST==params: return _PT_TRIS_CACHE
    vu,fu=_pt_top_data()
    _PT_TRIS_CACHE=_pt_obj_to_tris(vu,fu)+_double_sided(_build_pt_tip(shape=shape,length=length,
        flat_r=flat_r,hole_r=hole_r,hole_d=hole_d))
    _PT_PARAMS_LAST=params
    return _PT_TRIS_CACHE


class SpinTrackView(GLMeshView):
    """Spin Track 3D görünümü. OpenGL backend."""
    _COLOR_DEF = "#2255cc"
    _PRESETS   = ["#2255cc","#cc2222","#22aa44","#cc7722","#8822cc","#888888","#111111","#eeeeee"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self.conn_h = 4.0
        self._color = QColor(self._COLOR_DEF)
        self._rx = 60.0; self._ry = 25.0

    def set_conn_h(self, v):
        self.conn_h = v
        global _ST_TRIS_CACHE; _ST_TRIS_CACHE = None
        self.invalidate_mesh()

    def set_color(self, c):
        self._color = c
        self.invalidate_mesh()

    def _tick(self):
        if self._auto: self._spin_angle = (self._spin_angle + 0.4) % 360
        self.update()

    def _view_scale(self):
        tris = _st_tris(self.conn_h)
        if not tris: return 0.05
        all_v = [v for _, v1, v2, v3 in tris for v in [v1, v2, v3]]
        r_max = max(math.sqrt(v[0]**2+v[1]**2+v[2]**2) for v in all_v) or 10.0
        return (1.0 / 2.3) / r_max

    def _get_groups(self):
        tris = _st_tris(self.conn_h)
        r = self._color.redF(); g = self._color.greenF(); b = self._color.blueF()
        amb, dif = (0.22, 0.78) if _DARK else (0.42, 0.58)
        return [(tris, (r, g, b), amb, dif)]
class SpinTrackPanel(QWidget):
    _COLOR_DEF = "#2255cc"
    _PRESETS   = ["#2255cc","#cc2222","#22aa44","#cc7722","#8822cc","#888888","#111111","#eeeeee"]

    def __init__(self, view, parent=None):
        super().__init__(parent)
        self._view=view; self._dirty_cb=None; self._color=QColor(self._COLOR_DEF)
        v=QVBoxLayout(self); v.setContentsMargins(0,0,0,0); v.setSpacing(0)
        sa=QScrollArea(); sa.setWidgetResizable(True)
        sa.setStyleSheet(
            f"QScrollArea{{border:none;background:{SIDEBAR.name()};}}"
            f"QScrollBar:vertical{{background:{BG.name()};width:5px;}}"
            f"QScrollBar::handle:vertical{{background:{BORDER.name()};border-radius:2px;min-height:20px;}}"
            f"QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}")
        inner=QWidget(); inner.setStyleSheet(f"background:{SIDEBAR.name()};")
        iv=QVBoxLayout(inner); iv.setContentsMargins(0,4,0,8); iv.setSpacing(0)
        ss_sec=(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;"
                f"font-weight:700;letter-spacing:1px;background:transparent;")
        ss_lbl=f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;background:transparent;"
        ss_sp=(f"QDoubleSpinBox{{color:{TPRI.name()};font-family:'Segoe UI';font-size:9px;"
               f"background:{PANEL.name()};border:1px solid {BORDER.name()};border-radius:3px;padding:2px 4px;}}"
               f"QDoubleSpinBox:focus{{border-color:{ACCENT.name()};}}"
               f"QDoubleSpinBox::up-button,QDoubleSpinBox::down-button{{width:14px;}}")
        def sec(t):
            lb=QLabel(t); lb.setStyleSheet(ss_sec); lb.setContentsMargins(10,8,10,4); return lb
        def row(lbl,wgt):
            rw=QWidget(); rw.setStyleSheet("background:transparent;")
            rl=QHBoxLayout(rw); rl.setContentsMargins(10,2,10,2); rl.setSpacing(8)
            lb=QLabel(lbl); lb.setStyleSheet(ss_lbl); rl.addWidget(lb); rl.addStretch(); rl.addWidget(wgt); return rw
        iv.addWidget(sec(tr("track_length")))
        self._conn_spin=QDoubleSpinBox()
        # Wiki birimi: ST numarası = 0.1mm (ST85=8.5mm … ST250=25.0mm)
        self._conn_spin.setRange(85, 250)
        self._conn_spin.setSingleStep(5); self._conn_spin.setDecimals(0)
        self._conn_spin.setSuffix(""); self._conn_spin.setValue(110)
        self._conn_spin.setFixedWidth(80); self._conn_spin.setStyleSheet(ss_sp)
        self._conn_spin.valueChanged.connect(self._on_len)
        iv.addWidget(row(tr("st_number"), self._conn_spin))

        # Deneysel uyarı etiketi (231-250 arası)
        self._exp_lbl = QLabel("⚠ " + (tr("experimental")))
        self._exp_lbl.setStyleSheet(
            f"color:#cc8800;font-family:'Segoe UI';font-size:8px;"
            f"background:transparent;padding:0 10px;")
        self._exp_lbl.setVisible(False)
        iv.addWidget(self._exp_lbl)

        iv.addWidget(hdiv())

        # ST Puanları
        iv.addWidget(sec(tr("part_stats")))
        sb_atk, self._st_upd_atk = stat_bar_live(tr("attack"),   ATK, max_val=3)
        sb_def, self._st_upd_def = stat_bar_live(tr("defense"),  DEF, max_val=3)
        sb_sta, self._st_upd_sta = stat_bar_live(tr("stamina"),  STA, max_val=3)
        iv.addWidget(sb_atk); iv.addWidget(sb_def); iv.addWidget(sb_sta)
        iv.addWidget(hdiv())
        iv.addWidget(sec(tr("color")))
        cr=QHBoxLayout(); cr.setSpacing(5); cr.setContentsMargins(10,2,10,2)
        self._color_btn=QPushButton("🎨  "+(tr("pick_color")))
        self._color_btn.setFixedHeight(26); self._color_btn.setStyleSheet(self._cbtn_ss())
        self._color_btn.clicked.connect(self._pick_color)
        self._hex_in=QLineEdit(self._color.name()); self._hex_in.setFixedWidth(68)
        self._hex_in.setMaxLength(7); self._hex_in.setPlaceholderText("#rrggbb")
        self._hex_in.setStyleSheet(
            f"QLineEdit{{background:{PANEL.name()};color:{TPRI.name()};"
            f"border:1px solid {BORDER.name()};border-radius:3px;"
            f"font-family:'Consolas';font-size:9px;padding:2px 4px;}}"
            f"QLineEdit:focus{{border-color:{ACCENT.name()};}}")
        self._hex_in.editingFinished.connect(self._hex_changed)
        cr.addWidget(self._color_btn,1); cr.addWidget(self._hex_in)
        cw=QWidget(); cw.setStyleSheet("background:transparent;"); cw.setLayout(cr); iv.addWidget(cw)
        pg=QGridLayout(); pg.setSpacing(4); pg.setContentsMargins(10,4,10,4)
        for i,hx in enumerate(self._PRESETS):
            pb=QPushButton(); pb.setFixedSize(22,22); pb.setToolTip(hx)
            pb.setStyleSheet(f"background:{hx};border:1px solid {BORDER.name()};border-radius:3px;")
            pb.clicked.connect(lambda _=False,c=hx: self._set_color(QColor(c)))
            pg.addWidget(pb,i//4,i%4)
        pgw=QWidget(); pgw.setStyleSheet("background:transparent;"); pgw.setLayout(pg); iv.addWidget(pgw)
        iv.addWidget(hdiv())
        # ── Ağırlık (hesaplanan) ─────────────────────────────
        iv.addWidget(sec(tr("weight")))
        wrow=QWidget(); wrow.setStyleSheet("background:transparent;")
        wlay=QHBoxLayout(wrow); wlay.setContentsMargins(10,2,10,2); wlay.setSpacing(4)
        wlbl=QLabel(tr("calculated")); wlbl.setStyleSheet(ss_lbl)
        self._weight_lbl=QLabel("—")
        self._weight_lbl.setStyleSheet(f"color:{TPRI.name()};font-family:'Segoe UI';font-size:10px;font-weight:700;background:transparent;")
        wlay.addWidget(wlbl); wlay.addStretch(); wlay.addWidget(self._weight_lbl)
        iv.addWidget(wrow)
        self._weight_cb=None
        iv.addStretch(); sa.setWidget(inner); v.addWidget(sa,1)
        self._update_st_stats(110)
        self._recalc_weight()

    def _cbtn_ss(self):
        return (f"background:{PANEL.name()};color:{TPRI.name()};"
                f"border:1px solid {BORDER.name()};border-left:5px solid {self._color.name()};"
                f"border-radius:4px;font-family:'Segoe UI';font-size:9px;"
                f"text-align:left;padding-left:6px;")
    def _pick_color(self):
        c=QColorDialog.getColor(self._color,self,tr("st_color"))
        if c.isValid(): self._set_color(c)
    def _set_color(self,c):
        self._color=c; self._color_btn.setStyleSheet(self._cbtn_ss()); self._hex_in.setText(c.name())
        if self._view: self._view.set_color(c)
        if self._dirty_cb: self._dirty_cb()
    def _hex_changed(self):
        txt=self._hex_in.text().strip()
        if not txt.startswith("#"): txt="#"+txt
        c=QColor(txt)
        if c.isValid(): self._set_color(c)
        else: self._hex_in.setText(self._color.name())

    _ST_ALT_H = 4.0
    _ST_UST_H = 3.5

    def _total_to_conn(self, st_num):
        """Wiki ST numarası (0.1mm) → connector yüksekliği (mm)."""
        return max(0.0, st_num / 10.0 - self._ST_ALT_H - self._ST_UST_H)

    @staticmethod
    def _st_stats(n):
        """ST numarasına göre (atk, def, sta) döndürür."""
        if   85  <= n <= 89:  return (3, 0, 0)
        elif 90  <= n <= 94:  return (2, 0, 0)
        elif 95  <= n <= 100: return (1, 1, 0)
        elif 101 <= n <= 109: return (1, 1, 0)  # 1 atk + 1 def
        elif 110 <= n <= 119: return (0, 2, 0)
        elif 120 <= n <= 124: return (0, 3, 0)
        elif 125 <= n <= 134: return (0, 2, 0)
        elif 135 <= n <= 144: return (0, 1, 1)  # 1 def + 1 sta
        elif 145 <= n <= 159: return (0, 1, 1)
        elif 160 <= n <= 199: return (0, 0, 2)
        elif 200 <= n <= 250: return (0, 0, 3)
        return (0, 0, 0)

    def _update_st_stats(self, n):
        atk, def_, sta = self._st_stats(n)
        self._cached_atk = atk
        self._cached_def = def_
        self._cached_sta = sta
        self._st_upd_atk(atk)
        self._st_upd_def(def_)
        self._st_upd_sta(sta)
        self._exp_lbl.setVisible(231 <= n <= 250)

    def _on_len(self, val):
        n = int(val)
        if self._view: self._view.set_conn_h(self._total_to_conn(n))
        self._update_st_stats(n)
        self._recalc_weight()
        if self._dirty_cb: self._dirty_cb()

    def set_dirty_callback(self, cb): self._dirty_cb = cb

    def load_from(self, data):
        v = float(data.get("spin_track_length", 110))
        self._conn_spin.blockSignals(True); self._conn_spin.setValue(v); self._conn_spin.blockSignals(False)
        n = int(v)
        if self._view: self._view.set_conn_h(self._total_to_conn(n))
        self._update_st_stats(n)
        c = QColor(data.get("spin_track_color", self._COLOR_DEF))
        if c.isValid(): self._set_color(c)
        self._recalc_weight()

    def get_data(self):
        return {"spin_track_length": self._conn_spin.value(), "spin_track_color": self._color.name()}

    def _recalc_weight(self):
        conn_h = self._total_to_conn(self._conn_spin.value())
        weight = self._calc_weight_trimesh(conn_h)
        if weight is None:
            # Trimesh yok → wiki verilerinden lineer regresyon (max ~%5 hata)
            # Veri: ST85=1.2g … ST230=4.1g  →  weight = 0.19255*mm - 0.46020
            mm = self._conn_spin.value() / 10.0
            weight = round(max(0.0, 0.19255 * mm - 0.46020), 2)
        self._cached_weight = weight
        self._weight_lbl.setText(f"{self._cached_weight:.2f} g")
        if self._weight_cb: self._weight_cb()

    @staticmethod
    def _calc_weight_trimesh(conn_h: float):
        """trimesh varsa birleşik ST mesh'inden hacim hesaplar, yoksa None döner."""
        try:
            import trimesh, numpy as np
        except ImportError:
            return None
        try:
            tris = _st_tris(conn_h)
            # Vertex ve yüz listesi oluştur
            verts_list = []
            faces_list = []
            vert_map = {}
            for tri in tris:
                first = tri[0]
                if isinstance(first, (tuple, list)) and isinstance(first[0], float):
                    vs = [tri[0], tri[1], tri[2]]
                else:
                    vs = [tri[1], tri[2], tri[3]]
                face = []
                for v in vs:
                    key = (round(v[0],5), round(v[1],5), round(v[2],5))
                    if key not in vert_map:
                        vert_map[key] = len(verts_list)
                        verts_list.append(key)
                    face.append(vert_map[key])
                faces_list.append(face)
            vertices = np.array(verts_list, dtype=float)
            faces    = np.array(faces_list, dtype=int)
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
            trimesh.repair.fix_normals(mesh)
            try:
                trimesh.repair.fill_holes(mesh)
            except Exception:
                pass  # networkx yoksa atla
            if mesh.is_watertight:
                vol_cm3 = abs(mesh.volume) / 1000.0  # mm³ → cm³
                return round(vol_cm3 * _ABS_DENSITY, 2)
        except Exception:
            pass
        return None

    def set_weight_callback(self, cb): self._weight_cb = cb
    def get_weight(self) -> float: return getattr(self, '_cached_weight', 0.0)


class PerformanceTipView(GLMeshView):
    """Performance Tip 3D görünümü. OpenGL backend."""
    _COLOR_DEF_DARK="#3a7abd"; _COLOR_DEF_LIGHT="#5a9add"
    _PRESETS=["#3a7abd","#cc2222","#22aa44","#cc7722","#8822cc","#888888","#111111","#eeeeee"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(240, 220)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self.tip_shape="sharp"; self.tip_length=3.0
        self.tip_flat_r=1.5; self.tip_hole_r=0.6; self.tip_hole_d=0.8
        self._color = QColor(self._COLOR_DEF_DARK if _DARK else self._COLOR_DEF_LIGHT)
        self._rx = 55.0; self._ry = 20.0
        self._top_face_count = None

    def set_color(self, c):
        self._color = c
        self.invalidate_mesh()

    def set_params(self, **kw):
        for k, v in kw.items(): setattr(self, k, v)
        global _PT_TRIS_CACHE; _PT_TRIS_CACHE = None
        self._top_face_count = None
        self.invalidate_mesh()

    def _tick(self):
        if self._auto: self._spin_angle = (self._spin_angle + 0.4) % 360
        self.update()

    def _view_scale(self):
        tris = _pt_tris(self.tip_shape, self.tip_length, self.tip_flat_r, self.tip_hole_r, self.tip_hole_d)
        if not tris: return 0.05
        all_v = [v for _, v1, v2, v3 in tris for v in [v1, v2, v3]]
        r_max = max(math.sqrt(v[0]**2+v[1]**2+v[2]**2) for v in all_v) or 10.0
        return (1.0 / 2.3) / r_max

    def _center_offset(self):
        tris = _pt_tris(self.tip_shape, self.tip_length, self.tip_flat_r, self.tip_hole_r, self.tip_hole_d)
        if not tris: return (0.0, 0.0, 0.0)
        all_v = [v for _, v1, v2, v3 in tris for v in [v1, v2, v3]]
        zs = [v[2] for v in all_v]
        z_mid = (max(zs) + min(zs)) / 2 if zs else 0.0
        return (0.0, 0.0, z_mid)

    def _get_groups(self):
        tris = _pt_tris(self.tip_shape, self.tip_length, self.tip_flat_r, self.tip_hole_r, self.tip_hole_d)
        pr = self._color.redF(); pg = self._color.greenF(); pb = self._color.blueF()
        amb, dif = (0.22, 0.78) if _DARK else (0.42, 0.58)
        return [(tris, (pr, pg, pb), amb, dif)]
class PerformanceTipPanel(QWidget):
    _COLOR_DEF="#3a7abd"
    _PRESETS   =["#3a7abd","#cc2222","#22aa44","#cc7722","#8822cc","#888888","#111111","#eeeeee"]
    _SHAPES    =[("sharp",), ("round",), ("flat",), ("sharp_hole",), ("flat_hole",)]

    def __init__(self,view,parent=None):
        super().__init__(parent)
        self._view=view; self._dirty_cb=None; self._color=QColor(self._COLOR_DEF); self._cur_shape="sharp"
        v=QVBoxLayout(self); v.setContentsMargins(0,0,0,0); v.setSpacing(0)
        sa=QScrollArea(); sa.setWidgetResizable(True)
        sa.setStyleSheet(
            f"QScrollArea{{border:none;background:{SIDEBAR.name()};}}"
            f"QScrollBar:vertical{{background:{BG.name()};width:5px;}}"
            f"QScrollBar::handle:vertical{{background:{BORDER.name()};border-radius:2px;min-height:20px;}}"
            f"QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}")
        inner=QWidget(); inner.setStyleSheet(f"background:{SIDEBAR.name()};")
        iv=QVBoxLayout(inner); iv.setContentsMargins(0,4,0,8); iv.setSpacing(0)
        ss_sec=(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;"
                f"font-weight:700;letter-spacing:1px;background:transparent;")
        ss_lbl=f"color:{TSEC.name()};font-family:'Segoe UI';font-size:8px;background:transparent;"
        ss_sp=(f"QDoubleSpinBox{{color:{TPRI.name()};font-family:'Segoe UI';font-size:9px;"
               f"background:{PANEL.name()};border:1px solid {BORDER.name()};border-radius:3px;padding:2px 4px;}}"
               f"QDoubleSpinBox:focus{{border-color:{ACCENT.name()};}}"
               f"QDoubleSpinBox::up-button,QDoubleSpinBox::down-button{{width:14px;}}")
        def sec(t):
            lb=QLabel(t); lb.setStyleSheet(ss_sec); lb.setContentsMargins(10,8,10,4); return lb
        def row(lbl,wgt):
            rw=QWidget(); rw.setStyleSheet("background:transparent;")
            rl=QHBoxLayout(rw); rl.setContentsMargins(10,2,10,2); rl.setSpacing(8)
            lb=QLabel(lbl); lb.setStyleSheet(ss_lbl); rl.addWidget(lb); rl.addStretch(); rl.addWidget(wgt); return rw
        def dspin(lo,hi,step,val,suf=""):
            sp=QDoubleSpinBox(); sp.setRange(lo,hi); sp.setSingleStep(step); sp.setDecimals(1)
            sp.setValue(val); sp.setFixedWidth(72)
            if suf: sp.setSuffix(suf)
            sp.setStyleSheet(ss_sp); return sp

        iv.addWidget(sec(tr("shape")))
        self._shape_btns={}
        for (key,) in self._SHAPES:
            lbl=tr(f"shape_{key}")
            btn=QPushButton(lbl); btn.setCheckable(True); btn.setChecked(key=="sharp")
            btn.setStyleSheet(
                f"QPushButton{{background:{PANEL.name()};color:{TSEC.name()};"
                f"border:1px solid {BORDER.name()};border-radius:3px;"
                f"font-family:'Segoe UI';font-size:9px;padding:4px 8px;text-align:left;}}"
                f"QPushButton:checked{{background:{ACCENT.name()}22;color:{TPRI.name()};"
                f"border-color:{ACCENT.name()};}}")
            btn.clicked.connect(lambda _=False,k=key: self._on_shape(k))
            bw=QWidget(); bw.setStyleSheet("background:transparent;")
            bl=QHBoxLayout(bw); bl.setContentsMargins(10,2,10,2); bl.addWidget(btn); bl.addStretch()
            iv.addWidget(bw); self._shape_btns[key]=btn
        iv.addWidget(hdiv())
        iv.addWidget(sec(tr("tip_length")))
        self._len_spin=dspin(1.0,5.0,0.5,3.0," mm")
        self._len_spin.valueChanged.connect(self._on_params)
        iv.addWidget(row(tr("length"),self._len_spin))
        iv.addWidget(hdiv())
        self._flat_sec=sec(tr("semi_flat_r"))
        iv.addWidget(self._flat_sec)
        self._flat_spin=dspin(0.3,4.0,0.1,1.5," mm"); self._flat_spin.valueChanged.connect(self._on_params)
        self._flat_row=row(tr("cylinder_r"),self._flat_spin)
        iv.addWidget(self._flat_row)
        iv.addWidget(hdiv())
        self._hole_sec=sec(tr("hole"))
        iv.addWidget(self._hole_sec)
        self._hole_r_spin=dspin(0.2,2.0,0.1,0.6," mm"); self._hole_r_spin.valueChanged.connect(self._on_params)
        self._hole_r_row=row(tr("radius"),self._hole_r_spin); iv.addWidget(self._hole_r_row)
        self._hole_d_spin=dspin(0.2,2.0,0.1,0.8," mm"); self._hole_d_spin.valueChanged.connect(self._on_params)
        self._hole_d_row=row(tr("depth"),self._hole_d_spin); iv.addWidget(self._hole_d_row)
        iv.addWidget(hdiv())
        iv.addWidget(sec(tr("weight")))
        wrow=QWidget(); wrow.setStyleSheet("background:transparent;")
        wlay=QHBoxLayout(wrow); wlay.setContentsMargins(10,2,10,2); wlay.setSpacing(4)
        wlbl=QLabel(tr("calculated")); wlbl.setStyleSheet(ss_lbl)
        self._weight_lbl=QLabel("—")
        self._weight_lbl.setStyleSheet(f"color:{TPRI.name()};font-family:'Segoe UI';font-size:10px;font-weight:700;background:transparent;")
        wlay.addWidget(wlbl); wlay.addStretch(); wlay.addWidget(self._weight_lbl)
        iv.addWidget(wrow)
        self._weight_cb=None; self._cached_weight=0.0
        iv.addWidget(hdiv())
        iv.addWidget(sec(tr("part_stats")))
        sb_atk, self._pt_upd_atk = stat_bar_live(tr("attack"),  ATK, max_val=6)
        sb_def, self._pt_upd_def = stat_bar_live(tr("defense"), DEF, max_val=6)
        sb_sta, self._pt_upd_sta = stat_bar_live(tr("stamina"), STA, max_val=6)
        iv.addWidget(sb_atk); iv.addWidget(sb_def); iv.addWidget(sb_sta)
        iv.addWidget(hdiv())
        iv.addWidget(sec(tr("color")))
        cr=QHBoxLayout(); cr.setSpacing(5); cr.setContentsMargins(10,2,10,2)
        self._color_btn=QPushButton("🎨  "+(tr("pick_color")))
        self._color_btn.setFixedHeight(26); self._color_btn.setStyleSheet(self._cbtn_ss())
        self._color_btn.clicked.connect(self._pick_color)
        self._hex_in=QLineEdit(self._color.name()); self._hex_in.setFixedWidth(68)
        self._hex_in.setMaxLength(7); self._hex_in.setPlaceholderText("#rrggbb")
        self._hex_in.setStyleSheet(
            f"QLineEdit{{background:{PANEL.name()};color:{TPRI.name()};"
            f"border:1px solid {BORDER.name()};border-radius:3px;"
            f"font-family:'Consolas';font-size:9px;padding:2px 4px;}}"
            f"QLineEdit:focus{{border-color:{ACCENT.name()};}}")
        self._hex_in.editingFinished.connect(self._hex_changed)
        cr.addWidget(self._color_btn,1); cr.addWidget(self._hex_in)
        cw=QWidget(); cw.setStyleSheet("background:transparent;"); cw.setLayout(cr); iv.addWidget(cw)
        pg=QGridLayout(); pg.setSpacing(4); pg.setContentsMargins(10,4,10,4)
        for i,hx in enumerate(self._PRESETS):
            pb=QPushButton(); pb.setFixedSize(22,22); pb.setToolTip(hx)
            pb.setStyleSheet(f"background:{hx};border:1px solid {BORDER.name()};border-radius:3px;")
            pb.clicked.connect(lambda _=False,c=hx: self._set_color(QColor(c)))
            pg.addWidget(pb,i//4,i%4)
        pgw=QWidget(); pgw.setStyleSheet("background:transparent;"); pgw.setLayout(pg); iv.addWidget(pgw)
        iv.addStretch(); sa.setWidget(inner); v.addWidget(sa,1)
        self._refresh_vis()
        self._pt_calc_stats()
        self._recalc_weight()

    def _cbtn_ss(self):
        return (f"background:{PANEL.name()};color:{TPRI.name()};"
                f"border:1px solid {BORDER.name()};border-left:5px solid {self._color.name()};"
                f"border-radius:4px;font-family:'Segoe UI';font-size:9px;"
                f"text-align:left;padding-left:6px;")
    def _pick_color(self):
        c=QColorDialog.getColor(self._color,self,tr("pt_color"))
        if c.isValid(): self._set_color(c)
    def _set_color(self,c):
        self._color=c; self._color_btn.setStyleSheet(self._cbtn_ss()); self._hex_in.setText(c.name())
        if self._view: self._view.set_color(c)
        if self._dirty_cb: self._dirty_cb()
    def _hex_changed(self):
        txt=self._hex_in.text().strip()
        if not txt.startswith("#"): txt="#"+txt
        c=QColor(txt)
        if c.isValid(): self._set_color(c)
        else: self._hex_in.setText(self._color.name())
    def _pt_calc_stats(self):
        """Shape + parametre bazlı atk/def/sta hesaplar (max 5, min 0)."""
        shape = self._cur_shape
        length  = self._len_spin.value()
        flat_r  = self._flat_spin.value()
        hole_r  = self._hole_r_spin.value()
        hole_d  = self._hole_d_spin.value()

        # Baz değerler
        base = {
            "sharp":      (0, 1, 4),
            "round":      (0, 5, 2),
            "flat":       (3, 1, 2),
            "sharp_hole": (2, 0, 4),
            "flat_hole":  (4, 0, 2),
        }
        atk, def_, sta = base.get(shape, (0, 0, 0))

        # length: kısa → etkisiz, uzun → sta+1 atk-1
        if length > 3.0:
            sta += 1
            atk -= 1

        # flat_r bonusu: orta = 2.15mm, sadece flat tiplerinde. Büyük → sta-1
        if "flat" in shape:
            if flat_r > 2.15:
                sta -= 1

        # hole bonusları: orta = 1.1mm (0.2–2.0 arası)
        if "hole" in shape:
            if hole_r > 1.1:
                sta -= 1
            else:
                atk -= 1
            if hole_d > 1.1:
                def_ -= 1
            else:
                def_ += 1

        # 0–5 arasında tut
        atk  = max(0, min(6, atk))
        def_ = max(0, min(6, def_))
        sta  = max(0, min(6, sta))

        self._cached_atk = atk
        self._cached_def = def_
        self._cached_sta = sta
        self._pt_upd_atk(atk)
        self._pt_upd_def(def_)
        self._pt_upd_sta(sta)

    def _on_shape(self, key):
        self._cur_shape = key
        for k, b in self._shape_btns.items(): b.setChecked(k == key)
        self._refresh_vis(); self._on_params()

    def _refresh_vis(self):
        is_flat = "flat" in self._cur_shape; is_hole = "hole" in self._cur_shape
        self._flat_sec.setVisible(is_flat); self._flat_row.setVisible(is_flat)
        self._hole_sec.setVisible(is_hole); self._hole_r_row.setVisible(is_hole); self._hole_d_row.setVisible(is_hole)

    def _on_params(self):
        if self._view:
            self._view.set_params(tip_shape=self._cur_shape, tip_length=self._len_spin.value(),
                tip_flat_r=self._flat_spin.value(), tip_hole_r=self._hole_r_spin.value(),
                tip_hole_d=self._hole_d_spin.value())
        self._pt_calc_stats()
        self._recalc_weight()
        if self._dirty_cb: self._dirty_cb()

    def _recalc_weight(self):
        # _double_sided olmadan ham mesh — trimesh için manifold olması lazım
        vu, fu = _pt_top_data()
        raw_tris = _pt_obj_to_tris(vu, fu) + _build_pt_tip(
            shape=self._cur_shape, length=self._len_spin.value(),
            flat_r=self._flat_spin.value(), hole_r=self._hole_r_spin.value(),
            hole_d=self._hole_d_spin.value())
        weight = self._calc_weight_trimesh(raw_tris)
        if weight is None:
            weight = 0.0
        self._cached_weight = weight
        self._weight_lbl.setText(f"{weight:.2f} g")
        if self._weight_cb: self._weight_cb()

    @staticmethod
    def _calc_weight_trimesh(tris):
        try:
            import trimesh, numpy as np
        except ImportError:
            return None
        try:
            verts_list = []; faces_list = []; vert_map = {}
            for tri in tris:
                first = tri[0]
                if isinstance(first, (tuple, list)) and isinstance(first[0], float):
                    vs = [tri[0], tri[1], tri[2]]
                else:
                    vs = [tri[1], tri[2], tri[3]]
                face = []
                for v in vs:
                    key = (round(v[0],5), round(v[1],5), round(v[2],5))
                    if key not in vert_map:
                        vert_map[key] = len(verts_list); verts_list.append(key)
                    face.append(vert_map[key])
                faces_list.append(face)
            mesh = trimesh.Trimesh(vertices=np.array(verts_list), faces=np.array(faces_list), process=True)
            trimesh.repair.fix_normals(mesh)
            try:
                trimesh.repair.fill_holes(mesh)
            except Exception:
                pass
            vol = abs(mesh.volume)
            if vol > 0.001:  # sıfır değilse kullan
                return round(vol / 1000.0 * _ABS_DENSITY, 2)
        except Exception as e:
            import sys; print(f"[PT weight ERROR] {e}", file=sys.stderr)
        return None

    def set_weight_callback(self, cb): self._weight_cb = cb
    def get_weight(self) -> float: return self._cached_weight
    def set_dirty_callback(self,cb): self._dirty_cb=cb
    def load_from(self,data):
        shape=data.get("pt_shape","sharp"); self._on_shape(shape)
        for sp,key,dv in [(self._len_spin,"pt_length",3.0),(self._flat_spin,"pt_flat_r",1.5),
                          (self._hole_r_spin,"pt_hole_r",0.6),(self._hole_d_spin,"pt_hole_d",0.8)]:
            sp.blockSignals(True); sp.setValue(float(data.get(key,dv))); sp.blockSignals(False)
        c=QColor(data.get("pt_color",self._COLOR_DEF))
        if c.isValid(): self._set_color(c)
        self._on_params()
    def get_data(self):
        return {"pt_shape":self._cur_shape,"pt_length":self._len_spin.value(),
                "pt_flat_r":self._flat_spin.value(),"pt_hole_r":self._hole_r_spin.value(),
                "pt_hole_d":self._hole_d_spin.value(),"pt_color":self._color.name()}

# ── FusionWheelPanel ──────────────────────────────────────────
class FusionWheelPanel(QWidget):
    """Fusion Wheel kanat tasarım paneli."""

    def __init__(self, view: "FusionWheelView", parent=None):
        super().__init__(parent)
        self._view     = view
        self._dirty_cb = None
        self._color_blade = QColor(FusionWheelView._BLADE_DEF)
        self.setStyleSheet("background:transparent;")
        self._build()

    # ─────────────────────────────────────────────────────────
    def _build(self):
        from PySide6.QtWidgets import QScrollArea as _SA

        ss_lbl = (f"color:{TSEC.name()};font-family:'Segoe UI';"
                  "font-size:8px;background:transparent;font-weight:600;letter-spacing:1px;")
        ss_val = (f"color:{TPRI.name()};font-family:'Segoe UI';"
                  "font-size:9px;background:transparent;")
        ss_inp = (
            f"QSpinBox,QDoubleSpinBox{{color:{TPRI.name()};font-family:'Segoe UI';font-size:10px;"
            f"background:{PANEL.name()};border:1px solid {BORDER.name()};"
            f"padding:3px 6px;selection-background-color:{ACCENT.name()};selection-color:#fff;}}"
            f"QSpinBox::up-button,QSpinBox::down-button,"
            f"QDoubleSpinBox::up-button,QDoubleSpinBox::down-button{{"
            f"background:{PANEL.name()};border:none;width:16px;}}"
        )
        ss_radio = (
            f"QRadioButton{{color:{TPRI.name()};font-family:'Segoe UI';"
            f"font-size:9px;background:transparent;spacing:5px;}}"
            f"QRadioButton::indicator{{width:12px;height:12px;"
            f"border:1px solid {BORDER.name()};border-radius:6px;background:{PANEL.name()};}}"
            f"QRadioButton::indicator:checked{{background:{ACCENT.name()};border-color:{ACCENT.name()};}}"
        )

        def sec(txt):
            lb = QLabel(txt); lb.setStyleSheet(ss_lbl); return lb

        def row(lbl, w):
            r=QWidget(); r.setStyleSheet("background:transparent;")
            rl=QHBoxLayout(r); rl.setContentsMargins(0,0,0,0); rl.setSpacing(6)
            lb=QLabel(lbl); lb.setFixedWidth(90); lb.setStyleSheet(ss_val)
            rl.addWidget(lb); rl.addWidget(w); return r

        def dspin(lo, hi, step, val, dec=2):
            s=QDoubleSpinBox(); s.setRange(lo,hi); s.setSingleStep(step)
            s.setDecimals(dec); s.setValue(val); s.setStyleSheet(ss_inp); return s

        # ── scroll wrapper ────────────────────────────────────
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0,0,0,0); outer.setSpacing(0)
        sc = _SA(); sc.setWidgetResizable(True)
        sc.setStyleSheet(
            f"QScrollArea{{border:none;background:transparent;}}"
            f"QScrollBar:vertical{{background:{SIDEBAR.name()};width:5px;}}"
            f"QScrollBar::handle:vertical{{background:{BORDER.name()};border-radius:2px;min-height:20px;}}"
            f"QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}"
        )
        inner_w = QWidget(); inner_w.setStyleSheet("background:transparent;")
        v = QVBoxLayout(inner_w)
        v.setContentsMargins(10,10,10,10); v.setSpacing(8)
        sc.setWidget(inner_w); outer.addWidget(sc)

        # ── ORTAK: kanat sayısı ───────────────────────────────
        v.addWidget(sec(tr("blade_count")))
        self._bc = QSpinBox(); self._bc.setRange(1,16); self._bc.setValue(3)
        self._bc.setStyleSheet(ss_inp); self._bc.valueChanged.connect(self._on_count)
        v.addWidget(row(tr("count"), self._bc))

        v.addWidget(hdiv())

        # ── ORTAK: kanat tipi (sadece count>1'de aktif) ───────
        v.addWidget(sec(tr("blade_type")))
        self._type_group  = QButtonGroup(self)
        self._type_radios : dict[str, QRadioButton] = {}
        self._type_widget = QWidget(); self._type_widget.setStyleSheet("background:transparent;")
        tw_lay = QVBoxLayout(self._type_widget)
        tw_lay.setContentsMargins(0,0,0,0); tw_lay.setSpacing(3)
        type_labels = {"wing":"Wing — yumuşak","spike":"Spike — diken","flat":"Flat — düz plaka","blade":"Blade — Dragoon"}
        for key, lbl in type_labels.items():
            rb = QRadioButton(lbl); rb.setStyleSheet(ss_radio)
            rb.setChecked(key=="wing")
            rb.toggled.connect(lambda checked,k=key: self._on_type(k,checked))
            self._type_group.addButton(rb); self._type_radios[key]=rb
            tw_lay.addWidget(rb)
        v.addWidget(self._type_widget)

        v.addWidget(hdiv())

        # ── ORTAK: dış çap / uç incelme / gap ────────────────
        v.addWidget(sec(tr("common")))
        self._depth = dspin(1.0, 25.0, 0.5, 6.0, 1)
        self._depth.valueChanged.connect(self._update)
        v.addWidget(row(tr("length_mm"), self._depth))

        self._taper = dspin(0.0, 1.0, 0.05, 0.0)
        self._taper.valueChanged.connect(self._update)
        v.addWidget(row(tr("tip_taper"), self._taper))

        self._gap = dspin(0.05, 0.70, 0.05, 0.25)
        self._gap.valueChanged.connect(self._update)
        self._gap_row = row(tr("gap_ratio"), self._gap)
        v.addWidget(self._gap_row)

        v.addWidget(hdiv())

        # ── TIP-SPECIFIC ayar grupları ────────────────────────
        def tip_group(widgets_list):
            w = QWidget(); w.setStyleSheet("background:transparent;")
            wl = QVBoxLayout(w); wl.setContentsMargins(0,0,0,0); wl.setSpacing(4)
            for ww in widgets_list: wl.addWidget(ww)
            return w

        # wing
        self._wing_sec = sec(tr("wing_settings"))
        self._wing_camber = dspin(0.0, 0.5, 0.02, 0.10)
        self._wing_camber.valueChanged.connect(self._update)
        self._wing_sweep  = dspin(0.0, 40.0, 1.0, 10.0, 1)
        self._wing_sweep.valueChanged.connect(self._update)
        self._wing_grp = tip_group([
            self._wing_sec,
            row(tr("camber"), self._wing_camber),
            row("Sweep °",  self._wing_sweep),
        ])

        # spike
        self._spike_sec = sec(tr("spike_settings"))
        self._spike_ratio = dspin(0.1, 1.5, 0.05, 0.5)
        self._spike_ratio.valueChanged.connect(self._update)
        self._spike_grp = tip_group([
            self._spike_sec,
            row(tr("base_ratio"), self._spike_ratio),
        ])

        # flat
        self._flat_sec = sec(tr("flat_settings"))
        self._flat_bevel = dspin(0.0, 0.4, 0.02, 0.15)
        self._flat_bevel.valueChanged.connect(self._update)
        self._flat_grp = tip_group([
            self._flat_sec,
            row("Bevel", self._flat_bevel),
        ])

        # blade
        self._blade_sec  = sec(tr("blade_settings"))
        self._blade_sweep_s = dspin(0.0, 50.0, 1.0, 20.0, 1)
        self._blade_sweep_s.valueChanged.connect(self._update)
        self._blade_asym_s  = dspin(0.0, 0.8, 0.05, 0.35)
        self._blade_asym_s.valueChanged.connect(self._update)
        self._blade_grp = tip_group([
            self._blade_sec,
            row("Sweep °", self._blade_sweep_s),
            row(tr("asymmetry"), self._blade_asym_s),
        ])

        for grp in (self._wing_grp, self._spike_grp, self._flat_grp, self._blade_grp):
            v.addWidget(grp)

        v.addWidget(hdiv())
        v.addWidget(sec(tr("weight")))
        wrow = QWidget(); wrow.setStyleSheet("background:transparent;")
        wlay = QHBoxLayout(wrow); wlay.setContentsMargins(10,2,10,2); wlay.setSpacing(4)
        wlbl = QLabel(tr("calculated"))
        wlbl.setStyleSheet(f"color:{TSEC.name()};font-family:'Segoe UI';font-size:9px;background:transparent;font-weight:600;letter-spacing:1px;")
        self._weight_lbl = QLabel("—")
        self._weight_lbl.setStyleSheet(f"color:{TPRI.name()};font-family:'Segoe UI';font-size:10px;font-weight:700;background:transparent;")
        wlay.addWidget(wlbl); wlay.addStretch(); wlay.addWidget(self._weight_lbl)
        v.addWidget(wrow)
        self._weight_cb = None

        v.addWidget(hdiv())
        v.addWidget(sec(tr("part_stats")))
        sb_atk, self._fw_upd_atk = stat_bar_live(tr("attack"),  ATK, max_val=7)
        sb_def, self._fw_upd_def = stat_bar_live(tr("defense"), DEF, max_val=7)
        sb_sta, self._fw_upd_sta = stat_bar_live(tr("stamina"), STA, max_val=7)
        v.addWidget(sb_atk); v.addWidget(sb_def); v.addWidget(sb_sta)

        v.addStretch()

        # Başlangıçta tip gruplarını güncelle
        self._refresh_tip_groups("wing")
        self._refresh_count_ui(3)
        self._recalc_weight()

    # ── görünürlük kontrolü ───────────────────────────────────
    def _refresh_tip_groups(self, active_type: str):
        for key, grp in [("wing",self._wing_grp),("spike",self._spike_grp),
                          ("flat",self._flat_grp),("blade",self._blade_grp)]:
            grp.setVisible(key == active_type)

    def _refresh_count_ui(self, count: int):
        """count==1 → tip seçimi + gap gizle. count 2-4 → sadece wing."""
        single = (count == 1)
        wing_only = (2 <= count <= 4)
        self._type_widget.setVisible(not single)
        self._gap_row.setVisible(not single)
        if single:
            for grp in (self._wing_grp,self._spike_grp,self._flat_grp,self._blade_grp):
                grp.setVisible(False)
        elif wing_only:
            # 2-4 arası sadece wing — diğer radio'ları devre dışı bırak
            for key, rb in self._type_radios.items():
                rb.setEnabled(key == "wing")
            self._type_radios["wing"].setChecked(True)
            self._refresh_tip_groups("wing")
        else:
            # 5+ → hepsini aç
            for rb in self._type_radios.values():
                rb.setEnabled(True)
            self._refresh_tip_groups(
                next((k for k,rb in self._type_radios.items() if rb.isChecked()), "wing")
            )

    # ── event handlers ────────────────────────────────────────
    def _on_count(self, val):
        self._refresh_count_ui(val)
        self._update()

    def _on_type(self, key, checked):
        if checked:
            self._refresh_tip_groups(key)
            self._view.rebuild(blade_type=key)
            if self._dirty_cb: self._dirty_cb()

    def _update(self):
        bt = next((k for k,rb in self._type_radios.items() if rb.isChecked()), "wing")
        self._view.rebuild(
            blade_count  = self._bc.value(),
            blade_type   = bt,
            blade_depth  = self._depth.value(),
            taper        = self._taper.value(),
            gap_frac     = self._gap.value(),
            wing_camber  = self._wing_camber.value(),
            wing_sweep   = self._wing_sweep.value(),
            spike_ratio  = self._spike_ratio.value(),
            flat_bevel   = self._flat_bevel.value(),
            blade_sweep  = self._blade_sweep_s.value(),
            blade_asym   = self._blade_asym_s.value(),
        )
        if self._dirty_cb: self._dirty_cb()
        self._recalc_weight()
    def _color_btn_ss(self):
        return (f"background:{PANEL.name()};color:{TPRI.name()};"
                f"border:1px solid {BORDER.name()};"
                f"border-left:5px solid {self._color_blade.name()};"
                f"border-radius:4px;font-family:'Segoe UI';font-size:9px;"
                f"text-align:left;padding-left:6px;")

    def _recalc_weight(self):
        bc  = self._bc.value()
        dep = self._depth.value()
        weight = round(28.5 + bc * dep * 0.10, 2)
        self._cached_weight = weight
        if hasattr(self, '_weight_lbl'):
            self._weight_lbl.setText(f"{weight:.2f} g")
        if self._weight_cb: self._weight_cb()
        self._recalc_stats(weight)

    def _fw_roundness(self):
        """Mesh vertex'lerinden yuvarlıklık skoru hesaplar (0.0=tam çıkıntılı, 1.0=tam yuvarlak)."""
        try:
            bt = next((k for k,rb in self._type_radios.items() if rb.isChecked()), "wing")
            raw_tris = build_blade_tris(
                blade_count=self._bc.value(), blade_type=bt,
                blade_depth=self._depth.value(), taper=self._taper.value(),
                gap_frac=self._gap.value(), wing_camber=self._wing_camber.value(),
                wing_sweep=self._wing_sweep.value(), spike_ratio=self._spike_ratio.value(),
                flat_bevel=self._flat_bevel.value(), blade_sweep=self._blade_sweep_s.value(),
                blade_asym=self._blade_asym_s.value(),
            )
            import math
            # Tüm vertex'leri XY düzlemine yansıt
            radii = []
            for tri in raw_tris:
                first = tri[0]
                vs = [tri[0],tri[1],tri[2]] if (isinstance(first,(tuple,list)) and isinstance(first[0],float)) else [tri[1],tri[2],tri[3]]
                for v in vs:
                    radii.append(math.sqrt(v[0]**2 + v[1]**2))
            if not radii:
                return 0.5
            r_max = max(radii)
            r_mean = sum(radii) / len(radii)
            # Ortalama/max oranı: 1.0=tam daire, düşükse çıkıntılı
            return r_mean / r_max if r_max > 0 else 0.5
        except Exception:
            return 0.5

    def _recalc_stats(self, weight: float):
        """Yuvarlıklık + ağırlık → atk/def/sta puanları."""
        roundness = self._fw_roundness()   # 0.0–1.0
        # Ağırlık normalize: 28.5g=0.0, 45g=1.0
        w_norm = max(0.0, min(1.0, (weight - 28.5) / 16.5))

        def score3(val):
            """0-1 değeri → 0/1/2/3 puan (3 eşik)."""
            if val >= 0.80: return 3
            if val >= 0.50: return 2
            if val >= 0.20: return 1
            return 0

        # Çıkıntı = yuvarlıklığın tersi
        protrusion = 1.0 - roundness

        # Spike tipi → çıkıntı bonusu (gap şartı yok)
        bt = next((k for k,rb in self._type_radios.items() if rb.isChecked()), "wing")
        if bt == "spike":
            protrusion = min(1.0, protrusion + 0.3)

        atk = 1 + score3(protrusion) + score3(w_norm)
        def_ = 1 + score3(roundness)  + score3(w_norm)
        sta  = 1 + score3(roundness)  + score3(1.0 - w_norm)

        atk  = max(1, min(7, atk))
        def_ = max(1, min(7, def_))
        sta  = max(1, min(7, sta))

        self._cached_atk = atk
        self._cached_def = def_
        self._cached_sta = sta
        self._fw_upd_atk(atk)
        self._fw_upd_def(def_)
        self._fw_upd_sta(sta)

    # ── public API ────────────────────────────────────────────
    def set_dirty_callback(self, cb): self._dirty_cb = cb
    def set_weight_callback(self, cb): self._weight_cb = cb
    def get_weight(self) -> float: return getattr(self, '_cached_weight', 0.0)

    def load_from(self, data: dict):
        bc  = int(data.get("fusion_wheel_blades",3))
        bt  = data.get("fusion_wheel_blade_type","wing")
        dep = float(data.get("fusion_wheel_blade_depth",6.0))
        tap = float(data.get("fusion_wheel_taper",0.0))
        gap = float(data.get("fusion_wheel_gap",0.25))
        wca = float(data.get("fw_wing_camber",0.10))
        wsp = float(data.get("fw_wing_sweep",10.0))
        spr = float(data.get("fw_spike_ratio",0.5))
        fbv = float(data.get("fw_flat_bevel",0.15))
        bsw = float(data.get("fw_blade_sweep",20.0))
        bam = float(data.get("fw_blade_asym",0.35))
        co  = data.get("fusion_wheel_color","")

        for w in (self._bc,self._depth,self._taper,self._gap,
                  self._wing_camber,self._wing_sweep,self._spike_ratio,
                  self._flat_bevel,self._blade_sweep_s,self._blade_asym_s):
            w.blockSignals(True)

        self._bc.setValue(bc)
        self._depth.setValue(dep); self._taper.setValue(tap); self._gap.setValue(gap)
        self._wing_camber.setValue(wca); self._wing_sweep.setValue(wsp)
        self._spike_ratio.setValue(spr); self._flat_bevel.setValue(fbv)
        self._blade_sweep_s.setValue(bsw); self._blade_asym_s.setValue(bam)

        for w in (self._bc,self._depth,self._taper,self._gap,
                  self._wing_camber,self._wing_sweep,self._spike_ratio,
                  self._flat_bevel,self._blade_sweep_s,self._blade_asym_s):
            w.blockSignals(False)

        if bt in self._type_radios:
            self._type_radios[bt].blockSignals(True)
            self._type_radios[bt].setChecked(True)
            self._type_radios[bt].blockSignals(False)

        if co:
            c=QColor(co)
            if c.isValid():
                self._color_blade=c

        self._refresh_tip_groups(bt)
        self._refresh_count_ui(bc)

        self._view.blade_count=bc; self._view.blade_type=bt
        self._view.blade_depth=dep; self._view.taper=tap; self._view.gap_frac=gap
        self._view.wing_camber=wca; self._view.wing_sweep=wsp
        self._view.spike_ratio=spr; self._view.flat_bevel=fbv
        self._view.blade_sweep=bsw; self._view.blade_asym=bam
        if co: self._view.set_color_blade(QColor(co) if QColor(co).isValid() else self._color_blade)
        self._view.invalidate_mesh()
        self._recalc_weight()

    def get_data(self) -> dict:
        bt = next((k for k,rb in self._type_radios.items() if rb.isChecked()),"wing")
        return {
            "fusion_wheel_blades":     self._bc.value(),
            "fusion_wheel_blade_type": bt,
            "fusion_wheel_blade_depth": round(self._depth.value(),1),
            "fusion_wheel_taper":      round(self._taper.value(),3),
            "fusion_wheel_gap":        round(self._gap.value(),3),
            "fw_wing_camber":          round(self._wing_camber.value(),3),
            "fw_wing_sweep":           round(self._wing_sweep.value(),1),
            "fw_spike_ratio":          round(self._spike_ratio.value(),3),
            "fw_flat_bevel":           round(self._flat_bevel.value(),3),
            "fw_blade_sweep":          round(self._blade_sweep_s.value(),1),
            "fw_blade_asym":           round(self._blade_asym_s.value(),3),
            "fusion_wheel_color":      self._color_blade.name(),
        }










# ══════════════════════════════════════════════════════════════
# DIŞA AKTARMA  — OBJ + PNG + ZIP
# ══════════════════════════════════════════════════════════════

def _tris_to_obj_str(tris, object_name="mesh") -> str:
    """(normal,v1,v2,v3) listesini OBJ formatına çevir."""
    lines = [f"# BeiDesignCAD export — {object_name}", f"o {object_name}", ""]
    vert_idx = {}
    verts = []
    normals = []
    faces = []
    vi = 1
    for n, v1, v2, v3 in tris:
        fi = []
        for v in (v1, v2, v3):
            key = (round(v[0],6), round(v[1],6), round(v[2],6))
            if key not in vert_idx:
                vert_idx[key] = vi
                verts.append(key)
                vi += 1
            fi.append(vert_idx[key])
        normals.append(n)
        faces.append((fi[0], fi[1], fi[2], len(normals)))
    for vx, vy, vz in verts:
        lines.append(f"v {vx:.6f} {vy:.6f} {vz:.6f}")
    lines.append("")
    for nx, ny, nz in normals:
        lines.append(f"vn {nx:.6f} {ny:.6f} {nz:.6f}")
    lines.append("")
    for f1, f2, f3, ni in faces:
        lines.append(f"f {f1}//{ni} {f2}//{ni} {f3}//{ni}")
    return "\n".join(lines)


def _mesh_volume_cm3(tris: list) -> float:
    """Kapalı mesh'in hacmini cm³ cinsinden hesaplar (divergence theorem).
    (v1,v2,v3[,n]) ve (n,v1,v2,v3) formatlarını otomatik ayırt eder."""
    vol_mm3 = 0.0
    for tri in tris:
        # İlk eleman float içeriyorsa vertex, aksi halde normal vektörü
        first = tri[0]
        if isinstance(first, (tuple, list)) and isinstance(first[0], float):
            v1, v2, v3 = tri[0], tri[1], tri[2]
        else:
            v1, v2, v3 = tri[1], tri[2], tri[3]
        x1,y1,z1 = v1; x2,y2,z2 = v2; x3,y3,z3 = v3
        vol_mm3 += (x1*(y2*z3 - y3*z2)
                  + x2*(y3*z1 - y1*z3)
                  + x3*(y1*z2 - y2*z1))
    return abs(vol_mm3) / 6.0 / 1000.0   # mm³ → cm³


_ABS_DENSITY   = 1.05   # g/cm³ — enjeksiyon ABS plastiği
_ZAMAK_DENSITY = 6.6    # g/cm³ — zamak (zinc alloy), Metal Fusion FW


def _export_obj_file(tris, object_name, parent_widget):
    """OBJ dosyası kaydet diyalogu."""
    from PySide6.QtWidgets import QFileDialog
    path, _ = QFileDialog.getSaveFileName(
        parent_widget,
        f"{tr('export_win_title')} — {object_name}",
        f"{object_name}.obj",
        "Wavefront OBJ (*.obj)"
    )
    if not path:
        return
    try:
        Path(path).write_text(_tris_to_obj_str(tris, object_name), encoding="utf-8")
    except Exception as e:
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(parent_widget, "Hata", str(e))


def _crop_hexagon_texture(qimage, hex_r=_FB_HEX_R, pad=_FB_TEX_PAD):
    """Kare QImage'ı altıgen maskesiyle kırp, RGBA döndür."""
    from PySide6.QtGui import QPainter, QPolygonF
    from PySide6.QtCore import QPointF
    import math
    img = qimage.convertToFormat(qimage.Format.Format_RGBA8888)
    w, h = img.width(), img.height()
    out = img.__class__(w, h, img.Format.Format_RGBA8888)
    out.fill(0)  # şeffaf
    painter = QPainter(out)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    # 6gen köşeleri (flat-top, 30° rotasyon)
    half = hex_r * (1.0 + pad)
    pts = []
    for i in range(6):
        angle = math.radians(60 * i + 30)
        px = 0.5 + 0.5 * math.cos(angle)
        py = 0.5 + 0.5 * math.sin(angle)
        pts.append(QPointF(px * w, py * h))
    poly = QPolygonF(pts)
    painter.setClipRegion(__import__('PySide6.QtGui', fromlist=['QRegion']).QRegion(
        poly.toPolygon()
    ))
    painter.drawImage(0, 0, img)
    painter.end()
    return out


def _export_fb_texture(fb_view, parent_widget):
    """Face Bolt hexagon texture'ını PNG olarak kaydet."""
    from PySide6.QtWidgets import QFileDialog, QMessageBox
    if fb_view is None or fb_view._texture is None:
        QMessageBox.warning(parent_widget,
            tr("warning"),
            tr("no_texture_fb"))
        return
    path, _ = QFileDialog.getSaveFileName(
        parent_widget,
        tr("export_label"),
        "face_bolt_label.png",
        "PNG (*.png)"
    )
    if not path:
        return
    try:
        cropped = _crop_hexagon_texture(fb_view._texture)
        cropped.save(path, "PNG")
    except Exception as e:
        QMessageBox.critical(parent_widget, "Hata", str(e))


def _export_all_zip(fb_view, er_view, fw_view, st_view, pt_view, parent_widget):
    """5 OBJ + 1 PNG'yi ZIP olarak dışa aktar."""
    import zipfile, io
    from PySide6.QtWidgets import QFileDialog, QMessageBox

    path, _ = QFileDialog.getSaveFileName(
        parent_widget,
        tr("export_all"),
        "beyblade_export.zip",
        "ZIP (*.zip)"
    )
    if not path:
        return

    try:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:

            # 1. Face Bolt OBJ
            fb_tris = _face_bolt_tris()
            zf.writestr("face_bolt.obj", _tris_to_obj_str(fb_tris, "face_bolt"))

            # 2. Face Bolt label PNG
            if fb_view is not None and fb_view._texture is not None:
                import tempfile, os
                cropped = _crop_hexagon_texture(fb_view._texture)
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    tmp_path = tmp.name
                cropped.save(tmp_path, "PNG")
                with open(tmp_path, "rb") as f:
                    zf.writestr("face_bolt_label.png", f.read())
                os.unlink(tmp_path)

            # 3. Energy Ring OBJ
            if er_view is not None and er_view._raw_tris:
                zf.writestr("energy_ring.obj", _tris_to_obj_str(er_view._raw_tris, "energy_ring"))

            # 4. Fusion Wheel OBJ (tinker + blade)
            fw_tris = _tinker_tris()
            if fw_view is not None:
                if fw_view._blade_cache is None:
                    fw_view._get_groups()
                if fw_view._blade_cache:
                    fw_tris = fw_tris + fw_view._blade_cache
            zf.writestr("fusion_wheel.obj", _tris_to_obj_str(fw_tris, "fusion_wheel"))

            # 5. Spin Track OBJ
            if st_view is not None:
                st_tris = _st_tris(st_view.conn_h)
                zf.writestr("spin_track.obj", _tris_to_obj_str(st_tris, "spin_track"))

            # 6. Performance Tip OBJ
            if pt_view is not None:
                pt_tris = _pt_tris(pt_view.tip_shape, pt_view.tip_length,
                                   pt_view.tip_flat_r, pt_view.tip_hole_r,
                                   pt_view.tip_hole_d)
                zf.writestr("performance_tip.obj", _tris_to_obj_str(pt_tris, "performance_tip"))

        Path(path).write_bytes(buf.getvalue())
        QMessageBox.information(parent_widget,
            tr("done"),
            f"{tr('exported_msg')}: {Path(path).name}")

    except Exception as e:
        import traceback
        QMessageBox.critical(parent_widget, "Hata", traceback.format_exc())


def _export_btn(label, callback, parent):
    """Küçük dışa aktarma butonu."""
    btn = QPushButton(label, parent)
    btn.setFixedHeight(22)
    btn.setStyleSheet(
        f"QPushButton{{background:{PANEL.name()};color:{TPRI.name()};"
        f"border:1px solid {BORDER.name()};border-radius:3px;"
        f"font-family:'Segoe UI';font-size:8px;padding:0 6px;}}"
        f"QPushButton:hover{{border-color:{ACCENT.name()};color:{ACCENT.name()};}}"
    )
    btn.clicked.connect(callback)
    return btn


def make_center(series_id):
    w = QWidget(); w.setMinimumWidth(280)
    w.setStyleSheet(f"background:{BG.name()};")
    v = QVBoxLayout(w); v.setContentsMargins(0,0,0,0); v.setSpacing(0)

    if series_id == "beigoma":
        v.addWidget(sec_header(tr("view_3d")))
        view = BeigomaView(); v.addWidget(view, 1)
        _timer = QTimer(w); _timer.timeout.connect(view._spin); _timer.start(30)
        return w, view, None, None, None, None, None

    # hybrid_wheel: Face Bolt + Energy Ring + Fusion Wheel 3D + parça listesi
    fb_view = FaceBoltView()
    fb_view.setFixedHeight(200)
    v.addWidget(sec_header(tr("fb_3d_view")))
    v.addWidget(fb_view)
    # FB export butonları
    fb_btn_row = QWidget(); fb_btn_row.setStyleSheet("background:transparent;")
    fb_btn_lay = QHBoxLayout(fb_btn_row); fb_btn_lay.setContentsMargins(4,2,4,2); fb_btn_lay.setSpacing(4)
    fb_btn_lay.addWidget(_export_btn("⬇ OBJ", lambda: _export_obj_file(_face_bolt_tris(), "face_bolt", w), w))
    fb_btn_lay.addWidget(_export_btn(tr("png_label"),
                                     lambda: _export_fb_texture(fb_view, w), w))
    fb_btn_lay.addStretch()
    v.addWidget(fb_btn_row)
    v.addWidget(hdiv())

    er_view = EnergyRingView()
    er_view.setFixedHeight(200)
    v.addWidget(sec_header(tr("er_3d_view")))
    v.addWidget(er_view)
    er_btn_row = QWidget(); er_btn_row.setStyleSheet("background:transparent;")
    er_btn_lay = QHBoxLayout(er_btn_row); er_btn_lay.setContentsMargins(4,2,4,2); er_btn_lay.setSpacing(4)
    er_btn_lay.addWidget(_export_btn("⬇ OBJ",
        lambda: _export_obj_file(er_view._raw_tris if er_view._raw_tris else [], "energy_ring", w), w))
    er_btn_lay.addStretch()
    v.addWidget(er_btn_row)
    v.addWidget(hdiv())

    fw_view = FusionWheelView()
    fw_view.setFixedHeight(200)
    v.addWidget(sec_header(tr("fw_3d_view")))
    v.addWidget(fw_view)
    def _fw_export():
        tris = _tinker_tris()
        if fw_view._blade_cache is None: fw_view._get_groups()
        if fw_view._blade_cache: tris = tris + fw_view._blade_cache
        _export_obj_file(tris, "fusion_wheel", w)
    fw_btn_row = QWidget(); fw_btn_row.setStyleSheet("background:transparent;")
    fw_btn_lay = QHBoxLayout(fw_btn_row); fw_btn_lay.setContentsMargins(4,2,4,2); fw_btn_lay.setSpacing(4)
    fw_btn_lay.addWidget(_export_btn("⬇ OBJ", _fw_export, w))
    fw_btn_lay.addStretch()
    v.addWidget(fw_btn_row)
    v.addWidget(hdiv())

    st_view = SpinTrackView()
    st_view.setFixedHeight(200)
    v.addWidget(sec_header(tr("st_3d_view")))
    v.addWidget(st_view)
    st_btn_row = QWidget(); st_btn_row.setStyleSheet("background:transparent;")
    st_btn_lay = QHBoxLayout(st_btn_row); st_btn_lay.setContentsMargins(4,2,4,2); st_btn_lay.setSpacing(4)
    st_btn_lay.addWidget(_export_btn("⬇ OBJ",
        lambda: _export_obj_file(_st_tris(st_view.conn_h), "spin_track", w), w))
    st_btn_lay.addStretch()
    v.addWidget(st_btn_row)
    v.addWidget(hdiv())

    pt_view = PerformanceTipView()
    pt_view.setFixedHeight(200)
    v.addWidget(sec_header(tr("pt_3d_view")))
    v.addWidget(pt_view)
    def _pt_export():
        tris = _pt_tris(pt_view.tip_shape, pt_view.tip_length,
                        pt_view.tip_flat_r, pt_view.tip_hole_r, pt_view.tip_hole_d)
        _export_obj_file(tris, "performance_tip", w)
    pt_btn_row = QWidget(); pt_btn_row.setStyleSheet("background:transparent;")
    pt_btn_lay = QHBoxLayout(pt_btn_row); pt_btn_lay.setContentsMargins(4,2,4,2); pt_btn_lay.setSpacing(4)
    pt_btn_lay.addWidget(_export_btn("⬇ OBJ", _pt_export, w))
    pt_btn_lay.addStretch()
    v.addWidget(pt_btn_row)
    v.addWidget(hdiv())

    print("[GL] make_center: tüm view'lar oluşturuldu, timer başlatılıyor")
    # ── Merkezi timer: 5 ayrı timer yerine tek 33ms timer ────────
    def _central_tick():
        fb_view._on_tick()
        er_view._tick()
        fw_view._tick()
        st_view._tick()
        pt_view._tick()
    _ctimer = QTimer(w)
    _ctimer.timeout.connect(_central_tick)
    _ctimer.start(33)   # ~30 fps — 5 ayrı 30ms timer yerine 1 timer

    # Dışarıdan preview tick bağlamak için callback desteği
    w._add_tick = lambda fn: _ctimer.timeout.connect(fn)

    return w, None, fb_view, er_view, fw_view, st_view, pt_view


def make_right_with_panel(series_id, primary_view=None, face_bolt_view=None, energy_ring_view=None, fusion_wheel_view=None, spin_track_view=None, perf_tip_view=None):
    """(widget, fb_panel_or_None, er_panel_or_None, fw_panel_or_None) döndürür."""
    w = QWidget(); w.setMinimumWidth(180)
    w.setStyleSheet(f"background:{SIDEBAR.name()};border-left:1px solid {BORDER.name()};")
    v = QVBoxLayout(w); v.setContentsMargins(0,0,0,0); v.setSpacing(0)
    fb_panel = None
    er_panel = None
    fw_panel = None
    st_panel = None
    pt_panel = None

    if series_id == "beigoma":
        v.addWidget(sec_header(tr("design_cfg")))
        fb_panel = BeigomaPanel(primary_view)
        v.addWidget(fb_panel, 1)

    elif series_id == "hybrid_wheel":
        # Sekmeli panel: Face Bolt | Energy Ring | Fusion Wheel | Spin Track | Perf. Tip
        tabs = QTabWidget()
        tabs.setStyleSheet(
            f"QTabWidget::pane{{border:none;background:{SIDEBAR.name()};}}"
            f"QTabBar::tab{{background:{PANEL.name()};color:{TSEC.name()};"
            f"font-family:'Segoe UI';font-size:7px;padding:4px 6px;"
            f"border:1px solid {BORDER.name()};border-bottom:none;border-radius:3px 3px 0 0;}}"
            f"QTabBar::tab:selected{{background:{SIDEBAR.name()};color:{TPRI.name()};"
            f"border-bottom:1px solid {SIDEBAR.name()};}}"
        )
        fb_panel = FaceBoltPanel(face_bolt_view)
        er_panel = EnergyRingPanel(energy_ring_view)
        fw_panel = FusionWheelPanel(fusion_wheel_view) if fusion_wheel_view is not None else None
        st_panel = SpinTrackPanel(spin_track_view) if spin_track_view is not None else None
        pt_panel = PerformanceTipPanel(perf_tip_view) if perf_tip_view is not None else None
        tabs.addTab(fb_panel, "Face Bolt")
        tabs.addTab(er_panel, "Energy Ring")
        if fw_panel is not None:
            tabs.addTab(fw_panel, "Fusion Wheel")
        if st_panel is not None:
            tabs.addTab(st_panel, "Spin Track")
        if pt_panel is not None:
            tabs.addTab(pt_panel, "Perf. Tip")
        v.addWidget(tabs, 1)

    else:
        v.addWidget(sec_header(tr("part_settings")))
        ph = QWidget(); ph.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ph.setStyleSheet(f"background:{BG.name()};")
        lb = QLabel("Parça seçilince\nayarlar burada görünür")
        lb.setAlignment(Qt.AlignCenter)
        lb.setStyleSheet(f"color:{TDIM.name()};font-family:'Segoe UI';font-size:9px;background:transparent;")
        hl = QVBoxLayout(ph); hl.addStretch(); hl.addWidget(lb); hl.addStretch()
        v.addWidget(ph, 3)

    v.addStretch()
    return w, fb_panel, er_panel, fw_panel, st_panel, pt_panel



# ══════════════════════════════════════════════════════════════
# PENCERE
# ══════════════════════════════════════════════════════════════

def _series_label(series_id):
    return {"hybrid_wheel": tr("hws_title"), "beigoma": tr("bgm_title")}.get(series_id, series_id)

class EditorWindow(QMainWindow):
    def __init__(self, proj_path: Path, series_id: str):
        super().__init__()
        self._proj_path = proj_path
        self._series_id = series_id
        self._dirty     = False
        self._panel     = None
        self._fb_panel  = None
        self._er_panel  = None
        self._fw_panel  = None
        self._st_panel  = None
        self._pt_panel  = None

        self.setMinimumSize(900, 560)
        self.resize(1280, 760)
        self._update_title()

        # Dosyayı oku ve doğrula
        file_data = self._load_and_validate(proj_path)
        if file_data is None:
            # Kullanıcı "Vazgeç" dedi — pencere oluşturuldu ama hemen kapanacak
            QTimer.singleShot(0, self.close)
            return

        self._build_ui()

        # Panellere dosyadan değerleri yükle (dirty tetiklememeli)
        for p in (self._fb_panel, self._er_panel, self._fw_panel, self._st_panel, self._pt_panel):
            if p is not None:
                p.load_from(file_data)

        # load_from bittikten sonra dirty/weight callback'lerini bağla
        for p in (self._fb_panel, self._er_panel, self._fw_panel, self._st_panel, self._pt_panel):
            if p is not None:
                p.set_dirty_callback(self._mark_dirty)
        if hasattr(self._fb_panel, 'set_weight_callback') and self._fb_panel:
            self._fb_panel.set_weight_callback(self._refresh_total_weight)
        if hasattr(self._er_panel, 'set_weight_callback') and self._er_panel:
            self._er_panel.set_weight_callback(self._refresh_total_weight)
        if hasattr(self._fw_panel, 'set_weight_callback') and self._fw_panel:
            self._fw_panel.set_weight_callback(self._refresh_total_weight)
        if hasattr(self._st_panel, 'set_weight_callback') and self._st_panel:
            self._st_panel.set_weight_callback(self._refresh_total_weight)
        if hasattr(self._pt_panel, 'set_weight_callback') and self._pt_panel:
            self._pt_panel.set_weight_callback(self._refresh_total_weight)
        self._refresh_total_weight()

        # Ctrl+S kısayolu
        QShortcut(QKeySequence.StandardKey.Save, self, activated=self._save)

    # ── Başlık ────────────────────────────────────────────────
    def _update_title(self):
        marker = " •" if self._dirty else ""
        self.setWindowTitle(f"BeiDesignCAD — {self._proj_path.stem}{marker}")

    # ── Dirty flag ────────────────────────────────────────────
    def _mark_dirty(self):
        if not self._dirty:
            self._dirty = True
            self._update_title()
        # Preview'ı da güncelle
        if hasattr(self, '_preview_view') and self._preview_view is not None:
            self._refresh_preview()

    # ── Dosya oku + doğrula ───────────────────────────────────
    def _load_and_validate(self, path: Path) -> dict | None:
        """
        Dosyayı okur. Hata varsa kullanıcıya Kurtar/Vazgeç sorar.
        Geçerli data dict döner; vazgeçilirse None döner.
        """
        if not path.exists():
            # Yeni dosya — boş data
            return {}

        data   = bei_read(path)
        errors = bei_validate(data)
        if not errors:
            return data

        # Hata var → Kurtar / Vazgeç
        err_text = "\n".join(f"  • {e}" for e in errors)
        msg = QMessageBox(self)
        msg.setWindowTitle(tr("corrupt_title"))
        msg.setText(tr("corrupt_msg").format(errors=err_text))
        msg.setIcon(QMessageBox.Icon.Warning)
        recover_btn = msg.addButton(tr("recover"), QMessageBox.ButtonRole.AcceptRole)
        abort_btn   = msg.addButton(tr("abort"),   QMessageBox.ButtonRole.RejectRole)
        msg.exec()
        if msg.clickedButton() == abort_btn:
            return None

        # Kurtar: geçerli alanları tut, zorunlu eksikleri seri/argüman'dan doldur
        recovered = {k: v for k, v in data.items() if k in ALL_VALID_KEYS}
        if "series" not in recovered:
            recovered["series"] = self._series_id
        if "name" not in recovered:
            recovered["name"] = self._proj_path.stem
        if "created" not in recovered:
            from datetime import datetime
            recovered["created"] = datetime.now().isoformat(timespec="seconds")
        # Dosyayı hemen düzeltilmiş haliyle yaz
        bei_write(self._proj_path, recovered)
        return recovered

    # ── UI inşa ───────────────────────────────────────────────
    def _build_ui(self):
        label = _series_label(self._series_id)
        root  = QWidget()
        root.setStyleSheet(f"background:{BG.name()};")
        self.setCentralWidget(root)
        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(EditorTopBar(self._proj_path.stem, label))
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        print(f"[GL] _build_ui: make_center çağrılıyor, series={self._series_id}")
        center_w, primary_view, fb_view, er_view, fw_view, st_view, pt_view = make_center(self._series_id)
        print("[GL] _build_ui: make_center döndü")

        # ── Birleşik önizleme view ────────────────────────────
        if self._series_id == "hybrid_wheel":
            self._preview_view = BeybladePreviewView()
        else:
            self._preview_view = None

        left_w, self._update_total_weight, self._update_power = make_left(self._series_id, self._preview_view,
            export_all_cb=lambda: _export_all_zip(
                self._fb_view, self._er_view, self._fw_view,
                self._st_view, self._pt_view, self))
        body.addWidget(left_w, 1)
        if self._series_id == "beigoma":
            left_w.hide()
        body.addWidget(center_w, 1)
        right_w, fb_panel, er_panel, fw_panel, st_panel, pt_panel = make_right_with_panel(
            self._series_id, primary_view, fb_view, er_view, fw_view, st_view, pt_view)
        body.addWidget(right_w, 1)
        vbox.addLayout(body, 1)

        self._fb_panel = fb_panel
        self._er_panel = er_panel
        self._fw_panel = fw_panel
        self._st_panel = st_panel
        self._pt_panel = pt_panel
        self._fb_view  = fb_view
        self._er_view  = er_view
        self._fw_view  = fw_view
        self._st_view  = st_view
        self._pt_view  = pt_view
        # Geriye uyumluluk
        self._panel = fb_panel or er_panel or fw_panel

        # Preview'ı başlangıçta güncelle
        if self._preview_view is not None:
            QTimer.singleShot(200, self._refresh_preview)
            if hasattr(center_w, '_add_tick'):
                center_w._add_tick(self._preview_view._on_tick)

    def _refresh_total_weight(self):
        """Tüm parçaların ağırlığını toplayıp sol paneli güncelle."""
        if not hasattr(self, '_update_total_weight') or self._update_total_weight is None:
            return
        total = 0.0
        if self._fb_panel is not None and hasattr(self._fb_panel, 'get_weight'):
            total += self._fb_panel.get_weight()
        if self._er_panel is not None and hasattr(self._er_panel, 'get_weight'):
            total += self._er_panel.get_weight()
        if self._fw_panel is not None and hasattr(self._fw_panel, 'get_weight'):
            total += self._fw_panel.get_weight()
        if self._st_panel is not None and hasattr(self._st_panel, 'get_weight'):
            total += self._st_panel.get_weight()
        if self._pt_panel is not None and hasattr(self._pt_panel, 'get_weight'):
            total += self._pt_panel.get_weight()
        self._update_total_weight(total)

        # Güç puanları — tüm panellerin cached istatistiklerini topla
        if not hasattr(self, '_update_power') or self._update_power is None:
            return

        def _get(panel, key):
            return getattr(panel, key, 0) if panel else 0

        total_atk = (_get(self._er_panel, '_cached_atk') + _get(self._fw_panel, '_cached_atk') +
                     _get(self._st_panel, '_cached_atk') + _get(self._pt_panel, '_cached_atk'))
        total_def = (_get(self._er_panel, '_cached_def') + _get(self._fw_panel, '_cached_def') +
                     _get(self._st_panel, '_cached_def') + _get(self._pt_panel, '_cached_def'))
        total_sta = (_get(self._er_panel, '_cached_sta') + _get(self._fw_panel, '_cached_sta') +
                     _get(self._st_panel, '_cached_sta') + _get(self._pt_panel, '_cached_sta'))
        self._update_power(total_atk, total_def, total_sta)

    def _refresh_preview(self):
        if self._preview_view is None:
            return
        self._preview_view.update_from_panels(
            fb_view=self._fb_view,
            er_view=self._er_view,
            fw_view=self._fw_view,
            st_view=self._st_view,
            pt_view=self._pt_view,
        )

    # ── Kaydet ────────────────────────────────────────────────
    def _save(self):
        data = bei_read(self._proj_path)
        for p in (self._fb_panel, self._er_panel, self._fw_panel, self._st_panel, self._pt_panel):
            if p is not None:
                data.update(p.get_data())
        bei_write(self._proj_path, data)
        self._dirty = False
        self._update_title()

    # ── Kapat ─────────────────────────────────────────────────
    def closeEvent(self, event):
        if not self._dirty:
            event.accept()
            return
        msg = QMessageBox(self)
        msg.setWindowTitle(tr("unsaved_title"))
        msg.setText(tr("unsaved_msg").format(name=self._proj_path.stem))
        msg.setIcon(QMessageBox.Icon.Question)
        save_btn   = msg.addButton(tr("save"),       QMessageBox.ButtonRole.AcceptRole)
        nosave_btn = msg.addButton(tr("dont_save"),  QMessageBox.ButtonRole.DestructiveRole)
        cancel_btn = msg.addButton(tr("cancel"),     QMessageBox.ButtonRole.RejectRole)
        msg.setDefaultButton(save_btn)
        msg.exec()
        clicked = msg.clickedButton()
        if clicked == save_btn:
            self._save()
            event.accept()
        elif clicked == nosave_btn:
            event.accept()
        else:
            event.ignore()




# ══════════════════════════════════════════════════════════════
# BEİDESİGNCAD — Birleşik Giriş Noktası
# ══════════════════════════════════════════════════════════════

def _apply_gpu_env():
    """GPU/renderer ortam değişkenlerini QApplication'dan ÖNCE set eder."""
    import platform
    _os = platform.system()
    if _os == "Windows":
        os.environ.setdefault("QT_OPENGL",         "desktop")
        os.environ.setdefault("QT_ANGLE_PLATFORM",  "d3d11")
        os.environ.setdefault("SHIM_MCCOMPAT",      "0x800000001")
    elif _os == "Linux":
        os.environ.setdefault("QT_OPENGL",              "desktop")
        os.environ.setdefault("LIBGL_ALWAYS_SOFTWARE",  "0")
        os.environ.setdefault("MESA_GL_VERSION_OVERRIDE","3.3")
    elif _os == "Darwin":
        os.environ.setdefault("QT_OPENGL", "desktop")
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")


def _apply_palette(app):
    """Editor temasına uygun QPalette uygula."""
    from PySide6.QtGui import QPalette
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window,          BG)
    pal.setColor(QPalette.ColorRole.WindowText,      TPRI)
    pal.setColor(QPalette.ColorRole.Base,            PANEL)
    pal.setColor(QPalette.ColorRole.AlternateBase,   SIDEBAR)
    pal.setColor(QPalette.ColorRole.Text,            TPRI)
    pal.setColor(QPalette.ColorRole.ButtonText,      TPRI)
    pal.setColor(QPalette.ColorRole.Button,          PANEL)
    pal.setColor(QPalette.ColorRole.Highlight,       ACCENT)
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    pal.setColor(QPalette.ColorRole.ToolTipBase,     SIDEBAR)
    pal.setColor(QPalette.ColorRole.ToolTipText,     TPRI)
    pal.setColor(QPalette.ColorRole.PlaceholderText, TDIM)
    app.setPalette(pal)


def main():
    _apply_gpu_env()

    settings = load_settings()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("BeiDesignCAD")

    _apply_palette(app)

    window = MainMenu(settings)
    window.show()

    # Renderer tanısı
    try:
        from PySide6.QtGui import QOpenGLContext
        ctx_type = QOpenGLContext.openGLModuleType()
        type_name = {
            QOpenGLContext.LibGL:   "LibGL (natif OpenGL ✓)",
            QOpenGLContext.LibGLES: "LibGLES / ANGLE (yazılımsal olabilir)",
        }.get(ctx_type, f"Bilinmiyor ({ctx_type})")
        print(f"[GPU] OpenGL backend: {type_name}")
    except Exception as e:
        print(f"[GPU] Renderer sorgulanamadı: {e}")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()