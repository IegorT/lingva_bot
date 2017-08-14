# -*- coding: utf-8 -*-

import sqlite3
import shelve
from config import shelve_db, sqlite_db
tb_name = 'words'

#SQLite worker
class DBWorker:

    def __init__(self, dbname=sqlite_db):
        self.dbname = dbname
        self.connect = sqlite3.connect(dbname)
        self.cursor = self.connect.cursor()

    def add_new(self, word_eng, word_rus):
        # add new word to the base DB
        words = (word_eng, word_rus)
        execute_command = \
        'INSERT INTO {0} (eng, rus) VALUES (?, ?)'.format(tb_name)
        if compare_words(word_eng, word_rus) == None:
            return True
        else:
            with self.connect:
                self.cursor.execute(execute_command, words)
                self.connect.commit()
            return False
            

    def del_word(self, word_eng, word_rus):
        # del words from DB 
        words = (word_eng, word_rus)
        execute_command = \
        'DELETE FROM {0} WHERE eng = (?) AND rus = (?)'.format(tb_name)
        with self.connect:
            self.cursor.execute(execute_command, words)
            self.connect.commit()
        
    def compare_words(self, word_eng, word_rus):
        # compere words from user and DB and return False if their None in DB
        words = (word_eng, word_rus)
        execute_command = \
        'SELECT * FROM {0} WHERE eng = (?) AND rus = (?)'.format(tb_name)
        with self.connect:
            return self.cursor.execute(execute_command, words).fetchone()

    def random_word(self, user_num):
        # return random word with minimun point from DB
        execute_command = \
        ("SELECT eng, rus FROM {0} WHERE {1} = (SELECT min({1}) FROM {0}) ORDER by RANDOM () LIMIT 1").format(tb_name, user_num)
        with self.connect:
            return self.cursor.execute(execute_command).fetchone()
        
    def add_point(self, user_num, word_eng, word_rus):
        # add one point to user
        words = (word_eng, word_rus, word_eng, word_rus)
        execute_command = \
        ("UPDATE {0} SET {1} = (1 + (SELECT {1} FROM {0} WHERE eng = (?) AND rus =(?))) WHERE eng =(?) AND rus =(?)").format(tb_name, user_num)
        with self.connect:
                self.cursor.execute(execute_command, words)
                self.connect.commit()
      
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connect.close()

#Shelve worker
def save_words(user, lang):
    """clear data from database, add new data and return word"""
    sqlite = DBWorker()
    eng, rus = sqlite.random_word(user)
    with shelve.open(shelve_db) as db:
        db[user] = '{0}-{1}-{2}'.format(eng, rus, lang)
    if lang == 'eng': return eng
    else: return rus

#load data file
def load_words(user):
    with shelve.open(shelve_db) as db:
        try:
            return db[user].split('-')
        except KeyError:
            return None
    
#clear data from database
def del_words(user):
    with shelve.open(shelve_db) as db:
        del db[user]

#change users status
def status(user_id, status=0):
    with shelve.open(shelve_db) as db:
        user_id = '{}'.format(user_id)
        db[user_id] = '{}'.format(status)
        

