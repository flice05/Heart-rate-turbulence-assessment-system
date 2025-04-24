import math
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk

low_freq = 8
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
    
    rmssd = np.sqrt((1/(len(rr_intervals_)-1)) * sum(differences))
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
    duration = (s_peak - q_peak) / fs # QRS complex duration 

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


def is_large_amplitude(mean_ampl, r_peak_):
    if r_peak_ > mean_ampl * 1.2:
        return True

    return False

def find_extrasystols(q_peaks, r_peaks, s_peaks, rr_intervals):
    """Find RR intervals indexes of extrasystoles
    
    :param q_peaks: Q peaks indexes
    :param r_peaks: R peaks indexes
    :param s_peaks: S peaks indexes
    :param rr_intervals: array of RR intervals duration

    :return: Array of RR intervals indexes corresponding to the PVC
    """
    extrasystols_rr_intervals = [] # Массив индексов RR интервалов, соответствующих ЖЭ

    mean_amplitude = np.mean([ecg_data[r_peaks]])

    qrs_peaks: List[List[int]] = list()

    for i in range(0, len(q_peaks)):
        qrs = [q_peaks[i], s_peaks[i]]
        qrs_peaks.append(qrs)

    for i in range(0, len(qrs_peaks)):
        q = q_peaks[i]
        r = r_peaks[i]
        s = s_peaks[i]

        if (i == 0) or (i == len(qrs_peaks) - 1) or (i == len(qrs_peaks) - 2):
            continue
        else:
            small_rr_interval: bool = is_rr_interval_small(rr_intervals[i - 1])
            compensatory_pause: bool = is_compensatory_pause(rr_intervals[i - 1], rr_intervals[i])
            long_qrs: bool = is_qrs_long(q, s)
            large_amplitude: bool = is_large_amplitude(mean_amplitude, r)

            if small_rr_interval and compensatory_pause and long_qrs and large_amplitude:
                extrasystols_rr_intervals.append(i - 1)

    return extrasystols_rr_intervals


def calculate_turbulence_onset(rrs_before_pvc):
    # how to calculate turbulence onset: ((RR1 + RR2) − (RR−1 + RR−2))/(RR−1 + RR−2) ∗ 100[%]

    prev1, prev2, next1, next2 = rrs_before_pvc
    return (((next1 + next2) - (prev1 + prev2)) / (prev1 + prev2)) * 100 # turbulence onset in percents (%)



def calculate_turbulence_slope(rr_intevals_after_pvc):
    max_slope = -1000
    for i in range(16):
        after_pvc_5: List = rr_intevals_after_pvc[i:i+5]
        max_slope = max((after_pvc_5[-1] - after_pvc_5[0]) * 1000, max_slope)

    return max_slope 



def analyz_heart_rate_turbulence(rr_intervals_array, pvc_rr_intervals):    
    # Из анализа исключаются RR, соответствующие следующим показателям: интервалы <300 мс, >2000 мс, 
    # с разницей между предшествующими синусовыми интервалами >200 мс, 
    # с отличием >20% от среднего из 5 последовательных синусовых интервалов.


    average_to = 0
    average_ts = 0
    count_ts_to = 0

    for i in range(len(pvc_rr_intervals)):
        if len(rr_intervals_array) - pvc_rr_intervals[i] > 20 and pvc_rr_intervals[i] >= 2:

            before_pvc = [rr_intervals_array[pvc_rr_intervals[i] - 1], 
                          rr_intervals_array[pvc_rr_intervals[i] - 2], 
                          rr_intervals_array[pvc_rr_intervals[i] + 1], 
                          rr_intervals_array[pvc_rr_intervals[i] + 2]]

            after_pvc = [rr_intervals_array[pvc_rr_intervals[i]+2:pvc_rr_intervals[i]+22]]

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

    average_to = average_to / count_ts_to
    average_ts = average_ts / count_ts_to

    return average_to, average_ts


ecg_data = np.loadtxt('../Dataset/ecg_new.TXT', skiprows=2)

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


print(f"Q = {q_peaks_indexes}")
print(f"S = {s_peaks_indexes}")

rr_intervals = np.diff(r_peaks_indexes) / sampling_rate * 1000 # in milliseconds (ms)
print(len(r_peaks_indexes))
print(f'ЧСС = {60 / np.mean(rr_intervals)}')
time = np.arange(len(filtered_ecg)) / sampling_rate
r_ts = np.array(r_peaks_indexes) / sampling_rate
q_ts = np.array(q_peaks_indexes) / sampling_rate
s_ts = np.array(s_peaks_indexes) / sampling_rate
print(f"r = {r_peaks_indexes}")



print(f"Средний rr интервал: {np.mean(rr_intervals)}")
print(f"Количесвто RR интервалов: {len(rr_intervals)}")
        
    
extrasystols = find_extrasystols(q_peaks=q_peaks_indexes,
                                 r_peaks=r_peaks_indexes,
                                 s_peaks=s_peaks_indexes,
                                 rr_intervals=rr_intervals)


print(len(r_peaks_indexes))
print(len(q_peaks_indexes))
print(len(s_peaks_indexes))
print(f"Массив RR интервалов, соответствующих ЖЭ: {extrasystols}")
print(f"SDRR: {calculate_sdrr(rr_intervals)}")
print(f"RMSSD: {calculate_rmssd(rr_intervals, extrasystols)}")






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
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.legend()

plt.figure()
plt.scatter(rr_intervals[1:], rr_intervals[:-1])
plt.plot([0, max(np.max(rr_intervals[1:]), np.max(rr_intervals[:-1]))], 
         [0, max(np.max(rr_intervals[1:]), np.max(rr_intervals[:-1]))], "grey")
plt.grid()
plt.title("Скаттерограмма") 
plt.xlabel("RRi+1(сек)")
plt.ylabel("RRi+1 (сек)")

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
