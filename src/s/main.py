import sys
import random
from dataclasses import dataclass

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QGraphicsOpacityEffect 
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint

@dataclass
class Souvenir:
    name: str
    image_path: str


class SouvenirMachine(QWidget):
    def __init__(self):
        super().__init__()
        self.balance = 0
        self.souvenirs = {
            10: [Souvenir("Магнит", "images/magnet.png"), Souvenir("Открытка", "images/postcard.png"), Souvenir("Значок", "images/badge.png")],
            20: [Souvenir("Брелок", "images/keychain.png"), Souvenir("Ручка", "images/pen.png"), Souvenir("Блокнот", "images/notebook.png")],
            30: [Souvenir("Кружка", "images/mug.png"), Souvenir("Футболка", "images/tshirt.png"), Souvenir("Кепка", "images/cap.png")],
            40: [Souvenir("Статуэтка", "images/figurine.png"), Souvenir("Шарф", "images/scarf.png"), Souvenir("Зонт", "images/umbrella.png")]
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Сувенирный автомат')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #E0E0E0;")

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(20)
        mainLayout.setContentsMargins(30, 30, 30, 30)

        title = QLabel('Сувенирный автомат')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1A1A1A;")
        mainLayout.addWidget(title)

        self.balanceLabel = QLabel(f'Баланс: {self.balance} ₽')
        self.balanceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balanceLabel.setFont(QFont('Arial', 14))
        self.balanceLabel.setStyleSheet("color: #1A1A1A;")
        mainLayout.addWidget(self.balanceLabel)

        controlPanel = QHBoxLayout()
        controlPanel.setSpacing(10)

        self.moneyInput = QLineEdit()
        self.moneyInput.setPlaceholderText('Введите сумму')
        self.moneyInput.setStyleSheet("padding: 10px; border: 2px solid #A0A0A0; border-radius: 5px; background-color: #FFFFFF; color: #1A1A1A;")
        controlPanel.addWidget(self.moneyInput)

        depositButton = QPushButton('Внести деньги')
        depositButton.clicked.connect(self.depositMoney)
        depositButton.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        controlPanel.addWidget(depositButton)

        withdrawButton = QPushButton('Выдать средства')
        withdrawButton.clicked.connect(self.withdrawMoney)
        withdrawButton.setStyleSheet("""
            QPushButton {
                background-color: #FF9800; 
                color: white; 
                padding: 10px; 
                border: none; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e68a00;
            }
        """)
        controlPanel.addWidget(withdrawButton)

        mainLayout.addLayout(controlPanel)

        souvenirButtons = QHBoxLayout()
        souvenirButtons.setSpacing(10)

        buttons = [
            ('Сувенир за 10 ₽', 10),
            ('Сувенир за 20 ₽', 20),
            ('Сувенир за 30 ₽', 30),
            ('Сувенир за 40 ₽', 40)
        ]

        for text, price in buttons:
            button = QPushButton(text)
            button.clicked.connect(lambda checked, p=price: self.dispenseSouvenir(p))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3; 
                    color: white; 
                    padding: 15px; 
                    border: none; 
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #1e87db;
                }
            """)
            souvenirButtons.addWidget(button)

        mainLayout.addLayout(souvenirButtons)

        # Информационное окно
        self.infoField = QLabel()
        self.infoField.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.infoField.setStyleSheet("background-color: #FFFFFF; border: 2px solid #A0A0A0; border-radius: 5px; padding: 20px; color: #1A1A1A; font-size: 16px; font-weight: bold;")
        self.infoField.setFixedHeight(100)
        mainLayout.addWidget(self.infoField)

        # Окно для выдачи сувениров
        self.souvenirOutputArea = QWidget()
        self.souvenirOutputArea.setFixedHeight(200)
        self.souvenirOutputArea.setStyleSheet("background-color: #FFFFFF; border: 2px solid #A0A0A0; border-radius: 5px;")
        
        self.souvenirOutputLayout = QVBoxLayout(self.souvenirOutputArea)
        
        # Создаем QLabel для отображения сувенира
        self.souvenirImageLabel = QLabel()
        self.souvenirImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.souvenirOutputLayout.addWidget(self.souvenirImageLabel)
        
        mainLayout.addWidget(self.souvenirOutputArea)

        self.setLayout(mainLayout)

        # Создаем QLabel для отображения карты
        self.cardImageLabel = QLabel(self)
        pixmap = QPixmap("images/card.png")
        if pixmap.isNull():
            print("Не удалось загрузить изображение карты.")
        else:
            scaled_pixmap = pixmap.scaled(85, 54, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.cardImageLabel.setPixmap(scaled_pixmap)
        self.cardImageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cardImageLabel.hide()  # Изначально скрываем карту
        self.cardImageLabel.raise_() # Поднимаем карту поверх всех элементов после установки layout

    def depositMoney(self):
        try:
            amount = int(self.moneyInput.text())
            if amount <= 0:
                raise ValueError()

            self.balance += amount
            self.updateBalance()
            self.moneyInput.clear()
            self.infoField.setText(f"Внесено {amount} ₽")
            self.animateCard()
        except ValueError:
            self.infoField.setText("<font color='red'>Пожалуйста, введите корректную сумму.</font>")

    def withdrawMoney(self):
        if self.balance > 0:
            amount = self.balance
            self.infoField.setText(f"Выдано {amount} ₽")
            self.balance = 0
            self.updateBalance()
        else:
            self.infoField.setText("<font color='red'>Нет средств для выдачи.</font>")

    def dispenseSouvenir(self, price):
        if self.balance >= price:
            self.balance -= price
            self.updateBalance()
            souvenir = random.choice(self.souvenirs[price])
            self.infoField.setText(f"Выдан сувенир:\n{souvenir.name}\n(стоимость {price} ₽)")
            self.displaySouvenirImage(souvenir)
        else:
            self.infoField.setText("<font color='red'>Недостаточно средств.</font>")

    def displaySouvenirImage(self, souvenir):
        pixmap = QPixmap(souvenir.image_path)
        self.souvenirImageLabel.setPixmap(pixmap.scaled(self.souvenirOutputArea.size(), Qt.AspectRatioMode.KeepAspectRatio))

        # Создаем и устанавливаем эффект прозрачности
        opacity_effect = QGraphicsOpacityEffect()
        self.souvenirImageLabel.setGraphicsEffect(opacity_effect)
        
        # Создаем анимацию для эффекта прозрачности
        self.animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.animation.setDuration(1000)  # Длительность анимации в миллисекундах
        self.animation.setStartValue(0)   # Начальное значение (полностью прозрачное)
        self.animation.setEndValue(1)     # Конечное значение (полностью видимое)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)  # Плавное появление и затухание
        self.animation.start()

    def animateCard(self):
        self.cardImageLabel.show()  # Показываем карту перед анимацией
        start_pos = QPoint(0, self.height() - self.cardImageLabel.height())  # Начальная позиция внизу слева
        
        # Получаем глобальные координаты поля ввода
        input_pos = self.moneyInput.mapTo(self, QPoint(0, 0))
        end_pos = QPoint(input_pos.x(), input_pos.y())  # Конечная позиция у поля ввода

        self.cardImageLabel.move(start_pos)

        # Создаем анимацию для перемещения карты
        self.cardAnimation = QPropertyAnimation(self.cardImageLabel, b"pos")
        self.cardAnimation.setDuration(2000)
        self.cardAnimation.setStartValue(start_pos)
        self.cardAnimation.setEndValue(end_pos)
        self.cardAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Устанавливаем связь между анимацией и скрытием карты
        self.cardAnimation.finished.connect(lambda: self.cardImageLabel.hide())  # Скрываем карту после анимации

        # Запускаем анимацию перемещения
        self.cardAnimation.start()

    def updateBalance(self):
        self.balanceLabel.setText(f'Баланс: {self.balance} ₽')

        # Создаем и добавляем эффект прозрачности для balanceLabel
        opacity_effect = QGraphicsOpacityEffect(self.balanceLabel)
        self.balanceLabel.setGraphicsEffect(opacity_effect)

        # Анимация для изменения прозрачности
        self.balanceAnimation = QPropertyAnimation(opacity_effect, b"opacity")
        self.balanceAnimation.setDuration(500)
        self.balanceAnimation.setStartValue(0.3)
        self.balanceAnimation.setEndValue(1.0)
        self.balanceAnimation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.balanceAnimation.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    machine = SouvenirMachine()
    machine.show()

    sys.exit(app.exec())
