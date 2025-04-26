from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import numpy as np

def solve_captcha(image_path, target_color=None, is_color_check=False):
    """
    Универсальный солвер капчи, который определяет тип и решает:
    1. Текстовые капчи (с помощью OCR)
    2. Цветные капчи (поиск элементов заданного цвета)
    
    Параметры:
    - image_path: путь к изображению капчи
    - target_color: (R, G, B) - целевой цвет для цветной капчи (опционально)
    - is_color_check: если True, сначала проверяет на цветную капчу
    
    Возвращает:
    - Для текстовой капчи: текст
    - Для цветной капчи: координаты (x, y) или список координат
    - None, если не удалось решить
    """
    try:
        img = Image.open(image_path)
        
        # Сначала проверяем на цветную капчу, если указан target_color или is_color_check=True
        if target_color is not None or is_color_check:
            color_result = _solve_color_captcha(img, target_color)
            if color_result is not None:
                return color_result
        
        # Если не цветная, пробуем решить как текстовую
        text_result = _solve_text_captcha(img)
        return text_result if text_result else None
        
    except Exception as e:
        print(f"Ошибка при обработке капчи: {e}")
        return None

def _solve_text_captcha(img):
    """Внутренняя функция для решения текстовой капчи"""
    try:
        # Предварительная обработка изображения
        img = img.convert('L')  # В градации серого
        img = ImageEnhance.Contrast(img).enhance(2)  # Увеличиваем контраст
        img = img.filter(ImageFilter.SHARPEN)  # Улучшаем резкость
        
        # Конфигурация Tesseract для капчи
        custom_config = r'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        text = pytesseract.image_to_string(img, config=custom_config)
        
        return text.strip() if text else None
    except:
        return None

def _solve_color_captcha(img, target_color=None):
    """Внутренняя функция для решения цветной капчи"""
    try:
        img = img.convert('RGB')
        pixels = np.array(img)
        
        # Если цвет не указан, пытаемся определить доминирующий цвет
        if target_color is None:
            # Простая логика определения доминирующего цвета
            unique_colors, counts = np.unique(pixels.reshape(-1, 3), axis=0, return_counts=True)
            target_color = unique_colors[np.argmax(counts)]
        
        # Параметры чувствительности к цвету
        threshold = 30
        
        # Находим пиксели, близкие к целевому цвету
        color_diff = np.sqrt(np.sum((pixels - target_color)**2, axis=2))
        matches = color_diff < threshold
        
        # Находим координаты совпадений
        y_indices, x_indices = np.where(matches)
        
        if len(x_indices) == 0:
            return None
        
        # Группируем близкие точки в кластеры
        from sklearn.cluster import DBSCAN
        coords = list(zip(x_indices, y_indices))
        clustering = DBSCAN(eps=10, min_samples=5).fit(coords)
        
        # Находим центры кластеров
        clusters = {}
        for i, label in enumerate(clustering.labels_):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(coords[i])
        
        # Возвращаем центры всех значимых кластеров
        result = []
        for label, points in clusters.items():
            if label != -1 and len(points) > 5:  # Игнорируем шум и маленькие группы
                avg_x = int(np.mean([p[0] for p in points]))
                avg_y = int(np.mean([p[1] for p in points]))
                result.append((avg_x, avg_y))
        
        return result[0] if len(result) == 1 else result if result else None
    except:
        return None

# Примеры использования:
# 1. Для текстовой капчи:
# print(solve_captcha('text_captcha.png'))

# 2. Для цветной капчи (когда знаем целевой цвет):
# print(solve_captcha('color_captcha.png', target_color=(255, 0, 0)))

# 3. Для автоматического определения:
# print(solve_captcha('unknown_captcha.png', is_color_check=True))