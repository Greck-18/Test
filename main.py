import sqlite3
from abc import abstractmethod,ABC


class University(ABC):
    '''Абстрактный класс'''

    #инициализация бд
    _database="university.db"
    try:
        _connection=sqlite3.connect(_database)
    except sqlite3.Error:
        raise Exception("You have problem")
    _cursor=_connection.cursor()

    def __str__(self):
        return """Выберете что вы хотите выпонить:
                1-Просмотр
                2-Добавление
                3-Удаение"""

    
    def _close_db(self):
        self.connection.close()

    #создание таьлицы
    @abstractmethod
    def _create_table(self):
        pass

    #вывод информации
    @abstractmethod
    def show_info(self):
        pass

    #добавление информации
    @abstractmethod
    def add_info(self):
        pass

    #удлаение информации
    @abstractmethod
    def del_info(self):
        pass



class Student(University):
    '''Класс студент'''
    def __init__(self):
        pass


    def _create_table(self):
        query="CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT NOT NULL,group_id INTEGER NOT NULL,FOREIGN KEY(group_id) REFERENCES groups(id))"
        self._cursor.execute(query)

    def show_info(self):
        with self._connection:
            data= self._cursor.execute("SELECT students.name , groups.number FROM groups INNER JOIN students ON students.group_id=groups.id").fetchall()
            return "\n".join("{}\t{}".format(k, v) for k, v in dict(data).items())
             


    def add_info(self):
        _name,_group=(input("Введите имя ученика: "),int(input("Введите группу , где он учится: ")))
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT number FROM groups").fetchall()) for i in j]
            if _group not in data:
                self._cursor.execute("INSERT INTO groups(number) VALUES(?)",(_group,))
            if len(data)>0:
                group_id=self._cursor.execute("SELECT id FROM groups WHERE number=?",(_group,)).fetchone()[0]
            else:
                group_id=1
            return self._cursor.execute("INSERT INTO students(name,group_id) VALUES(?,?)",(_name,group_id))

    def del_info(self):
        _name=input("Введите имя ученика , которого хотите удалить: ")
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM students").fetchall()) for i in j]
            if _name in data:
                return self._cursor.execute("DELETE FROM students WHERE name=(?)",(_name,))
            raise Exception("Такого пользователя не существует!")
    

class Teacher(University):
    """Класс преподаватель"""
    def __init__(self):
        pass

    def _create_table(self):
        query="CREATE TABLE IF NOT EXISTS teachers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT NOT NULL,subject_id INTEGER NOT NULL,FOREIGN KEY(subject_id) REFERENCES subjects(id))"
        return self._cursor.execute(query)

    def show_info(self):
        with self._connection:
            data = self._cursor.execute("SELECT teachers.name , subjects.name FROM subjects INNER JOIN teachers ON teachers.subject_id=subjects.id").fetchall()
            return "\n".join("{}\t{}".format(k, v) for k, v in dict(data).items())
    
    def add_info(self):
        _name,_subject=(input("Введите имя преподавателя: "),input("Введите предмет , который он введёт: "))
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM subjects").fetchall()) for i in j]
            if _subject not in data:
                self._cursor.execute("INSERT INTO subjects(name) VALUES(?)",(_subject,))
            if len(data)>0:
                subject_id=self._cursor.execute("SELECT id FROM subjects WHERE name=?",(_subject,)).fetchone()[0]
            else:
                subject_id=1
            return self._cursor.execute("INSERT INTO teachers(name,subject_id) VALUES(?,?)",(_name,subject_id))

    def del_info(self):
        _name=input("Введите имя преподавателя , которого хотите удалить: ")
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM teachers").fetchall()) for i in j]
            if _name in data:
                return self._cursor.execute("DELETE FROM teachers WHERE name=(?)",(_name,))
            raise Exception("Такого пользователя не существует!")



class Subject(University):
    """Класс предметов преподавателей"""
    def __init__(self):
        pass

    def _create_table(self):
        query="CREATE TABLE IF NOT EXISTS subjects(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT NOT NULL)"
        return self._cursor.execute(query)
    
    def show_info(self):
        with self._connection:
            return "\n".join(" ".join(sub) for sub in self._cursor.execute("SELECT name FROM subjects").fetchall())
            

    def add_info(self):
        _subject=input("Введите предмет,который хотите добавить: ")
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM subjects").fetchall()) for i in j]
            if _subject not in data:
                return self._cursor.execute("INSERT INTO subjects(name) VALUES(?)",(_subject,))
    
    def del_info(self):
        _subject=input("Введите предмет,который хотите удалить: ")
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM subjects").fetchall()) for i in j]
            if _subject in data:
                return self._cursor.execute("DELETE FROM subjects WHERE name=(?)",(_subject,))
            raise Exception("Такого предмета не существует!")
            



class Group(University):
    """Класс групп учащихся"""
    def __init__(self):
        pass

    def _create_table(self):
        query="CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,number INTEGER NOT NULL)"
        return self._cursor.execute(query)


    def show_info(self):
        with self._connection:
            return '\n'.join([str(item) for sublist in self._cursor.execute("SELECT number FROM groups").fetchall() for item in sublist])

    def add_info(self):
        _number=int(input("Введите номер группы , которую хотите добавить: "))
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT number FROM groups").fetchall()) for i in j]
            if _number not in data:
                return self._cursor.execute("INSERT INTO groups(number) VALUES(?)",(_number,))

    def del_info(self):
        _number=int(input("Введите номер группы , которую хотите удалить: "))
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT number FROM groups").fetchall()) for i in j]
            if _number in data:
                return self._cursor.execute("DELETE FROM groups WHERE number=(?)",(_number,))
            raise Exception("Такой группы  не существует!")



class Menu():
    """Класс пользовательского меню"""
    def __init__(self):
        self._student=Student()
        self._teacher=Teacher()
        self._group=Group()
        self._subject=Subject()
    

    def __str__(self):
        pass 

    def _create_db(self):
        self._student._create_table()
        self._teacher._create_table()
        self._group._create_table()
        self._subject._create_table()

    def main(self):
        while True:
            choice=input("""Выберете с каким объектом работать:
                    1-Студент
                    2-Учитель
                    3-Предмет
                    4-Группа
                    0-выход\nВаш выбор: """)
            if choice=='1':
                _object=self._student
            elif choice == '2':
                _object=self._teacher
            elif choice == '3':
                _object =self._subject
            elif choice == '4':
                _object = self._group
            else :
                return 0
            
            print(_object)
            chose=input("Введите номер: ")
            if chose =='1':
                print(_object.show_info())
            elif chose == '2':
                _object.add_info()
            elif chose =='3':
                _object.del_info()


if __name__=="__main__":
    obj=Menu()
    obj._create_db()
    obj.main()




            


        










    
