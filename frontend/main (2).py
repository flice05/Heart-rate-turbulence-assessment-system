import sys
import matplotlib

matplotlib.use('QtAgg')

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene
from PyQt6 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from MTUCI111 import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self,*args, **kwargs):
        super(MyWidget, self).__init__(*args, **kwargs)
        # Устанавливаем график в QGraphicsView
        self.df = pd.read_csv('New100.TXT', header=None)
        self.window_length = 668  # Длина окна по умолчанию
        self.current_position = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.scene = QGraphicsScene(self)
        self.scene.addWidget(self.canvas)
        self.ui.graphicsView.setScene(self.scene)
        # Слайдеры
        self.ui.horizontalSlider_2.setMinimum(0)
        self.ui.horizontalSlider_2.setMaximum(len(self.df) - 1 - self.window_length)
        self.ui.horizontalSlider_2.setValue(self.current_position)
        self.ui.horizontalSlider_2.valueChanged.connect(self.update_plot)

        self.ui.horizontalSlider.setRange(1, 100)
        self.ui.horizontalSlider.setMinimum(1)
        self.ui.horizontalSlider.setMaximum(len(self.df))
        self.ui.horizontalSlider.setValue(self.window_length)
        self.ui.horizontalSlider.valueChanged.connect(self.update_window_length)

        self.ui.horizontalSlider_3 = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.ui.horizontalSlider_3.setMinimum(1)  # Минимальная высота в точках
        self.ui.horizontalSlider_3.setMaximum(900)  # Максимальная высота в точках
        self.ui.horizontalSlider_3.setValue(20)
        self.ui.horizontalSlider_2.valueChanged.connect(self.update_plot)

        self.plot_ecg()

    def plot_ecg(self):
        ecg_signal = np.loadtxt('New100.TXT')
        self.df = pd.read_csv('New100.TXT', header=None)
        t = np.linspace(0, len(ecg_signal) / 1000, len(ecg_signal))  # Предполагаем, что частота дискретизации 1000 Гц

        # Отображение графика
        self.ax.clear()
        self.ax.plot(t, ecg_signal)
        self.ax.set_title('ЭКГ сигнал')

        # Установка начальных масштабов

        self.ax.set_xlabel("Время")
        self.ax.set_ylabel("Амплитуда")

        # Установка начальных масштабов

        self.canvas.draw()
        # Создаем слайдер для текущей позиции окна


    def update_plot(self):
        self.current_position = self.ui.horizontalSlider_2.value()

        start = self.current_position
        end = start + self.window_length

        # Получаем высоту из слайдера высоты скользящего окна
        height = self.height_slider.value()

        self.sc.ax.clear()  # Очищаем предыдущий график
        self.sc.ax.plot(self.df[start:end])  # Отображаем данные в пределах окна
        self.sc.ax.set_title("График ЭКГ")
        self.sc.ax.set_xlabel("Время")
        self.sc.ax.set_ylabel("Амплитуда")

        # Устанавливаем лимиты по оси Y в зависимости от высоты скользящего окна
        y_min = min(self.df[start:end]) - height // 2
        y_max = max(self.df[start:end]) + height // 2
        self.sc.ax.set_ylim(y_min, y_max)

        self.sc.draw()  # Перерисовываем график


    def update_window_length(self):
        """Обновляет длину окна в зависимости от значения слайдера."""
        self.window_length = self.length_slider.value()

        # Обновляем максимальное значение слайдера позиции окна
        self.position_slider.setMaximum(len(self.df) - 1 - self.window_length)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())