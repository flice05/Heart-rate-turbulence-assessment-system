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


# def filter_ecg(ecg_signal, fs):
#     # Фильтр Баттерворта
#     b, a = signal.butter(5, [low_freq, high_freq], fs=fs, btype='bandpass')
#     filtered_ecg = signal.lfilter(b, a, ecg_signal)
#     return filtered_ecg
#
#
# def find_r_peaks_indexes(filtered_signal, fs):
#     diff_ecg = np.ediff1d(filtered_ecg)
#
#     squared_diff = diff_ecg ** 2
#
#     window_size = int(fs * 0.08)
#     integrated_ecg = np.convolve(squared_diff, np.ones(window_size), mode='same') / window_size
#
#     noise_level = np.median(integrated_ecg)
#     threshold_qrs = noise_level + 0.15 * np.max(integrated_ecg)
#     r_peak_indices = find_peaks(integrated_ecg, height=threshold_qrs)[0]
#
#     return r_peak_indices


# def butter_bandpass(lowcut, highcut, fs, order=5):
#     nyq = 0.5 * fs
#     low = lowcut / nyq
#     high = highcut / nyq
#     sos = signal.butter(order, [low, high], analog=False, btype='bandpass')
#     return sos
#
#
# def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
#     sos = butter_bandpass(lowcut, highcut, fs, order=order)
#     y = signal.sosfilt(sos, data)
#     return y


def find_q_peaks_indexes(ecg, r_peaks):
    q_peaks = []
    for i in r_peaks:
        q_minn = i
        for j in range(1, 6):
            if ecg[i - j] < q_minn:
                q_minn = i - j
        q_peaks.append(q_minn)
        print(f"Добавлен элемент {q_minn}    {i}")

    return q_peaks


def find_s_peaks_indexes(ecg, r_peaks):
    s_peaks = []
    for i in r_peaks:
        s_minn = i
        for j in range(1, 11):
            if ecg[i + j] < s_minn:
                s_minn = i + j
        s_peaks.append(s_minn)
        print(f"Добавлен элемент {s_minn}    {i}")

    return s_peaks


def remove_incorrect_qrs_complex(_q_peaks, _r_peaks, _s_peaks):
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


def find_qrs_duration(q_peaks_, s_peaks_, fs):

    duration = list() # QRS complexes duration array
    for q, s in zip(q_peaks_, s_peaks_):
        duration.append((s - q) / fs)

    return duration



ecg_data = np.loadtxt('Dataset/New100.TXT')
sampling_rate = 100
# filtered_ecg = filter_ecg(ecg_data, sampling_rate)
# filtered_ecg = ecg_clean(ecg_data, sampling_rate, "neurokit")
filtered_ecg = signal_filter(ecg_data, sampling_rate, low_freq, high_freq, "butterworth", 5)
# r_peak_indexes = find_r_peaks_indexes(filtered_ecg, sampling_rate)

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


def find_extrasystols():
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
