import re

def generator_numbers(text: str):
    """
    Генератор, що знаходить усі дійсні числа в тексті.
 
    Дійсні числа мають бути чітко відокремлені пробілами з обох боків
    (або знаходитися на початку/кінці рядка).
 
    Args:
        text: Вхідний рядок для аналізу.
 
    Yields:
        Дійсні числа типу float, знайдені в тексті.
    """
    # Регулярний вираз для пошуку цілих чисел а також чисел з десятковою крапкою або комою
    pattern = r'\b\d+[.,]?\d*\b'
    
    for match in re.finditer(pattern, text):
        number_str = match.group()
        
        try:
            yield float(number_str.replace(',', '.'))
        except ValueError:
            # Skip invalid matches if any
            continue


def sum_profit(text: str, func=generator_numbers) -> float:
    """
    Обчислює загальну суму дійсних чисел у тексті.
 
    Args:
        text: Вхідний рядок для аналізу.
        func:  Функція-генератор для отримання чисел із тексту.
 
    Returns:
        Загальна сума знайдених дійсних чисел.
    """
    return sum(func(text))


# Тестування функції sum_profit з генератором generator_numbers
if __name__ == "__main__":
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів. Також враховуємо бонус у розмірі 150 доларів, що додає до загальної суми."
    
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
    
    # Очікуваний результат: Загальний дохід: 1501.46

