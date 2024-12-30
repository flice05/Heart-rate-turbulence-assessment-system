import math
import numpy as np
from neurokit2 import ecg_clean, signal_filter
from scipy import signal
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
# from biosppy.signals.ecg import hamilton_segmenter
# from systole.detectors import pan_tompkins, hamilton
# from systole.detection import ecg_peaks
import neurokit2 as nk

low_freq = 5
high_freq = 15


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
    duration = (s_peak - q_peak) / fs # QRS complex duration 

    return duration



ecg_data = np.loadtxt('Dataset/New100.TXT')
sampling_rate = 100
filtered_ecg = nk.signal_filter(ecg_data, sampling_rate, low_freq, high_freq, "butterworth", 5)

_, r_peaks_indexes_raw = nk.ecg_peaks(filtered_ecg, sampling_rate=sampling_rate)
r_peaks_indexes_raw = r_peaks_indexes_raw["ECG_R_Peaks"][1:-1]

_, waves = nk.ecg_delineate(filtered_ecg,
                            r_peaks_indexes_raw,
                            sampling_rate=sampling_rate,
                            method="peak",
                            show=False,
                            show_type='peaks')

q_peaks_indexes_raw = waves["ECG_Q_Peaks"]
s_peaks_indexes_raw = waves["ECG_S_Peaks"]

q_peaks_indexes, r_peaks_indexes, s_peaks_indexes = remove_incorrect_qrs_complex(_q_peaks=q_peaks_indexes_raw,
                                                                                 _r_peaks=r_peaks_indexes_raw,
                                                                                 _s_peaks=s_peaks_indexes_raw)

qrs_complexes_duration = find_qrs_duration(q_peaks_=q_peaks_indexes, s_peaks_=s_peaks_indexes, fs=sampling_rate)

print(f"Q = {q_peaks_indexes}")
print(f"S = {s_peaks_indexes}")

rr_intervals = np.diff(r_peaks_indexes) / sampling_rate
print(len(r_peaks_indexes))
print(f'ЧСС = {60 / np.mean(rr_intervals)}')
time = np.arange(len(filtered_ecg)) / sampling_rate
r_ts = np.array(r_peaks_indexes) / sampling_rate
q_ts = np.array(q_peaks_indexes) / sampling_rate
s_ts = np.array(s_peaks_indexes) / sampling_rate
print(f"r = {r_peaks_indexes}")



print(f"Средний rr интервал: {np.mean(rr_intervals) * 0.7}")


def find_extrasystols(q_peaks_indexes, r_peaks_indexes, s_peak_indexes):
    # count_extrasystols = 0
    # potential_extrasystols_peaks_indexes = []
    # for i in range(len(rr_intervals)):
    #     if rr_intervals[i] < np.mean(rr_intervals)* 0.7:
    #         count_extrasystols += 1
    #         potential_extrasystols_peaks_indexes.append(i)
    #
    # extrasystols = []
    # for peak_index in potential_extrasystols_peaks_indexes:
    #     if peak_index == 0 or peak_index == len(rr_intervals) - 1:
    #         continue
    #
    #     previous_rr_interval = rr_intervals[peak_index - 1]
    #     next_rr_interval = rr_intervals[peak_index]
    #     if previous_rr_interval + next_rr_interval >= 2 * np.mean(rr_intervals):
    #         print(1)
    #         print(peak_index + 1)
    #
    # print(f"Количество потенциальных экстрасистол: {count_extrasystols}")
    # print(f"Индексы потенциальных экстрасистол: {potential_extrasystols_peaks_indexes} {len(potential_extrasystols_peaks_indexes)}")
    # print(np.mean(rr_intervals))
    pass

print(len(r_peaks_indexes))
print(len(q_peaks_indexes))
print(len(s_peaks_indexes))
print(f"duration of qrs complexes {qrs_complexes_duration}")


plt.figure()
plt.plot(time, ecg_data, label="Исходная ЭКГ")
plt.plot(time, filtered_ecg, label="Отфильтрованная ЭКГ")
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()

plt.figure()
plt.plot(time, filtered_ecg)
plt.plot(r_ts, filtered_ecg[r_peaks_indexes], 'ro', label="R peaks")
plt.plot(q_ts, filtered_ecg[q_peaks_indexes], "go", label="Q peaks")
plt.plot(s_ts, filtered_ecg[s_peaks_indexes], "bo", label="S peaks")
plt.legend()

plt.figure()
for i in range(len(rr_intervals)):
    rr_intervals[i] *= 1000
plt.plot([i[0] for i in enumerate(rr_intervals)], rr_intervals)
plt.xlabel("Номер RR-интервала")
plt.ylabel("RR-интервал, мс")

plt.figure()
plt.hist(rr_intervals, len(rr_intervals))
plt.xlabel('RR, мс')
plt.ylabel('Количество RR')

plt.show()
