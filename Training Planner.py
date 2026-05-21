import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Инициализация окна
root = tk.Tk()
root.title("Training Planner")
root.geometry("800x600")

# Настройка весов строк и столбцов для адаптивности
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# --- ОСНОВНОЙ КОНТЕЙНЕР ---
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
main_frame.columnconfigure(0, weight=3)  # Форма ввода занимает 75 % ширины
main_frame.columnconfigure(1, weight=1)  # Панель фильтрации — 25 % ширины
main_frame.rowconfigure(1, weight=1)        # Таблица занимает основную часть высоты

# --- ФОРМА ВВОДА (слева, pack) ---
input_frame = tk.Frame(main_frame)
input_frame.grid(row=0, column=0, sticky="new", pady=(0, 10))
input_frame.columnconfigure(0, weight=1)

# Поля формы
tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").pack(pady=2, anchor="w")
date_entry = tk.Entry(input_frame)
date_entry.pack(fill="x", pady=2)

tk.Label(input_frame, text="Тип тренировки:").pack(pady=2, anchor="w")
training_type_entry = tk.Entry(input_frame)
training_type_entry.pack(fill="x", pady=2)

tk.Label(input_frame, text="Длительность (мин):").pack(pady=2, anchor="w")
duration_entry = tk.Entry(input_frame)
duration_entry.pack(fill="x", pady=2)

def add_training():
    date = date_entry.get()
    training_type = training_type_entry.get()
    duration = duration_entry.get()

    # Проверка корректности ввода
    if not is_valid_date(date):
        messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
        return
    if not is_valid_duration(duration):
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
        return

    # Добавляем в таблицу
    tree.insert('', 'end', values=(date, training_type, duration))

    # Сохраняем в JSON
    save_to_json()

    # Очищаем поля ввода
    date_entry.delete(0, tk.END)
    training_type_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)

def apply_filter():
    filter_type = filter_type_entry.get().lower().strip()
    filter_date = filter_date_entry.get().strip()

    items = tree.get_children()
    for item in items:
        values = tree.item(item)['values']
        show_item = True


        if filter_type and filter_type not in values[1].lower():
            show_item = False
        if filter_date and filter_date != values[0]:
            show_item = False

        if show_item:
            tree.item(item, tags=('visible',))
        else:
            tree.item(item, tags=('hidden',))

    tree.tag_configure('visible', foreground='black')
    tree.tag_configure('hidden', foreground='white')


def reset_filter():
    for item in tree.get_children():
        tree.item(item, tags=('visible',))
    filter_type_entry.delete(0, tk.END)
    filter_date_entry.delete(0, tk.END)

# Кнопка «Добавить тренировку»
add_button = tk.Button(input_frame, text="Добавить тренировку", command=add_training, bg="#25dd2e")
add_button.pack(pady=10)

# --- ПАНЕЛЬ ФИЛЬТРАЦИИ (справа, grid) ---
filter_frame = tk.Frame(main_frame, relief="groove", borderwidth=2)
filter_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
filter_frame.columnconfigure(0, weight=1)

tk.Label(filter_frame, text="Фильтрация по типу:").grid(row=0, column=0, sticky="w", pady=5)
filter_type_entry = tk.Entry(filter_frame)
filter_type_entry.grid(row=1, column=0, sticky="ew", pady=2)

tk.Label(filter_frame, text="Фильтрация по дате:").grid(row=2, column=0, sticky="w", pady=5)
filter_date_entry = tk.Entry(filter_frame)
filter_date_entry.grid(row=3, column=0, sticky="ew", pady=2)

# Кнопки фильтрации
button_frame = tk.Frame(filter_frame)
button_frame.grid(row=4, column=0, pady=10)
button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

filter_button = tk.Button(button_frame, text="Применить фильтр", command=apply_filter,bg="#25dd2e")
filter_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

reset_button = tk.Button(button_frame, text="Сбросить фильтр", command=reset_filter, bg="#dd4c4c")
reset_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

# --- ТАБЛИЦА (занимает всю нижнюю часть) ---
table_frame = tk.Frame(main_frame)
table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
table_frame.columnconfigure(0, weight=1)
table_frame.rowconfigure(0, weight=1)

columns = ('Дата', 'Тип тренировки', 'Длительность')
tree = ttk.Treeview(table_frame, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill="both", expand=True)

# --- ФУНКЦИИ ---


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_valid_duration(duration_str):
    try:
        duration = float(duration_str)
        return duration > 0
    except ValueError:
        return False

def save_to_json():
    data = []
    for item in tree.get_children():
        data.append(tree.item(item)['values'])
    with open('trainings.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json():
    if os.path.exists('trainings.json'):
        with open('trainings.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                tree.insert('', 'end', values=item)






# --- ЗАПУСК ---
# Загружаем данные при старте
load_from_json()
root.mainloop()














