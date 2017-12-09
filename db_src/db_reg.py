import psycopg2
import config
import requests
import json
import telebot

def connect():
    db = psycopg2.connect(dbname=config.dbname, host=config.host, port=config.port, user=config.user,
                          password=config.passwd)
    return db

'''
#Регистрация
db = connect()
cur = db.cursor()
try:
    cur.execute('SELECT * from public."user";')
except:
    print("I can't SELECT from user")

rows = cur.fetchall()
print("\nRows: \n")
for row in rows:
    print("   ", row[0])

'''

def addUser(chat_id):
    db = connect()
    cur = db.cursor()
    try:
        cur.execute("INSERT INTO public.user(id) VALUES (%(id)s);", chat_id)
        print('DONE')
        db.commit()
    except:
        print("I can't SELECT from user")

def addCityToUser(user_id, city_id):
    db = connect()
    cur = db.cursor()
    try:
        cur.execute("""
                    INSERT INTO public.user_city(user_id, city_id) 
                    VALUES (%s, %s);
                    """ ,
                    (user_id, city_id))
        print('DONE')
        db.commit()
    except:
        print("I can't SELECT from user")

def addEvent(dic):
    url = "https://kudago.com/public-api/v1.2/event-categories/?lang=ru"
    headers = {'Content-Type': 'application/json'}
    r = requests.get(url, '', headers=headers)
    dic = r.json()

    db = connect()
    cur = db.cursor()
    for d in dic:
        try:
            cur.execute("""
                        INSERT INTO public.event(event_id, event_name) 
                        VALUES (%s, %s);
                        """ ,
                        (d['slug'], d['name']))
            print('DONE')
            db.commit()
        except:
            print("I can't SELECT from user")
