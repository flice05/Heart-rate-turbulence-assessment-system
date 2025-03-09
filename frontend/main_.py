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
import neurokit2 as nk
from open_file import Ui_MainWindow1
from design_and_soft import Ui_MainWindow
import math
from typing import List


class MyWidget1(QMainWindow, Ui_MainWindow1):
    def __init__(self, *args, **kwargs):
        super(MyWidget1, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow1()
        self.setupUi(self)
        self.ok_button_start.clicked.connect(self.open2)

    def open2(self):
        way0 = QtCore.QStandardPaths.standardLocations(
        QtCore.QStandardPaths.StandardLocation.DocumentsLocation)[0]
        way, _ = QtWidgets.QFileDialog.getOpenFileName(
                None, 'Open Text File', way0, "Text Files (*.txt);;All Files (*)")
        print("Загрузка................")
        chislo = int(self.lineEdit.text())
        chislo1 = int(self.lineEdit_2.text())
        self.sub_window =mainn(way,chislo,chislo1)


def mainn(way,chislo,chislo1):
    class MyWidget(QMainWindow, Ui_MainWindow):
        def __init__(self,*args, **kwargs):
            super(MyWidget, self).__init__(*args, **kwargs)
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.label_7.setText(lab1)
            self.ui.label_7.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_7.setStyleSheet("font-weight: bold")
            self.ui.label_2.setText(lab2)
            self.ui.label_2.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_2.setStyleSheet("font-weight: bold")
            self.ui.label_3.setText(lab3)
            self.ui.label_3.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_3.setStyleSheet("font-weight: bold")
            self.ui.label.setText(lab4)
            self.ui.label.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label.setStyleSheet("font-weight: bold")
            self.ui.label_10.setText(lab5)
            self.ui.label_10.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_10.setStyleSheet("font-weight: bold")
            self.ui.label_9.setText(lab6)
            self.ui.label_9.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_9.setStyleSheet("font-weight: bold")
            self.ui.label_11.setText(lab7)
            self.ui.label_11.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_11.setStyleSheet("font-weight: bold")
            self.ui.label_12.setText(lab8)
            self.ui.label_12.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_12.setStyleSheet("font-weight: bold")
            self.ui.label_8.setText(lab9)
            self.ui.label_8.setFont(QtGui.QFont('SansSerif', 16))
            self.ui.label_8.setStyleSheet("font-weight: bold")

            self.load_data(way)
            self.figure, self.grath = plt.subplots()
            self.canvas = FigureCanvas(self.figure)
            self.scene = QGraphicsScene(self)
            self.scene.addWidget(self.canvas)
            self.ui.graphicsView.setScene(self.scene)
            self.figure, self.grath1 = plt.subplots()
            self.canvas1 = FigureCanvas(self.figure)
            self.scene1 = QGraphicsScene(self)
            self.scene1.addWidget(self.canvas1)
            self.ui.graphicsView_2.setScene(self.scene1)
            self.window_length = 100
            self.current_position = 0
            self.window_length2 = 100
            self.current_position2 = 0
            self.ui.horizontalSlider_2.setMinimum(0)
            self.ui.horizontalSlider_2.setMaximum(len(self.znach) - 1 - self.window_length)
            self.ui.horizontalSlider_2.setValue(self.current_position)
            self.ui.horizontalSlider_2.valueChanged.connect(self.update_plot)
            self.ui.horizontalSlider.setMinimum(1)
            self.ui.horizontalSlider.setMaximum(len(self.znach))
            self.ui.horizontalSlider.setValue(self.window_length)
            self.ui.horizontalSlider_3.setMinimum(1)
            self.ui.horizontalSlider_3.setMaximum(500)
            self.ui.horizontalSlider_3.setValue(20)
            self.ui.horizontalSlider_5.setMinimum(0)
            self.ui.horizontalSlider_5.setMaximum(800 - 1 - self.window_length2)
            self.ui.horizontalSlider_5.setValue(self.current_position2)
            self.ui.horizontalSlider_5.valueChanged.connect(self.update_plot)
            self.ui.horizontalSlider_4.setMinimum(1)
            self.ui.horizontalSlider_4.setMaximum(800)
            self.ui.horizontalSlider_4.setValue(self.window_length2)
            self.ui.horizontalSlider_6.setMinimum(1)
            self.ui.horizontalSlider_6.setMaximum(500)
            self.ui.horizontalSlider_6.setValue(20)

            self.ui.horizontalSlider_2.valueChanged.connect(self.update_plot)
            self.ui.horizontalSlider.valueChanged.connect(self.update_window_length)
            self.ui.horizontalSlider_3.valueChanged.connect(self.update_plot)
            self.ui.horizontalSlider_5.valueChanged.connect(self.update_plot2)
            self.ui.horizontalSlider_4.valueChanged.connect(self.update_window_length2)
            self.ui.horizontalSlider_6.valueChanged.connect(self.update_plot2)
            self.update_plot()
            self.update_plot2()

        def resizeEvent(self, event):
            super().resizeEvent(event)
            if self.canvas is not None or self.canvas1 is not None:
                s = self.size()
                w = s.width() - 100
                h = s.height() - 250
                self.canvas.resize(w, h)
                self.canvas1.resize(w, h)




        def load_data(self, filename):
            self.znach = pd.read_csv(filename, header=None)
            self.znach.columns = ['ECG']
            self.ui.horizontalSlider_2.setMaximum(len(self.znach) - 1 - 100)




        def update_plot(self):
            self.current_position = self.ui.horizontalSlider_2.value()
            start = self.current_position
            end = start + self.window_length
            height = self.ui.horizontalSlider_3.value()
            self.grath.clear()
            self.grath.plot(self.znach[start:end])
            self.grath.set_title("График ЭКГ")
            self.grath.set_xlabel("Время")
            self.grath.set_ylabel("Амплитуда")
            y_min = min(self.znach['ECG'][start:end]) - height // 2
            y_max = max(self.znach['ECG'][start:end]) + height // 2
            self.grath.set_ylim(y_min, y_max)
            self.canvas.draw()

        def update_window_length(self):
            self.window_length = self.ui.horizontalSlider.value()
            self.ui.horizontalSlider_2.setMaximum(len(self.znach) - 1 - self.window_length)
            self.update_plot()




        def update_plot2(self):
            rr_intervals_ms = [interval * 1000 for interval in rr_intervals]
            self.znach1 = rr_intervals_ms
            self.ui.horizontalSlider_5.setMaximum(800 - 1 - self.window_length2)
            self.current_position2 = self.ui.horizontalSlider_5.value()
            start = self.current_position2
            end = start + self.window_length2
            height = self.ui.horizontalSlider_6.value()
            self.grath1.clear()
            self.grath1.plot(self.znach1[start:end])
            self.grath1.set_title("График RR-интервалов")
            self.grath1.set_xlabel("Номер RR-интервала")
            self.grath1.set_ylabel("RR-интервал, мс")
            y_min = min(self.znach1[start:end]) - height // 2
            y_max = max(self.znach1[start:end]) + height // 2
            self.grath1.set_ylim(y_min, y_max)
            self.canvas1.draw()

        def update_window_length2(self):
            self.window_length2 = self.ui.horizontalSlider_4.value()
            self.ui.horizontalSlider_5.setMaximum(800 - 1 - self.window_length2)
            self.update_plot2()


    low_freq = chislo
    high_freq = chislo1


    def calculate_sdrr(rr_intervals_):
        rr_intervals_ = [i  for i in rr_intervals_]
        std = np.std(rr_intervals_)
        return std


    def calculate_rmssd(rr_intervals_, pvc):
        rr_intervals_ = [i  for i in rr_intervals_]
        for i in range(len(pvc)):
            del rr_intervals_[pvc[i]]

        nn_intervals_ = rr_intervals_
        differences = list()
        for i in range(len(nn_intervals_) - 1):
            differences.append(((nn_intervals_[i + 1] - nn_intervals_[i]) ** 2))

        rmssd = np.sqrt((1 / (len(rr_intervals_) - 1)) * sum(differences))
        return rmssd


    def remove_incorrect_qrs_complex(_q_peaks, _r_peaks, _s_peaks):
        """
        :param _q_peaks: array of Q peaks indexes (including incorrect values)
        :param _r_peaks: array of R peaks indexes (including incorrect values)
        :param _s_peaks: array of S peaks indexes (including incorrect values)

        :return: arrays with correct Q, R, S peaks indexes
        """
        # remove NaN values
        for i in range(0, len(_q_peaks)):
            if math.isnan(_q_peaks[i]):
                _q_peaks.pop(i)

        for i in range(0, len(_s_peaks)):
            if math.isnan(_s_peaks[i]):
                _s_peaks.pop(i)

        for i in range(0, len(_r_peaks)):
            if math.isnan(_r_peaks[i]):
                _r_peaks.pop(i)

        mean_r_peak_amplitude = np.mean([filtered_ecg[i] for i in _r_peaks])
        q_peaks_new = list()
        r_peaks_new = list()
        s_peaks_new = list()

        # remove low amplitude QRS complexes
        for q, r, s in zip(_q_peaks, _r_peaks, _s_peaks):
            if filtered_ecg[r] > (mean_r_peak_amplitude * 0.6):
                q_peaks_new.append(q)
                r_peaks_new.append(r)
                s_peaks_new.append(s)

        return q_peaks_new, r_peaks_new, s_peaks_new


    def find_qrs_duration(q_peak: int, s_peak: int, fs: int):
        """Find duration of QRS complex

        :param q_peak: Q peak index
        :param s_peak: S peak index
        :param fs: Sampling rate

        :return: duration of QRS complex in seconds
        """
        duration = (s_peak - q_peak) / fs  # QRS complex duration

        return duration


    def is_rr_interval_small(rr_interval):
        if rr_interval < np.mean(rr_intervals) * 0.7:
            return True

        return False


    def is_compensatory_pause(previous_rr_interval, next_rr_interval):
        if previous_rr_interval + next_rr_interval >= 2 * np.mean(rr_intervals):
            return True

        return False


    def is_qrs_long(q, s):
        qrs_duration = find_qrs_duration(q, s, sampling_rate)

        # Checking the duration of the QRS complex for deviations from the norm
        if qrs_duration >= 0.18:
            return True

        return False


    def find_extrasystols(q_peaks, s_peaks, rr_intervals):
        """Find RR intervals indexes of extrasystoles

        :param q_peaks: Q peak index
        :param s_peaks: S peak index
        :param rr_intervals: array of RR intervals duration

        :return: Array of RR intervals indexes corresponding to the PVC
        """
        extrasystols_rr_intervals = []  # Массив индексов RR интервалов, соответствующих ЖЭ

        qrs_peaks: List[List[int]] = list()

        for i in range(0, len(q_peaks)):
            qrs = [q_peaks[i], s_peaks[i]]
            qrs_peaks.append(qrs)

        for i in range(0, len(qrs_peaks)):
            q = q_peaks[i]
            s = s_peaks[i]

            if (i == 0) or (i == len(qrs_peaks) - 1) or (i == len(qrs_peaks) - 2):
                continue
            else:
                small_rr_interval: bool = is_rr_interval_small(rr_intervals[i - 1])
                compensatory_pause: bool = is_compensatory_pause(rr_intervals[i - 1], rr_intervals[i])
                long_qrs: bool = is_qrs_long(q, s)

                if small_rr_interval and compensatory_pause and long_qrs:
                    extrasystols_rr_intervals.append(i - 1)

        return extrasystols_rr_intervals


    def calculate_turbulence_onset(rrs_before_pvc):
        prev1, prev2, next1, next2 = rrs_before_pvc
        # how to calculate turbulence onset: ((RR1 + RR2) − (RR−1 + RR−2))/(RR−1 + RR−2) ∗ 100[%]
        return (((next1 + next2) - (prev1 + prev2)) / (prev1 + prev2)) * 100  # turbulence onset in percents (%)


    def calculate_turbulence_slope(rr_intevals_after_pvc):
        max_slope = -1000
        for i in range(16):
            after_pvc_5: List = rr_intevals_after_pvc[i:i + 5]
            max_slope = max((after_pvc_5[-1] - after_pvc_5[0]) * 1000, max_slope)

        return max_slope


    def analyz_heart_rate_turbulence(rr_intervals_array, pvc_rr_intervals):
        # turbulence_onset --- percent change in the average of the two normal beats after
        # and the two normal beats before the VPC

        average_to = 0
        average_ts = 0
        count_ts_to = 0

        for i in range(len(pvc_rr_intervals)):
            if len(rr_intervals_array) - pvc_rr_intervals[i] > 20 and pvc_rr_intervals[i] >= 2:

                before_pvc = [rr_intervals_array[pvc_rr_intervals[i] - 1],
                              rr_intervals_array[pvc_rr_intervals[i] - 2],
                              rr_intervals_array[pvc_rr_intervals[i] + 1],
                              rr_intervals_array[pvc_rr_intervals[i] + 2]]

                after_pvc = [rr_intervals_array[pvc_rr_intervals[i] + 2:pvc_rr_intervals[i] + 22]]

                if any(rr > 2000 or rr < 300 for rr in before_pvc + after_pvc):
                    continue
                if any(i > 200 for i in np.diff(before_pvc)):
                    continue
                if any(i > 1.2 * np.mean(after_pvc) for i in after_pvc):
                    continue

                onset = calculate_turbulence_onset(before_pvc)

                slope = calculate_turbulence_slope(after_pvc)

                average_to += onset
                average_ts += slope
                count_ts_to += 1
        if count_ts_to == 0:
            average_to = 0
        else:
            average_to = average_to / count_ts_to
        if count_ts_to == 0:
            average_to = 0
        else:
            average_ts = average_ts / count_ts_to

        return average_to, average_ts

    ecg_data = np.loadtxt(way, skiprows=2)
    sampling_rate = 100
    filtered_ecg = nk.signal_filter(ecg_data, sampling_rate, low_freq, high_freq, "butterworth", 5)

    _, r_peaks_indexes_raw = nk.ecg_peaks(filtered_ecg, sampling_rate=sampling_rate)
    r_peaks_indexes_raw = r_peaks_indexes_raw["ECG_R_Peaks"][1:-1]

    _, waves = nk.ecg_delineate(filtered_ecg,
                                r_peaks_indexes_raw,
                                sampling_rate=sampling_rate,
                                method="peak",
                                show=False,
                                show_type='all')

    q_peaks_indexes_raw = waves["ECG_Q_Peaks"]
    s_peaks_indexes_raw = waves["ECG_S_Peaks"]

    # if there are problems with the fact that there are 1 more R peak than Q and S peaks, then you need to do this: _r_peaks=r_peaks_indexes_raw[:-1]
    q_peaks_indexes, r_peaks_indexes, s_peaks_indexes = remove_incorrect_qrs_complex(_q_peaks=q_peaks_indexes_raw,
                                                                                     _r_peaks=r_peaks_indexes_raw,
                                                                                     _s_peaks=s_peaks_indexes_raw)


    def find_average_qrs(q_peaks, s_peaks):
        qrs_complexes = list()
        for i in range(0, len(q_peaks)):
            q = q_peaks[i]
            s = s_peaks[i]
            duration = find_qrs_duration(q_peak=q, s_peak=s, fs=sampling_rate)
            qrs_complexes.append(duration)

        return np.mean(qrs_complexes)

    print(f"Q = {q_peaks_indexes}")
    print(f"S = {s_peaks_indexes}")

    rr_intervals = np.diff(r_peaks_indexes) / sampling_rate * 1000 # in milliseconds (ms)
    print(len(r_peaks_indexes))
    lab4 = (f'ЧСС(частота сердечных сокращений): {round(60000 / np.mean(rr_intervals),2) } уд./мин')
    time = np.arange(len(filtered_ecg)) / sampling_rate
    r_ts = np.array(r_peaks_indexes) / sampling_rate
    q_ts = np.array(q_peaks_indexes) / sampling_rate
    s_ts = np.array(s_peaks_indexes) / sampling_rate
    print(f"r = {r_peaks_indexes}")

    lab1 = (f"Средний RR интервал(средний интервал между сердечными сокращениями): {round(np.mean(rr_intervals),2)} миллисекунд")
    print(f"Количесвто RR интервалов: {len(rr_intervals)}")

    extrasystols = find_extrasystols(q_peaks=q_peaks_indexes,
                                     s_peaks=s_peaks_indexes,
                                     rr_intervals=rr_intervals)
    count_ = 0
    for i in extrasystols:
        count_ +=1


    print(len(r_peaks_indexes))
    print(len(q_peaks_indexes))
    print(len(s_peaks_indexes))

    print(f"Массив RR интервалов, соответствующих ЖЭ: {extrasystols}")
    lab2 = (f"SDRR(изменение RR интервалов во времени): {round(calculate_sdrr(rr_intervals),2)}")
    lab3 = (f"RMSSD(изменение интервала между началами двух сердечных циклов): {round(calculate_rmssd(rr_intervals, extrasystols),2)}")
    average_onset, average_slope = analyz_heart_rate_turbulence(rr_intervals_array=rr_intervals,
                                                                pvc_rr_intervals=extrasystols)
    if average_onset == 0:
        lab5 = (f"Средний TO(изменение интервалов между двумя сокращениями сердца): не обнаружено")
    else:
        lab5 = (f"Средний TO(изменение интервалов между двумя сокращениями сердца): {average_onset}")
    if average_slope == 0:
        lab6 = (f"Средний TS(наклон  изменений величин RR): не обнаружено")
    else:
        lab6 = (f"Средний TS(наклон  изменений величин RR): {average_slope}")
    lab7 = (f"Количество ЖЭ(желудочковых екстрасистол): {count_}")
    if count_ == 0:
        lab8 = ("Ритм сердца нормальный. Нарушений не выявлено")
    if count_ == 1:
        lab8 = ("Выявлена 1 желудочковая экстрасистола (ЖЭС). В норме экстрасистолия отсутствует.")
    if count_ > 1:
        lab8 = (f"Выявлено {count_} желудочковых экстрасистол (ЖЭС). В норме экстрасистолия отсутствует.")
    lab9 = (f"Средний QRS(желудочковый комплекс от начала зубца Q до конца зубца S): {round(find_average_qrs(q_peaks_indexes, s_peaks_indexes),2)} сек")
    ex = MyWidget()
    ex.show()
    return ex




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget1()
    ex.show()
    sys.exit(app.exec())