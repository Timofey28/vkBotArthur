import bs4
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from data import token, dima_token, my_id, V
from utility import bOptions, bChains, bGroups, bExit, daysInMonths, monthName_to_No, time_to_pairNo, study_groups, return_codes
from utility import c1, c2, c3, c4, fullC1, fullC2, fullC3, fullC4, greetings, gratitudes, response_to_gratitude, swearings
import requests
import random
import json
from bs4 import BeautifulSoup
from time import *
import string
import datetime
import threading
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from replit import db
from background import keep_alive


keep_alive()

session = vk_api.VkApi(token=token)
vk = session.get_api()
longpoll = VkLongPoll(session)
personChains = []
dates_str = []
existing_study_groups = set()
for key in study_groups.keys():
    existing_study_groups.add(study_groups[key])

print("Бот запущен")


# Статусы:
# 0 - человека нет в БД
# 1 - нет ни группы, ни цепочек (мы еще на знакомы, выбери из списка свою учебную группу), ожидается группа
# 2 - выбрана группа, но нет цепочек (для начала выбери свои цепочки обучения ...), ожидаются цепочки
# 3 - смена цепочки, ожидаются цепочки
# 4 - смена группы, ожидается группа
# 10 - главное меню, все есть
# 11 - ожидается дата, чтобы показать расписаниее в этот день
# 12 - выбор определенной недели, ожидается неделя


def process(buddy_id, msg):
    global personChains, dates_str
    status = 0 if str(buddy_id) not in db.keys() else db[str(buddy_id)]["status"]

    if not status:
        person = requests.get(f"https://api.vk.com/method/users.get?user_ids={buddy_id}&fields=sex&access_token={token}&v={V}").json()
        msgToMe = f'Новый собеседник у бота Артура - [id{buddy_id}|{person["response"][0]["first_name"]} {person["response"][0]["last_name"]}]'
        requests.get(f"https://api.vk.com/method/messages.send?user_id={my_id}&message={msgToMe}&random_id=0&access_token={dima_token}&v={V}")
        if msg.lower() == "начать" or isGreeting(msg.lower()):
            send(user_id=buddy_id, msg=f'Привет, {person["response"][0]["first_name"]}!', kbrd=None)
        sex = 'a' if person["response"][0]["sex"] == 1 else ''
        db[str(buddy_id)] = {"status": 1, "name": person["response"][0]["first_name"], "surname": person["response"][0]["last_name"], "sex": sex, "chains": [], "group": ''}
        for i in range(3):
            bGroups["buttons"][i][0]["color"] = "secondary"
        send(buddy_id, bGroups, "Мы пока не знакомы, выбери свою учебную группу")

    elif status == 1 or status == 4:
        if msg in existing_study_groups:
            db[str(buddy_id)]["group"] = msg
            if status == 1:
                db[str(buddy_id)]["status"] = 2
                for i in range(4):
                    bChains["buttons"][i][0]["color"] = "secondary"
                send(user_id=buddy_id, msg=f"Выбрана группа {msg}", kbrd=None)
                send(user_id=buddy_id, msg="Выбери свои цепочки обучения", attachment='photo-215267285_457239444', kbrd=bChains)
            else:
                db[str(buddy_id)]["status"] = 10
                send(buddy_id, bOptions, f"Выбрана группа {msg}")
        else:
            for i in range(3):
                bGroups["buttons"][i][0]["color"] = "secondary"
            if status == 1:
                send(buddy_id, bGroups, "Выбери, пожалуйста, свою учебную группу <3")
            else:
                group = db[str(buddy_id)]["group"]
                if group == study_groups['12']:
                    bGroups["buttons"][0][0]["color"] = "positive"
                elif group == study_groups['14']:
                    bGroups["buttons"][1][0]["color"] = "positive"
                elif group == study_groups['21']:
                    bGroups["buttons"][2][0]["color"] = "positive"
                send(buddy_id, bGroups, "Выбери группу")

    elif status == 2 or status == 3:
        if msg == c1 or msg == c2 or msg == c3 or msg == c4:
            db[str(buddy_id)]["status"] = 10
            full = ''
            if msg == c1:
                db[str(buddy_id)]["chains"] = [1, 2]
                personChains = [1, 2]
                full = fullC1
            elif msg == c2:
                db[str(buddy_id)]["chains"] = [3, 4]
                personChains = [3, 4]
                full = fullC2
            elif msg == c3:
                db[str(buddy_id)]["chains"] = [2, 3]
                personChains = [2, 3]
                full = fullC3
            elif msg == c4:
                db[str(buddy_id)]["chains"] = [1, 4]
                personChains = [1, 4]
                full = fullC4
            send(buddy_id, bOptions, f'Выбраны цепочки № {personChains[0]} и {personChains[1]}: "{full}"')
        else:
            for i in range(4):
                bChains["buttons"][i][0]["color"] = "secondary"
            if status == 2:
                send(user_id=buddy_id, msg="Выбери, пожалуйста, свои цепочки обучения <3", attachment='photo-215267285_457239444', kbrd=bChains)
            else:
                personChains = db[str(buddy_id)]["chains"]
                if personChains == [1, 2]:
                    bChains["buttons"][0][0]["color"] = "positive"
                elif personChains == [3, 4]:
                    bChains["buttons"][1][0]["color"] = "positive"
                elif personChains == [2, 3]:
                    bChains["buttons"][2][0]["color"] = "positive"
                elif personChains == [1, 4]:
                    bChains["buttons"][3][0]["color"] = "positive"
                send(user_id=buddy_id, msg="Выбери цепочки обучения", attachment='photo-215267285_457239444', kbrd=bChains)

    elif status == 10:
        msg = msg.lower()
        info = db[str(buddy_id)]
        group = info["group"]
        personChains = info["chains"]
        sex = info["sex"]
        if msg == "на сегодня":
            vk.messages.setActivity(user_id=buddy_id, type='typing')
            getSchedule(user_id=buddy_id, num=1, group=group)
        elif msg == "на завтра":
            vk.messages.setActivity(user_id=buddy_id, type='typing')
            getSchedule(user_id=buddy_id, num=2, group=group)
        elif msg == "расписание до конца недели":
            vk.messages.setActivity(user_id=buddy_id, type='typing')
            getSchedule(user_id=buddy_id, num=3, group=group)
        elif msg == "расписание на следующую неделю":
            vk.messages.setActivity(user_id=buddy_id, type='typing')
            getSchedule(user_id=buddy_id, num=4, group=group)
        elif msg == "расписание в определенный день":
            db[str(buddy_id)]["status"] = 11
            send(buddy_id, bExit, "Могу скинуть расписание на любой день в пределах текущего семестра\n\nВведи дату в любом из следующих форматов:\n\n- 8 марта\n- 08.03\n- 8.3")
        elif msg == "расписание в определенную неделю":
            db[str(buddy_id)]["status"] = 12
            status12(buddy_id, group)
        elif msg == "сменить группу":
            db[str(buddy_id)]["status"] = 4
            for i in range(3):
                bGroups["buttons"][i][0]["color"] = "secondary"
            if group == study_groups['12']:
                bGroups["buttons"][0][0]["color"] = "positive"
            elif group == study_groups['14']:
                bGroups["buttons"][1][0]["color"] = "positive"
            elif group == study_groups['21']:
                bGroups["buttons"][2][0]["color"] = "positive"
            send(buddy_id, bGroups, "Выбери группу")
        elif msg == "сменить цепочки":
            db[str(buddy_id)]["status"] = 3
            for i in range(4):
                bChains["buttons"][i][0]["color"] = "secondary"
            if personChains == [1, 2]:
                bChains["buttons"][0][0]["color"] = "positive"
            elif personChains == [3, 4]:
                bChains["buttons"][1][0]["color"] = "positive"
            elif personChains == [2, 3]:
                bChains["buttons"][2][0]["color"] = "positive"
            elif personChains == [1, 4]:
                bChains["buttons"][3][0]["color"] = "positive"
            send(user_id=buddy_id, msg="Выбери цепочки обучения", attachment='photo-215267285_457239444', kbrd=bChains)
        else:
            if msg == "начать" or isGreeting(msg):
                send(buddy_id, bOptions, f'Привет, {db[str(buddy_id)]["name"]}!')
            elif isSwearing(msg):
                if sex == '':
                    send(buddy_id, bOptions, "Сам такой")
                else:
                    send(buddy_id, bOptions, "Сама такая")
            elif isGratitude(msg):
                if sex == '':
                    rand = random.randint(0, len(response_to_gratitude) - 1)
                else:
                    rand = random.randint(0, len(response_to_gratitude) - 2)
                send(buddy_id, bOptions, response_to_gratitude[rand])
            elif len(msg) > 0 and msg[0].isascii() and msg[0].isalpha():
                send(buddy_id, bOptions, "Извини, не понимаю на пендосском (")
            elif "люди" in msg.lower() and buddy_id == my_id:
                msgToMe = ''
                for person in db.keys():
                    if msgToMe:
                        msgToMe += '\n\n'
                    msgToMe += f"[id{person}|{person}]"
                    for info in db[person]:
                        if info == "chains":
                            msgToMe += f"\n{info} -> {f'{db[person][info][0]}, {db[person][info][1]}' if db[person][info] else ''}"
                        else:
                            msgToMe += f"\n{info} -> {db[person][info]}"
                send(my_id, bOptions, msgToMe)
            elif msg.lower()[:5] == "удали" and buddy_id == my_id:
                try:
                    link = msg[msg.find(' ') + 1:].strip()
                    if link == "меня":
                        del db[f'{my_id}']
                    else:
                        link = link[link.find('id') + 2:]
                        del db[str(link)]
                    send(user_id=my_id, msg='✅', kbrd=None)
                except:
                    send(user_id=my_id, msg='❌', kbrd=None)
            else:
                send(buddy_id, bOptions, "Нажми любую кнопку на клавиатуре")

    elif status == 11:
        gotIt: bool
        if msg.lower() == "в главное меню":
            db[str(buddy_id)]["status"] = 10
            send(buddy_id, bOptions, "😉")
            return
        msg = msg.strip()
        day, month = 0, 0
        curr_year = datetime.datetime.now().year
        if curr_year == 2024 or curr_year == 2028 or curr_year == 2032:
            daysInMonths[2] = 29
        if msg.find(' ') != -1:
            try:
                day = int(msg[:msg.find(' ')])
                month = monthName_to_No[msg[msg.rfind(' ') + 1:]]
                gotIt = True
            except:
                gotIt = False
        elif msg.find('.') != -1:
            while msg.count('.') > 1:
                msg = msg[:msg.rfind('.')]
            try:
                day = int(msg[:msg.find('.')])
                month = int(msg[msg.find('.') + 1:])
                gotIt = True
            except:
                gotIt = False
        else:
            gotIt = False
        if gotIt:
            if day < 1 or day > daysInMonths[month]:
                msg = 'Введи дату в одном из представленных ниже формате, либо нажми кнопку "в главное меню"\n\nВозможные форматы:\n- 8 марта\n- 08.03\n- 8.3'
                if month == 2 and day == 29:
                    msg = f'В {curr_year} году в феврале 28 дней. ' + msg
                else:
                    msg = 'Такой даты не существует. ' + msg
                send(buddy_id, bExit, msg)
            else:
                info = db[str(buddy_id)]
                group = info["group"]
                personChains = info["chains"]
                if getScheduleForSpecificDay(buddy_id, group, month, day):
                    db[str(buddy_id)]["status"] = 10
        else:
            send(buddy_id, bExit, 'Неверный формат. Введи дату в одном из представленных ниже формате, либо нажми кнопку "в главное меню"\n\nВозможные форматы:\n- 8 марта\n- 08.03\n- 8.3')

    elif status == 12:
        info = db[str(buddy_id)]
        group = info["group"]
        personChains = info["chains"]
        if msg in dates_str:
            db[str(buddy_id)]["status"] = 10
            getSchedule(buddy_id, 5, group, dates_str.index(msg) + 1)
        elif msg.lower() == "в главное меню":
            db[str(buddy_id)]["status"] = 10
            send(buddy_id, bOptions, "😉")
        else:
            status12(buddy_id, group, True)


def baseOnChains(subject):
    global personChains
    chains = {
        'Технология производства средств информационно-вычислительной техники': 1,
        'Микроконтроллеры': 2,
        'Информационная теория оценок': 3,
        'Надежность информационных систем': 4,
    }
    if type(subject) is str:
        return True
    if subject["name"] in chains and chains[subject["name"]] not in personChains:
        return False
    else:
        return True


def status12(buddy_id, group, buddyIsStupid=False):
    global dates_str
    vk.messages.setActivity(user_id=buddy_id, type='typing')
    if buddyIsStupid:
        send(buddy_id, bExit, "Ответ неверный. Выбери любую неделю выше или нажми кнопку \"в главное меню\" под стандартной клавиатурой 😉")
    else:
        url = f"https://mai.ru/education/studies/schedule/index.php?group={group}"
        soup = getTextFromUrl(url)
        if type(soup) is str:
            db[str(buddy_id)]["status"] = 10
            send(buddy_id, bOptions, soup)
            return
        workWeekChoice = soup.find(id="collapseWeeks")
        dates = workWeekChoice.find_all(class_="w-100 d-block text-center")
        dates_str = [f"{date.next[:date.next.find(' - ')][:-5]} - {date.next[date.next.find(' - ') + 3:][:-5]}" for date in dates]
        dt = datetime.datetime.now()
        weekNo = determineWeekNo([[date.next[:date.next.find(' - ')], date.next[date.next.find(' - ') + 3:]] for date in dates], f"{dt.day}.{dt.month}.{dt.year}")
        buttons = getBWeeks(dates_str, weekNo)
        send(buddy_id, buttons[0], "Учебные недели № 1-9")
        send(buddy_id, buttons[1], "Учебные недели № 10-18")
        send(buddy_id, bExit, "Выбери любую учебную неделю и я скину соответствующее для нее расписание!\nДля выхода в главное меню нажми единственную кнопку под стандартной клавиатурой ⬇")


def getBWeeks(dates, weekNo):
    bWeeks1 = {
        "inline": True,
        "buttons": []
    }
    bWeeks2 = {
        "inline": True,
        "buttons": []
    }
    single = {
        "action": {
            "type": "text",
            "label": "",
        },
        "color": "secondary"
    }
    buttons1, buttons2 = [], []
    for i in range(3):
        l1, l2, l3 = deepcopy(single), deepcopy(single), deepcopy(single)
        l1["action"]["label"] = dates[3 * i]
        l2["action"]["label"] = dates[3 * i + 1]
        l3["action"]["label"] = dates[3 * i + 2]
        buttons1.append([l1, l2, l3])
        l1, l2, l3 = deepcopy(single), deepcopy(single), deepcopy(single)
        l1["action"]["label"] = dates[3 * i + 9]
        l2["action"]["label"] = dates[3 * i + 10]
        l3["action"]["label"] = dates[3 * i + 11]
        buttons2.append([l1, l2, l3])
    if weekNo != -1:
        if weekNo <= 9:
            buttons1[int((weekNo - 1) / 3)][int((weekNo - 1) % 3)]["color"] = "positive"
        else:
            buttons2[int((weekNo - 10) / 3)][int((weekNo - 10) % 3)]["color"] = "positive"
    bWeeks1["buttons"] = buttons1
    bWeeks2["buttons"] = buttons2
    return [bWeeks1, bWeeks2]


def getScheduleForSpecificDay(user_id, group, month, day):
    global personChains
    vk.messages.setActivity(user_id=user_id, type='typing')
    url = f"https://mai.ru/education/studies/schedule/index.php?group={group}"
    soup = getTextFromUrl(url)
    if type(soup) is str:
        db[str(user_id)]["status"] = 10
        send(user_id, bOptions, soup)
        return

    workWeekChoice = soup.find(id="collapseWeeks")
    dates = workWeekChoice.find_all(class_="w-100 d-block text-center")
    dates = [[date.next[:date.next.find(' - ')], date.next[date.next.find(' - ') + 3:]] for date in dates]
    neededDate = f"{day}.{month}.{datetime.datetime.now().year}"
    todayDate = str(datetime.date.today()).replace('-', '.')
    todayDate = todayDate[8:] + '.' + todayDate[5:7] + '.' + todayDate[:4]
    if isInDateInterval(neededDate, [dates[0][0], dates[-1][1]]):
        weekNo = determineWeekNo(dates, neededDate)
        if isSame(dates[weekNo - 1][1], neededDate):
            if isSame(todayDate, neededDate):
                send(user_id, bOptions, "Сегодня воскресенье, занятий нет")
            elif isInDateInterval(neededDate, ['28.07.2002', todayDate]):
                send(user_id, bOptions, "Это воскресенье, занятий не было")
            else:
                send(user_id, bOptions, "Это воскресенье, занятий не будет")
        else:
            url += f"&week={weekNo}"
            text = requests.get(url=url).text
            soup = BeautifulSoup(text, 'lxml')
            schedule = soup.find(class_="step mb-5")
            week = [tag.string.strip() if tag.string else tag for tag in schedule.find_all(class_="mb-4")]

            sub = {}
            weekDay = []
            for i in range(len(week)):
                if type(week[i]) is str:
                    current_day = int(week[i][week[i].find('\xa0') + 1:week[i].rfind('\xa0')])
                    current_month = monthName_to_No[week[i][week[i].rfind('\xa0') + 1:]]
                    if weekDay:
                        break
                    elif current_day == day:
                        weekDay.append(week[i])
                    elif current_day > day and current_month == month:
                        if isInDateInterval(neededDate, ['28.07.2002', todayDate]):
                            send(user_id, bOptions, "В этот день не было занятий")
                        else:
                            send(user_id, bOptions, "В этот день не будет занятий")
                        return True
                else:
                    if not weekDay:
                        if i == len(week) - 1:
                            if isInDateInterval(neededDate, ['28.07.2002', todayDate]):
                                send(user_id, bOptions, "В этот день не было занятий")
                            else:
                                send(user_id, bOptions, "В этот день не будет занятий")
                            return True
                        continue
                    sub['name'] = week[i].p.next.strip()
                    span = week[i].find(class_='text-nowrap')
                    if span:
                        sub['name'] += ' ' + span.next.strip()
                    sub['type'] = week[i].find(class_='badge').next.strip()
                    time_prepod_classroom = week[i].find('ul')
                    time_prepod_classroom = list(filter(lambda x: x != '\n', time_prepod_classroom))
                    sub['time'] = time_prepod_classroom[0].next
                    if len(time_prepod_classroom) >= 3:
                        sub['prepod'] = time_prepod_classroom[1].a.next
                        sub['prepod_link'] = 'https://mai.ru' + time_prepod_classroom[1].a['href']
                        sub['classroom'] = [room.contents[-1] for room in time_prepod_classroom[2:]]
                    elif len(time_prepod_classroom) == 2:
                        sub['classroom'] = [time_prepod_classroom[1].contents[-1]]
                    else:
                        print(f"в time_prepod_classrom 1 значение, а {len(time_prepod_classroom)}")
                        print(sub)
                    weekDay.append(sub)
                    sub = {}

            weekDay = list(filter(baseOnChains, weekDay))
            msgToSend = weekDay[0] + '\n---------------------------------\n'
            for j in range(1, len(weekDay)):
                if j != 1:
                    msgToSend += '\n\n'
                msgToSend += f"{time_to_pairNo[weekDay[j]['time'][:2]]} пара:\n{weekDay[j]['name']} ({weekDay[j]['type']})"
                msgToSend += '\n' + weekDay[j]['time']
                msgToSend += '\nАудитория: ' + ' / '.join(weekDay[j]['classroom'])
                if 'prepod' in weekDay[j]:
                    shortenedLink = vk.utils.getShortLink(url=weekDay[j]["prepod_link"])["short_url"]
                    msgToSend += '\n' + weekDay[j]['prepod'] + '\n*** ' + shortenedLink + ' ***'
            send(user_id, bOptions, msgToSend)
        return True
    else:
        db[str(user_id)]["status"] = 10
        send(user_id, bOptions, f"Дата должна находится в интервале от {dates[0][0]} до {dates[-1][1]}")
        return False


def getSchedule(user_id, num, group, weekNo=None):
    url = f"https://mai.ru/education/studies/schedule/index.php?group={group}"
    if num == 5:
        url += f"&week={weekNo}"
    elif num == 3 or num == 4:
        soup = getTextFromUrl(url)
        if type(soup) is str:
            send(user_id, bOptions, soup)
            return
        workWeekChoice = soup.find(id="collapseWeeks")
        todayDate = str(datetime.date.today()).replace('-', '.')
        todayDate = todayDate[8:] + '.' + todayDate[5:7] + '.' + todayDate[:4]
        dates = workWeekChoice.find_all(class_="w-100 d-block text-center")
        dates = [[date.next[:date.next.find(' - ')], date.next[date.next.find(' - ') + 3:]] for date in dates]
        weekNo = determineWeekNo(dates, todayDate)
        if num == 4:
            weekNo += 1
        if weekNo == -1:
            msg = f"В диалоге с [id{user_id}|user] weekNo стала -1, а так низя:"
            url = f"https://api.vk.com/method/messages.send?user_id={my_id}&message={msg}&random_id=0&access_token={dima_token}&v={V}"
            requests.get(url=url)
            send(user_id=user_id, msg="Fatal error", kbrd=None)
            exit(-1)
        if num == 3 and isSame(todayDate, dates[weekNo - 1][1]):
            send(user_id, bOptions, "Эта неделя заканчивается сегодня")
            return
        url += f"&week={weekNo}"
    try:
        soup = getTextFromUrl(url)
        if type(soup) is str:
            send(user_id, bOptions, soup)
            return
        schedule = soup.find(class_="step mb-5")
        week = [tag.string.strip() if tag.string else tag for tag in schedule.find_all(class_="mb-4")]
    except AttributeError:
        schedule = bs4.BeautifulSoup(getStepMb5HTML(group, weekNo), 'lxml')
        week = [tag.string.strip() if tag.string else tag for tag in schedule.find_all(class_="mb-4")]

    sub = {}
    day = []
    days = []
    for i in range(len(week)):
        if type(week[i]) is str:
            if i != 0:
                days.append(day)
                day = []
                if num == 1:
                    break
                if len(days) == 2 and num == 2:
                    break
            day.append(week[i])
        else:
            sub['name'] = week[i].p.next.strip()
            span = week[i].find(class_='text-nowrap')
            if span:
                sub['name'] += ' ' + span.next.strip()
            sub['type'] = week[i].find(class_='badge').next.strip()
            time_prepod_classroom = week[i].find('ul')
            time_prepod_classroom = list(filter(lambda x: x != '\n', time_prepod_classroom))
            sub['time'] = time_prepod_classroom[0].next
            if len(time_prepod_classroom) >= 3:
                sub['prepod'] = time_prepod_classroom[1].a.next
                sub['prepod_link'] = 'https://mai.ru' + time_prepod_classroom[1].a['href']
                sub['classroom'] = [room.contents[-1] for room in time_prepod_classroom[2:]]
            elif len(time_prepod_classroom) == 2:
                sub['classroom'] = [time_prepod_classroom[1].contents[-1]]
            else:
                print(f"в time_prepod_classrom 1 значение, а {len(time_prepod_classroom)}")
                print(sub)
            day.append(sub)
            sub = {}
        if i == len(week) - 1:
            days.append(day)

    todayDate = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=3)).strftime("%d.%m.%Y")
    todayMonth = int(todayDate[3:5])
    todayDay = int(todayDate[:2])
    tomorrow = int((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1, hours=3)).strftime("%d"))
    firstDay = int(days[0][0][days[0][0].find('\xa0') + 1:days[0][0].rfind('\xa0')])
    if num == 1 and firstDay != todayDay:
        send(user_id, bOptions, "Сегодня занятий нет")
        return
    if num == 2:
        haveSchedule = False
        for x in days:
            if int(x[0][x[0].find('\xa0')+1:x[0].rfind('\xa0')]) == tomorrow:
                days = [x]
                haveSchedule = True
                break
        if not haveSchedule:
            send(user_id, bOptions, "Завтра занятий не будет")
            return

    for i in range(len(days)):
        days[i] = list(filter(baseOnChains, days[i]))

    if not days:
        msg = f"[id{user_id}|Fatal error:] days == [] в getSchedule()"
        url = f"https://api.vk.com/method/messages.send?user_id={my_id}&message={msg}&random_id=0&access_token={dima_token}&v={V}"
        requests.get(url=url)
        vk.messages.markAsRead(peer_id=user_id)
        return
    for i in range(len(days)):
        if num == 3:
            date = days[i][0]
            if date.count('\xa0') < 2:
                msg = f'[id{user_id}|В функции getSchedule в строке days[i][0] меньше 2 символов "backslash xa0"]'
                url = f"https://api.vk.com/method/messages.send?user_id={my_id}&message={msg}&random_id=0&access_token={dima_token}&v={V}"
                requests.get(url=url)
                vk.messages.markAsRead(peer_id=user_id)
                send(user_id=user_id, msg="Возникла непредвиденная ошибка, она будет исправлена в ближайшее время", kbrd=None)
                return
            day = int(date[date.find('\xa0') + 1:date.rfind('\xa0')])
            month = monthName_to_No[date[date.rfind('\xa0') + 1:]]
            isPast: bool
            if month < todayMonth:
                isPast = True
            elif month > todayMonth:
                isPast = False
            else:
                if day < todayDay:
                    isPast = True
                else:
                    isPast = False
            if isPast:
                continue
        answer = days[i][0] + '\n---------------------------------\n'
        for j in range(1, len(days[i])):
            if j != 1:
                answer += '\n\n'
            answer += time_to_pairNo[days[i][j]['time'][:2]] + ' пара:\n' + days[i][j]['name'] + ' (' + days[i][j]['type'] + ')'
            answer += '\n' + days[i][j]['time']
            answer += '\nАудитория: ' + ' / '.join(days[i][j]['classroom'])
            if 'prepod' in days[i][j]:
                shortenedLink = vk.utils.getShortLink(url=days[i][j]["prepod_link"])["short_url"]
                answer += '\n' + days[i][j]['prepod'] + '\n*** ' + shortenedLink + ' ***'
        if i == len(days) - 1:
            send(user_id, bOptions, answer)
        else:
            send(user_id, None, answer)


def getStepMb5HTML(group, weekNo):
    browser = webdriver.Chrome()
    url = 'https://mai.ru/education/studies/schedule/index.php'
    browser.get(url)
    browser.implicitly_wait(10)

    Select(browser.find_element(By.ID, "department")).select_by_value("Институт №3")
    Select(browser.find_element(By.ID, "course")).select_by_value(group[4:5])
    browser.find_element(By.XPATH, '//button[text()="Отобразить"]').click()
    browser.implicitly_wait(10)
    browser.find_element(By.LINK_TEXT, group).click()
    browser.implicitly_wait(10)

    result = browser.find_element(By.CSS_SELECTOR, ".step.mb-5").get_attribute('outerHTML')
    browser.quit()
    return result


def isSame(date1, date2):
    if date1.count('.') != 2 or date2.count('.') != 2:
        print("\nОшибка в сравнении дат: даты в неверном формате")
        return False
    day1, day2 = int(date1[:date1.find('.')]), int(date2[:date2.find('.')])
    month1, month2 = int(date1[date1.find('.')+1:date1.rfind('.')]), int(date2[date2.find('.')+1:date2.rfind('.')])
    year1, year2 = int(date1[date1.rfind('.')+1:]), int(date2[date2.rfind('.')+1:])
    return day1 == day2 and month1 == month2 and year1 == year2


def determineWeekNo(dates, todayDate):
    for i in range(len(dates)):
        if isInDateInterval(todayDate, dates[i]):
            return i + 1
    return -1


def isInDateInterval(todayDate, dateInterval):
    moreOrEqualToLeft = True
    lessOrEqualToRight = True
    leftBoundary = dateInterval[0]
    rightBoundary = dateInterval[1]

    if int(todayDate[todayDate.rfind('.') + 1:]) < int(leftBoundary[leftBoundary.rfind('.') + 1:]):
        moreOrEqualToLeft = False
    elif int(todayDate[todayDate.rfind('.') + 1:]) > int(leftBoundary[leftBoundary.rfind('.') + 1:]):
        moreOrEqualToLeft = True
    else:
        if todayDate.count('.') == 2:
            if int(todayDate[todayDate.find('.') + 1:todayDate.rfind('.')]) < int(leftBoundary[3:5]):
                moreOrEqualToLeft = False
            elif int(todayDate[todayDate.find('.') + 1:todayDate.rfind('.')]) > int(leftBoundary[3:5]):
                moreOrEqualToLeft = True
            else:
                if int(todayDate[:todayDate.find('.')]) < int(leftBoundary[:2]):
                    moreOrEqualToLeft = False
                else:
                    moreOrEqualToLeft = True
        else:
            if int(todayDate[:todayDate.find('.')]) < int(leftBoundary[:2]):
                moreOrEqualToLeft = False
            else:
                moreOrEqualToLeft = True

    if int(todayDate[todayDate.rfind('.') + 1:]) > int(rightBoundary[rightBoundary.rfind('.') + 1:]):
        lessOrEqualToRight = False
    elif int(todayDate[todayDate.rfind('.') + 1:]) < int(rightBoundary[rightBoundary.rfind('.') + 1:]):
        lessOrEqualToRight = True
    else:
        if todayDate.count('.') == 2:
            if int(todayDate[todayDate.find('.') + 1:todayDate.rfind('.')]) > int(rightBoundary[3:5]):
                lessOrEqualToRight = False
            elif int(todayDate[todayDate.find('.') + 1:todayDate.rfind('.')]) < int(rightBoundary[3:5]):
                lessOrEqualToRight = True
            else:
                if int(todayDate[:todayDate.find('.')]) > int(rightBoundary[:2]):
                    lessOrEqualToRight = False
                else:
                    lessOrEqualToRight = True
        else:
            if int(todayDate[:todayDate.find('.')]) > int(rightBoundary[:2]):
                lessOrEqualToRight = False
            else:
                lessOrEqualToRight = True

    return moreOrEqualToLeft and lessOrEqualToRight


def send(user_id, kbrd, msg="", attachment=""):
    for _ in range(3):
        try:
            if kbrd:
                kbrdStr = json.dumps(kbrd, ensure_ascii=False).encode("utf-8")
                kbrdStr = str(kbrdStr.decode("utf-8"))
                vk.messages.send(user_id=user_id, message=msg, attachment=attachment, random_id=0, keyboard=kbrdStr)
            else:
                vk.messages.send(user_id=user_id, message=msg, attachment=attachment, random_id=0)
        except:
            to_me = f"[id{user_id}|Ошибка отправления сообщения]"
            requests.get(f"https://api.vk.com/method/messages.send?user_id={my_id}&message={to_me}&random_id=0&access_token={dima_token}v={V}")
            sleep(0.5)
            continue
        break


def getTextFromUrl(url):
    resp = requests.get(url=url)
    if resp.status_code != 200:
        if resp.status_code not in return_codes:
            return f"Не удалось выполнить запрос, неизвестная ошибка ({resp.status_code})"
        else:
            msg = f"Не удалось выполнить запрос"
            if resp.status_code >= 500:
                msg += ": ошибка на стороне маёвского сервера"
            msg += f"\n{resp.status_code} -> {return_codes[resp.status_code]}"
            return msg
    else:
        return BeautifulSoup(resp.text, 'lxml')


def isGreeting(text):
    text = text.strip().lower()
    for greeting in greetings:
        if greeting == text:
            return True
        if greeting in text:
            before = text.find(greeting) - 1
            after = text.find(greeting) + len(greeting)
            punct = string.punctuation + ' '
            if (before == -1 or text[before] in punct) and (after == len(text) or text[after] in punct):
                return True
    return False


def isGratitude(text):
    text = text.strip().lower()
    for gratitude in gratitudes:
        if gratitude in text or text in gratitude and len(text) > 0:
            return True
    return False


def isSwearing(text):
    text = text.strip().lower()
    for swearing in swearings:
        if swearing == text:
            return True
        if swearing in text:
            before = text.find(swearing) - 1
            after = text.find(swearing) + len(swearing)
            punct = string.punctuation + ' '
            if (before == -1 or text[before] in punct) and (after == len(text) or text[after] in punct):
                return True
    return False


if __name__ == '__main__':
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.from_user and event.to_me:
                    threading.Thread(process(event.user_id, event.text)).start()
        except requests.exceptions.ConnectionError as e:
            log_message = f"Error: {str(e)}\n{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}\n\n"
            with open("ErrorLog.txt", "a", encoding="utf-8") as file:
                file.write(log_message)
            print(log_message)
            sleep(1)
        except requests.exceptions.ReadTimeout as e:
            log_message = f"Error: {str(e)}\n{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}\n\n"
            with open("ErrorLog.txt", "a", encoding="utf-8") as file:
                file.write(log_message)
            print(log_message)
            sleep(1)
