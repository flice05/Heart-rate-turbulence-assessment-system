import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import pandas as pd


def filter_ecg_signal(data: np.ndarray[float], fs: int, cutoff_freq: int, order: int) -> np.ndarray:
    """Функция для фильтрации ЭКГ сигнала"""

    nyq: float = 0.5 * fs  # Частота_Найквиста
    normal_cutoff: float = cutoff_freq / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # Применение фильтра
    filtered = filtfilt(b, a, data)
    return filtered


# Загрузка данных из CSV-файла
noisy_ecg = pd.read_csv("path_to_ecg.csv")
noisy_ecg_voltages = noisy_ecg["Voltage"].values

fs = 1000  # Частота дискретизации (Гц)
cutoff_freq = 50  # Частота среза (Гц)
order = 5  # Порядок фильтра

# Применение фильтра
filtered_ecg = filter_ecg_signal(noisy_ecg_voltages, fs, cutoff_freq, order)

# Визуализация результата
plt.figure(figsize=(12, 6))
plt.plot(noisy_ecg, label='ЭКГ с шумом')
plt.plot(filtered_ecg, label='Отфильтрованная ЭКГ')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)
plt.show()
