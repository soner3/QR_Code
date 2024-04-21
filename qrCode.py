import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QFileDialog,
)
import qrcode
from PyQt5.QtGui import QIcon, QTextDocument, QPixmap
from PyQt5.QtCore import Qt
import os


STYLE = """
    QPushButton {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 18pt;
    }
    QLineEdit{
        font-family: Arial, Helvetica, sans-serif;
        font-size: 18pt;
        color: black;
    }

"""


class QRCode(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR-Code Generator")
        self.setMinimumSize(1700, 1000)
        self.setWindowIcon(QIcon("Icon.png"))

        # QR-Code
        self.document = QTextDocument()
        self.bild = None

        # Widgets
        self.text_field = QTextEdit()
        self.text_field.setReadOnly(True)
        self.speichern = QPushButton("Speichern")
        self.speichern.setFixedHeight(100)
        self.link_feld = QLineEdit()
        self.link_feld.setFixedHeight(100)
        self.link_feld.setPlaceholderText("Link Eingeben")
        self.qr_code_button = QPushButton("QR-Code Generieren")
        self.qr_code_button.setFixedHeight(100)
        self.delete = QPushButton("Alle Felder Löschen")
        self.delete.setFixedHeight(100)

        # Layout
        self.vbox_links = QVBoxLayout()
        self.vbox_rechts = QVBoxLayout()
        self.hbox = QHBoxLayout(self)

        self.vbox_links.addWidget(self.text_field)

        self.vbox_rechts.addWidget(self.link_feld)
        self.vbox_rechts.addWidget(self.qr_code_button)
        self.vbox_rechts.addWidget(self.speichern)

        self.vbox_rechts.addWidget(self.delete)

        self.hbox.addLayout(self.vbox_links)
        self.hbox.addLayout(self.vbox_rechts)

        # Connections
        self.speichern.clicked.connect(self.save)
        self.qr_code_button.clicked.connect(self.generate)
        self.delete.clicked.connect(self.delete_all)

        # Style
        self.setStyleSheet(STYLE)

        self.show()

    def save(self):
        if not self.bild:
            self.text_field.setText("Kein Bild Vorhanden")
            self.text_field.setStyleSheet("color: red; font-size: 25pt;")
        else:
            try:
                options = QFileDialog.Options()
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Bild speichern",
                    "",
                    "Bilder (*.png *.jpg *.jpeg)",
                    options=options,
                )

                if file_path:
                    pixmap = QPixmap(100, 100)
                    if pixmap.save(file_path):
                        self.text_field.setText(
                            "Bild erfolgreich unter", file_path, "gespeichert."
                        )
                        self.text_field.setStyleSheet("color: black; font-size: 25pt;")

                    else:
                        self.text_field.setText("Fehler Beim Speichern!")
                        self.text_field.setStyleSheet("color: red; font-size: 25pt;")
                    os.remove(self.bild)
            except:
                print("Fehler beim Speichern!")
                self.text_field.setStyleSheet("color: red; font-size: 25pt;")

    def generate(self):
        if not os.path.exists("QR_Codes"):
            os.makedirs("QR_Codes")
        if (self.link_feld.text() == "") or (self.link_feld.text() == "Das Linkfeld ist leer"):
            self.link_feld.setText("Das Linkfeld ist leer")

        else:
            qr = qrcode.QRCode(
                version=1,
                box_size=15,
                border=15,
            )
            qr.add_data(self.link_feld.text())
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save("QR_Codes/QR-Code.png")
            self.bild = "QR_Codes/QR-Code.png"

            self.document.setHtml("<img src=QR_Codes/QR-Code.png>")
            self.text_field.setDocument(self.document)

    def delete_all(self):
        self.text_field.clear()
        self.link_feld.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qrCode = QRCode()
    qrCode.show()
    sys.exit(app.exec_())
