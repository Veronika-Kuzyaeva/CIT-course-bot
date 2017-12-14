from db_src.db_reg import *

from KudaGoAPIrequest import getDigest
from AI_module import Similarity

class User:
    'User\' info & click counter & prefer events'
    count = 0
    current_city = ''
    current_event = ''
    usersEvents = {}
    usersActivity = {}
    simList = []

    def __init__(self, chat_id):
        self.chat_id = chat_id

    def addEventClick(self, evName):
        if (evName not in self.usersEvents):
            self.usersEvents.update({evName : 1})
        else:
            self.usersEvents[evName]+=1


    def addActDigest(self):
        self.usersActivity = {}
        newDigest = getDigest(self.current_city, self.current_event)
        active = {m[1]: m[2] for m in selectActivity(self.chat_id)}
        print(active)
        print(newDigest)
        i=0
        for act in newDigest:
            print(str(act['id']))
            if(str(act['id']) not in active):
                self.usersActivity[i] = {
                    'id' : act['id'],
                    'msg' : "%s\n%s\n[Ссылка на событие](%s)" %
                        (act['short_title'], act['description'], act['site_url']),
                    'mark' : 0
                }
                i+=1

    def addActRecomendation(self):
        self.usersActivity = {}
        recomendIdList = {i[0] for i in getRecomendation(self.chat_id, self.simList)}
        active = {m[1]: m[2] for m in selectActivity(self.chat_id)}
        newDigest = getDigest(self.current_city, self.current_event, recomendIdList)
        i=0
        for act in newDigest:
            print(str(act['id']))
            if(str(act['id']) not in active):
                self.usersActivity[i] = {
                    'id' : act['id'],
                    'msg' : "%s\n%s\n[Ссылка на событие](%s)" %
                        (act['short_title'], act['description'], act['site_url']),
                    'mark' : 0
                }
                i+=1


    def setMark(self, act_id, mark):
        for act in self.usersActivity:
            if (self.usersActivity[act]['id'] == act_id):
                self.usersActivity[act]['mark'] = mark


    def setSimilaruty(self):
        simDict = {c: Similarity(self.chat_id, c) for c in selectAllUsers() if self.chat_id != c[0]}
        l = lambda x: x[1]
        self.simList = sorted(simDict.items(), key=l, reverse=True)[:5]


    def addInfoToDB(self):
        addCountPercent(self.chat_id, self.count, self.usersEvents)
        addActivity(self.chat_id, self.usersActivity)
        #self.usersActivity = {}