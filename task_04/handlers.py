"""
Функції-обробники команд бота.

Обробники команд повертають рядок із результатом — без жодних print чи input.
Кожен обробник захищений декоратором @input_error, який перехоплює
ValueError / KeyError / IndexError і повертає зрозуміле повідомлення
замість того, щоб переривати програму.

Ручні перевірки len(args) замінені на розпакування з довірою до декоратора:
якщо аргументів замало — розпакування само кине ValueError, який декоратор
перехопить і поверне відповідне повідомлення.
"""

from decorators import input_error


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    """
    Додає новий контакт у словник.

    Очікує рівно два аргументи: ім'я та телефон.
    При розпакуванні в менше або більше значень — ValueError → декоратор.

    :param args: список аргументів — очікується [ім'я, телефон]
    :param contacts: словник контактів (мутується)
    :return: рядок з результатом операції
    """
    name, phone = args  # ValueError якщо args не рівно 2 елементи

    if name in contacts:
        return f"Contact '{name}' already exists. Use 'change' to update."

    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    """
    Змінює номер телефону для існуючого контакту.

    Очікує рівно два аргументи: ім'я та новий телефон.
    Якщо контакту немає — KeyError → декоратор.

    :param args: список аргументів — очікується [ім'я, новий_телефон]
    :param contacts: словник контактів (мутується)
    :return: рядок з результатом операції
    """
    name, phone = args  # ValueError якщо args не рівно 2 елементи

    # Явно кидаємо KeyError, щоб декоратор повернув "Contact not found."
    if name not in contacts:
        raise KeyError(name)

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    """
    Повертає номер телефону для зазначеного контакту.

    Очікує рівно один аргумент: ім'я.
    Якщо args порожній — IndexError → декоратор.
    Якщо контакту немає — KeyError → декоратор.

    :param args: список аргументів — очікується [ім'я]
    :param contacts: словник контактів
    :return: номер телефону або повідомлення про помилку
    """
    name = args[0]          # IndexError якщо args порожній
    return contacts[name]   # KeyError якщо контакт не знайдений


@input_error
def show_all(contacts: dict[str, str]) -> str:
    """
    Формує рядок із усіма збереженими контактами.

    :param contacts: словник контактів
    :return: відформатований список або повідомлення про порожню книгу
    """
    if not contacts:
        return "No contacts saved."

    name_width = max(len(name) for name in contacts)
    lines = [f"{name:<{name_width}} : {phone}"
             for name, phone in contacts.items()]
    return "\n".join(lines)