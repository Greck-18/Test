import sqlite3
from abc import abstractmethod,ABC


class University(ABC):

    _database="university.db"
    try:
        _connection=sqlite3.connect(_database)
    except sqlite3.Error:
        raise Exception("You have problem")
    _cursor=_connection.cursor()
    
    def _close_db(self):
        self.connection.close()

    @abstractmethod
    def _create_db(self):
        pass

    @abstractmethod
    def show_info(self):
        pass

    @abstractmethod
    def add_info(self):
        pass

    @abstractmethod
    def del_info(self):
        pass





        

class Student(University):

    def __init__(self):
        pass


    def _create_db(self):
        query="CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT NOT NULL,group_id INTEGER NOT NULL,FOREIGN KEY(group_id) REFERENCES groups(id))"
        self._cursor.execute(query)

    def show_info(self):
        with self._connection:
            return self._cursor.execute("SELECT students.name , groups.number FROM groups INNER JOIN students ON students.group_id=groups.id").fetchall()

    def add_info(self,name,group):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT number FROM groups").fetchall()) for i in j]
            if group not in data:
                self._cursor.execute("INSERT INTO groups(number) VALUES(?)",(group,))
            if len(data)>0:
                group_id=self._cursor.execute("SELECT id FROM groups WHERE number=?",(group,)).fetchone()[0]
            else:
                group_id=1
            return self._cursor.execute("INSERT INTO students(name,group_id) VALUES(?,?)",(name,group_id))

    def del_info(self,name):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM students").fetchall()) for i in j]
            if name in data:
                return self._cursor.execute("DELETE FROM students WHERE name=(?)",(name,))
            raise Exception("Такого пользователя не существует!")
    
class Teacher(University):

    def __init__(self):
        pass

    def _create_db(self):
        query="CREATE TABLE IF NOT EXISTS teachers(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT NOT NULL,subject_id INTEGER NOT NULL,FOREIGN KEY(subject_id) REFERENCES subjects(id))"
        return self._cursor.execute(query)

    def show_info(self):
        with self._connection:
            return self._cursor.execute("SELECT teachers.name , subjects.name FROM subjects INNER JOIN teachers ON teachers.subject_id=subjects.id").fetchall()
    
    def add_info(self,name,subject):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM subjects").fetchall()) for i in j]
            if subject not in data:
                self._cursor.execute("INSERT INTO subjects(name) VALUES(?)",(subject,))
            if len(data)>0:
                subject_id=self._cursor.execute("SELECT id FROM subjects WHERE name=?",(subject,)).fetchone()[0]
            else:
                subject_id=1
            return self._cursor.execute("INSERT INTO teachers(name,subject_id) VALUES(?,?)",(name,subject_id))

    def del_info(self,name):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM teachers").fetchall()) for i in j]
            if name in data:
                return self._cursor.execute("DELETE FROM teachers WHERE name=(?)",(name,))
            raise Exception("Такого пользователя не существует!")



class Subject(University):

    def __init__(self):
        pass

    def _create_db(self):
        query="CREATE TABLE IF NOT EXISTS subjects(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT NOT NULL)"
        return self._cursor.execute(query)
    
    def show_info(self):
        with self._connection:
            return self._cursor.execute("SELECT name FROM subjects").fetchall()
            

    def add_info(self,subject):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM subjects").fetchall()) for i in j]
            if subject not in data:
                return self._cursor.execute("INSERT INTO subjects(name) VALUES(?)",(subject,))
    
    def del_info(self,subject):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT name FROM subjects").fetchall()) for i in j]
            if subject in data:
                return self._cursor.execute("DELETE FROM subjects WHERE name=(?)",(subject,))
            raise Exception("Такого предмета не существует!")
            



class Group(University):

    def __init__(self):
        pass

    def _create_db(self):
        query="CREATE TABLE IF NOT EXISTS groups(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,number INTEGER NOT NULL)"
        return self._cursor.execute(query)


    def show_info(self):
        with self._connection:
            return self._cursor.execute("SELECT number FROM groups").fetchall()

    def add_info(self,number):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT number FROM groups").fetchall()) for i in j]
            if number not in data:
                return self._cursor.execute("INSERT INTO groups(number) VALUES(?)",(number,))

    def del_info(self,number):
        with self._connection:
            data=[i for j in list(self._cursor.execute("SELECT number FROM groups").fetchall()) for i in j]
            if number in data:
                return self._cursor.execute("DELETE FROM groups WHERE number=(?)",(number,))
            raise Exception("Такой группы  не существует!")















    
