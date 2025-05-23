import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from fuzzy_kontrol import hesapla_tasarruf

class TasarrufApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enerji Tasarrufu Hesaplama")
        self.setGeometry(300, 300, 500, 400)
        self.setStyleSheet("background-color: #f5f7fa;")

        layout = QVBoxLayout()

        # Başlık
        title = QLabel("🔌 Enerji Tasarrufu Hesaplayıcı")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.labels = [
            "Cihaz Kullanım Süresi (saat):",
            "Günlük Kullanım Sıklığı:",
            "Enerji Kullanımı (Wh):",
            "Mevsim (0:Yaz, 1:Kış, 2:Bahar):",
            "Toplam Enerji Kullanımı (Wh):"
        ]
        
        self.entries = []
        for label_text in self.labels:
            row = QVBoxLayout()
            label = QLabel(label_text)
            label.setFont(QFont("Arial", 11))
            entry = QLineEdit()
            entry.setPlaceholderText("Değer giriniz")
            entry.setStyleSheet("""
                QLineEdit {
                    padding: 8px;
                    border: 1px solid #bdc3c7;
                    border-radius: 6px;
                    background-color: white;
                }
            """)
            row.addWidget(label)
            row.addWidget(entry)
            layout.addLayout(row)
            self.entries.append(entry)

        # Hesapla Butonu
        self.calc_button = QPushButton("HESAPLA")
        self.calc_button.clicked.connect(self.hesapla_sonuclar)
        self.calc_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(self.calc_button)

        self.setLayout(layout)

    def hesapla_sonuclar(self):
        try:
            zaman_val = float(self.entries[0].text())
            kullanma_orani_val = float(self.entries[1].text())
            enerji_val = float(self.entries[2].text())
            mevsim_val = float(self.entries[3].text())
            toplam_enerji_val = float(self.entries[4].text())

            tasarruf, kullanim = hesapla_tasarruf(
                zaman_val, kullanma_orani_val, enerji_val, mevsim_val, toplam_enerji_val, show_graph=True
            )

            QMessageBox.information(
                self, "Sonuçlar",
                f"🔋 Önerilen Enerji Tasarrufu Seviyesi: {tasarruf:.2f}\n"
                f"⏱️ Önerilen Kullanım Süresi: {kullanim:.2f}"
            )
        except ValueError:
            QMessageBox.warning(self, "Hata", "⚠️ Lütfen tüm alanlara geçerli bir sayı giriniz!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TasarrufApp()
    window.show()
    sys.exit(app.exec_())
