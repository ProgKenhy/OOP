#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from keyboard import Keyboard


def show_menu():
    """Показывает меню программы"""
    print("\n" + "=" * 50)
    print("VIRTUAL KEYBOARD SIMULATOR")
    print("=" * 50)
    print("Commands:")
    print("  1. Type character (e.g., 'a', 'b', 'c')")
    print("  2. Key combinations:")
    print("     - ctrl+plus  : Volume Up")
    print("     - ctrl+minus : Volume Down")
    print("     - ctrl+p     : Media Player")
    print("     - ctrl+l     : Clear Screen")
    print("  3. Special commands:")
    print("     - undo       : Undo last command")
    print("     - redo       : Redo last undone command")
    print("     - bindings   : Show key bindings")
    print("     - history    : Show command history")
    print("     - stats      : Show statistics")
    print("     - clear      : Clear console")
    print("     - exit       : Exit program")
    print("=" * 50)


def main():
    """Главная функция программы"""
    keyboard = Keyboard()

    print("Virtual Keyboard initialized!")
    print("Output will be written to console and 'output.txt' file")

    # Очищаем файл вывода при запуске
    keyboard.output_manager.clear_file()

    while True:
        show_menu()

        try:
            user_input = input("\nEnter command: ").strip()

            if not user_input:
                continue

            # Специальные команды
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'undo':
                keyboard.undo()
            elif user_input.lower() == 'redo':
                keyboard.redo()
            elif user_input.lower() == 'bindings':
                keyboard.show_bindings()
            elif user_input.lower() == 'history':
                keyboard.show_history()
            elif user_input.lower() == 'stats':
                stats = keyboard.get_stats()
                print(f"\nStatistics:")
                print(f"  Total commands executed: {stats['total_commands']}")
                print(f"  Current history position: {stats['current_position']}")
                print(f"  Key bindings defined: {stats['key_bindings']}")
                print(f"  Current text length: {stats['current_text_length']}")
            elif user_input.lower() == 'clear':
                keyboard.press_key('ctrl+l')
            elif user_input.startswith('bind '):
                # Добавление новой привязки: bind ctrl+x command_type
                parts = user_input.split(' ', 2)
                if len(parts) == 3:
                    _, key_combo, command_type = parts
                    keyboard.add_key_binding(key_combo, command_type)
                else:
                    print("Usage: bind <key_combination> <command_type>")
            elif user_input.startswith('unbind '):
                # Удаление привязки: unbind ctrl+x
                parts = user_input.split(' ', 1)
                if len(parts) == 2:
                    _, key_combo = parts
                    keyboard.remove_key_binding(key_combo)
                else:
                    print("Usage: unbind <key_combination>")
            else:
                keyboard.press_key(user_input)

        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
