import math
from db_src.db_reg import getEventMarkInfo

# Функция определяет насколько пользователи похожи во вкусах
# На вход подаются номера пользователей
def Similarity(chat_id, other_user_id):
    marks_chat_id = {m[1]: m[2] for m in getEventMarkInfo(chat_id)}
    print(marks_chat_id)
    marks_other_user = {m[1] : m[2] for m in getEventMarkInfo(other_user_id)}
    print(marks_other_user)

    # Вспомогательные переменные для расчёта формулы
    simUV = 0
    simU = 0
    simV = 0
    # Количество фильмов
    for i in marks_chat_id:
        if(i in marks_other_user):
            simUV = simUV + (marks_chat_id[i] * marks_other_user[i])
            simU = simU + (marks_chat_id[i] ** 2)
            simV = simV + (marks_other_user[i] ** 2)
    if((math.sqrt(simU) * math.sqrt(simV))>0):
        total = simUV / (math.sqrt(simU) * math.sqrt(simV))
        return total
    else:
        return 0