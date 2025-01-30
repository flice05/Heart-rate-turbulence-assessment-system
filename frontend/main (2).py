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

from MTUCI1111 import Ui_MainWindow
import math
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk

low_freq = 5
high_freq = 20


def calculate_sdrr(rr_intervals_):
    rr_intervals_ = [i * 1000 for i in rr_intervals_]
    std = np.std(rr_intervals_)
    return std


def calculate_rmssd(rr_intervals_, pvc):
    rr_intervals_ = [i * 1000 for i in rr_intervals_]
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


def calculate_turbulence_onset(prev1, prev2, next1, next2):
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
        if len(rr_intervals_array) - pvc_rr_intervals[i] > 20:
            onset = calculate_turbulence_onset(rr_intervals_array[pvc_rr_intervals[i] - 1],  # rr_previous_1
                                               rr_intervals_array[pvc_rr_intervals[i] - 2],  # rr_previos_2
                                               rr_intervals_array[pvc_rr_intervals[i] + 1],  # rr_next_1
                                               rr_intervals_array[pvc_rr_intervals[i] + 2])  # rr_next_2

            slope = calculate_turbulence_slope(rr_intervals_array[pvc_rr_intervals[i] + 2:pvc_rr_intervals[i] + 22])

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


ecg_data = np.loadtxt('Dataset/New1001.TXT', skiprows=2)

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

rr_intervals = np.diff(r_peaks_indexes) / sampling_rate  # in seconds
print(len(r_peaks_indexes))
lab4 = (f'ЧСС: {round(60 / np.mean(rr_intervals),2) } уд./мин')
time = np.arange(len(filtered_ecg)) / sampling_rate
r_ts = np.array(r_peaks_indexes) / sampling_rate
q_ts = np.array(q_peaks_indexes) / sampling_rate
s_ts = np.array(s_peaks_indexes) / sampling_rate
print(f"r = {r_peaks_indexes}")

lab1 = (f"Средний RR интервал: {round(np.mean(rr_intervals),2)} секунд")
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
lab2 = (f"SDRR: {round(calculate_sdrr(rr_intervals),2)}")
lab3 = (f"RMSSD: {round(calculate_rmssd(rr_intervals, extrasystols),2)}")
average_onset, average_slope = analyz_heart_rate_turbulence(rr_intervals_array=rr_intervals,
                                                            pvc_rr_intervals=extrasystols)
if average_onset == 0:
    lab5 = (f"Средний TO: необнаружено")
else:
    lab5 = (f"Средний TO: {average_onset}")
if average_slope == 0:
    lab6 = (f"Средний TS: необнаружено")
else:
    lab6 = (f"Средний TO: {average_slope}")
lab7 = (f"Количество ЖЭ: {count_}")
if count_ == 0:
    lab8 = ("Ритм сердца нормальный. Нарушений не выявлено")
if count_ == 1:
    lab8 = ("Выявлена 1 желудочковая экстрасистола (ЖЭС). В норме экстрасистолия отсутствует.")
if count_ > 1:
    lab8 = (f"Выявлено {count_} желудочковых экстрасистол (ЖЭС). В норме экстрасистолия отсутствует.")
lab9 = (f"Средний QRS: {round(find_average_qrs(q_peaks_indexes, s_peaks_indexes),2)} сек")
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self,*args, **kwargs):
        super(MyWidget, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_7.setText(lab1)
        self.ui.label_7.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label_2.setText(lab2)
        self.ui.label_2.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label_3.setText(lab3)
        self.ui.label_3.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label.setText(lab4)
        self.ui.label.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label_10.setText(lab5)
        self.ui.label_10.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label_9.setText(lab6)
        self.ui.label_9.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label_11.setText(lab7)
        self.ui.label_11.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label_12.setText(lab8)
        self.ui.label_12.setFont(QtGui.QFont('SansSerif', 28))
        self.ui.label_8.setText(lab9)
        self.ui.label_8.setFont(QtGui.QFont('SansSerif', 28))
        self.figure, self.pt = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.gr_itog = QGraphicsScene(self)
        self.gr_itog.addWidget(self.canvas)
        self.ui.graphicsView.setScene(self.gr_itog)
        self.figure, self.pt1 = plt.subplots()
        self.canvas1 = FigureCanvas(self.figure)
        self.canvas1.mpl_connect('scroll_event', self.zoom_graph1)
        self.gr_itog1 = QGraphicsScene(self)
        self.gr_itog1.addWidget(self.canvas1)
        self.ui.graphicsView_2.setScene(self.gr_itog1)
        self.plot_ecg()
        self.plot_ecg1()

    def plot_ecg(self):
        ecg = np.loadtxt('New100.TXT')
        grath = np.linspace(0, len(ecg) / 40, len(ecg))

        self.pt.clear()  # Очищаем предыдущий график
        self.pt.plot(grath, ecg)
        self.pt.set_title('ЭКГ сигнал')
        self.pt.set_xlabel("Время")
        self.pt.set_ylabel("Амплитуда")
        self.pt.set_ylim(bottom=0)  # Устанавливаем нижний предел по оси Y
        self.canvas.draw()  # Обновляем canvas

        # Подключаем обработчик события прокрутки
        self.canvas.mpl_connect('scroll_event', self.zoom_graph)

    def plot_ecg1(self):
        self.figure.clear()
        rr_intervals_ms = [interval * 1000 for interval in rr_intervals]
        pt1 = self.figure.add_subplot(111)
        pt1.plot(range(len(rr_intervals_ms)), rr_intervals_ms,linestyle='-')
        pt1.set_title("График RR-интервалов")
        pt1.set_xlabel("Номер RR-интервала")
        pt1.set_ylabel("RR-интервал, мс")
        self.canvas1.draw()

    def zoom_graph(self, event):
        ax = self.pt 
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()       
        x1 = event.xdata
        y1 = event.ydata
        if x1 is None or y1 is None:
            return        
        zoom_factor = 1.2
        if event.button == 'up':  
            scale_factor = 1 / zoom_factor
        elif event.button == 'down':  
            scale_factor = zoom_factor
        else:
            return 
        new_xlim = [x1 + (x - x1) * scale_factor for x in xlim]
        new_ylim = [y1 + (y - y1) * scale_factor for y in ylim]
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        self.canvas.draw()


    def zoom_graph1(self, event):
        pt1 = self.figure.get_axes()[0]
        xlim = pt1.get_xlim()
        ylim = pt1.get_ylim()
        x1 = event.xdata
        y1 = event.ydata
        if x1 is None or y1 is None:
            return  
        zoom_factor = 1.2
        if event.button == 'up':
            scale_factor = 1 / zoom_factor
        elif event.button == 'down':  
            scale_factor = zoom_factor
        else:
            return
        new_xlim = [x1 + (x - x1) * scale_factor for x in xlim]
        new_ylim = [y1 + (y - y1) * scale_factor for y in ylim]

        pt1.set_xlim(new_xlim)
        pt1.set_ylim(new_ylim)

     
        self.canvas1.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
