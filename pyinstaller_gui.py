"""
PyInstaller GUI - All-in-One Python to EXE Builder
A child-friendly, comprehensive GUI for packaging Python apps.
Requires: pip install PyQt5 pyinstaller pillow
"""

import sys
import os
import json
import subprocess
import threading
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit, QTabWidget,
    QCheckBox, QComboBox, QGroupBox, QScrollArea, QFrame, QSizePolicy,
    QProgressBar, QMessageBox, QListWidget, QListWidgetItem, QSplitter,
    QRadioButton, QButtonGroup, QSpinBox, QStackedWidget, QToolButton,
    QGridLayout, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QPixmap, QIcon, QDragEnterEvent, QDropEvent,
    QPainter, QBrush, QPen, QLinearGradient
)

# ─── PIL import (for PNG→ICO converter) ────────────────────────────────────
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# ══════════════════════════════════════════════════════════════════════════════
#  STYLE SHEET  – bright, friendly, child-readable
# ══════════════════════════════════════════════════════════════════════════════
STYLE = """
QMainWindow, QWidget {
    background-color: #1a1a2e;
    color: #e8e8f0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

/* ── Tab Widget ── */
QTabWidget::pane {
    border: 2px solid #3d3d6b;
    border-radius: 10px;
    background: #16213e;
}
QTabBar::tab {
    background: #0f3460;
    color: #a0a0c8;
    padding: 10px 20px;
    margin: 2px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    min-width: 110px;
}
QTabBar::tab:selected {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #e94560,stop:1 #ff6b6b);
    color: white;
}
QTabBar::tab:hover:!selected { background: #1a4080; color: #e0e0ff; }

/* ── Group Boxes ── */
QGroupBox {
    font-size: 14px;
    font-weight: bold;
    color: #ff9a56;
    border: 2px solid #3d3d6b;
    border-radius: 10px;
    margin-top: 14px;
    padding: 10px;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 6px; }

/* ── Buttons ── */
QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #0f3460,stop:1 #1a4080);
    color: #e8e8ff;
    border: 2px solid #3d3d6b;
    border-radius: 10px;
    padding: 9px 18px;
    font-size: 14px;
    font-weight: bold;
    min-height: 36px;
}
QPushButton:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #e94560,stop:1 #ff6b6b);
    color: white;
    border-color: #ff6b6b;
}
QPushButton:pressed { background: #c73652; }
QPushButton:disabled { background: #2a2a4a; color: #666688; border-color: #2a2a4a; }

QPushButton#big_build_btn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #11998e,stop:1 #38ef7d);
    color: #0d0d1a;
    font-size: 20px;
    font-weight: bold;
    border-radius: 14px;
    padding: 14px 30px;
    min-height: 56px;
    border: none;
}
QPushButton#big_build_btn:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #38ef7d,stop:1 #11998e);
}
QPushButton#big_build_btn:disabled {
    background: #2a4a40;
    color: #668866;
}

QPushButton#danger_btn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #e94560,stop:1 #c73652);
    color: white;
    border: none;
}
QPushButton#danger_btn:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff6b8a,stop:1 #e94560);
}

QPushButton#icon_btn {
    background: #0f3460;
    border: 2px dashed #3d3d6b;
    border-radius: 10px;
    font-size: 13px;
    color: #a0a0c8;
    min-height: 70px;
}
QPushButton#icon_btn:hover { border-color: #e94560; color: #ff9a56; background: #1a2a50; }

/* ── Inputs ── */
QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background: #0d1b3e;
    border: 2px solid #3d3d6b;
    border-radius: 8px;
    color: #e0e0ff;
    padding: 6px 10px;
    font-size: 13px;
    selection-background-color: #e94560;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus { border-color: #e94560; }
QComboBox::drop-down { border: none; padding-right: 8px; }
QComboBox QAbstractItemView {
    background: #0d1b3e; color: #e0e0ff;
    selection-background-color: #e94560;
    border: 2px solid #3d3d6b;
}

/* ── List Widget ── */
QListWidget {
    background: #0d1b3e;
    border: 2px solid #3d3d6b;
    border-radius: 8px;
    color: #e0e0ff;
}
QListWidget::item { padding: 6px 10px; }
QListWidget::item:selected { background: #e94560; border-radius: 4px; }
QListWidget::item:hover:!selected { background: #1a2a5a; }

/* ── CheckBox ── */
QCheckBox { color: #c8c8e8; font-size: 13px; spacing: 8px; }
QCheckBox::indicator { width: 20px; height: 20px; border-radius: 6px; border: 2px solid #3d3d6b; background: #0d1b3e; }
QCheckBox::indicator:checked { background: #e94560; border-color: #e94560; }
QCheckBox::indicator:hover { border-color: #ff6b6b; }

/* ── Radio Button ── */
QRadioButton { color: #c8c8e8; font-size: 13px; spacing: 8px; }
QRadioButton::indicator { width: 18px; height: 18px; border-radius: 9px; border: 2px solid #3d3d6b; background: #0d1b3e; }
QRadioButton::indicator:checked { background: #38ef7d; border-color: #38ef7d; }

/* ── Progress Bar ── */
QProgressBar {
    background: #0d1b3e;
    border: 2px solid #3d3d6b;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
    min-height: 24px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #11998e,stop:1 #38ef7d);
    border-radius: 8px;
}

/* ── ScrollBar ── */
QScrollBar:vertical { background: #0d1b3e; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #3d3d6b; border-radius: 5px; min-height: 20px; }
QScrollBar::handle:vertical:hover { background: #e94560; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ── Labels ── */
QLabel#title_label {
    font-size: 24px;
    font-weight: bold;
    color: #ff9a56;
}
QLabel#subtitle_label {
    font-size: 13px;
    color: #8888aa;
}
QLabel#step_label {
    font-size: 16px;
    font-weight: bold;
    color: #38ef7d;
}
QLabel#emoji_label {
    font-size: 30px;
}
QLabel#status_ok { color: #38ef7d; font-weight: bold; }
QLabel#status_err { color: #e94560; font-weight: bold; }
QLabel#status_warn { color: #ffcc44; font-weight: bold; }

/* ── Separator ── */
QFrame[frameShape="4"], QFrame[frameShape="5"] { color: #3d3d6b; }

/* ── Tool Output ── */
QTextEdit#log_output {
    background: #050d1a;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    color: #7fff7f;
    border: 2px solid #003300;
}

/* ── Splitter ── */
QSplitter::handle { background: #3d3d6b; width: 3px; border-radius: 2px; }

/* ── ToolButton ── */
QToolButton {
    background: #0f3460;
    border: 2px solid #3d3d6b;
    border-radius: 8px;
    padding: 6px 12px;
    color: #e0e0ff;
    font-size: 13px;
}
QToolButton:hover { background: #1a4080; border-color: #e94560; }
"""


# ══════════════════════════════════════════════════════════════════════════════
#  WORKER THREAD  – runs PyInstaller without blocking the UI
# ══════════════════════════════════════════════════════════════════════════════
class BuildWorker(QThread):
    log_line  = pyqtSignal(str)
    progress  = pyqtSignal(int)
    finished  = pyqtSignal(bool, str)

    def __init__(self, cmd, work_dir):
        super().__init__()
        self.cmd = cmd
        self.work_dir = work_dir

    def run(self):
        try:
            self.log_line.emit("▶ Starting build…\n")
            proc = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.work_dir,
                bufsize=1
            )
            keywords = ["INFO:", "WARNING:", "ERROR:", "Appending", "Building",
                        "Collecting", "completed", "successfully"]
            line_count = 0
            for line in proc.stdout:
                self.log_line.emit(line)
                line_count += 1
                # rough progress estimation
                pct = min(90, line_count // 2)
                self.progress.emit(pct)

            proc.wait()
            if proc.returncode == 0:
                self.progress.emit(100)
                self.finished.emit(True, "✅ Build completed successfully!")
            else:
                self.finished.emit(False, f"❌ Build failed (exit code {proc.returncode})")
        except Exception as e:
            self.finished.emit(False, f"❌ Exception: {e}")


# ══════════════════════════════════════════════════════════════════════════════
#  DRAG-DROP FILE BUTTON
# ══════════════════════════════════════════════════════════════════════════════
class DropZone(QPushButton):
    file_dropped = pyqtSignal(str)

    def __init__(self, label, extensions, parent=None):
        super().__init__(label, parent)
        self.extensions = extensions
        self.setAcceptDrops(True)
        self.setObjectName("icon_btn")

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            urls = e.mimeData().urls()
            if any(urls[0].toLocalFile().lower().endswith(ext) for ext in self.extensions):
                e.acceptProposedAction()
                self.setStyleSheet("border-color: #38ef7d; color: #38ef7d;")

    def dragLeaveEvent(self, e):
        self.setStyleSheet("")

    def dropEvent(self, e: QDropEvent):
        self.setStyleSheet("")
        path = e.mimeData().urls()[0].toLocalFile()
        if any(path.lower().endswith(ext) for ext in self.extensions):
            self.file_dropped.emit(path)


# ══════════════════════════════════════════════════════════════════════════════
#  ICON PREVIEW LABEL
# ══════════════════════════════════════════════════════════════════════════════
class IconPreview(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(80, 80)
        self.setAlignment(Qt.AlignCenter)
        self._draw_empty()

    def _draw_empty(self):
        pix = QPixmap(80, 80)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setPen(QPen(QColor("#3d3d6b"), 2, Qt.DashLine))
        p.setBrush(QColor("#0d1b3e"))
        p.drawRoundedRect(4, 4, 72, 72, 8, 8)
        p.setPen(QColor("#3d3d6b"))
        p.setFont(QFont("Arial", 22))
        p.drawText(pix.rect(), Qt.AlignCenter, "🖼")
        p.end()
        self.setPixmap(pix)

    def set_icon(self, path):
        pix = QPixmap(path).scaled(72, 72, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pix)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN WINDOW
# ══════════════════════════════════════════════════════════════════════════════
class PyInstallerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 PyPackager – Python → EXE Builder")
        self.setMinimumSize(920, 700)
        self.resize(1060, 780)
        self.setStyleSheet(STYLE)

        # state
        self._main_script = ""
        self._extra_files = []   # list of (src, dest_folder) tuples
        self._icon_path   = ""
        self._worker      = None
        self._build_dir   = ""

        self._build_ui()
        self._check_tools()

    # ── TOP-LEVEL LAYOUT ────────────────────────────────────────────────────
    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        vbox = QVBoxLayout(root)
        vbox.setContentsMargins(16, 12, 16, 12)
        vbox.setSpacing(10)

        # header
        vbox.addWidget(self._make_header())

        # tool-status bar
        self._status_bar = self._make_status_bar()
        vbox.addWidget(self._status_bar)

        # tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        vbox.addWidget(self.tabs, 1)

        # ── Tab 1: Build ──
        self.tabs.addTab(self._make_build_tab(),   "🏗️  Build")
        # ── Tab 2: Advanced ──
        self.tabs.addTab(self._make_advanced_tab(),"⚙️  Options")
        # ── Tab 3: PNG → ICO ──
        self.tabs.addTab(self._make_ico_tab(),     "🎨  PNG → ICO")
        # ── Tab 4: Log ──
        self.tabs.addTab(self._make_log_tab(),     "📋  Build Log")
        # ── Tab 5: Help ──
        self.tabs.addTab(self._make_help_tab(),    "❓  Help")

        # big BUILD button + progress at bottom
        vbox.addWidget(self._make_build_footer())

    # ─────────────────────────────────────────────────────────────────────────
    def _make_header(self):
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)

        emoji = QLabel("🚀")
        emoji.setObjectName("emoji_label")
        h.addWidget(emoji)

        col = QVBoxLayout()
        col.setSpacing(2)
        title = QLabel("PyPackager")
        title.setObjectName("title_label")
        sub = QLabel("Turn your Python scripts into standalone .exe files — no coding needed!")
        sub.setObjectName("subtitle_label")
        col.addWidget(title)
        col.addWidget(sub)
        h.addLayout(col)
        h.addStretch()

        # version badge
        badge = QLabel("v1.0")
        badge.setStyleSheet("background:#e94560;color:white;font-weight:bold;border-radius:8px;padding:4px 10px;")
        h.addWidget(badge)
        return w

    def _make_status_bar(self):
        w = QWidget()
        w.setStyleSheet("background:#0a0f2a;border-radius:8px;")
        h = QHBoxLayout(w)
        h.setContentsMargins(12, 6, 12, 6)

        self._lbl_pyinstaller = self._status_label("PyInstaller")
        self._lbl_python      = self._status_label("Python")
        self._lbl_pillow      = self._status_label("Pillow (PNG→ICO)")

        for lbl in (self._lbl_pyinstaller, self._lbl_python, self._lbl_pillow):
            h.addWidget(lbl)
            h.addSpacing(20)
        h.addStretch()
        return w

    def _status_label(self, name):
        lbl = QLabel(f"⬤ {name}: checking…")
        lbl.setObjectName("status_warn")
        return lbl

    # ─── BUILD TAB ──────────────────────────────────────────────────────────
    def _make_build_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        w = QWidget()
        scroll.setWidget(w)
        v = QVBoxLayout(w)
        v.setSpacing(14)

        # ── Step 1: Main script ──
        g1 = QGroupBox("  Step 1 ▸ Choose your main Python file  🐍")
        g1l = QVBoxLayout(g1)

        lbl1 = QLabel("This is the .py file you want to turn into an EXE (the one with if __name__ == '__main__':).")
        lbl1.setWordWrap(True)
        lbl1.setStyleSheet("color:#a0a0c8;")
        g1l.addWidget(lbl1)

        row = QHBoxLayout()
        self._entry_main = QLineEdit()
        self._entry_main.setPlaceholderText("📂  Click 'Browse' or drag-and-drop your .py file here…")
        self._entry_main.textChanged.connect(self._on_main_changed)
        row.addWidget(self._entry_main)

        btn_browse = QPushButton("📂 Browse")
        btn_browse.clicked.connect(self._browse_main)
        row.addWidget(btn_browse)
        g1l.addLayout(row)

        self._drop_main = DropZone("🐍 Or drag & drop your .py file here", [".py"])
        self._drop_main.setFixedHeight(70)
        self._drop_main.clicked.connect(self._browse_main)
        self._drop_main.file_dropped.connect(self._set_main_script)
        g1l.addWidget(self._drop_main)
        v.addWidget(g1)

        # ── Step 2: Output name ──
        g2 = QGroupBox("  Step 2 ▸ Name your EXE  💾")
        g2l = QVBoxLayout(g2)
        lbl2 = QLabel("What should the .exe file be called? (Don't add .exe — it's added automatically)")
        lbl2.setWordWrap(True)
        lbl2.setStyleSheet("color:#a0a0c8;")
        g2l.addWidget(lbl2)
        self._entry_name = QLineEdit()
        self._entry_name.setPlaceholderText("e.g.  MyAwesomeApp")
        g2l.addWidget(self._entry_name)
        v.addWidget(g2)

        # ── Step 3: Single vs Multi-file ──
        g3 = QGroupBox("  Step 3 ▸ Project type  📁")
        g3l = QVBoxLayout(g3)
        lbl3 = QLabel("Does your project use multiple .py files, images, or other resources?")
        lbl3.setWordWrap(True)
        lbl3.setStyleSheet("color:#a0a0c8;")
        g3l.addWidget(lbl3)

        rrow = QHBoxLayout()
        self._radio_single = QRadioButton("🗒️  Single-file project  (just one .py)")
        self._radio_multi  = QRadioButton("📦  Multi-file project  (multiple .py files and/or other files)")
        self._radio_single.setChecked(True)
        self._radio_single.toggled.connect(self._toggle_multi_panel)
        rrow.addWidget(self._radio_single)
        rrow.addWidget(self._radio_multi)
        rrow.addStretch()
        g3l.addLayout(rrow)

        # multi-file panel (hidden initially)
        self._multi_panel = QWidget()
        mp = QVBoxLayout(self._multi_panel)
        mp.setContentsMargins(0, 8, 0, 0)

        mp_lbl = QLabel("Add any extra files your program needs (other .py files, images, data files, etc.):")
        mp_lbl.setStyleSheet("color:#a0a0c8;")
        mp.addWidget(mp_lbl)

        mp_row = QHBoxLayout()
        self._list_extras = QListWidget()
        self._list_extras.setFixedHeight(120)
        mp_row.addWidget(self._list_extras)

        mp_btn_col = QVBoxLayout()
        btn_add_extra = QPushButton("➕ Add File")
        btn_add_extra.clicked.connect(self._add_extra_file)
        btn_rem_extra = QPushButton("🗑 Remove")
        btn_rem_extra.setObjectName("danger_btn")
        btn_rem_extra.clicked.connect(self._remove_extra_file)
        btn_add_folder = QPushButton("📁 Add Folder")
        btn_add_folder.clicked.connect(self._add_extra_folder)
        mp_btn_col.addWidget(btn_add_extra)
        mp_btn_col.addWidget(btn_rem_extra)
        mp_btn_col.addWidget(btn_add_folder)
        mp_btn_col.addStretch()
        mp_row.addLayout(mp_btn_col)
        mp.addLayout(mp_row)

        tip = QLabel("💡 Tip: For multiple .py files, PyInstaller finds them automatically if you select the MAIN file in Step 1!")
        tip.setWordWrap(True)
        tip.setStyleSheet("color:#ffcc44;font-style:italic;")
        mp.addWidget(tip)

        g3l.addWidget(self._multi_panel)
        self._multi_panel.setVisible(False)
        v.addWidget(g3)

        # ── Step 4: Icon ──
        g4 = QGroupBox("  Step 4 ▸ Choose an icon (optional)  🖼️")
        g4l = QHBoxLayout(g4)
        lbl4_col = QVBoxLayout()
        lbl4 = QLabel("Give your EXE a custom icon!  Use the PNG→ICO tab to convert a PNG first.")
        lbl4.setWordWrap(True)
        lbl4.setStyleSheet("color:#a0a0c8;")
        lbl4_col.addWidget(lbl4)
        row4 = QHBoxLayout()
        self._entry_icon = QLineEdit()
        self._entry_icon.setPlaceholderText("📂  Select a .ico file…")
        self._entry_icon.textChanged.connect(self._on_icon_changed)
        row4.addWidget(self._entry_icon)
        btn_ico = QPushButton("📂 Browse")
        btn_ico.clicked.connect(self._browse_icon)
        row4.addWidget(btn_ico)
        btn_clear_ico = QPushButton("✖")
        btn_clear_ico.setFixedWidth(36)
        btn_clear_ico.setToolTip("Clear icon")
        btn_clear_ico.clicked.connect(lambda: self._entry_icon.clear())
        row4.addWidget(btn_clear_ico)
        lbl4_col.addLayout(row4)

        drop_ico = DropZone("🖼️ Drag & drop .ico file here", [".ico"])
        drop_ico.setFixedHeight(58)
        drop_ico.file_dropped.connect(self._set_icon)
        drop_ico.clicked.connect(self._browse_icon)
        lbl4_col.addWidget(drop_ico)
        g4l.addLayout(lbl4_col)

        self._icon_preview = IconPreview()
        g4l.addWidget(self._icon_preview)
        v.addWidget(g4)

        # ── Step 5: Output folder ──
        g5 = QGroupBox("  Step 5 ▸ Output folder  📤")
        g5l = QVBoxLayout(g5)
        lbl5 = QLabel("Where should the finished EXE be saved? (Leave blank to use the same folder as your script)")
        lbl5.setWordWrap(True)
        lbl5.setStyleSheet("color:#a0a0c8;")
        g5l.addWidget(lbl5)
        row5 = QHBoxLayout()
        self._entry_out = QLineEdit()
        self._entry_out.setPlaceholderText("e.g.  C:\\MyApps\\dist   (optional)")
        row5.addWidget(self._entry_out)
        btn_out = QPushButton("📂 Browse")
        btn_out.clicked.connect(self._browse_output)
        row5.addWidget(btn_out)
        g5l.addLayout(row5)
        v.addWidget(g5)

        v.addStretch()
        return scroll

    # ─── ADVANCED TAB ───────────────────────────────────────────────────────
    def _make_advanced_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        w = QWidget()
        scroll.setWidget(w)
        v = QVBoxLayout(w)
        v.setSpacing(14)

        # ── Bundle mode ──
        g1 = QGroupBox("  📦 Bundle Mode")
        g1l = QVBoxLayout(g1)
        self._chk_onefile = QCheckBox("📄 One-File Mode  —  pack everything into a single .exe\n"
                                      "       (easier to share, but opens a little slower)")
        self._chk_onefile.setChecked(True)
        g1l.addWidget(self._chk_onefile)
        v.addWidget(g1)

        # ── Window mode ──
        g2 = QGroupBox("  🪟 Window / Console")
        g2l = QVBoxLayout(g2)
        lbl = QLabel("Does your program show windows (GUI app) or print text in a terminal?")
        lbl.setStyleSheet("color:#a0a0c8;")
        g2l.addWidget(lbl)
        self._radio_windowed = QRadioButton("🖼️  Windowed  —  no black terminal window  (for GUI apps: Tkinter, PyQt, etc.)")
        self._radio_console  = QRadioButton("💻  Console   —  show the black terminal window  (for scripts that print output)")
        self._radio_windowed.setChecked(True)
        g2l.addWidget(self._radio_windowed)
        g2l.addWidget(self._radio_console)
        v.addWidget(g2)

        # ── UPX compression ──
        g3 = QGroupBox("  🗜️ Compression (UPX)")
        g3l = QVBoxLayout(g3)
        self._chk_upx = QCheckBox("Enable UPX compression  (makes the EXE smaller, but UPX must be installed separately)")
        self._chk_upx_exclude = QCheckBox("Exclude common DLLs from UPX  (can fix crashes on some systems)")
        g3l.addWidget(self._chk_upx)
        g3l.addWidget(self._chk_upx_exclude)
        v.addWidget(g3)

        # ── Hidden imports ──
        g4 = QGroupBox("  🔍 Hidden Imports  (advanced)")
        g4l = QVBoxLayout(g4)
        lbl4 = QLabel("If your EXE crashes with 'ModuleNotFoundError', add the missing module names here\n"
                       "(one per line, e.g.  pkg_resources  or  cv2):")
        lbl4.setWordWrap(True)
        lbl4.setStyleSheet("color:#a0a0c8;")
        g4l.addWidget(lbl4)
        self._txt_hidden = QTextEdit()
        self._txt_hidden.setPlaceholderText("e.g.\npkg_resources\ncv2\npydantic")
        self._txt_hidden.setFixedHeight(100)
        g4l.addWidget(self._txt_hidden)
        v.addWidget(g4)

        # ── Data files ──
        g5 = QGroupBox("  📂 Extra Data Files / Folders  (advanced)")
        g5l = QVBoxLayout(g5)
        lbl5 = QLabel("Manually specify --add-data entries (src:dest).  "
                       "For most cases the 'Multi-file project' option in Build tab is easier.")
        lbl5.setWordWrap(True)
        lbl5.setStyleSheet("color:#a0a0c8;")
        g5l.addWidget(lbl5)
        self._txt_data = QTextEdit()
        self._txt_data.setPlaceholderText("e.g.\nC:\\myapp\\images;images\nC:\\myapp\\data;data")
        self._txt_data.setFixedHeight(90)
        g5l.addWidget(self._txt_data)
        v.addWidget(g5)

        # ── App version / metadata ──
        g6 = QGroupBox("  ℹ️ App Metadata  (optional — shows in Properties › Details)")
        g6l = QGridLayout(g6)
        labels = ["Product name:", "Company name:", "Version:", "Description:"]
        self._meta_name = QLineEdit()
        self._meta_name.setPlaceholderText("My Awesome App")
        self._meta_company = QLineEdit()
        self._meta_company.setPlaceholderText("My Company")
        self._meta_version = QLineEdit()
        self._meta_version.setPlaceholderText("1.0.0.0")
        self._meta_desc = QLineEdit()
        self._meta_desc.setPlaceholderText("A great app")
        for i, (lbl, widget) in enumerate(zip(labels, [
                self._meta_name, self._meta_company, self._meta_version, self._meta_desc])):
            g6l.addWidget(QLabel(lbl), i, 0)
            g6l.addWidget(widget, i, 1)
        v.addWidget(g6)

        # ── Extra PyInstaller args ──
        g7 = QGroupBox("  🛠️ Extra Arguments  (for experts)")
        g7l = QVBoxLayout(g7)
        lbl7 = QLabel("Additional command-line arguments passed directly to PyInstaller:")
        lbl7.setStyleSheet("color:#a0a0c8;")
        g7l.addWidget(lbl7)
        self._entry_extra_args = QLineEdit()
        self._entry_extra_args.setPlaceholderText("e.g.  --clean  --log-level DEBUG")
        g7l.addWidget(self._entry_extra_args)
        v.addWidget(g7)

        # ── Clean build ──
        g8 = QGroupBox("  🧹 Build Cache")
        g8l = QHBoxLayout(g8)
        self._chk_clean = QCheckBox("Clean build cache before building  (slower but safer)")
        self._chk_clean.setChecked(True)
        g8l.addWidget(self._chk_clean)
        g8l.addStretch()
        v.addWidget(g8)

        v.addStretch()
        return scroll

    # ─── PNG → ICO TAB ──────────────────────────────────────────────────────
    def _make_ico_tab(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setSpacing(16)

        if not PIL_AVAILABLE:
            warn = QLabel("⚠️  Pillow is not installed.  Run:  pip install pillow\n"
                          "Then restart PyPackager.")
            warn.setStyleSheet("color:#ffcc44;font-size:16px;font-weight:bold;padding:20px;")
            warn.setAlignment(Qt.AlignCenter)
            v.addWidget(warn)
            return w

        # intro
        intro = QLabel("🎨  Convert any PNG image into a Windows icon (.ico) file\n"
                        "Great for giving your EXE a professional look!")
        intro.setStyleSheet("color:#a0a0c8;font-size:14px;")
        intro.setAlignment(Qt.AlignCenter)
        v.addWidget(intro)

        # drop zone
        g1 = QGroupBox("  Step 1 ▸ Choose a PNG image")
        g1l = QVBoxLayout(g1)
        self._ico_drop = DropZone("🖼️ Drag & drop a PNG file here\n(or click to browse)", [".png"])
        self._ico_drop.setFixedHeight(100)
        self._ico_drop.clicked.connect(self._ico_browse_png)
        self._ico_drop.file_dropped.connect(self._ico_set_png)
        g1l.addWidget(self._ico_drop)

        row_src = QHBoxLayout()
        self._ico_entry_png = QLineEdit()
        self._ico_entry_png.setPlaceholderText("Path to your PNG file…")
        self._ico_entry_png.textChanged.connect(self._ico_preview_update)
        row_src.addWidget(self._ico_entry_png)
        btn_ico_browse = QPushButton("📂 Browse")
        btn_ico_browse.clicked.connect(self._ico_browse_png)
        row_src.addWidget(btn_ico_browse)
        g1l.addLayout(row_src)
        v.addWidget(g1)

        # preview + sizes
        g2 = QGroupBox("  Step 2 ▸ Preview & choose sizes")
        g2l = QHBoxLayout(g2)

        # preview
        self._ico_preview_lbl = QLabel()
        self._ico_preview_lbl.setFixedSize(128, 128)
        self._ico_preview_lbl.setAlignment(Qt.AlignCenter)
        self._ico_preview_lbl.setStyleSheet("background:#0d1b3e;border:2px dashed #3d3d6b;border-radius:10px;")
        self._ico_preview_lbl.setText("no image")
        g2l.addWidget(self._ico_preview_lbl)

        # size checkboxes
        size_frame = QGroupBox("Icon sizes to include:")
        size_layout = QVBoxLayout(size_frame)
        self._ico_sizes = {}
        for sz in [16, 32, 48, 64, 128, 256]:
            chk = QCheckBox(f"{sz}×{sz} px")
            chk.setChecked(sz in [16, 32, 48, 256])
            self._ico_sizes[sz] = chk
            size_layout.addWidget(chk)
        g2l.addWidget(size_frame)
        g2l.addStretch()
        v.addWidget(g2)

        # output
        g3 = QGroupBox("  Step 3 ▸ Choose where to save the .ico")
        g3l = QVBoxLayout(g3)
        row_dst = QHBoxLayout()
        self._ico_entry_dst = QLineEdit()
        self._ico_entry_dst.setPlaceholderText("Output .ico file path… (leave blank to save next to the PNG)")
        row_dst.addWidget(self._ico_entry_dst)
        btn_ico_dst = QPushButton("📂 Browse")
        btn_ico_dst.clicked.connect(self._ico_browse_dst)
        row_dst.addWidget(btn_ico_dst)
        g3l.addLayout(row_dst)
        v.addWidget(g3)

        # convert button
        btn_convert = QPushButton("✨ Convert to ICO!")
        btn_convert.setObjectName("big_build_btn")
        btn_convert.clicked.connect(self._ico_convert)
        v.addWidget(btn_convert)

        self._ico_status = QLabel("")
        self._ico_status.setAlignment(Qt.AlignCenter)
        self._ico_status.setObjectName("status_ok")
        v.addWidget(self._ico_status)

        # quick-use button
        self._ico_use_btn = QPushButton("📌 Use this ICO in Build tab")
        self._ico_use_btn.setVisible(False)
        self._ico_use_btn.clicked.connect(self._ico_use_in_build)
        v.addWidget(self._ico_use_btn)

        v.addStretch()
        self._ico_last_output = ""
        return w

    # ─── LOG TAB ────────────────────────────────────────────────────────────
    def _make_log_tab(self):
        w = QWidget()
        v = QVBoxLayout(w)

        # Create the log widget FIRST
        self._log = QTextEdit()
        self._log.setReadOnly(True)
        self._log.setObjectName("log_output")

        bar = QHBoxLayout()
        lbl = QLabel("📋  Build output:")
        bar.addWidget(lbl)
        bar.addStretch()

        btn_copy = QPushButton("📋 Copy all")
        btn_copy.clicked.connect(lambda: QApplication.clipboard().setText(self._log.toPlainText()))

        btn_clear = QPushButton("🗑 Clear")
        btn_clear.setObjectName("danger_btn")
        btn_clear.clicked.connect(self._log.clear)

        btn_open_dist = QPushButton("📂 Open dist folder")
        btn_open_dist.clicked.connect(self._open_dist)

        bar.addWidget(btn_copy)
        bar.addWidget(btn_clear)
        bar.addWidget(btn_open_dist)
        v.addLayout(bar)

        v.addWidget(self._log)
        return w

    # ─── HELP TAB ───────────────────────────────────────────────────────────
    def _make_help_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        w = QWidget()
        scroll.setWidget(w)
        v = QVBoxLayout(w)

        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setStyleSheet("background:#0d1b3e;border:2px solid #3d3d6b;border-radius:10px;color:#c8c8e8;font-size:13px;")
        help_text.setHtml("""
<style>
  h2 { color: #ff9a56; }
  h3 { color: #38ef7d; }
  code { background: #050d1a; color: #7fff7f; padding: 2px 6px; border-radius: 4px; }
  li { margin: 4px 0; }
  p { color: #a0a0c8; }
</style>
<h2>🚀 Welcome to PyPackager!</h2>
<p>PyPackager makes it super easy to turn your Python scripts into Windows .exe files that anyone can run — even if they don't have Python installed.</p>

<h3>📋 Quick Start (3 steps)</h3>
<ol>
  <li><b>Build tab:</b> Select your main <code>.py</code> file → give your EXE a name → hit <b>BUILD!</b></li>
  <li>Wait for the green progress bar to finish.</li>
  <li>Your EXE will be in the <code>dist</code> folder next to your script (or in the folder you chose).</li>
</ol>

<h3>🗒️ Single-file vs Multi-file projects</h3>
<p><b>Single-file:</b> Your whole program is in one <code>.py</code> file. Just pick it and build!<br>
<b>Multi-file:</b> Your program has multiple <code>.py</code> files or uses images/data files. Switch to multi-file mode and add the extra resources.</p>

<h3>🎨 Making an icon</h3>
<ol>
  <li>Go to the <b>PNG → ICO</b> tab.</li>
  <li>Drop in any PNG image (square images look best, e.g. 256×256).</li>
  <li>Click <b>Convert to ICO</b>.</li>
  <li>Click <b>Use this ICO in Build tab</b> to apply it automatically.</li>
</ol>

<h3>⚙️ Common Options</h3>
<ul>
  <li><b>One-File Mode:</b> Packs everything into one <code>.exe</code>. Great for sharing. A bit slower to start.</li>
  <li><b>Windowed:</b> No black console window — use this for GUI programs (Tkinter, PyQt, etc.).</li>
  <li><b>Console:</b> Shows a terminal — use this if your program prints text.</li>
  <li><b>Hidden Imports:</b> If your EXE crashes with <i>"ModuleNotFoundError"</i>, add the module name here.</li>
</ul>

<h3>❓ Troubleshooting</h3>
<ul>
  <li><b>EXE crashes immediately:</b> Switch from Windowed to Console mode and look for error messages.</li>
  <li><b>Missing module error:</b> Add the module to <i>Hidden Imports</i> in the Options tab.</li>
  <li><b>Missing file error:</b> Switch to multi-file project mode and add the missing file.</li>
  <li><b>EXE is huge:</b> This is normal — PyInstaller bundles Python itself. Enable UPX compression to shrink it.</li>
  <li><b>Antivirus flags the EXE:</b> This is a known PyInstaller issue. The EXE is safe, but you may need to add an antivirus exception.</li>
</ul>

<h3>🛠️ Installation Requirements</h3>
<p>Make sure these are installed:</p>
<code>pip install pyinstaller pillow</code>
""")
        v.addWidget(help_text)
        return scroll

    # ─── BUILD FOOTER ───────────────────────────────────────────────────────
    def _make_build_footer(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 4, 0, 0)
        v.setSpacing(8)

        # progress
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setFormat("  Ready to build!")
        self._progress.setFixedHeight(28)
        v.addWidget(self._progress)

        # buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self._btn_build = QPushButton("🔨  BUILD EXE!")
        self._btn_build.setObjectName("big_build_btn")
        self._btn_build.clicked.connect(self._start_build)
        btn_row.addWidget(self._btn_build, 3)

        self._btn_stop = QPushButton("⏹ Stop")
        self._btn_stop.setObjectName("danger_btn")
        self._btn_stop.setEnabled(False)
        self._btn_stop.clicked.connect(self._stop_build)
        btn_row.addWidget(self._btn_stop, 1)

        btn_preset = QPushButton("💾 Save Preset")
        btn_preset.clicked.connect(self._save_preset)
        btn_row.addWidget(btn_preset, 1)

        btn_load = QPushButton("📂 Load Preset")
        btn_load.clicked.connect(self._load_preset)
        btn_row.addWidget(btn_load, 1)

        v.addLayout(btn_row)

        # status label
        self._lbl_build_status = QLabel("Select your Python file and hit BUILD! ✨")
        self._lbl_build_status.setAlignment(Qt.AlignCenter)
        self._lbl_build_status.setStyleSheet("color:#a0a0c8;")
        v.addWidget(self._lbl_build_status)

        return w

    # ══════════════════════════════════════════════════════════════════════════
    #  TOOL CHECK
    # ══════════════════════════════════════════════════════════════════════════
    def _check_tools(self):
        # Python
        pv = sys.version.split()[0]
        self._lbl_python.setText(f"✅ Python {pv}")
        self._lbl_python.setObjectName("status_ok")

        # PyInstaller
        try:
            result = subprocess.run(["pyinstaller", "--version"], capture_output=True, text=True)
            ver = result.stdout.strip()
            self._lbl_pyinstaller.setText(f"✅ PyInstaller {ver}")
            self._lbl_pyinstaller.setObjectName("status_ok")
            self._pyinstaller_ok = True
        except FileNotFoundError:
            self._lbl_pyinstaller.setText("❌ PyInstaller — not found!  Run: pip install pyinstaller")
            self._lbl_pyinstaller.setObjectName("status_err")
            self._pyinstaller_ok = False

        # Pillow
        if PIL_AVAILABLE:
            from PIL import __version__ as pil_ver
            self._lbl_pillow.setText(f"✅ Pillow {pil_ver}")
            self._lbl_pillow.setObjectName("status_ok")
        else:
            self._lbl_pillow.setText("⚠️ Pillow — not found  (PNG→ICO disabled).  Run: pip install pillow")
            self._lbl_pillow.setObjectName("status_warn")

        # force style refresh
        for lbl in (self._lbl_python, self._lbl_pyinstaller, self._lbl_pillow):
            lbl.style().unpolish(lbl)
            lbl.style().polish(lbl)

    # ══════════════════════════════════════════════════════════════════════════
    #  SIGNAL HANDLERS – Build tab
    # ══════════════════════════════════════════════════════════════════════════
    def _browse_main(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select main Python file", "", "Python Files (*.py)")
        if path:
            self._set_main_script(path)

    def _set_main_script(self, path):
        self._entry_main.setText(path)

    def _on_main_changed(self, text):
        self._main_script = text
        if text and not self._entry_name.text():
            self._entry_name.setText(Path(text).stem)

    def _toggle_multi_panel(self, checked):
        self._multi_panel.setVisible(not checked)

    def _add_extra_file(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Add extra files", "", "All Files (*)")
        for p in paths:
            self._list_extras.addItem(f"FILE: {p}")
            self._extra_files.append(("FILE", p))

    def _add_extra_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Add folder")
        if folder:
            self._list_extras.addItem(f"DIR:  {folder}")
            self._extra_files.append(("DIR", folder))

    def _remove_extra_file(self):
        row = self._list_extras.currentRow()
        if row >= 0:
            self._list_extras.takeItem(row)
            del self._extra_files[row]

    def _browse_icon(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select icon file", "", "Icon Files (*.ico)")
        if path:
            self._set_icon(path)

    def _set_icon(self, path):
        self._entry_icon.setText(path)

    def _on_icon_changed(self, text):
        self._icon_path = text
        if text and os.path.isfile(text):
            self._icon_preview.set_icon(text)
        else:
            self._icon_preview._draw_empty()

    def _browse_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder:
            self._entry_out.setText(folder)

    # ══════════════════════════════════════════════════════════════════════════
    #  BUILD LOGIC
    # ══════════════════════════════════════════════════════════════════════════
    def _start_build(self):
        script = self._entry_main.text().strip()
        if not script:
            QMessageBox.warning(self, "Missing file", "Please select your main Python file first! 🐍")
            return
        if not os.path.isfile(script):
            QMessageBox.warning(self, "File not found", f"Can't find:\n{script}")
            return
        if not getattr(self, "_pyinstaller_ok", False):
            QMessageBox.critical(self, "PyInstaller missing",
                "PyInstaller is not installed.\n\nRun this in a terminal:\n\n    pip install pyinstaller")
            return

        cmd = self._build_command(script)
        self._build_dir = os.path.dirname(script) or "."

        self._log.clear()
        self._log.append(f"Command:\n  {' '.join(cmd)}\n{'─'*60}\n")
        self.tabs.setCurrentIndex(3)  # switch to log

        self._btn_build.setEnabled(False)
        self._btn_stop.setEnabled(True)
        self._progress.setValue(0)
        self._progress.setFormat("  Building…  %p%")
        self._lbl_build_status.setText("⏳ Building — please wait…")
        self._lbl_build_status.setStyleSheet("color:#ffcc44;font-weight:bold;")

        self._worker = BuildWorker(cmd, self._build_dir)
        self._worker.log_line.connect(self._append_log)
        self._worker.progress.connect(self._progress.setValue)
        self._worker.finished.connect(self._on_build_done)
        self._worker.start()

    def _build_command(self, script):
        name = self._entry_name.text().strip() or Path(script).stem
        cmd = [sys.executable, "-m", "PyInstaller"]

        if self._chk_onefile.isChecked():
            cmd.append("--onefile")

        if self._radio_windowed.isChecked():
            cmd.append("--windowed")

        if not self._chk_upx.isChecked():
            cmd.append("--noupx")

        if self._chk_clean.isChecked():
            cmd.append("--clean")

        icon = self._entry_icon.text().strip()
        if icon and os.path.isfile(icon):
            cmd += ["--icon", icon]

        out = self._entry_out.text().strip()
        if out:
            cmd += ["--distpath", out]

        cmd += ["--name", name]

        # hidden imports
        for mod in self._txt_hidden.toPlainText().splitlines():
            mod = mod.strip()
            if mod:
                cmd += ["--hidden-import", mod]

        # data files from advanced tab
        for line in self._txt_data.toPlainText().splitlines():
            line = line.strip()
            if line:
                cmd += ["--add-data", line]

        # extra files from multi-file mode
        for kind, path in self._extra_files:
            sep = ";" if sys.platform == "win32" else ":"
            if kind == "FILE":
                dest = "."
                cmd += ["--add-data", f"{path}{sep}{dest}"]
            else:
                name_only = os.path.basename(path)
                cmd += ["--add-data", f"{path}{sep}{name_only}"]

        # version info (Windows only, requires a version file)
        if sys.platform == "win32":
            ver_file = self._maybe_write_version_info()
            if ver_file:
                cmd += ["--version-file", ver_file]

        # extra args
        extra = self._entry_extra_args.text().strip()
        if extra:
            cmd += extra.split()

        cmd.append(script)
        return cmd

    def _maybe_write_version_info(self):
        """Write a PyInstaller version info file if metadata was provided."""
        ver  = self._meta_version.text().strip() or "1.0.0.0"
        pname= self._meta_name.text().strip()
        comp = self._meta_company.text().strip()
        desc = self._meta_desc.text().strip()
        if not any([pname, comp, desc]):
            return None

        parts = [int(x) for x in (ver + ".0.0.0.0").split(".")[:4]]
        content = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({parts[0]},{parts[1]},{parts[2]},{parts[3]}),
    prodvers=({parts[0]},{parts[1]},{parts[2]},{parts[3]}),
    mask=0x3f, flags=0x0, OS=0x4, fileType=0x1, subtype=0x0,
    date=(0,0)
  ),
  kids=[
    StringFileInfo([StringTable('040904B0', [
      StringStruct('CompanyName', '{comp}'),
      StringStruct('FileDescription', '{desc}'),
      StringStruct('FileVersion', '{ver}'),
      StringStruct('ProductName', '{pname}'),
      StringStruct('ProductVersion', '{ver}'),
    ])]),
    VarFileInfo([VarStruct('Translation', [0x0409, 1200])])
  ]
)
"""
        path = os.path.join(self._build_dir, "_version_info.txt")
        with open(path, "w") as f:
            f.write(content)
        return path

    def _append_log(self, text):
        self._log.moveCursor(self._log.textCursor().End)
        self._log.insertPlainText(text)
        self._log.moveCursor(self._log.textCursor().End)

    def _on_build_done(self, success, msg):
        self._btn_build.setEnabled(True)
        self._btn_stop.setEnabled(False)
        self._progress.setFormat(f"  {msg}")
        if success:
            self._lbl_build_status.setText("✅ " + msg)
            self._lbl_build_status.setStyleSheet("color:#38ef7d;font-weight:bold;font-size:15px;")
            QMessageBox.information(self, "Build complete! 🎉",
                f"{msg}\n\nYour EXE is in the 'dist' folder.\n\nCheck the Build Log tab for details.")
        else:
            self._lbl_build_status.setText("❌ " + msg)
            self._lbl_build_status.setStyleSheet("color:#e94560;font-weight:bold;font-size:15px;")
            QMessageBox.critical(self, "Build failed ❌",
                f"{msg}\n\nCheck the Build Log tab for details.\n\n"
                "Tip: switch to Console mode and run the EXE to see error messages.")

    def _stop_build(self):
        if self._worker and self._worker.isRunning():
            self._worker.terminate()
            self._btn_build.setEnabled(True)
            self._btn_stop.setEnabled(False)
            self._lbl_build_status.setText("⏹ Build stopped.")
            self._lbl_build_status.setStyleSheet("color:#ffcc44;")

    def _open_dist(self):
        script = self._entry_main.text().strip()
        out = self._entry_out.text().strip()
        dist = out if out else (os.path.join(os.path.dirname(script), "dist") if script else "")
        if dist and os.path.isdir(dist):
            if sys.platform == "win32":
                os.startfile(dist)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", dist])
            else:
                subprocess.Popen(["xdg-open", dist])
        else:
            QMessageBox.information(self, "Not found", "dist folder not found yet. Build first!")

    # ══════════════════════════════════════════════════════════════════════════
    #  PNG → ICO LOGIC
    # ══════════════════════════════════════════════════════════════════════════
    def _ico_browse_png(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PNG image", "", "PNG Images (*.png)")
        if path:
            self._ico_set_png(path)

    def _ico_set_png(self, path):
        self._ico_entry_png.setText(path)
        self._ico_preview_update(path)

    def _ico_preview_update(self, path=None):
        path = path or self._ico_entry_png.text()
        if path and os.path.isfile(path):
            pix = QPixmap(path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self._ico_preview_lbl.setPixmap(pix)
        else:
            self._ico_preview_lbl.setPixmap(QPixmap())
            self._ico_preview_lbl.setText("no image")

    def _ico_browse_dst(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save ICO file", "", "Icon Files (*.ico)")
        if path:
            if not path.lower().endswith(".ico"):
                path += ".ico"
            self._ico_entry_dst.setText(path)

    def _ico_convert(self):
        src = self._ico_entry_png.text().strip()
        if not src or not os.path.isfile(src):
            self._ico_status.setText("⚠️ Please select a PNG file first!")
            self._ico_status.setObjectName("status_warn")
            return

        dst = self._ico_entry_dst.text().strip()
        if not dst:
            dst = str(Path(src).with_suffix(".ico"))

        sizes = [sz for sz, chk in self._ico_sizes.items() if chk.isChecked()]
        if not sizes:
            self._ico_status.setText("⚠️ Please select at least one size!")
            return

        try:
            img = Image.open(src).convert("RGBA")
            resized = []
            for sz in sorted(sizes):
                resized.append(img.resize((sz, sz), Image.LANCZOS))
            resized[0].save(dst, format="ICO", sizes=[(r.width, r.height) for r in resized],
                            append_images=resized[1:])
            self._ico_status.setText(f"✅ Saved: {dst}")
            self._ico_status.setObjectName("status_ok")
            self._ico_last_output = dst
            self._ico_use_btn.setVisible(True)
        except Exception as e:
            self._ico_status.setText(f"❌ Error: {e}")
            self._ico_status.setObjectName("status_err")

        self._ico_status.style().unpolish(self._ico_status)
        self._ico_status.style().polish(self._ico_status)

    def _ico_use_in_build(self):
        if self._ico_last_output:
            self._entry_icon.setText(self._ico_last_output)
            self.tabs.setCurrentIndex(0)

    # ══════════════════════════════════════════════════════════════════════════
    #  PRESET SAVE / LOAD
    # ══════════════════════════════════════════════════════════════════════════
    def _collect_preset(self):
        return {
            "main_script":    self._entry_main.text(),
            "exe_name":       self._entry_name.text(),
            "icon":           self._entry_icon.text(),
            "output_dir":     self._entry_out.text(),
            "onefile":        self._chk_onefile.isChecked(),
            "windowed":       self._radio_windowed.isChecked(),
            "upx":            self._chk_upx.isChecked(),
            "clean":          self._chk_clean.isChecked(),
            "hidden_imports": self._txt_hidden.toPlainText(),
            "extra_data":     self._txt_data.toPlainText(),
            "extra_args":     self._entry_extra_args.text(),
            "meta_name":      self._meta_name.text(),
            "meta_company":   self._meta_company.text(),
            "meta_version":   self._meta_version.text(),
            "meta_desc":      self._meta_desc.text(),
            "multi_mode":     self._radio_multi.isChecked(),
            "extra_files":    self._extra_files,
        }

    def _apply_preset(self, data):
        self._entry_main.setText(data.get("main_script", ""))
        self._entry_name.setText(data.get("exe_name", ""))
        self._entry_icon.setText(data.get("icon", ""))
        self._entry_out.setText(data.get("output_dir", ""))
        self._chk_onefile.setChecked(data.get("onefile", True))
        if data.get("windowed", True):
            self._radio_windowed.setChecked(True)
        else:
            self._radio_console.setChecked(True)
        self._chk_upx.setChecked(data.get("upx", False))
        self._chk_clean.setChecked(data.get("clean", True))
        self._txt_hidden.setPlainText(data.get("hidden_imports", ""))
        self._txt_data.setPlainText(data.get("extra_data", ""))
        self._entry_extra_args.setText(data.get("extra_args", ""))
        self._meta_name.setText(data.get("meta_name", ""))
        self._meta_company.setText(data.get("meta_company", ""))
        self._meta_version.setText(data.get("meta_version", ""))
        self._meta_desc.setText(data.get("meta_desc", ""))
        if data.get("multi_mode", False):
            self._radio_multi.setChecked(True)
        else:
            self._radio_single.setChecked(True)
        self._extra_files = data.get("extra_files", [])
        self._list_extras.clear()
        for kind, path in self._extra_files:
            self._list_extras.addItem(f"{kind}: {path}")

    def _save_preset(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Preset", "", "JSON (*.json)")
        if path:
            with open(path, "w") as f:
                json.dump(self._collect_preset(), f, indent=2)
            QMessageBox.information(self, "Saved", f"Preset saved to:\n{path}")

    def _load_preset(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Preset", "", "JSON (*.json)")
        if path:
            try:
                with open(path) as f:
                    data = json.load(f)
                self._apply_preset(data)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not load preset:\n{e}")


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PyPackager")
    app.setApplicationVersion("1.0")

    # set app-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    win = PyInstallerGUI()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
