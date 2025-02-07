import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os
import html5lib

# Создание объекта UserAgent
ua = UserAgent()

# Ввод ссылки/ID стим профиля
url_steam = input('Введите url или id стим профиля: ')
# Извлечение ID профиля из ссылки
result = ''.join(c if c.isdigit() else ' ' for c in url_steam).split()
id_steam = [int(item) for item in result]
final = id_steam[0]

# Создание сессии
session = requests.Session()
session.headers.update({'User-Agent': ua.chrome})

# Запросы с использованием сессии
dota = session.get(f"https://ru.dotabuff.com/players/{final}")
dota_record = session.get(f"https://ru.dotabuff.com/players/{final}/records")
dota_sens = session.get(f"https://ru.dotabuff.com/players/{final}/scenarios")

# Проверка на работоспособность и продолжение кода
if dota.status_code == 200:
    print('Запрос к Dotabuff выполнен успешно.')
    soup = BeautifulSoup(dota.content, "html5lib")
    base_stat = soup.findAll('div', class_='header-content-secondary')
    hero_stat = soup.findAll('div', class_='r-row')

    # Форматированный вывод статистики
    print("\nСтатистика Dota 2:")
    for stat in base_stat:
        stat_text = stat.text.strip()
        # Извлечение даты последней игры
        last_game_date = stat_text[:10].strip()
        # Извлечение количества игр (побед/лузов)
        matches = stat.find('span', class_='game-record').text.strip()
        # Извлечение доли побед
        win_rate = stat.findAll('dd')[-1].text.strip()

        print(f"Последняя игра: {last_game_date}")
        print(f"Матчи: {matches}")
        print(f"Доля побед: {win_rate}%")

    # Получаем статистику персонажей пользователя
    print("\nСамые активные герои:\nHero|Last Game| Stats")
    # Когда информация о героях заканчивается выдается AttributeError дабы он не ломал код нужен try
    try:
        for hero in hero_stat:
            hero_name = hero.find('div', class_="r-none-mobile").find('a').text.strip()
            hero_data = hero.find('div', class_='subtext minor').text.strip()
            hero_stat_match = hero.findAll('div', class_='r-fluid r-10 r-line-graph')[0].find('div', class_='r-body').text.strip()
            hero_stat_winrate = hero.findAll('div', class_='r-fluid r-10 r-line-graph')[1].find('div', class_='r-body').text.strip()
            hero_stat_ycp = hero.findAll('div', class_='r-fluid r-10 r-line-graph')[2].find('div', class_='r-body').text.strip()
            print(f"{hero_name} | Последняя игра была сыграна: {hero_data} | Сыграно: {hero_stat_match} матчей | Winrate: {hero_stat_winrate} | KDA: {hero_stat_ycp}")
    except AttributeError:
        print('Список окончен\n')
    #Получаем рекорды игрока
if dota_record.status_code == 200:
    records = BeautifulSoup(dota_record.content, "html5lib")
    record_stat = records.findAll('div', class_='content-inner')
    try:
        for rec in record_stat:
            req = rec.findAll('div', 'player-records')
            long_match = rec.findAll('div', 'record')[0].find('div', class_='value').text.strip()
            most_kills = rec.findAll('div', 'record')[1].find('div', class_='value').text.strip()
            most_denau_creeps = rec.findAll('div', 'record')[2].find('div', class_='value').text.strip()
            most_farm = rec.findAll('div', 'record')[5].find('div', class_='value').text.strip()
            most_exp = rec.findAll('div', 'record')[6].find('div', class_='value').text.strip()
            most_dmg_hero = rec.findAll('div', 'record')[7].find('div', class_='value').text.strip()
            most_ycp = rec.findAll('div', 'record')[10].find('div', class_='value').text.strip()
            most_record_wins = rec.findAll('div', 'record')[12].find('div', class_='value').text.strip()
            most_record_loses = rec.findAll('div', 'record')[13].find('div', class_='value').text.strip()
            print('Рекорды игрока:')
            print(f"Самый длинный матч: {long_match} |Большее кол-во убийст: {most_kills} |Наибольшее кол-во добиваний: {most_denau_creeps} |\n"
                  f"Найбольшее число золота: {most_farm} |Найбольшее число опыта: {most_exp} |Больше всего урона по игрокам: {most_dmg_hero} |\n"
                  f"Наилучшее УСП: {most_ycp} |Найбольшая серия побед: {most_record_wins} |Найбольшая серия поражений: {most_record_loses} |\n")
    except IndexError:
        print('Список окончен')
    #Получаем различные сценария типа: Игр в группе, кол-во игр в определённом режиме и т.д
if dota_sens.status_code == 200:
    sens_soup = BeautifulSoup(dota_sens.content, "html5lib")
    sens_stat = sens_soup.findAll('table', class_='r-tab-enabled')
    try:
        for sens in sens_stat:
            def_matchs = sens.findAll('tbody')[2].find('tr').findAll('td')[1].text.strip()
            def_matchs_winrate = sens.findAll('tbody')[2].find('tr').findAll('td')[2].text.strip()
            rating_matchs = sens.findAll('tbody')[2].findAll('tr')[1].findAll('td')[1].text.strip()
            rating_matchs_winrate = sens.findAll('tbody')[2].findAll('tr')[1].findAll('td')[2].text.strip()
            daer = sens.findAll('tbody')[4].find('tr').findAll('td')[1].text.strip()
            daer_winrate = sens.findAll('tbody')[4].find('tr').findAll('td')[2].text.strip()
            radiant = sens.findAll('tbody')[4].findAll('tr')[1].findAll('td')[1].text.strip()
            radiant_winrate = sens.findAll('tbody')[4].findAll('tr')[1].findAll('td')[2].text.strip()
            print('Статистика матчей:')
            print(f"Обычные матчи: {def_matchs} |{def_matchs_winrate}|\n"
                  f"Рейтинговые матчи: {rating_matchs} |{rating_matchs_winrate}|\n"
                  f"Игры за даер: {daer} |{daer_winrate}|\n"
                  f"Игры за редиант: {radiant} |{radiant_winrate}|")
    except IndexError:
        print('Список окончен')
else:
    print('Ошибка при запросе к Dotabuff.')
os.system('pause')