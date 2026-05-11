"""Головна точка входу для програми, яка реалізує консольного бота-помічника 
для роботи з книгою контактів.
 
Усі print та input відбуваються виключно тут — обробники команд лише
повертають рядки. Це робить логіку легко тестованою і відокремлює
взаємодію з користувачем від бізнес-логіки.
 
Підтримувані команди:
    hello                       — привітання
    help                        — список доступних команд
    add <name> <phone>          — додати контакт
    change <name> <new_phone>   — оновити номер існуючого контакту
    phone <name>                — показати номер контакту
    all                         — показати всі контакти
    close, exit                 — завершити роботу

Використання:
    python main.py
"""
 
from parser import parse_input
from handlers import add_contact, change_contact, show_phone, show_all
 
 
def main() -> None:
    """Головний цикл запит-відповідь."""
    contacts: dict[str, str] = {}
    print("Welcome to the assistant bot! Type 'help' for available commands.")
 
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
 
        if command in ("close", "exit"):
            print("Good bye!")
            break
        # Команда 'help' не була вказана в умові, 
        # але вона корисна для користувача, тому я її додав.
        elif command == "help":
            print(
                "Available commands: \n"
                "hello - for greeting, \n"
                "add <name> <phone> - to add a contact, \n"
                "change <name> <new_phone> - to update a contact's phone number, \n"
                "phone <name> - to show a contact's phone number, \n"
                "all - to show all contacts, \n"
                "close/exit - to exit the program"
            )
 
        elif command == "hello":
            print("How can I help you?")
 
        elif command == "add":
            print(add_contact(args, contacts))
 
        elif command == "change":
            print(change_contact(args, contacts))
 
        elif command == "phone":
            print(show_phone(args, contacts))
 
        elif command == "all":
            print(show_all(contacts))
 
        else:
            print("Invalid command.")
 
 
if __name__ == "__main__":
    main()
