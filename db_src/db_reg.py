import psycopg2
import config
import requests


def connect():
    db = psycopg2.connect(dbname=config.dbname, host=config.host,
                          port=config.port, user=config.user, password=config.passwd)
    return db



def selectAllUsers():
    db = connect()
    cur = db.cursor()
    try:
        cur.execute('SELECT * from public."user";')
    except:
        print("I can't SELECT from user")

    rows = cur.fetchall()
    return(rows)

def selectActivity(chat_id):
    db = connect()
    cur = db.cursor()
    rows = []
    try:
        cur.execute("""
                        SELECT * FROM public.user_activity
                        WHERE user_id = %s;
                        """,
                    (str(chat_id),))
        rows = cur.fetchall()
    except:
        print("I can't SELECT into user_event")

    return (rows)


def addUser(chat_id):
    db = connect()
    cur = db.cursor()
    try:
        cur.execute("""
                    INSERT INTO public.user(id) 
                    VALUES (%s);
                    """,
                    (chat_id))
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
                    """,
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
                        """,
                        (d['slug'], d['name']))
            print('DONE')
            db.commit()
        except:
            print("I can't INSERT into event")


def addCountPercent(chat_id, count, usersEvents):
    db = connect()
    print('I\'m here')
    cur = db.cursor()

    for d in usersEvents:
        print(chat_id, d, int((usersEvents[d] / count) * 5))
        try:
            cur.execute("""
                        INSERT INTO public.user_event(user_id, event_id, count) 
                        VALUES (%s, %s, %s);
                        """,
                        (str(chat_id), d, int((usersEvents[d] / count) * 5)))
            print('DONE')
            db.commit()
        except:
            db.rollback()
            print("I can't INSERT into user_event")
            print("I try UPDATE user_event")
            cur.execute("""
                        UPDATE public.user_event
                        SET count = %s
                        WHERE user_id = %s AND event_id = %s;
                        """,
                        (int((usersEvents[d] / count) * 5), str(chat_id), d))
            print('DONE')
            db.commit()


def addActivity(chat_id, UA):
    db = connect()

    cur = db.cursor()

    print('AAAAAAAAAAAAAAAAAAAAAAA', UA)

    usersActivity = { i: {'id' : UA[i]['id'], 'mark' : UA[i]['mark']} for i in UA if UA[i]['mark'] != 0}

    for d in usersActivity:
        print(chat_id, usersActivity[d]['id'], usersActivity[d]['mark'])
        try:
            cur.execute("""
                        INSERT INTO public.user_activity(user_id, act_id, mark) 
                        VALUES (%s, %s, %s);
                        """,
                        (str(chat_id), usersActivity[d]['id'], usersActivity[d]['mark']))
            print('DONE')
            db.commit()
        except:
            db.rollback()
            print("I can't INSERT into user_activity")
            if(usersActivity[d]['mark'] != 0):
                print("I try UPDATE user_activity")
                cur.execute("""
                            UPDATE public.user_activity
                            SET mark = %s
                            WHERE user_id = %s AND act_id = %s;
                            """,
                            (usersActivity[d]['mark'], str(chat_id), str(usersActivity[d]['id'])))
                print('DONE')
            db.commit()

def getEventMarkInfo(chat_id):
    db = connect()
    cur = db.cursor()
    rows = []
    try:
        cur.execute("""
                    SELECT * FROM public.user_event 
                    WHERE user_id = %s AND count!=0;
                    """,
                    (str(chat_id),))
        rows = cur.fetchall()
    except:
        print("I can't SELECT into user_event")

    return(rows)


def getRecomendation(chat_id, simList):
    db = connect()
    cur = db.cursor()
    rows = []
    try:
        cur.execute("""
                    SELECT n1.act_id, avg(n1.mark)
                    FROM (SELECT act_id, mark
                        FROM public.user_activity
                        WHERE user_id != %s AND user_id = ANY(%s)) n1
                    GROUP BY n1.act_id
                    HAVING avg(n1.mark) >= 2.5
                    ORDER BY 2 DESC;
                    """,
                    (str(chat_id), simList))
        rows = cur.fetchall()
    except:
        print("I can't SELECT into user_event")
    return(rows)