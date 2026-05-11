"""
Завдання 3: Аналізатор лог-файлів.

Скрипт читає лог-файл, виводить статистику за рівнями логування
та (за потреби) детальні записи для вказаного рівня.

Використання:
    python main.py <шлях_до_файлу> [рівень_логування]

Приклади:
    python main.py logfile.log
    python main.py logfile.log error
"""

import sys
from typing import Callable


# ---------------------------------------------------------------------------
# Парсинг та завантаження
# ---------------------------------------------------------------------------

def parse_log_line(line: str) -> dict:
    """
    Розбирає один рядок логу на складові частини.

    Очікуваний формат: YYYY-MM-DD HH:MM:SS LEVEL Message text

    Args:
        line: Рядок з лог-файлу.

    Returns:
        Словник з ключами: date, time, level, message.

    Raises:
        ValueError: якщо рядок не відповідає очікуваному формату.
    """

    # немає сенсу парсити рядок регулярками, якщо ми вже знаємо, що він має 4 частини, 
    # розділені пробілами. split відпрацює швидше

    parts = line.strip().split(" ", 3)
    if len(parts) < 4:
        raise ValueError(f"Невірний формат рядка: '{line.strip()}'")
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2].upper(),
        "message": parts[3],
    }


def load_logs(file_path: str):
    """
    Генератор, що ліниво читає лог-файл рядок за рядком.

    Файловий об'єкт у Python сам є ітератором — ітерація по ньому
    зчитує по одному рядку без завантаження всього файлу в пам'ять.
    Це важливо для великих лог-файлів: у пам'яті одночасно знаходиться
    лише один розібраний запис, а не весь список.

    Args:
        file_path: Шлях до лог-файлу.

    Yields:
        Словники (результати parse_log_line) по одному.

    Raises:
        FileNotFoundError: якщо файл не знайдено.
        IOError: при інших помилках читання файлу.
    """
    try:
        fh = open(file_path, "r", encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не знайдено: '{file_path}'")
    except OSError as exc:
        raise IOError(f"Помилка читання файлу: {exc}") from exc

    with fh:
        for number, line in enumerate(fh, start=1):  # fh — ітератор рядків
            line = line.strip()
            if not line:          # пропускаємо порожні рядки
                continue
            try:
                yield parse_log_line(line)
            except ValueError as exc:
                # Попереджаємо, але продовжуємо обробку
                print(f"[Увага] Рядок {number} пропущено — {exc}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Фільтрація та підрахунок  (функціональне програмування: filter + lambda)
# ---------------------------------------------------------------------------

def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Повертає лише ті записи, що відповідають вказаному рівню логування.

    Використовує вбудовану функцію filter() та лямбда-вираз.

    Args:
        logs:  Список словників лог-записів.
        level: Рівень логування (регістр не важливий).

    Returns:
        Відфільтрований список записів.
    """
    target = level.upper()
    return list(filter(lambda entry: entry["level"] == target, logs))


def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів для кожного рівня логування.

    Використовує defaultdict(int): (з попередніх тем) звернення до 
    відсутнього ключа автоматично створює його зі значенням 0, тому 
    явна перевірка 'чи існує ключ' не потрібна. 
    Один прохід по списку — O(n).

    Args:
        logs: Список словників лог-записів.

    Returns:
        Звичайний словник {рівень: кількість}, відсортований за рівнем.
    """
    from collections import defaultdict

    counts: defaultdict[str, int] = defaultdict(int)
    for entry in logs:
        counts[entry["level"]] += 1

    return dict(sorted(counts.items()))


# ---------------------------------------------------------------------------
# Виведення результатів
# ---------------------------------------------------------------------------

def display_log_counts(counts: dict) -> None:
    """
    Виводить таблицю статистики за рівнями логування.

    Args:
        counts: Словник {рівень: кількість} від count_logs_by_level.
    """
    col_level = "Рівень логування"
    col_count = "Кількість"
    width_level = max(len(col_level), max((len(k) for k in counts), default=0))
    width_count = max(len(col_count), max((len(str(v)) for v in counts.values()), default=0))

    header = f"{col_level:<{width_level}} | {col_count:<{width_count}}"
    separator = "-" * width_level + "-+-" + "-" * width_count
    print(header)
    print(separator)
    for level, count in counts.items():
        print(f"{level:<{width_level}} | {count:<{width_count}}")


def display_filtered_logs(logs: list, level: str) -> None:
    """
    Виводить детальні записи для вказаного рівня логування.

    Args:
        logs:  Список відфільтрованих записів.
        level: Рівень, за яким виконувалась фільтрація.
    """
    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for entry in logs:
        print(f"{entry['date']} {entry['time']} - {entry['message']}")


# ---------------------------------------------------------------------------
# Точка входу
# ---------------------------------------------------------------------------

def main() -> None:
    """Головна функція: обробляє аргументи та запускає аналіз."""
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу> [рівень_логування]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_filter: str | None = sys.argv[2] if len(sys.argv) >= 3 else None

    # Завантаження логів — генератор читає файл рядок за рядком.
    # Використання генератора дозволяє обробляти великі файли без перевантаження пам'яті,
    # Генератор можна пройти лише один раз, тому матеріалізуємо його
    # в список тут і більше не відкриваємо файл повторно.
    # Для підрахунку статистики + фільтрації список потрібен двічі,
    # тому одноразова матеріалізація — правильний компроміс.
    try:
        logs = list(load_logs(file_path))
    except (FileNotFoundError, IOError) as exc:
        print(f"Помилка: {exc}", file=sys.stderr)
        sys.exit(1)

    if not logs:
        print("Лог-файл порожній або не містить коректних записів.")
        sys.exit(0)

    # Статистика за рівнями
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    # Деталі для вказаного рівня (необов'язково)
    if level_filter:
        filtered = filter_logs_by_level(logs, level_filter)
        if filtered:
            display_filtered_logs(filtered, level_filter)
        else:
            print(f"\nЗаписів рівня '{level_filter.upper()}' не знайдено.")


if __name__ == "__main__":
    main()