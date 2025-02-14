import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QHBoxLayout, QAction, QMenu, QDialog, QFormLayout, QLabel, QLineEdit as QLE
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile, QWebEngineHistory
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


class BrowserTab(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setUrl(QUrl("https://www.google.com"))

    def set_url(self, url):
        self.setUrl(QUrl(url))


class SettingsDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")

        self.history = history

        # Geçmiş listesi
        self.history_list = QLabel(self)
        history_text = "\n".join([item.url().toString() for item in self.history.items()])
        self.history_list.setText(f"İnternet Geçmişi:\n{history_text}")

        # Şifreler kısmı (burada gerçek şifre bilgisi yerine örnek metin var)
        self.passwords_label = QLabel("Şifreler:\n(Şifreler şu anda gösterilmiyor)", self)

        form_layout = QFormLayout()
        form_layout.addRow("Geçmiş:", self.history_list)
        form_layout.addRow("Şifreler:", self.passwords_label)

        self.setLayout(form_layout)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Galipinium")
        self.setGeometry(100, 100, 1200, 800)

        self.browser_tabs = QTabWidget()
        self.browser_tabs.setTabsClosable(True)
        self.browser_tabs.tabCloseRequested.connect(self.close_tab)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("URL veya Arama Yapın...")
        self.url_input.returnPressed.connect(self.load_url)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.browser_tabs)

        self.main_widget = QWidget(self)
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.add_new_tab()  # Başlangıçta yeni bir sekme ekleyin

        # Ayarlar menüsü
        self.settings_menu = self.create_settings_menu()

        self.show()

    def add_new_tab(self):
        new_tab = BrowserTab()
        tab_index = self.browser_tabs.addTab(new_tab, "Google")
        self.browser_tabs.setCurrentIndex(tab_index)

    def load_url(self):
        url = self.url_input.text()
        current_tab = self.browser_tabs.currentWidget()
        if current_tab:
            current_tab.set_url(url)

    def close_tab(self, index):
        if self.browser_tabs.count() > 1:
            self.browser_tabs.removeTab(index)
        else:
            self.browser_tabs.currentWidget().setUrl(QUrl("about:blank"))  # Tek sekme kaldığında, sayfayı temizle

    def create_settings_menu(self):
        settings_menu = QMenu("Ayarlar", self)
        
        # Geçmiş ve şifreler için ayarlar
        settings_action = QAction("Ayarlar", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        return settings_menu

    def open_settings(self):
        settings_dialog = SettingsDialog(self.browser_tabs.currentWidget().history(), self)
        settings_dialog.exec_()

    def keyPressEvent(self, event):
        if event.key() == 16777220:  # Enter tuşu
            self.load_url()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        context_menu.addAction(self.settings_menu.menuAction())
        context_menu.exec_(event.globalPos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    sys.exit(app.exec_())
