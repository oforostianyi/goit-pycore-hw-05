"""
Декоратори для обробки помилок введення користувача.

Декоратор input_error перехоплює типові винятки, що виникають у
функціях-обробниках команд, і повертає зрозуміле повідомлення
замість того, щоб ламати програму.
"""

from functools import wraps


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.

    Перехоплює:
        ValueError  — розпакування args не вдалося (замало аргументів)
        KeyError    — звернення до відсутнього ключа в словнику контактів
        IndexError  — звернення до відсутнього індексу в списку args

    Args:
        func: Функція-обробник команди.

    Returns:
        Обгорнута функція, яка повертає рядок з помилкою замість виключення.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the argument for the command."

    return inner