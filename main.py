import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox
from tkinter import Button
from tkinter import ttk
from tkinter import simpledialog
#импорт всего что нужно да и в принципе всего что возможно походу


class Main (tk.Frame):
    def __init__ (self, master):
        self.master = master
        self.con = sq.connect ('rabotniki.db')
        self.tree = ttk.Treeview()
        self.tree["columns"] = ("ID", "Name", "Phone", "Email", "Salary")
        self.tree.heading ("ID", text = "ID")
        self.tree.heading ("Name", text = "Name")
        self.tree.heading ("Phone", text = "Phone")
        self.tree.heading ("Email", text = "Email")
        self.tree.heading ("Salary", text = "Salary")
        self.tree.pack (padx = 20, pady = 20)
        #таблицу сделали

        self.create_widjet ()
        self.create_table ()
        self.update_treeview()
        #сделали кнопки и таблицу и чтобы обновлялось

    
    def create_table (self):
        con = sq.connect ('rabotniki.db')
        cur = con.cursor ()
        #курсор прикрепили базу данных сделали

        cur.execute ('''
                   CREATE TABLE IF NOT EXISTS worker(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   number TEXT,
                   email TEXT,
                   salary TEXT
                   );
                   ''')
        con.commit ()
        #создали таблицу работников с колоннами там и всем что надо в таблицах
        

    def create_widjet (self):
        #виджеты кнопочки всякие
        self.button_add_worker = Button (self.master, text = "Добавить сотрудника", command = self.create_add_worker)
        self.button_add_worker.pack (pady = 10)
        #добавлять сотрудников кнопка
        self.button_delete_worker = Button (self.master, text = "Удалить сотрудника", command = self.delete_worker)
        self.button_delete_worker.pack (pady = 10)
        #удалять сотруддников кнопка
        self.button_edit_worker = Button (self.master, text = 'Изменить сотрудника', command = self.edit_worker)
        self.button_edit_worker.pack (pady=10)
        #изменять сотрудников кнопка
        self.button_search_worker = Button (self.master, text = 'Найти сотрудника', command = self.search_worker)
        self.button_search_worker.pack (pady=10)
        #искать сотрудников кнопка
        self.button_update = Button (self.master, text = 'Обновить', command = self.update_treeview)
        self.button_update.pack(pady = 10)
        #обновлять после поиска кнопка (чтобы снова показывало всех)


    def create_add_worker (self):
        name = simpledialog.askstring ("Ввод", "Введите ФИО сотрудника:")
        email = simpledialog.askstring ("Ввод", "Введите почту сотрудника:")
        number = simpledialog.askstring ("Ввод", "Введите номер сотрудника:")
        salary = simpledialog.askstring ("Ввод", "Введите зарплату сотрудника:")
        #переменные передать сделали

        con = sq.connect ('rabotniki.db')
        cur = con.cursor ()

        cur.execute ('INSERT INTO worker (name, number, email, salary) VALUES (?,?,?,?)', (name, number, email, salary))
        con.commit()
        self.update_treeview()
        #добавили сотрудника и обновили вид таблицы


    def update_treeview(self):
        #очистили вид
        for item in self.tree.get_children():
            self.tree.delete(item)

        cur = self.con.cursor()
        cur.execute("SELECT * FROM worker")
        worker = cur.fetchall()

        for worker in worker:
            self.tree.insert("", "end", values=worker)


    def delete_worker (self):
        con = sq.connect ('rabotniki.db')
        cur = self.con.cursor ()
        worker_id_to_delete = simpledialog.askinteger("Ввод", "Введите id сотрудника, которого нужно удалить:", )
        cur.execute('DELETE FROM worker WHERE id=?', (worker_id_to_delete,))
        self.con.commit()
        self.update_treeview()


    def edit_worker (self):
        id_worker_to_edit = simpledialog.askinteger("Ввод", "Введите id сотрудника, которого нужно изменить:", )

        self.con=sq.connect('rabotniki.db')
        cur=self.con.cursor()
        cur.execute("SELECT * FROM worker WHERE id=?", (id_worker_to_edit,))
        workers = cur.fetchone()

        if workers:
            #если сотрудник есть
            name_edit = simpledialog.askstring("Ввод", "Введите измененное имя сотрудника:", initialvalue=workers[1])
            number_edit = simpledialog.askstring("Ввод", "Введите измененный номер сотрудника:", initialvalue=workers[2])
            email_edit = simpledialog.askstring("Ввод", "Введите измененную почту сотрудника:", initialvalue=workers[3])
            salary_edit = simpledialog.askstring("Ввод", "Введите измененную зарплату сотрудника:", initialvalue=workers[4])
            #переменные передать чтобы изменить сделали

            cur.execute('UPDATE worker SET name=?, number=?, email=?, salary=? WHERE id=?', (name_edit, number_edit, email_edit, salary_edit, id_worker_to_edit))
            self.con.commit()
            self.update_treeview()
            #изменили данные сотрудника обновили вид таблицы
        else:
            #если сотрудника нет
            messagebox.showerror("Ошибка", "Сотрудник не найден")


    def search_worker(self):
        worker_to_search = simpledialog.askstring("Поиск", "Введите ФИО сотрудника:")
        
        con = sq.connect('rabotniki.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM worker WHERE name=?", (worker_to_search,))
        workers = cur.fetchall()
        #ввели и выбрали сотрудника нужного код

        if workers:
            #если есть сотрудник с таким ФИО
            self.tree.delete(*self.tree.get_children())
            for worker in workers:
                self.tree.insert("", "end", values=worker)

        else:
            #если нет такого сотрудника
            messagebox.showinfo("Инфо", "Нет сотрудника с таким ФИО")


    def on_closing (self):
        self.con.close()
        self.master.destroy()
        #чтобы закрыть окно сделали


if __name__ == '__main__':
    app = tk.Tk ()
    app1 = Main (app)
    app.title ('Сотрудники :3;3:3;3')
    app.geometry ('2000x500')
    app.protocol ("WM_DELETE_WINDOW", app1.on_closing)
    app.mainloop ()
    #сделали приложение окно название окна loop не помню что это но надо


#мэйд бай Горбунцова Екатерина, бай