import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox

class PhoneBookApp:
    def __init__(self, master):
        self.master = master
        master.title("Телефонная книга")
        master.geometry("600x500")
        master.configure(background="#ffffff")
        master.resizable(width=False, height=False)

        self.conn = None
        self.cursor = None

        self.create_database()
        self.create_widgets()
        self.update_tree()

    def create_database(self):
        try:
            self.conn = sqlite3.connect('phonebook.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contacts'")
            table_exists = self.cursor.fetchone()
            if not table_exists:
                self.cursor.execute('''
                    CREATE TABLE contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        surname TEXT,
                        phone TEXT UNIQUE,
                        email TEXT UNIQUE
                    )
                ''')
                self.conn.commit()
                print("Таблица 'contacts' создана.")
            else:
                print("Таблица 'contacts' уже существует.")

        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании/проверке базы данных: {e}")
            # Handle database creation failure appropriately (e.g., exit or disable features)

    def create_widgets(self):
        # Рамки
        frame_up = tk.Frame(self.master, width=500, height=50, bg="#6E3482")
        frame_up.grid(row=0, column=0, padx=0, pady=1, sticky="ew")

        frame_down = tk.Frame(self.master, width=600, height=150, bg="#ffffff")
        frame_down.grid(row=1, column=0, padx=0, pady=1, sticky="ew")

        frame_table = tk.Frame(self.master, width=600, height=300, bg="#ffffff", relief="flat")
        frame_table.grid(row=2, column=0, padx=10, pady=1, sticky="nsew")

        # Виджеты Frame_up
        app_name = tk.Label(frame_up, text="Телефонная книга", height=1, font=('Verdana 17 bold'), bg="#6E3482", fg="#ffffff")
        app_name.place(x=5, y=5)

        # Виджеты frame_down
        l_name = tk.Label(frame_down, text="Имя:", width=10, font=('Ivy 10'), bg="#ffffff", anchor=tk.W)
        l_name.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.e_name = tk.Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
        self.e_name.grid(row=0, column=1, padx=5, pady=5)

        l_surname = tk.Label(frame_down, text="Фамилия:", width=10, font=('Ivy 10'), bg="#ffffff", anchor=tk.W)
        l_surname.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.e_surname = tk.Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
        self.e_surname.grid(row=1, column=1, padx=5, pady=5)

        l_telephone = tk.Label(frame_down, text="Телефон:", width=10, font=('Ivy 10'), bg="#ffffff", anchor=tk.W)
        l_telephone.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.e_telephone = tk.Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
        self.e_telephone.grid(row=2, column=1, padx=5, pady=5)

        l_email = tk.Label(frame_down, text="Email:", width=10, height=1, font=('Ivy 10'), bg="#ffffff", anchor=tk.W)
        l_email.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.e_email = tk.Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
        self.e_email.grid(row=3, column=1, padx=5, pady=5)

        # Поле и кнопка поиска
        l_search = tk.Label(frame_down, text="Поиск:", width=10, font=('Ivy 10'), bg="#ffffff", anchor=tk.W)
        l_search.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.e_search = tk.Entry(frame_down, width=15, justify='left', font=('Ivy 11'), highlightthickness=1, relief="solid")
        self.e_search.grid(row=0, column=3, padx=5, pady=5)
        tk.Button(frame_down, text="Найти", command=self.search_contact, width=10).grid(row=0, column=4, padx=5, pady=5)


        # Кнопки
        tk.Button(frame_down, text="Добавить", command=self.add_contact, width=10).grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        tk.Button(frame_down, text="Удалить", command=self.delete_contact, width=10).grid(row=5, column=0, padx=5, pady=5)
        tk.Button(frame_down, text="Изменить", command=self.update_contact, width=10).grid(row=5, column=1, padx=5, pady=5)

        # Treeview
        listheader = ['ID', 'Имя', 'Фамилия', 'Номер', 'Email']
        self.tree = ttk.Treeview(frame_table, selectmode="extended", columns=listheader, show="headings")

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        for i, col in enumerate(listheader):
            self.tree.heading(i, text=col, anchor=tk.W)
            self.tree.column(i, anchor=tk.W, width=100)

    def update_tree(self, rows=None):
        if self.conn is None: #Check if database is already connected
            return
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            if rows is None:
                self.cursor.execute("SELECT * FROM contacts")
                rows = self.cursor.fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обновления дерева: {e}")

    def add_contact(self):
        name = self.e_name.get()
        surname = self.e_surname.get()
        phone = self.e_telephone.get()
        email = self.e_email.get()

        if not name:
            messagebox.showerror("Ошибка", "Поле 'Имя' обязательно для заполнения.")
            return
        if phone and not phone.isdigit():
            messagebox.showerror("Ошибка", "Неверный формат номера телефона.")
            return
        if email and "@" not in email:
            messagebox.showerror("Ошибка", "Неверный формат email.")
            return

        try:
            self.cursor.execute("INSERT INTO contacts (name, surname, phone, email) VALUES (?, ?, ?, ?)", (name, surname, phone, email))
            self.conn.commit()
            self.update_tree()
            self.clear_entries()
            messagebox.showinfo("Успех", "Контакт добавлен!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Контакт с таким номером телефона или email уже существует.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка добавления контакта: {e}")


    def delete_contact(self):
        try:
            selected_item = self.tree.selection()[0]
            item_id = self.tree.item(selected_item)['values'][0]
            self.cursor.execute("DELETE FROM contacts WHERE id = ?", (item_id,))
            self.conn.commit()
            self.update_tree()
            messagebox.showinfo("Успех", "Контакт удален!")
        except IndexError:
            messagebox.showerror("Ошибка", "Выберите контакт для удаления.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления контакта: {e}")

    def update_contact(self):
        try:
            selected_item = self.tree.selection()[0]
            item_id = self.tree.item(selected_item)['values'][0]
            name = self.e_name.get()
            surname = self.e_surname.get()
            phone = self.e_telephone.get()
            email = self.e_email.get()

            if not name:
                messagebox.showerror("Ошибка", "Поле 'Имя' обязательно для заполнения.")
                return
            if phone and not phone.isdigit():
                messagebox.showerror("Ошибка", "Неверный формат номера телефона.")
                return
            if email and "@" not in email:
                messagebox.showerror("Ошибка", "Неверный формат email.")
                return

            self.cursor.execute("UPDATE contacts SET name = ?, surname = ?, phone = ?, email = ? WHERE id = ?",
                               (name, surname, phone, email, item_id))
            self.conn.commit()
            self.update_tree()
            self.clear_entries()
            messagebox.showinfo("Успех", "Контакт обновлен!")
        except IndexError:
            messagebox.showerror("Ошибка", "Выберите контакт для обновления.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обновления контакта: {e}")

    def clear_entries(self):
        self.e_name.delete(0, tk.END)
        self.e_surname.delete(0, tk.END)
        self.e_telephone.delete(0, tk.END)
        self.e_email.delete(0, tk.END)

    def search_contact(self):
        search_term = self.e_search.get()
        if not search_term:
            messagebox.showwarning("Предупреждение", "Введите поисковый запрос!")
            return

        try:
            self.cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR surname LIKE ? OR phone LIKE ? OR email LIKE ?",
                               ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
            rows = self.cursor.fetchall()
            self.update_tree(rows)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")


root = tk.Tk()
app = PhoneBookApp(root)
root.mainloop()

