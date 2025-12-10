import cv2
import numpy as np
import sys
import os

# 1. Проверка наличия аргумента
if len(sys.argv) < 2:
    print("Ошибка! Укажите имя файла.")
    print("Пример: python measure.py 1.png")
    sys.exit(1)

filename = sys.argv[1]

# Проверка, существует ли файл
if not os.path.exists(filename):
    print(f"Файл '{filename}' не найден.")
    sys.exit(1)

# 2. Загрузка
image = cv2.imread(filename)

if image is None:
    print("Ошибка чтения изображения. Проверьте формат файла.")
    sys.exit(1)

# --- Обрезка левой полосы (как обсуждали ранее) ---
# Если картинки будут разной ширины, лучше обрезать не жестко 100px,
# а, например, первые 15% ширины, или оставить 100px, если дизайн фиксирован.
work_image = image[:, 100:]
# --------------------------------------------------

# 3. Обработка
gray = cv2.cvtColor(work_image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
proj = np.sum(thresh, axis=1)

# 4. Поиск строк (фильтр шума > 5 пикселей)
rows_with_text = np.where(proj > 5)[0]

lines = []
if len(rows_with_text) > 0:
    start = rows_with_text[0]
    for i in range(1, len(rows_with_text)):
        # Разрыв более 2 пикселей считаем новой строкой
        if rows_with_text[i] > rows_with_text[i-1] + 2:
            end = rows_with_text[i-1]
            lines.append((start, end))
            start = rows_with_text[i]
    lines.append((start, rows_with_text[-1]))

    print(f"Файл: {filename}")
    print(f"Найдено визуальных блоков: {len(lines)}")
    print("-" * 30)

    for i in range(len(lines) - 1):
        gap_size = lines[i+1][0] - lines[i][1]
        # Выводим текст, который можно скопировать в отчет
        print(f"Интервал {i+1}: {gap_size} px")
else:
    print("Текст не обнаружен.")