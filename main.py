import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import matplotlib.pyplot as plt


def get_noisy_ecg() -> np.ndarray[float]:
    """Функция для получения файла с ЭКГ сигналом"""

    # Магия ---> noisy_ecg = List[float]
    #              ||
    #              ||
    return noisy_ecg


def filter_ecg_signal(data: np.ndarray[float]) -> np.ndarray[float]:
    """Функция для фильтрации ЭКГ сигнала"""

    nyq: float = 0.5 * fs  # Частота_Найквиста
    normal_cutoff: float = cutoff_freq / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # Применение фильтра
    filtered = filtfilt(b, a, data)
    return filtered


def find_rr_intervals(filtered_ecg: np.ndarray[float]) -> np.ndarray[float]:
    """Функция для нахождения RR-интервалов"""
    peaks, _ = find_peaks(filtered_ecg, height=...)
    rr_intervals = np.diff(peaks) / fs
    return rr_intervals


noisy_ecg = get_noisy_ecg()

fs = 500 # Частота дискретизации (Гц)
cutoff_freq = 50  # Частота среза (Гц)
order = 3  # Порядок фильтра


time = np.arange(len(noisy_ecg)) / fs


# Применение фильтрации ЭКГ сигнала
filtered_ecg = filter_ecg_signal(noisy_ecg, fs, cutoff_freq, order)


# Нахождение rr-интервалов
rr_intervals = find_rr_intervals(filtered_ecg)

# Визуализация результата
plt.figure(figsize=(12, 6))
plt.plot(time, noisy_ecg, label='ЭКГ с шумом')
plt.plot(time, filtered_ecg, label='Отфильтрованная ЭКГ')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)
plt.show()
