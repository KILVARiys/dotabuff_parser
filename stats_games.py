import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# Создание объекта UserAgent
ua = UserAgent()

# Ввод ссылки/ID стим профиля
url_steam = "https://steamcommunity.com/profiles/76561199097155123"
# Извлечение ID профиля из ссылки
result = ''.join(c if c.isdigit() else ' ' for c in url_steam).split()
id_steam = [int(item) for item in result]
final = id_steam[0]

# Создание сессии
session = requests.Session()
session.headers.update({'User-Agent': ua.chrome})

# Запросы с использованием сессии
dota = session.get(f"https://ru.dotabuff.com/players/{final}")
rust = session.get(f"https://ruststats.cc/stats/user/{final}")

# Проверка на работоспособность и продолжение кода
# DOTABUFF
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
else:
    print('Ошибка при запросе к Dotabuff.')

# RUSTSTATS
if rust.status_code == 200:
    print('Запрос к RustStats выполнен успешно.')
    soup_rust = BeautifulSoup(rust.content, "html5lib")
    account_info = soup_rust.findAll('div', class_='main_search_profile')
    account_stat = soup_rust.findAll('div', class_='main_search_stats')

    print("\nСтатистика RUST:")
    for info in account_info:
        base_text = info.find('div', class_='main_search_profile_items').text.strip()
        # Убираем лишние пробелы
        base_text_no_extra_spaces = ' '.join(base_text.split())
        print(f"Информация о аккаунте: {base_text_no_extra_spaces}")

    for stats in account_stat:
        stat_rust_text = stats.findAll('div', class_='main_search_stats_item_content')[0].text.strip() #Убрать по оканчании настройки данного отдела(переменная для проверки html кода)
        print('Игровая статистика:')
        kill_stat = stats.findAll('div', class_='main_search_stats_item_content_info')[0].findAll('div')[1].text.strip()
        hit_stat = stats.findAll('div', class_='main_search_stats_item_content_info')[7].findAll('div')[1].text.strip()
        headshot_stat = stats.findAll('div', class_='main_search_stats_item_content_info')[5].findAll('div')[1].text.strip()

        print(f"Убийств: {kill_stat}|Процент попаданий: {hit_stat}|Процент голов: {headshot_stat}")
else:
    print('Ошибка при запросе к RustStats.')
