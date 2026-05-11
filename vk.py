import aiohttp
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text
import random
import json

TOKEN = "vk1.a.OXIJa8Zu7NilFZeQ2itlO4Q-_HVes2Rz3k2BRS2z8AZTKQvAGXyAj5Ku8z5rr4dvOju7LYBD2nwUrtHu2qdBBDnVRdth8nVUNiWRHYRVfQq08X8A2vzJe-Xr1WJoOJa3HFncqkNYcz07Cx8oKJgeJCz3N-jfqkkOVxKJb4PPBWCNqjjdxVVWX5_pjtNRrTi7q5aXyIl6fs_l3pU1oHWadQ"

bot = Bot(token=TOKEN)

games = {}
game_started = {}
player_sessions = {}
player_balance = {}
player_properties = {}
player_names = {}
property_owners = {}
player_buildings = {}
sent_start_button = {}
current_turn_index = {}
player_positions = {}
skip_turns_left = {}
laps_completed = {}
PHOTO_CACHE: dict[str, str] = {}
player_quiz_flags = {}
player_inventory = {}
user_states = {}
user_data = {}
turn_flags = {}

START_MONEY = 1500

property_groups = {
    "Оранжевые": [
        {"name": "ж/д Кая", "price": 200},
        {"name": "ж/д Мельниково", "price": 200},
        {"name": "ж/д Академическая", "price": 200},
        {"name": "ж/д Иркутск-Пасс.", "price": 200},
    ],
    "Турсервисы": [
        {"name": "Тур сервис: Гостиница «Звезда»", "price": 150},
        {"name": "Тур сервис: Турагенство «Анекс»", "price": 150},
    ],
    "Фиолетовые": [
        {"name": "Музей истории г.Иркутска", "price": 50, "house_price": 50, "rent": [3, 16, 40, 80, 128, 460]},
        {"name": "Вечный огонь", "price": 60, "house_price": 50, "rent": [4, 18, 44, 90, 145, 470]},
    ],
    "Бирюзовые": [
        {"name": "Арт-завод Доренберг", "price": 80, "house_price": 50, "rent": [6, 20, 52, 102, 164, 510]},
        {"name": "Галерея Виктора Бронштейна", "price": 80, "house_price": 50, "rent": [6, 20, 52, 102, 164, 510]},
        {"name": "Иркутский комсомолец", "price": 100, "house_price": 50, "rent": [8, 24, 60, 120, 194, 550]},
    ],
    "Розовые": [
        {"name": "Памятник Л.Гайдаю", "price": 120, "house_price": 100, "rent": [10, 36, 90, 180, 290, 660]},
        {"name": "Московские ворота", "price": 120, "house_price": 100, "rent": [10, 36, 90, 180, 290, 660]},
        {"name": "Театр юного зрителя", "price": 140, "house_price": 100, "rent": [12, 42, 105, 210, 335, 720]},
    ],
    "Голубые": [
        {"name": "Иркутский нерпинарий", "price": 160, "house_price": 100, "rent": [14, 46, 115, 230, 370, 760]},
        {"name": "Дом-музей Трубецких", "price": 160, "house_price": 100, "rent": [14, 46, 115, 230, 370, 760]},
        {"name": "Краеведческий музей", "price": 180, "house_price": 100, "rent": [16, 56, 140, 280, 450, 860]},
    ],
    "Красные": [
        {"name": "Музей им.Сукачева", "price": 200, "house_price": 150, "rent": [18, 70, 175, 350, 560, 1000]},
        {"name": "Казанская церковь", "price": 200, "house_price": 150, "rent": [18, 70, 175, 350, 560, 1000]},
        {"name": "Дом-музей Волконских", "price": 220, "house_price": 150, "rent": [20, 80, 200, 400, 640, 1100]},
    ],
    "Жёлтые": [
        {"name": "Колесо «Кругозор»", "price": 240, "house_price": 150, "rent": [24, 94, 235, 470, 755, 1240]},
        {"name": "Спорт-парк Поляна", "price": 240, "house_price": 150, "rent": [24, 94, 235, 470, 755, 1240]},
        {"name": "Музей-ледокол «Ангара»", "price": 260, "house_price": 150, "rent": [26, 102, 255, 510, 820, 1320]},
    ],
    "Зелёные": [
        {"name": "Памятник Александру III", "price": 280, "house_price": 200, "rent": [30, 126, 315, 630, 1010, 1560]},
        {"name": "Скульптура «Бабр»", "price": 280, "house_price": 200, "rent": [30, 126, 315, 630, 1010, 1560]},
        {"name": "Театр им.Загурского", "price": 300, "house_price": 200, "rent": [32, 140, 350, 700, 1120, 1700]},
    ],
    "Синие": [
        {"name": "Драмтеатр им.Охлопкова", "price": 320, "house_price": 200, "rent": [40, 160, 400, 800, 1280, 1900]},
        {"name": "Сквер Кирова", "price": 350, "house_price": 200, "rent": [44, 180, 450, 900, 1440, 2000]},
    ],
}

TRACK = {
    1: {"type": "property", "group": "Фиолетовые", "name": "Музей истории г.Иркутска"},
    2: {"type": "card", "name": "Сувенирная лавка"},
    3: {"type": "property", "group": "Фиолетовые", "name": "Вечный огонь"},
    4: {"type": "fee", "name": "Экосбор", "amount": 150},
    5: {"type": "railroad", "group": "Оранжевые", "name": "ж/д Кая"},
    6: {"type": "property", "group": "Бирюзовые", "name": "Арт-завод Доренберг"},
    7: {"type": "property", "group": "Бирюзовые", "name": "Галерея Виктора Бронштейна"},
    8: {"type": "card", "name": "Фото остановка"},
    9: {"type": "property", "group": "Бирюзовые", "name": "Иркутский комсомолец"},
    10: {"type": "rest", "name": "Прогулка"},
    11: {"type": "property", "group": "Розовые", "name": "Памятник Л.Гайдаю"},
    12: {"type": "utility", "group": "Турсервисы", "name": "Тур сервис: Гостиница «Звезда»"},
    13: {"type": "property", "group": "Розовые", "name": "Московские ворота"},
    14: {"type": "property", "group": "Розовые", "name": "Театр юного зрителя"},
    15: {"type": "railroad", "group": "Оранжевые", "name": "ж/д Мельниково"},
    16: {"type": "property", "group": "Голубые", "name": "Иркутский нерпинарий"},
    17: {"type": "card", "name": "Сувенирная лавка"},
    18: {"type": "property", "group": "Голубые", "name": "Дом-музей Трубецких"},
    19: {"type": "property", "group": "Голубые", "name": "Краеведческий музей"},
    20: {"type": "rest", "name": "Прогулка"},
    21: {"type": "property", "group": "Красные", "name": "Музей им.Сукачева"},
    22: {"type": "property", "group": "Красные", "name": "Казанская церковь"},
    23: {"type": "card", "name": "Фото остановка"},
    24: {"type": "property", "group": "Красные", "name": "Дом-музей Волконских"},
    25: {"type": "railroad", "group": "Оранжевые", "name": "ж/д Академическая"},
    26: {"type": "property", "group": "Жёлтые", "name": "Колесо «Кругозор»"},
    27: {"type": "property", "group": "Жёлтые", "name": "Спорт-парк Поляна"},
    28: {"type": "utility", "group": "Турсервисы", "name": "Тур сервис: Турагенство «Анекс»"},
    29: {"type": "property", "group": "Зелёные", "name": "Музей-ледокол «Ангара»"},
    30: {"type": "jail", "name": "В музей", "skip_turns": 2},
    31: {"type": "property", "group": "Зелёные", "name": "Памятник Александру III"},
    32: {"type": "property", "group": "Зелёные", "name": "Скульптура «Бабр»"},
    33: {"type": "card", "name": "Сувенирная лавка"},
    34: {"type": "property", "group": "Бирюзовые", "name": "Театр им.Загурского"},
    35: {"type": "railroad", "group": "Оранжевые", "name": "ж/д Иркутск-Пасс."},
    36: {"type": "card", "name": "Фото остановка"},
    37: {"type": "property", "group": "Синие", "name": "Драмтеатр им.Охлопкова"},
    38: {"type": "fee", "name": "Взнос", "amount": 150},
    39: {"type": "property", "group": "Синие", "name": "Сквер Кирова"},
    40: {"type": "start", "name": "Начало"},
}

TILE_CARD_POSITIONS = frozenset(
    {
        1,
        3,
        5,
        6,
        7,
        9,
        11,
        12,
        13,
        14,
        15,
        16,
        18,
        19,
        21,
        22,
        24,
        25,
        26,
        27,
        28,
        29,
        31,
        32,
        34,
        35,
        37,
        39,
    }
)

TILE_DETAILS: dict[int, dict[str, str]] = {
    1: {
        "info": "Музей истории города Иркутска основан в 1996 году и посвящён развитию города с XVII века до современности. Экспозиции включают археологические находки, документы и предметы быта.",
        "address": "г. Иркутск, ул. Франк-Каменецкого, 16А, этаж 1–2.",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/Музей_истории.jpg",
    },
    3: {
        "info": "Мемориал «Вечный огонь» в Иркутск посвящён памяти погибших в годы Великой Отечественной войны. Здесь горит огонь как символ вечной памяти и уважения к защитникам страны. У мемориала проходят памятные мероприятия и возложения цветов. Это одно из самых значимых мест воинской славы города.",
        "address": "г. Иркутск, Сквер у Вечного Огня",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/огонь.png",
    },
    6: {
        "info": "Арт-завод «Доренберг» в Иркутск — это креативное пространство, созданное на территории бывшего пивоваренного завода. Сегодня здесь проходят выставки, фестивали, концерты и городские мероприятия. Место объединяет современное искусство, дизайн и культурную жизнь города. Это популярная площадка для творчества и отдыха.",
        "address": "г. Иркутск, ул. Баррикад, 51/4",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/Доренберг.jpg",
    },
    7: {
        "info": "Одна из крупнейших частных художественных галерей за Уралом. Здесь представлены работы современных художников и скульпторов, включая известные выставки сибирского искусства. Пространство регулярно обновляет экспозиции и проводит культурные мероприятия. Галерея считается важным центром современной культуры Иркутска.",
        "address": "г. Иркутск, ул. Октябрьской революции, 3",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/галерея.jpg",
    },
    9: {
        "info": "Памятник в честь танковой колонны, построенной на средства комсомольцев. Он установлен 9 мая 1967 года и представляет собой танк Т-34-85. В годы войны жители области собирали деньги на боевую технику для фронта. Памятник символизирует вклад иркутян в Победу и поддержку армии.",
        "address": "г. Иркутск, Октябрьский район, ул. Советская",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/танк.jpg",
    },
    11: {
        "info": "Памятник режиссёру в Иркутске. Памятник Леониду Гайдаю в Иркутске установлен в 2012 году рядом с цирком. Скульптурная композиция изображает режиссёра и героев его фильмов — Труса, Балбеса и Бывалого. Гайдай показан в роли режиссёра, как будто снимающего сцену из «Кавказской пленницы». Памятник стал популярным местом у жителей и туристов, напоминая о его вкладе в советское кино.",
        "address": "г. Иркутск, Площадь Труда, Кировский район",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/гайдай.jpg",
    },
    13: {
        "info": "Триумфальная арка, построенная в 1813 году в честь победы России в Отечественной войне 1812 года. Они символизировали въезд в город со стороны Московского тракта и встречу гостей Иркутска. Первоначально ворота были деревянными, но позже восстановлены как каменный памятник. Сегодня это один из исторических символов города и важный архитектурный объект.",
        "address": "г. Иркутск, Нижняя набережная, 14/1",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/ворота.jpg",
    },
    14: {
        "info": "Один из ведущих театров города, основанный в 1928 году. Он специализируется на постановках для детей и подростков, а также классических и современных спектаклях. Здание театра расположено в историческом центре Иркутска и является культурной достопримечательностью. Сегодня ТЮЗ остаётся важной площадкой для развития театрального искусства в регионе.",
        "address": "г. Иркутск, ул. Ленина, 23",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/ТЮЗ.jpg",
    },
    16: {
        "info": "Уникальный театр, где выступают байкальские нерпы. Он расположен в центре города и показывает представления с дрессированными животными, которые выполняют трюки и взаимодействуют с тренерами. Нерпинарий знакомит посетителей с байкальской нерпой — эндемиком озера Байкал. Это одно из самых необычных и популярных развлечений для туристов в Иркутске.",
        "address": "г. Иркутск, 2-я Железнодорожная улица, 66",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/нерпинарий.jpg",
    },
    18: {
        "info": "Мемориальный музей, посвящённый жизни декабриста Сергея Трубецкого и его семьи в ссылке. Он находится в историческом деревянном доме, где Трубецкие жили в XIX веке. Экспозиция рассказывает о быте декабристов и их роли в истории России. Музей является частью комплекса «Иркутские дома декабристов» и важной культурной достопримечательностью города.",
        "address": "г. Иркутск, ул. Дзержинского, 64",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/Усальба_Трубецких.jpg",
    },
    19: {
        "info": "Один из старейших музеев Сибири, основанный в 1782 году. Его экспозиции посвящены природе, истории и культуре Прибайкалья. В коллекции есть археологические находки, этнографические предметы и материалы о развитии региона. Музей считается важным научным и культурным центром города..",
        "address": "г. Иркутск, ул. Карла Маркса, 2",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/краевед.jpg",
    },
    21: {
        "info": "Иркутский областной художественный музей имени В. П. Сукачёва является первой галереей за Уралом: ещё в XIX веке коллекция Сукачёва была единственной в Сибири, открытой для широкой публики, а французский профессор Ж. Легра в 1897 году назвал усадьбу Сукачёва «одной из редкостей Сибири». Начало музею было положено в 1870 году, когда Сукачёв, будучи студентом, приобрёл первые полотна в Петербурге. Сегодня музей обладает одним из крупнейших собраний искусства от Урала до Дальнего Востока; в коллекции представлены произведения русской и западноевропейской живописи, графики и скульптуры.",
        "address": "г. Иркутск, ул. Ленина, 5",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/музей.jpg",
    },
    22: {
        "info": "Храм строился на народные средства: деньги собирали долго, так как основными прихожанами были небогатые потомки каторжных, однако значительный вклад внесли иркутские купцы. В облике храма видны черты «узорочья», что придает ему особую самобытность, несмотря на постройку в конце XIX века. Судьба храма была трудной: после закрытия в 1936 году в церкви располагались склад книготорга, курсы киномехаников и завод «Сибирский сувенир», а здание неоднократно горело. Сегодня церковь полностью восстановлена в первоначальном виде, а внутреннее убранство, включая иконостас и росписи, воссоздано на пожертвования прихожан.",
        "address": "г. Иркутск, ул. Баррикад, 34/1",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/Церковь.jpg",
    },
    24: {
        "info": "Дом-музей князя С. Г. Волконского в Иркутске изначально был построен в 1837–1838 годах в селе Урик, где Волконские отбывали ссылку, а позже, получив разрешение переехать в Иркутск, князь перевез туда свой дом. Главной ценностью музея считается само здание, которое является образцом классицизма с элементами сибирского зодчества. В музее восстановлен домашний театр Волконских, и традиция проведения музыкально-литературных салонов поддерживается здесь по сей день.",
        "address": "г. Иркутск, пер. Волконского, 10",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/волконских.jpg",
    },
    26: {
        "info": "Высота колеса обозрения составляет около 50 метров, диаметр — 47,5 метров, его вес равен 182 тонны, а вес оснований — 190 тонн. На аттракционе установлено 24 закрытые кабинки, каждая из которых вмещает до 6 человек; есть одна специализированная кабинка для людей с ограниченными возможностями и две VIP-кабины с мягкими креслами и тонированными стёклами. Колесо построено с учётом норм сейсмичности, а перед запуском проводились испытания экстремальными нагрузками, что гарантирует высокий уровень безопасности.",
        "address": "г. Иркутск, Парк Остров Малый Конный, Конный остров,",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/кругозор.jpg",
    },
    27: {
        "info": "На данной территории была открыта первая в Иркутске вейк-станция — вейкбординг сочетает элементы сноуборда, скейтборда и серфинга. Инфраструктура включает русские бани с купелями, кафе «Кают-компания» на воде, гриль-домики и пространства для мероприятий (например, «Атмосфера»). Для посетителей также доступны волейбол, мини-футбол, батуты, тарзанка, веревочный парк и открытый бассейн.",
        "address": "г. Иркутск, Старо-Кузьмихинская улица, 37/3",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/поляна.jpg",
    },
    29: {
        "info": "Ледокол «Ангара» был построен в Англии на верфи «Сэр В. Г. Армстронг, Витворт и Ко» в Ньюкасле, а затем доставлен в Россию в разобранном виде и собран вручную в селе Лиственичном. Дизайн «Ангары» со скошенными трубами и заваленными внутрь бортами делал её похожей на «Ермака» — первый в мире арктический ледокол, построенный той же фирмой. В шутку «Ангару» называют чемпионом по погружениям, так как судно тонуло несколько раз: первый раз это случилось в 1928 году из-за пробоины, а позже, в 70–80-е годы, ледокол долгое время лежал на дне водохранилища в полузатопленном состоянии, пока его не отреставрировали для музея.",
        "address": "г. Иркутск, проспект Маршала Жукова, 36а/1",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/ледокол.jpg",
    },
    31: {
        "info": "Памятник Александру III в Иркутске был воздвигнут в знак признательности императору за его указ 1891 года о начале строительства Великого Сибирского пути (Транссиба). Оригинальный монумент работы скульптора Роберта Баха простоял всего 12 лет (1908–1920 годы) и был демонтирован советской властью. В 2003 году памятник был воссоздан, что стало важным событием для исторического облика города. Особенностью образа является то, что, в отличие от многих других монументов, здесь Александр III предстаёт в атаманском мундире с широкими шароварами, заправленными в сапоги, что подчёркивает его связь с сибирским казачеством.",
        "address": "г. Иркутск, Верхняя Набережная, Кировский район",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/александр3.jpg",
    },
    32: {
        "info": "Скульптура «Бабр» — один из главных символов Иркутск. Она изображает мифическое животное, похожее на тигра, с соболем в пасти. Этот образ используется и на гербе города. Бабр символизирует силу, богатство природы и историю Сибири.",
        "address": "г. Иркутск, 130-й квартал",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/бабр.jpg",
    },
    34: {
        "info": "Иркутский областной музыкальный театр имени Н. М. Загурского был основан в 1941 году на базе гастролировавшего в Иркутске Горьковского театра музыкальной комедии. В 2001 году, к 60-летию театра, ему было официально присвоено имя Николая Матвеевича Загурского, который внес огромный вклад в его развитие. На сегодняшний день это самая большая концертная площадка города.",
        "address": "г. Иркутск, ул. Седова, 29",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/загурского.png",
    },
    37: {
        "info": "Иркутский академический драмдатический театр имени Н. П. Охлопкова был основан в 1850 году, когда странствующая труппа приняла решение остаться в Иркутске, получив таким образом статус профессионального. Своё имя театр носит в честь выдающегося советского режиссёра и актёра Николая Павловича Охлопкова, который начинал здесь свой творческий путь. При театре 25 марта 1988 года был открыт собственный музей, посвящённый его богатой истории.",
        "address": "г. Иркутск, ул. Карла Маркса, 14",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/драмтеатр.jpg",
    },
    39: {
        "info": "Площадь является старейшей в городе и возникла в конце XVII века (около 1670 года) за южной стеной Иркутского острога. Ранее здесь находились Кафедральный собор и Тихвинская церковь, которые были разрушены в советское время (собор начали взрывать в 1932 году). За свою историю площадь называлась Кремлевской, Тихвинской и другими именами, прежде чем стала носить имя С. М. Кирова.",
        "address": "г. Иркутск, Сухэ-Батора, 7а/1",
        "photo_url": "https://raw.githubusercontent.com/meowrim/Babrograd/main/Photos/сквер.jpg",
    },
}

QUIZ_QUESTIONS = [
    {
        "question": "Что является символом Иркутска?",
        "options": ["Бабр", "Медведь", "Тигр"],
        "correct": 0
    },
    {
        "question": "Чем известен Байкал?",
        "options": ["Самое тёплое море", "Самое глубокое озеро в мире", "Большой вулкан"],
        "correct": 1
    },
    {
        "question": "В каком веке основан Иркутск?",
        "options": ["XII", "XVII", "XIX"],
        "correct": 1
    },
    {
        "question": "Что является важным транспортным узлом Иркутска?",
        "options": ["Морской порт", "Транссиб и ж/д", "Метро"],
        "correct": 1
    },
    {
        "question": "Какой писатель жил в Иркутске?",
        "options": ["Пушкин", "Распутин", "Толстой"],
        "correct": 1
    },
    {
        "question": "Что изображено на гербе Иркутска?",
        "options": ["Бабр с соболем", "Медведь с рыбой", "Орёл с мечом"],
        "correct": 0
    },
    {
        "question": "Какая река является единственным истоком Байкала?",
        "options": ["Лена", "Ангара", "Енисей"],
        "correct": 1
    },
    {
        "question": "Что такое 130-й квартал в Иркутске?",
        "options": [ "Современный бизнес-центр", "Исторический район", "Промышленная зона"],
        "correct": 1
    },
    {
        "question": "Что делает Байкал стратегически важным ресурсом?",
        "options": [
            "Наличие нефти",
            "Запасы пресной воды",
            "Золото в берегах"
        ],
        "correct": 1
    },  
    {
        "question": "Что было основой экономики Иркутска в ранний период?",
        "options": [
            "Рыболовство в океане",
            "Морское судостроение",
            "Торговля, пушнина и экспедиции в Сибирь"
        ],
        "correct": 2
    },
    {
        "question": "Что означает название 'Иркутск' по одной из версий?",
        "options": [
            "Город у реки Иркут",
            "Город солнца",
            "Город у Байкала"
        ],
        "correct": 0
    },
        {
        "question": "Что было одной из причин развития Иркутска в XVII–XVIII веках?",
        "options": [
            "Золото и нефть",
            "Морской флот",
            "Торговля и освоение Сибири"
        ],
        "correct": 2
    },
    {
        "question": "Какой регион связан с Иркутском через Байкал?",
        "options": [
            "Бурятия",
            "Крым",
            "Кавказ"
        ],
        "correct": 2
    },    
    {
        "question": "Почему климат Иркутска считается суровым?",
        "options": [
            "Из-за частых ураганов",
            "Из-за резких перепадов температур зимой и летом",
            "Из-за высокой влажности"
        ],
        "correct": 1
    },
    {
        "question": "Почему Иркутск важен в маршрутах Сибири?",
        "options": [
            "Он стоит на пересечении торговых и транспортных путей",
            "Он морской порт",
            "Он столица региона"
        ],
        "correct": 0
    },
    {
        "question": "Какой памятник связан с первопроходцами Сибири в Иркутске?",
        "options": [
            "Памятник основателям Иркутска",
            "Памятник космонавтам",
            "Памятник морякам"
        ],
        "correct": 0
    },
    {
        "question": "Чем известен памятник «Вечный огонь» в Иркутске?",
        "options": [
            "Посвящён Победе в Великой Отечественной войне",
            "Посвящён Байкалу",
            "Посвящён декабристам"
        ],
        "correct": 0
    },
    {
        "question": "Что символизирует памятник основателям Иркутска?",
        "options": [
            "Космические полёты",
            "Морские экспедиции",
            "Освоение Сибири"
        ],
        "correct": 0
    },
]

async def upload_photo_from_url(peer_id: int, url: str) -> str | None:
    if not url:
        return None

    timeout = aiohttp.ClientTimeout(total=45)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.read()

    if not data:
        return None

    upload_server = await bot.api.photos.get_messages_upload_server(peer_id=peer_id)

    form = aiohttp.FormData()
    form.add_field(
        "photo",
        data,
        filename="photo.jpg",
        content_type="image/jpeg"
    )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(upload_server.upload_url, data=form) as resp:
            upload_data = await resp.json()

    saved = await bot.api.photos.save_messages_photo(
        photo=upload_data["photo"],
        server=upload_data["server"],
        hash=upload_data["hash"]
    )

    if not saved:
        return None

    photo = saved[0]
    return f"photo{photo.owner_id}_{photo.id}"


async def maybe_send_tile_card(user_id: int, pos: int, keyboard=None) -> None:
    if pos not in TILE_CARD_POSITIONS:
        return

    d = TILE_DETAILS.get(pos)
    if not d:
        return

    info = (d.get("info") or "").strip()
    address = (d.get("address") or "").strip()
    photo_url = (d.get("photo_url") or "").strip()

    text_parts = []

    if info:
        text_parts.append(f"ℹ️ {info}")

    if address:
        text_parts.append(f"📍 Адрес:\n{address}")

    text = "\n\n".join(text_parts)

    attachment = None
    if photo_url:
        attachment = PHOTO_CACHE.get(photo_url)
        if not attachment:
            attachment = await upload_photo_from_url(user_id, photo_url)
            if attachment:
                PHOTO_CACHE[photo_url] = attachment

    await bot.api.messages.send(
        user_id=user_id,
        message=text,
        attachment=attachment,
        random_id=0
    )

async def send_quiz(user_id: int):
    q = random.choice(QUIZ_QUESTIONS)

    get_user_data(user_id)["quiz_correct"] = q["correct"]
    get_user_data(user_id)["quiz_correct_text"] = q["options"][q["correct"]]

    user_states[user_id] = "waiting_quiz_answer"

    k = Keyboard(inline=True)

    for i, option in enumerate(q["options"]):
        k.add(
            Text(
                option,
                payload={"cmd": "quiz_answer", "index": i}
            )
        )
        k.row()

    await send_to(
        user_id,
        f"🧠 Викторина!\n\n{q['question']}",
        keyboard=k
    )

def get_user_data(user_id: int) -> dict:
    return user_data.setdefault(user_id, {})


def clear_user_state(user_id: int) -> None:
    user_states.pop(user_id, None)
    user_data.pop(user_id, None)


def is_player_turn(user_id: int) -> bool:
    code = player_sessions.get(user_id)
    if not code or code not in current_turn_index:
        return False
    return games[code][current_turn_index[code]] == user_id


async def send_to(user_id: int, text: str, keyboard=None) -> None:
    await bot.api.messages.send(user_id=user_id, message=text, keyboard=keyboard, random_id=0)

def _truncate_label(text: str, max_len: int = 40) -> str:
    text = (text or "").strip()
    if len(text) <= max_len:
        return text
    return text[: max(0, max_len - 1)].rstrip() + "…"


def _btn(label: str, payload: dict):
    return Text(_truncate_label(label, 40), payload=payload)


async def ensure_player_name(user_id: int) -> str:
    existing = player_names.get(user_id)
    if existing:
        return existing
    try:
        users = await bot.api.users.get(user_ids=[user_id])
        if users:
            u = users[0]
            name = f"{u.first_name} {u.last_name}".strip()
        else:
            name = f"id{user_id}"
    except Exception:
        name = f"id{user_id}"
    player_names[user_id] = name
    return name

def _get_code(user_id: int) -> str | None:
    return player_sessions.get(user_id)


def _current_player_id(code: str) -> int | None:
    if code not in games or code not in current_turn_index:
        return None
    return games[code][current_turn_index[code]]

def _is_host(user_id: int) -> bool:
    code = _get_code(user_id)
    if not code or code not in games or not games[code]:
        return False
    return games[code][0] == user_id


def _reset_turn_flags(user_id: int) -> None:
    turn_flags[user_id] = {
        "rolled": False,
        "purchase_decided": False,
        "rent_paid": False,
        "can_buy": False,
        "can_build": False,
        "can_rent": False,
        "landed_tile": None,
        "dice_sum": None,
    }

async def show_inventory(user_id: int):
    items = player_inventory.get(user_id, [])

    if not items:
        await send_to(user_id, "🎒 У вас пока нет предметов.")
        return

    text = "🎒 Ваш инвентарь:\n\n"
    for item in items:
        text += f"• {item}\n"

    await send_to(user_id, text)

def spectator_keyboard():
    k = Keyboard(inline=True)

    k.add(_btn("💰 Посмотреть баланс", {"cmd": "show_balance"}))
    k.add(_btn("🏠 Своя собственность", {"cmd": "show_properties"})).row()
    k.add(_btn("👁 Собственность всех", {"cmd": "view_all_properties"}))
    k.add(_btn("🎒 Свой инвентарь", {"cmd": "show_inventory"}))

    return k

def _turn_keyboard(user_id: int):
    flags = turn_flags.get(user_id) or {}
    can_build = bool(flags.get("can_build"))

    k = Keyboard(inline=True)
    
    k.add(_btn("💰 Баланс", {"cmd": "balance_menu"}))
    k.add(_btn("🏠 Собственность", {"cmd": "property_menu"})).row()
    if can_build:
        k.add(_btn("🏗 Строить", {"cmd": "build_menu"}))
    k.add(_btn("✅ Завершить ход", {"cmd": "end_turn"}))
    if _is_host(user_id):
        k.row()
        k.add(_btn("🛑 Завершить игру", {"cmd": "end_game"}))
    return k


async def prompt_dice(user_id: int):
    _reset_turn_flags(user_id)

    if player_quiz_flags.get(user_id, {}).get("available"):
            player_quiz_flags[user_id]["available"] = False
            await send_quiz(user_id)
            return

    user_states[user_id] = "waiting_for_dice"
    await send_to(user_id, "🎲 Ваш ход! Введите сумму на кубиках (2–12):")


def _move_position(pos: int, dice_sum: int):
    total = pos - 1 + dice_sum
    new_pos = (total % 40) + 1
    passed_start = total >= 40
    return new_pos, passed_start


def _is_build_group(group_name: str) -> bool:
    return group_name not in ["Оранжевые", "Турсервисы"]


def _has_full_set(user_id: int, group_name: str) -> bool:
    if not group_name or group_name not in property_groups:
        return False
    if not _is_build_group(group_name):
        return False
    owned = set(player_properties.get(user_id, []))
    group_assets = {a["name"] for a in property_groups[group_name] if "rent" in a}
    return bool(group_assets) and group_assets.issubset(owned)


def _can_build_here(user_id: int, street_name: str) -> bool:
    group_name, asset = _find_asset_in_groups(street_name)
    if not asset:
        return False
    if "rent" not in asset:
        return False
    if property_owners.get(street_name) != user_id:
        return False
    return _has_full_set(user_id, group_name)


def _find_asset_in_groups(asset_name: str):
    for group_name, assets in property_groups.items():
        for a in assets:
            if a["name"] == asset_name:
                return group_name, a
    return None, None


def _tile_economy_from_groups(tile: dict):
    group_name, asset = _find_asset_in_groups(tile["name"])
    if not asset:
        return {}
    econ = {"price": asset.get("price", 0)}
    if "house_price" in asset:
        econ["house_price"] = asset.get("house_price")
    if "rent" in asset:
        econ["rent"] = asset.get("rent")
    econ["group"] = group_name
    return econ


async def resolve_landing(user_id: int, dice_sum: int):
    code = _get_code(user_id)
    if not code:
        await send_to(user_id, "❗ Вы не в игре.")
        return

    pos = player_positions.get(user_id, 40)
    new_pos, passed_start = _move_position(pos, dice_sum)
    player_positions[user_id] = new_pos

    if passed_start:
        prev_laps = laps_completed.get(user_id, 0)
        laps_completed[user_id] = prev_laps + 1
        if prev_laps > 0:
            player_balance[user_id] = player_balance.get(user_id, START_MONEY) + 200
        
        player_quiz_flags.setdefault(user_id, {"available": False, "asked": False})
        if prev_laps > 0:
            player_quiz_flags[user_id]["available"] = True
            player_quiz_flags[user_id]["asked"] = False

    tile = TRACK[new_pos]
    econ = _tile_economy_from_groups(tile) if tile["type"] in ["property", "railroad", "utility"] else {}
    full_tile = {**tile, **econ, "pos": new_pos}

    flags = turn_flags.setdefault(user_id, {})
    flags["rolled"] = True
    flags["dice_sum"] = dice_sum
    flags["landed_tile"] = full_tile

    ttype = tile["type"]
    title = f"📍 Выпало поле {new_pos}/40: {tile.get('name','')}"
    if passed_start:
        prev_laps = laps_completed.get(user_id, 1) - 1
        if prev_laps > 0:
            title += "\n🏁 Вы прошли «Начало»: +200₽"

    if ttype == "start":
        await send_to(user_id, f"{title}\n🏁 Начало. Ход продолжается.", keyboard=_turn_keyboard(user_id))
        return

    if ttype == "card":
        await send_to(user_id, f"{title}\n🃏 {tile['name']}. Возьмите карточку.", keyboard=_turn_keyboard(user_id))
        return

    if ttype == "rest":
        if tile["name"].lower().startswith("музей"):
            await send_to(user_id, f"{title}\n🚶 Просто прогулка мимо музея.", keyboard=_turn_keyboard(user_id))
        else:
            await send_to(user_id, f"{title}\n😌 Просто отдых.", keyboard=_turn_keyboard(user_id))
        return

    if ttype == "fee":
        amount = int(tile["amount"])
        bal = player_balance.get(user_id, START_MONEY)
        player_balance[user_id] = max(0, bal - amount)
        await send_to(user_id, f"{title}\n💸 {tile['name']}: -{amount}₽.\n💰 Баланс: {player_balance[user_id]}₽", keyboard=_turn_keyboard(user_id))
        flags["purchase_decided"] = True
        flags["can_buy"] = False
        flags["can_build"] = False
        flags["can_rent"] = False
        return

    if ttype == "jail":
        skip_turns_left[user_id] = int(tile.get("skip_turns", 2))
        await send_to(user_id, f"{title}\n🏛 {tile['name']}. Вы пропускаете {skip_turns_left[user_id]} своих хода(ов).", keyboard=_turn_keyboard(user_id))
        await end_turn(user_id)
        return

    name = tile["name"]
    price = int(econ.get("price", 0))

    owner_id = property_owners.get(name)
    if not isinstance(owner_id, int):
        owner_id = None

    if owner_id is None:
        desc_parts = [title, f"🏷 {name}", f"💵 Цена: {price}₽"]
        if ttype == "property":
            desc_parts.append(f"🏠 Цена дома: {econ.get('house_price')}₽")

        k = Keyboard(inline=True)
        k.add(_btn("✅ Купить", {"cmd": "buy_landed_yes"}))
        k.add(_btn("❌ Не покупать", {"cmd": "buy_landed_no"}))
        await maybe_send_tile_card(user_id, new_pos, keyboard=k)
        await send_to(user_id, "\n".join(desc_parts) + "\n\nКупить?", keyboard=k)
        flags["can_buy"] = True
        flags["purchase_decided"] = False
        return

    if owner_id == user_id:
        flags["purchase_decided"] = True
        flags["can_buy"] = False
        flags["can_build"] = bool(ttype == "property" and _can_build_here(user_id, name))
        flags["can_rent"] = False
        build_hint = "\n🏗 У вас полный комплект этой группы — можно строить." if flags["can_build"] else ""
        await maybe_send_tile_card(user_id, new_pos, keyboard=_turn_keyboard(user_id))
        await send_to(user_id, f"{title}\n🏠 Это ваша собственность: {name}.{build_hint}", keyboard=_turn_keyboard(user_id))
        return

    if not isinstance(owner_id, int):
        await send_to(user_id, f"{title}\n❗ Ошибка владельца. Считаю клетку ничьей.", keyboard=_turn_keyboard(user_id))
        return
    await ensure_player_name(owner_id)
    rent = 0
    if ttype == "railroad":
        owned = player_properties.get(owner_id, [])
        railroads = [TRACK[p]["name"] for p in TRACK if TRACK[p]["type"] == "railroad"]
        num_owned = sum(1 for r in railroads if r in owned)
        rent = 25 if num_owned == 1 else 50 if num_owned == 2 else 100 if num_owned == 3 else 200
    elif ttype == "utility":
        owned = player_properties.get(owner_id, [])
        utils = [TRACK[p]["name"] for p in TRACK if TRACK[p]["type"] == "utility"]
        num_owned = sum(1 for u in utils if u in owned)
        rent = dice_sum * (5 if num_owned == 1 else 10)
    else:
        buildings = player_buildings.get(owner_id, {}).get(name, {"houses": 0, "hotel": False})
        if buildings.get("hotel"):
            rent = int(econ["rent"][5])
        else:
            rent = int(econ["rent"][int(buildings.get("houses", 0))])

    bal_from = player_balance.get(user_id, START_MONEY)
    bal_to = player_balance.get(owner_id, START_MONEY)
    if bal_from < rent:
        await send_to(user_id, f"{title}\n❗ Это собственность игрока {player_names[owner_id]}.\n💸 Рента: {rent}₽, у вас: {bal_from}₽ (не хватает).", keyboard=_turn_keyboard(user_id))
        flags["rent_paid"] = True
        flags["purchase_decided"] = True
        flags["can_buy"] = False
        flags["can_build"] = False
        flags["can_rent"] = False
        return

    player_balance[user_id] = bal_from - rent
    player_balance[owner_id] = bal_to + rent

    await send_to(
        user_id,
        f"{title}\n❗ Это собственность игрока {player_names[owner_id]}.\n💸 Вы заплатили ренту: {rent}₽.\n💰 Ваш баланс: {player_balance[user_id]}₽",
        keyboard=_turn_keyboard(user_id),
    )
    await send_to(owner_id, f"💰 Вам заплатили {rent}₽ ренты за «{name}» от {player_names[user_id]}.\n💵 Баланс: {player_balance[owner_id]}₽")

    flags["rent_paid"] = True
    flags["purchase_decided"] = True
    flags["can_buy"] = False
    flags["can_build"] = False
    flags["can_rent"] = False


def find_street_info_and_group(street_name: str):
    for group, street_list in property_groups.items():
        for street in street_list:
            if street["name"].strip() == street_name.strip():
                return street, group
    return None, None


def get_property_price(property_name: str):
    for streets in property_groups.values():
        for prop in streets:
            if prop["name"] == property_name:
                return prop.get("price")
    return None


def start_menu_keyboard():
    return (
        Keyboard(inline=True)
        .add(Text("🚀 Создать игру", payload={"cmd": "create_game"}))
        .row()
        .add(Text("🔗 Присоединиться", payload={"cmd": "join_game"}))
    )


def main_turn_keyboard(user_id: int, is_host: bool):
    k = Keyboard(inline=True)

    k.add(Text("💰 Баланс", payload={"cmd": "balance_menu"}))
    k.add(Text("🛒 Купить", payload={"cmd": "buy_menu"})).row()

    k.add(Text("🏠 Собственность", payload={"cmd": "property_menu"}))
    k.add(Text("🏗 Строить", payload={"cmd": "build_menu"})).row()

    k.add(Text("💸 Рента", payload={"cmd": "rent_menu"}))
    k.add(Text("✅ Конец хода", payload={"cmd": "end_turn"}))

    if is_host:
        k.row()
        k.add(Text("🛑 Завершить игру", payload={"cmd": "end_game"}))

    return k


def yes_no_keyboard(payload_yes: dict, payload_no: dict, yes_label="Да", no_label="Нет"):
    k = Keyboard(inline=True)
    k.add(Text(yes_label, payload=payload_yes)).row()
    k.add(Text(no_label, payload=payload_no))
    return k


async def show_start_menu(user_id: int, user_msg: Message | None = None):
    if user_msg is not None:
        await user_msg.answer(
            "👋 Привет! Это бот для настольной игры «Баброград».\nВыберите действие:",
            keyboard=start_menu_keyboard(),
        )
    else:
        await send_to(user_id, "👋 Привет! Это бот для настольной игры «Баброград».\nВыберите действие:", start_menu_keyboard())


async def send_start_game_button(code: str):
    host_id = games[code][0]
    keyboard = Keyboard(inline=True).add(_btn("▶️ Начать игру", payload={"cmd": "start_game", "code": code}))
    await send_to(host_id, "✅ Игроки подключились. Вы можете начать игру:", keyboard=keyboard)
    sent_start_button[code] = True


async def start_game(code: str):
    players = games[code]
    game_started[code] = True
    host_id = players[0]
    current_turn_index[code] = 0

    property_owners.clear()
    player_buildings.clear()

    for user_id in players:
        await ensure_player_name(user_id)
        player_balance[user_id] = START_MONEY
        player_properties[user_id] = []
        player_positions[user_id] = 40
        skip_turns_left[user_id] = 0
        laps_completed[user_id] = 0
        _reset_turn_flags(user_id)

        text = f"🎲 Игра началась! Ваш баланс: {START_MONEY}₽"
        if user_id == host_id:
            await send_to(user_id, text + "\n🔔 Ваш ход!", keyboard=None)
        else:
            await send_to(user_id, text + "\n⏳ Ожидайте своей очереди.", keyboard=None)

    await prompt_dice(host_id)


async def end_turn(user_id: int):
    code = player_sessions.get(user_id)
    if not code or not is_player_turn(user_id):
        await send_to(user_id, "❗ Сейчас не ваш ход.")
        return

    players = games[code]
    current_turn_index[code] = (current_turn_index[code] + 1) % len(players)
    next_player_id = players[current_turn_index[code]]

    await send_to(user_id, "✅ Вы завершили ход.")

    for pid in players:
        await ensure_player_name(pid)
        if pid == next_player_id:
            await send_to(pid, "🔔 Ваш ход!", keyboard=None)
        else:
            await send_to(
            pid,
            f"⏳ Ход игрока {player_names[next_player_id]}",
            keyboard=spectator_keyboard()
        )

    if skip_turns_left.get(next_player_id, 0) > 0:
        await prompt_skip_turn_choice(next_player_id)
        return

    await prompt_dice(next_player_id)

async def prompt_skip_turn_choice(user_id: int):
    skips = skip_turns_left.get(user_id, 0)

    k = Keyboard(inline=True)
    k.add(Text("💰 Заплатить 50₽", payload={"cmd": "skip_pay"})).row()
    k.add(Text("🎲 Выпал дубль", payload={"cmd": "skip_roll"})).row()
    k.add(Text("❌ Остаться", payload={"cmd": "skip_stay"}))

    await send_to(
        user_id,
        f"⛔ Вы пропускаете ход. Осталось: {skips}\n"
        f"Хотите выйти досрочно?",
        keyboard=k
    )

async def end_game(user_id: int):
    code = player_sessions.get(user_id)
    if not code or code not in games:
        await send_to(user_id, "❗ Вы не участвуете в активной игре.")
        return

    if games[code][0] != user_id:
        await send_to(user_id, "❌ Только хост может завершить игру.")
        return

    player_ids = games[code]

    for pid in player_ids:
        player_sessions.pop(pid, None)
        player_balance.pop(pid, None)
        player_properties.pop(pid, None)
        player_names.pop(pid, None)
        player_buildings.pop(pid, None)

    for prop in list(property_owners.keys()):
        if property_owners[prop] in player_ids:
            del property_owners[prop]

    player_buildings.clear()

    del games[code]
    del sent_start_button[code]
    if code in current_turn_index:
        del current_turn_index[code]
    if code in game_started:
        del game_started[code]

    for pid in player_ids:
        await send_to(pid, "🛑 Игра завершена.\nВыберите действие ниже:", keyboard=start_menu_keyboard())


async def balance_menu(user_id: int):
    keyboard = (
        Keyboard(inline=True)
        .add(Text("💰 Текущий баланс", payload={"cmd": "show_balance"}))
        .row()
        .add(Text("🔄 Изменить баланс", payload={"cmd": "change_balance"}))
    )
    await send_to(user_id, "Выберите действие:", keyboard=keyboard)


async def show_balance(user_id: int):
    balance = player_balance.get(user_id, START_MONEY)
    await send_to(user_id, f"Ваш баланс: {balance}₽")


async def change_balance_command(user_id: int):
    if not is_player_turn(user_id):
        await send_to(user_id, "⏳ Сейчас не ваш ход.")
        return

    keyboard = (
        Keyboard(inline=True)
        .add(Text("➕ Пополнить баланс", payload={"cmd": "balance_add"}))
        .row()
        .add(Text("➖ Снять с баланса", payload={"cmd": "balance_subtract"}))
    )
    await send_to(user_id, "💰 Что вы хотите сделать с балансом?", keyboard=keyboard)
    user_states[user_id] = "waiting_for_action"
    get_user_data(user_id).clear()


async def choose_balance_action(user_id: int, action: str):
    get_user_data(user_id)["action"] = action
    user_states[user_id] = "waiting_for_amount"
    await send_to(user_id, "💸 Введите сумму (только число):")


async def process_balance_amount_input(user_id: int, text: str):
    state = user_states.get(user_id)
    if state != "waiting_for_amount":
        return False

    try:
        amount = int(text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        await send_to(user_id, "❗ Введите положительное целое число.")
        return True

    data = get_user_data(user_id)
    action = data.get("action")
    current_balance = player_balance.get(user_id, START_MONEY)

    if action == "balance_add":
        player_balance[user_id] = current_balance + amount
        await send_to(user_id, f"✅ Баланс пополнен на {amount}₽.\n💰 Новый баланс: {player_balance[user_id]}₽")
    elif action == "balance_subtract":
        if amount > current_balance:
            await send_to(user_id, f"❗ Недостаточно средств. У вас только {current_balance}₽.")
            clear_user_state(user_id)
            return True
        player_balance[user_id] = current_balance - amount
        await send_to(user_id, f"✅ С баланса снято {amount}₽.\n💰 Новый баланс: {player_balance[user_id]}₽")

    clear_user_state(user_id)
    return True


async def property_menu(user_id: int):
    keyboard = (
        Keyboard(inline=True)
        .add(Text("🏠 Текущая собственность", payload={"cmd": "show_properties"}))
        .row()
        .add(Text("🔄 Обмен собственностью", payload={"cmd": "trade_properties"}))
        .row()
        .add(Text("👁️‍🗨️ Просмотр собственности других", payload={"cmd": "view_all_properties"}))
    )
    await send_to(user_id, "Выберите действие с вашей собственностью:", keyboard=keyboard)


def _property_owner_group(p: str):
    for group_name, streets in property_groups.items():
        for street in streets:
            if street["name"].strip().lower() == p.strip().lower():
                return group_name
    return None


async def show_properties(user_id: int):
    props = player_properties.get(user_id, [])
    if not props:
        await send_to(user_id, "❗ У вас пока нет собственности.")
        return

    lines = []
    for p in props:
        buildings = player_buildings.get(user_id, {}).get(p, {"houses": 0, "hotel": False})
        houses = buildings["houses"]
        hotel = buildings["hotel"]
        street_color = _property_owner_group(p)

        if street_color in ["Заводы", "Железные дороги"]:
            lines.append(f"◆ {p} ({street_color})")
        else:
            lines.append(f"◆ {p} ({street_color}) \n 🏠 Дома: {houses} | 🏨 Отель: {'да' if hotel else 'нет'}")

    await send_to(user_id, "Ваша собственность:\n" + "\n".join(lines))


async def start_trade(user_id: int):
    if not is_player_turn(user_id):
        await send_to(user_id, "⏳ Сейчас не ваш ход.")
        return
    if user_id not in player_sessions:
        await send_to(user_id, "❗ Вы не находитесь в игре.")
        return

    code = player_sessions[user_id]
    players_in_game = games.get(code, [])
    other_players = [pid for pid in players_in_game if pid != user_id]
    if not other_players:
        await send_to(user_id, "❗ В игре нет других игроков для обмена.")
        return

    k = Keyboard(inline=True)
    row_size = 3
    for i, pid in enumerate(other_players):
        await ensure_player_name(pid)
        k.add(_btn(player_names[pid], payload={"cmd": "trade_player", "to_id": pid}))
        if (i + 1) % row_size == 0:
            k.row()

    await send_to(user_id, "🔄 Кому вы хотите передать собственность?", keyboard=k)
    user_states[user_id] = "choosing_player"
    get_user_data(user_id).clear()


async def choose_trade_partner(user_id: int, receiver_id: int):
    get_user_data(user_id)["receiver_id"] = receiver_id
    await ensure_player_name(receiver_id)

    sender_props = player_properties.get(user_id, [])
    if not sender_props:
        await send_to(user_id, "❗ У вас нет собственности для передачи.")
        clear_user_state(user_id)
        return

    owned_groups = []
    for group, props in property_groups.items():
        if any(p["name"] in sender_props for p in props):
            owned_groups.append(group)

    k = Keyboard(inline=True)
    row_size = 3
    for i, group in enumerate(owned_groups):
        k.add(_btn(group, payload={"cmd": "trade_group", "group": group}))
        if (i + 1) % row_size == 0:
            k.row()

    await send_to(user_id, "🎨 Выберите группу собственности:", keyboard=k)
    user_states[user_id] = "choosing_group"


async def choose_property_group(user_id: int, group_name: str):
    data = get_user_data(user_id)
    receiver_id = data.get("receiver_id")

    sender_props = player_properties.get(user_id, [])
    streets_in_group = property_groups.get(group_name, [])

    for street in streets_in_group:
        street_name = street["name"]
        if street_name in sender_props:
            buildings = player_buildings.get(user_id, {}).get(street_name, {"houses": 0, "hotel": False})
            if buildings["houses"] > 0 or buildings["hotel"]:
                await send_to(
                    user_id,
                    f"❌ Нельзя передать улицы из группы «{group_name}», потому что на одной из них есть постройки.",
                )
                clear_user_state(user_id)
                return

    owned_in_group = [p["name"] for p in streets_in_group if p["name"] in sender_props]
    if not owned_in_group:
        await send_to(user_id, "❗ У вас нет собственности в этой группе.")
        clear_user_state(user_id)
        return

    k = Keyboard(inline=True)
    row_size = 3
    for i, prop_name in enumerate(owned_in_group):
        k.add(_btn(prop_name, payload={"cmd": "trade_property", "prop": prop_name}))
        if (i + 1) % row_size == 0:
            k.row()

    await send_to(user_id, "🏘 Выберите конкретную собственность для передачи:", keyboard=k)
    user_states[user_id] = "choosing_property"


async def finalize_trade(user_id: int, property_name: str):
    data = get_user_data(user_id)
    receiver_id = data.get("receiver_id")
    if receiver_id is None:
        clear_user_state(user_id)
        await send_to(user_id, "❗ Ошибка обмена: получатель не найден.")
        return

    if property_name not in player_properties.get(user_id, []):
        clear_user_state(user_id)
        await send_to(user_id, "❗ Ошибка обмена: собственность не найдена у отправителя.")
        return

    player_properties[user_id].remove(property_name)
    player_properties.setdefault(receiver_id, []).append(property_name)
    property_owners[property_name] = receiver_id

    await send_to(user_id, f"✅ Вы передали {property_name} игроку {player_names[receiver_id]}.")
    await send_to(receiver_id, f"📦 Вы получили собственность «{property_name}» от {player_names[user_id]}!")
    clear_user_state(user_id)


async def view_all_properties(user_id: int):
    all_players = list(player_properties.keys())
    if not all_players:
        await send_to(user_id, "❗ В игре нет игроков.")
        return

    lines = []
    for player_id in all_players:
        props = player_properties.get(player_id, [])
        if not props:
            lines.append(f"🏷 Игрок: {player_names.get(player_id, 'Неизвестный')} \n ❗ Нет собственности")
            continue

        player_info = [f"🏷 Игрок: {player_names.get(player_id, 'Неизвестный')}"]
        for p in props:
            buildings = player_buildings.get(player_id, {}).get(p, {"houses": 0, "hotel": False})
            houses = buildings["houses"]
            hotel = buildings["hotel"]
            street_color = _property_owner_group(p)

            if street_color in ["Заводы", "Железные дороги"]:
                player_info.append(f"◆ {p} ({street_color})")
            else:
                player_info.append(
                    f"◆ {p} ({street_color}) \n 🏠 Дома: {houses} | 🏨 Отель: {'да' if hotel else 'нет'}"
                )

        lines.append("\n".join(player_info))

    await send_to(user_id, "👀 Собственность всех игроков:\n\n" + "\n\n".join(lines))


async def buy_menu(user_id: int):
    if not is_player_turn(user_id):
        await send_to(user_id, "⏳ Сейчас не ваш ход.")
        return

    k = Keyboard(inline=True)
    groups = list(property_groups.keys())
    row_size = 3
    for i, group in enumerate(groups):
        k.add(_btn(group, payload={"cmd": "buy_group", "group": group}))
        if (i + 1) % row_size == 0:
            k.row()
    await send_to(user_id, "Выбери цветовую группу или тип собственности:", keyboard=k)


async def show_properties_from_group(user_id: int, group: str):
    streets = property_groups.get(group, [])
    buttons = Keyboard(inline=True)

    for s in streets:
        name = s["name"]
        price = s.get("price", 0)

        if name in property_owners:
            owner_id = property_owners[name]
            await ensure_player_name(owner_id)
            owner_name = player_names.get(owner_id, "другой игрок")
            if owner_id == user_id:
                label = f"✅ {name}"
                buttons.add(_btn(label, payload={"cmd": "owned_property", "prop": name})).row()
            else:
                label = f"⛔ {name} ({owner_name})"
                buttons.add(_btn(label, payload={"cmd": "occupied_property", "prop": name})).row()
        else:
            label = f"🛒 {name} — {price}₽"
            buttons.add(_btn(label, payload={"cmd": "buy_property", "prop": name})).row()

    await send_to(user_id, f"🏘 Улицы в группе «{group}». Выбери доступную для покупки:", keyboard=buttons)


async def handle_buy_property(user_id: int, property_name: str):
    await send_to(user_id, "🛒 Покупка доступна только при попадании на клетку после броска кубиков.")


async def handle_owned_property(user_id: int, property_name: str):
    await send_to(user_id, f"🏠 {property_name} уже принадлежит вам")


async def handle_occupied_property(user_id: int, property_name: str):
    owner_id = property_owners.get(property_name)
    owner_name = player_names.get(owner_id, "другой игрок")
    await send_to(user_id, f"❌ {property_name} уже принадлежит {owner_name}")


async def show_build_menu(user_id: int):
    properties = player_properties.get(user_id, [])

    owned_groups = {}
    for group_name, streets in property_groups.items():
        group_owned_streets = []
        for street in streets:
            if street["name"] in properties:
                group_owned_streets.append(street["name"])
        if group_owned_streets:
            owned_groups[group_name] = group_owned_streets

    buttons = Keyboard(inline=True)
    buttons_added = False
    added_count = 0
    for group_name in owned_groups:
        if group_name in ["Турсервисы", "Оранжевые"]:
            continue

        full_group_streets = [street["name"] for street in property_groups[group_name]]
        if set(full_group_streets).issubset(set(properties)):
            if added_count % 2 == 0:
                buttons.add(Text(group_name, payload={"cmd": "choose_build_group", "group": group_name}))
            else:
                buttons.add(Text(group_name, payload={"cmd": "choose_build_group", "group": group_name})).row()
            buttons_added = True
            added_count += 1

    if not buttons_added:
        await send_to(user_id, "❗ У вас нет полной группы улиц для строительства.")
        return

    await send_to(user_id, "🏗 Выберите цветовую группу для строительства:", keyboard=buttons)


async def choose_street_in_group(user_id: int, group: str):
    streets = [street["name"] for street in property_groups[group]]
    buttons = Keyboard(inline=True)
    for street in streets:
        buttons.add(Text(street, payload={"cmd": "choose_build_street", "street": street})).row()
    await send_to(user_id, "🏘 Выберите улицу для строительства:", keyboard=buttons)


async def ask_build_option(user_id: int, street: str):
    data = get_user_data(user_id)
    data["street"] = street
    user_states[user_id] = "waiting_for_house_count"

    k = Keyboard(inline=True)
    k.add(Text("🏠 Построить дом", payload={"cmd": "build_house"})).row()
    k.add(Text("🏨 Построить отель", payload={"cmd": "build_hotel"}))
    await send_to(user_id, f"🏗 Что вы хотите построить на «{street}»?", keyboard=k)


async def build_house_callback(user_id: int):
    data = get_user_data(user_id)
    street_name = (data.get("street") or "").strip()
    if not street_name:
        await send_to(user_id, "❗ Улица не выбрана.")
        clear_user_state(user_id)
        return

    street_info, _group = find_street_info_and_group(street_name)
    if not street_info:
        await send_to(user_id, "❗ Улица не найдена.")
        clear_user_state(user_id)
        return

    buildings = player_buildings.setdefault(user_id, {}).setdefault(street_name, {"houses": 0, "hotel": False})
    if buildings["hotel"]:
        await send_to(user_id, "🏨 Отель уже построен на этой улице.")
        return
    if buildings["houses"] >= 4:
        await send_to(user_id, "❗ На улице уже 4 дома. Постройте отель.")
        return

    user_states[user_id] = "waiting_for_house_count"
    await send_to(user_id, f"🏠 Сколько домов построить на «{street_name}»? (1–{4 - buildings['houses']})")


async def process_house_count_input(user_id: int, text: str):
    if user_states.get(user_id) != "waiting_for_house_count":
        return False

    try:
        count = int(text)
        if count < 1 or count > 4:
            raise ValueError
    except ValueError:
        await send_to(user_id, "❗ Введите число от 1 до 4.")
        return True

    street_name = (get_user_data(user_id).get("street") or "").strip()
    if not street_name:
        await send_to(user_id, "❗ Улица не была выбрана.")
        clear_user_state(user_id)
        return True

    street_info, _group_name = find_street_info_and_group(street_name)
    if street_info is None:
        await send_to(user_id, f"❗ Улица «{street_name}» не найдена в базе.")
        clear_user_state(user_id)
        return True

    buildings = player_buildings.setdefault(user_id, {}).setdefault(street_name, {"houses": 0, "hotel": False})
    if buildings["hotel"]:
        await send_to(user_id, "🏨 Отель уже построен на этой улице.")
        clear_user_state(user_id)
        return True

    total_houses = buildings["houses"] + count
    if total_houses > 4:
        await send_to(user_id, "❗ Можно максимум 4 дома на одной улице.")
        clear_user_state(user_id)
        return True

    total_cost = count * street_info["house_price"]
    balance = player_balance.get(user_id, START_MONEY)
    if balance < total_cost:
        await send_to(user_id, f"💸 Не хватает средств. Нужно {total_cost}₽, у вас {balance}₽.")
        clear_user_state(user_id)
        return True

    player_balance[user_id] = balance - total_cost
    buildings["houses"] += count

    keyboard = Keyboard(inline=True)
    keyboard.add(Text("🔁 Продолжить строительство", payload={"cmd": "continue_building"})).row()
    keyboard.add(Text("🔚 Завершить", payload={"cmd": "cancel_building"}))

    await send_to(
        user_id,
        f"✅ Построено {count} дом(ов) на «{street_name}» за {total_cost}₽.\n"
        f"🏠 Всего домов: {buildings['houses']}, отель: {'✅' if buildings['hotel'] else '❌'}\n"
        f"💰 Остаток: {player_balance[user_id]}₽",
        keyboard=keyboard,
    )
    clear_user_state(user_id)
    return True


async def build_hotel_callback(user_id: int):
    data = get_user_data(user_id)
    street_name = (data.get("street") or "").strip()
    if not street_name:
        await send_to(user_id, "❗ Улица не выбрана.")
        clear_user_state(user_id)
        return

    street_info, _group = find_street_info_and_group(street_name)
    if not street_info:
        await send_to(user_id, f"❗ Улица «{street_name}» не найдена.")
        clear_user_state(user_id)
        return

    buildings = player_buildings.setdefault(user_id, {}).setdefault(street_name, {"houses": 0, "hotel": False})
    if buildings["hotel"]:
        await send_to(user_id, "🏨 Отель уже построен на этой улице.")
        return
    if buildings["houses"] < 4:
        await send_to(user_id, "❗ Для постройки отеля нужно 4 дома.")
        return

    cost = street_info["house_price"]
    balance = player_balance.get(user_id, START_MONEY)
    if balance < cost:
        await send_to(user_id, f"💸 Недостаточно средств. Нужно {cost}₽, у вас {balance}₽.")
        clear_user_state(user_id)
        return

    player_balance[user_id] = balance - cost
    buildings["houses"] = 0
    buildings["hotel"] = True

    keyboard = Keyboard(inline=True)
    keyboard.add(Text("🔁 Продолжить строительство", payload={"cmd": "continue_building"})).row()
    keyboard.add(Text("🔚 Завершить", payload={"cmd": "cancel_building"}))

    await send_to(
        user_id,
        f"🏨 Отель построен на «{street_name}» за {cost}₽.\n"
        f"💰 Остаток: {player_balance[user_id]}₽",
        keyboard=keyboard,
    )
    clear_user_state(user_id)


async def cancel_building(user_id: int):
    await send_to(user_id, "🔚 Строительство завершено.")


async def rent_menu(user_id: int):
    if not is_player_turn(user_id):
        await send_to(user_id, "⏳ Сейчас не ваш ход.")
        return

    other_players = [uid for uid in player_properties if uid != user_id]
    if not other_players:
        await send_to(user_id, "❗ Сейчас нет других игроков.")
        return

    k = Keyboard(inline=True)
    row_size = 3
    for i, uid in enumerate(other_players):
        await ensure_player_name(uid)
        k.add(_btn(player_names[uid], payload={"cmd": "rent_to", "to_id": uid}))
        if (i + 1) % row_size == 0:
            k.row()
    await send_to(user_id, "👤 Кому вы платите ренту?", keyboard=k)


async def choose_rent_group(user_id: int, to_id: int):
    get_user_data(user_id)["rent_to"] = to_id
    await ensure_player_name(to_id)

    owned = player_properties.get(to_id, [])
    groups_with_streets = set()
    for group_name, streets in property_groups.items():
        if any(street["name"] in owned for street in streets):
            groups_with_streets.add(group_name)

    if not groups_with_streets:
        await send_to(user_id, "❗ У этого игрока нет собственности.")
        clear_user_state(user_id)
        return

    k = Keyboard(inline=True)
    row_size = 3
    for i, group in enumerate(groups_with_streets):
        k.add(_btn(group, payload={"cmd": "rent_group", "group": group}))
        if (i + 1) % row_size == 0:
            k.row()

    await send_to(user_id, "🌈 На какую группу собственности попали?", keyboard=k)


async def choose_rent_street(user_id: int, group: str):
    data = get_user_data(user_id)
    to_id = data.get("rent_to")
    if to_id is None:
        await send_to(user_id, "❗ Ошибка ренты: получатель не найден.")
        clear_user_state(user_id)
        return

    owned = player_properties.get(to_id, [])
    streets = [street["name"] for street in property_groups[group] if street["name"] in owned]

    k = Keyboard(inline=True)
    for street in streets:
        k.add(_btn(street, payload={"cmd": "rent_street", "street": street})).row()
    await send_to(user_id, "🏘 Какая конкретно улица?", keyboard=k)


async def pay_rent(user_id: int, street_name: str):
    data = get_user_data(user_id)
    to_id = data.get("rent_to")
    if to_id is None:
        await send_to(user_id, "❗ Ошибка ренты: получатель не найден.")
        clear_user_state(user_id)
        return

    street_info, group_name = find_street_info_and_group(street_name)
    if not street_info:
        await send_to(user_id, "❗ Улица не найдена.")
        clear_user_state(user_id)
        return

    if group_name == "Заводы":
        data["rent_street"] = street_name
        data["rent_group"] = group_name
        data["rent_to"] = to_id
        user_states[user_id] = "wait_for_dice_sum"
        await send_to(user_id, "🎲 Введите сумму, выпавшую на кубиках (от 2 до 12):")
        return

    if group_name == "Железные дороги":
        owned = player_properties.get(to_id, [])
        railroads = [s["name"] for s in property_groups["Железные дороги"]]
        num_owned = sum(1 for r in railroads if r in owned)

        if num_owned == 1:
            rent = 25
        elif num_owned == 2:
            rent = 50
        elif num_owned == 3:
            rent = 100
        elif num_owned >= 4:
            rent = 200
        else:
            rent = 0
    else:
        buildings = player_buildings.get(to_id, {}).get(street_name, {"houses": 0, "hotel": False})
        if buildings["hotel"]:
            rent = street_info["rent"][5]
        else:
            rent = street_info["rent"][buildings["houses"]]

    balance_from = player_balance.get(user_id, START_MONEY)
    balance_to = player_balance.get(to_id, START_MONEY)

    if balance_from < rent:
        await send_to(user_id, f"💸 У вас не хватает денег. Рента: {rent}₽, у вас: {balance_from}₽.")
        clear_user_state(user_id)
        return

    player_balance[user_id] = balance_from - rent
    player_balance[to_id] = balance_to + rent

    await send_to(
        user_id,
        f"✅ Вы заплатили {rent}₽ ренты за «{street_name}» игроку {player_names[to_id]}.\n"
        f"📤 Ваш баланс: {player_balance[user_id]}₽\n"
        f"📥 Баланс получателя: {player_balance[to_id]}₽",
    )
    await send_to(
        to_id,
        f"💰 Вам заплатили {rent}₽ ренты за «{street_name}»!\n"
        f"👤 От: {player_names[user_id]}\n"
        f"💵 Ваш новый баланс: {player_balance[to_id]}₽",
    )
    clear_user_state(user_id)


async def process_dice_sum_input(user_id: int, text: str):
    if user_states.get(user_id) != "wait_for_dice_sum":
        return False

    try:
        dice_sum = int(text.strip())
        if dice_sum < 2 or dice_sum > 12:
            raise ValueError
    except ValueError:
        await send_to(user_id, "❗ Введите корректное число от 2 до 12.")
        return True

    data = get_user_data(user_id)
    to_id = data.get("rent_to")
    street_name = data.get("rent_street")
    if to_id is None or street_name is None:
        await send_to(user_id, "❗ Ошибка ренты: данные не найдены.")
        clear_user_state(user_id)
        return True

    owned = player_properties.get(to_id, [])
    factories = [s["name"] for s in property_groups["Заводы"]]
    num_owned = sum(1 for f in factories if f in owned)
    rent = dice_sum * (5 if num_owned == 1 else 10)

    balance_from = player_balance.get(user_id, START_MONEY)
    balance_to = player_balance.get(to_id, START_MONEY)

    if balance_from < rent:
        await send_to(user_id, f"💸 У вас не хватает денег. Рента: {rent}₽, у вас: {balance_from}₽.")
        clear_user_state(user_id)
        return True

    player_balance[user_id] = balance_from - rent
    player_balance[to_id] = balance_to + rent

    await send_to(
        user_id,
        f"✅ Вы заплатили {rent}₽ ренты за «{street_name}» игроку {player_names[to_id]}.\n"
        f"📤 Ваш баланс: {player_balance[user_id]}₽\n"
        f"📥 Баланс получателя: {player_balance[to_id]}₽",
    )
    await send_to(
        to_id,
        f"💰 Вам заплатили {rent}₽ ренты за «{street_name}»!\n"
        f"👤 От: {player_names[user_id]}\n"
        f"💵 Ваш новый баланс: {player_balance[to_id]}₽",
    )
    clear_user_state(user_id)
    return True


async def continue_building(user_id: int):
    await show_build_menu(user_id)


@bot.on.message()
async def router(message: Message):
    user_id = message.from_id

    if getattr(message, "payload", None):
        payload = message.payload
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                return

        cmd = payload.get("cmd")

        if cmd == "create_game":
            code = str(random.randint(1000, 9999))
            games[code] = [user_id]
            player_sessions[user_id] = code
            await ensure_player_name(user_id)
            sent_start_button[code] = False
            await send_to(user_id, f"🎮 Вы хост!\nКод игры: {code}\nЖдём игроков...")
            return

        if cmd == "join_game":
            user_states[user_id] = "waiting_game_code"
            get_user_data(user_id).clear()
            await send_to(user_id, "Введите код игры (4 цифры):")
            return

        if cmd == "start_game":
            code = str(payload.get("code") or "")
            if code not in games:
                await send_to(user_id, "❌ Игра не найдена.")
                return
            if games[code][0] != user_id:
                await send_to(user_id, "❗ Только хост может начать игру.")
                return
            await start_game(code)
            return

        if cmd == "end_turn":
            await end_turn(user_id)
            return

        if cmd == "end_game":
            await end_game(user_id)
            return

        if cmd == "balance_menu":
            await balance_menu(user_id)
            return

        if cmd == "show_balance":
            await show_balance(user_id)
            return

        if cmd == "change_balance":
            await change_balance_command(user_id)
            return

        if cmd == "balance_add":
            await choose_balance_action(user_id, "balance_add")
            return

        if cmd == "balance_subtract":
            await choose_balance_action(user_id, "balance_subtract")
            return

        if cmd == "property_menu":
            await property_menu(user_id)
            return

        if cmd == "show_properties":
            await show_properties(user_id)
            return

        if cmd == "trade_properties":
            await start_trade(user_id)
            return

        if cmd == "trade_player":
            if user_states.get(user_id) not in [None, "choosing_player"]:
                pass
            await choose_trade_partner(user_id, int(payload.get("to_id")))
            return

        if cmd == "trade_group":
            await choose_property_group(user_id, payload.get("group"))
            return

        if cmd == "trade_property":
            await finalize_trade(user_id, payload.get("prop"))
            return

        if cmd == "view_all_properties":
            await view_all_properties(user_id)
            return

        if cmd == "buy_menu":
            await buy_menu(user_id)
            return

        if cmd == "buy_group":
            await show_properties_from_group(user_id, payload.get("group"))
            return

        if cmd == "buy_property":
            await handle_buy_property(user_id, payload.get("prop"))
            return

        if cmd == "owned_property":
            await handle_owned_property(user_id, payload.get("prop"))
            return

        if cmd == "occupied_property":
            await handle_occupied_property(user_id, payload.get("prop"))
            return

        if cmd == "build_menu":
            if not is_player_turn(user_id):
                await send_to(user_id, "⏳ Сейчас не ваш ход.")
                return
            pos = player_positions.get(user_id, 40)
            tile = TRACK.get(pos)
            if not tile or tile.get("type") != "property":
                await send_to(user_id, "❗ Сейчас строить нельзя.", keyboard=_turn_keyboard(user_id))
                return
            street = tile.get("name")
            if not street or not _can_build_here(user_id, street):
                await send_to(user_id, "❗ Сейчас строить нельзя (нужен полный комплект и своя улица).", keyboard=_turn_keyboard(user_id))
                return
            await ask_build_option(user_id, street)
            return

        if cmd == "choose_build_group":
            await choose_street_in_group(user_id, payload.get("group"))
            return

        if cmd == "choose_build_street":
            await ask_build_option(user_id, payload.get("street"))
            return

        if cmd == "build_house":
            await build_house_callback(user_id)
            return

        if cmd == "build_hotel":
            await build_hotel_callback(user_id)
            return

        if cmd == "cancel_building":
            await cancel_building(user_id)
            clear_user_state(user_id)
            return

        if cmd == "continue_building":
            await continue_building(user_id)
            clear_user_state(user_id)
            return
        
        if cmd == "skip_pay":
            if skip_turns_left.get(user_id, 0) <= 0:
                await send_to(user_id, "❗ Вы не пропускаете ход.")
                return

            balance = player_balance.get(user_id, START_MONEY)

            if balance < 50:
                await send_to(user_id, "❗ Недостаточно денег (нужно 50₽).")
                return

            player_balance[user_id] = balance - 50
            skip_turns_left[user_id] = 0

            await send_to(user_id, "✅ Вы заплатили 50₽ и выходите!")
            await prompt_dice(user_id)
            return
        
        if cmd == "skip_stay":
            skips = skip_turns_left.get(user_id, 0)

            if skips <= 0:
                await send_to(user_id, "❗ Вы не пропускаете ход.")
                return

            skip_turns_left[user_id] -= 1

            await send_to(user_id, f"⏭ Вы остались. Осталось пропусков: {skip_turns_left[user_id]}")
            await end_turn(user_id)
            return
        
        if cmd == "skip_roll":
            if skip_turns_left.get(user_id, 0) <= 0:
                await send_to(user_id, "❗ Вы не пропускаете ход.")
                return

            skip_turns_left[user_id] = 0

            await send_to(user_id, "🎲 Выпал дубль! Вы больше не пропускаете ход.")
            await end_turn(user_id)
            return
        
        if cmd == "quiz_answer":
            if user_states.get(user_id) != "waiting_quiz_answer":
                return

            correct_index = get_user_data(user_id).get("quiz_correct")
            correct_text = get_user_data(user_id).get("quiz_correct_text")
            chosen = int(payload.get("index"))

            player_quiz_flags[user_id]["available"] = False
            clear_user_state(user_id)

            if chosen == correct_index:
                reward = 50
                player_balance[user_id] = player_balance.get(user_id, START_MONEY) + reward
                await send_to(user_id, f"🎉 Верно! +{reward}₽")
            else:
                await send_to(user_id, f"❌ Неверно.\nПравильный ответ: {correct_text}")

            await prompt_dice(user_id)
            return
    
        if cmd == "rent_menu":
            await send_to(user_id, "💸 Рента оплачивается автоматически при попадании на чужую собственность.")
            return

        if cmd == "rent_to":
            await send_to(user_id, "💸 Рента оплачивается автоматически при попадании на чужую собственность.")
            return

        if cmd == "rent_group":
            await send_to(user_id, "💸 Рента оплачивается автоматически при попадании на чужую собственность.")
            return

        if cmd == "rent_street":
            await send_to(user_id, "💸 Рента оплачивается автоматически при попадании на чужую собственность.")
            return
        
        elif cmd == "show_inventory":
            await show_inventory(user_id)

        if cmd == "buy_landed_yes":
            flags = turn_flags.get(user_id) or {}
            tile = flags.get("landed_tile")
            if not tile or not flags.get("can_buy") or flags.get("purchase_decided"):
                await send_to(user_id, "❗ Сейчас нельзя купить.", keyboard=_turn_keyboard(user_id))
                return

            name = tile["name"]
            price = int(tile.get("price", 0))
            balance = player_balance.get(user_id, START_MONEY)
            if balance < price:
                await send_to(user_id, f"💸 Недостаточно средств для покупки ({price}₽).", keyboard=_turn_keyboard(user_id))
                flags["purchase_decided"] = True
                flags["can_buy"] = False
                flags["can_build"] = False
                flags["can_rent"] = False
                return

            player_balance[user_id] = balance - price
            player_properties.setdefault(user_id, []).append(name)
            property_owners[name] = user_id

            flags["purchase_decided"] = True
            flags["can_buy"] = False
            flags["can_build"] = bool(tile["type"] == "property" and _can_build_here(user_id, name))
            flags["can_rent"] = True
            build_hint = "\n🏗 У вас полный комплект этой группы — можно строить." if flags["can_build"] else ""
            await send_to(
                user_id,
                f"✅ Вы купили «{name}» за {price}₽.\n💰 Баланс: {player_balance[user_id]}₽{build_hint}\n\nКакие действия ещё?",
                keyboard=_turn_keyboard(user_id),
            )
            return

        if cmd == "buy_landed_no":
            flags = turn_flags.get(user_id) or {}
            tile = flags.get("landed_tile")
            if not tile or flags.get("purchase_decided"):
                await send_to(user_id, "Ок.", keyboard=_turn_keyboard(user_id))
                return
            await send_to(user_id, "❌ Вы отказались от покупки.\n\nКакие действия ещё?", keyboard=_turn_keyboard(user_id))
            flags["purchase_decided"] = True
            flags["can_buy"] = False
            flags["can_build"] = False
            flags["can_rent"] = False
            return

        await send_to(user_id, "Неизвестное действие.")
        return

    state = user_states.get(user_id)
    if state == "waiting_game_code":
        code = (message.text or "").strip()
        if code.isdigit() and len(code) == 4:
            if code in games:
                if user_id not in games[code]:
                    games[code].append(user_id)
                    player_sessions[user_id] = code
                    await ensure_player_name(user_id)

                    await send_to(user_id, f"✅ Вы присоединились к игре {code}!")

                    if len(games[code]) >= 2 and not sent_start_button.get(code):
                        await send_start_game_button(code)
                else:
                    await send_to(user_id, "Вы уже в игре.")

                if len(games[code]) < 2:
                    await send_to(user_id, "Ожидаем начала игры от хоста...")
            else:
                await send_to(user_id, "❌ Игра с таким кодом не найдена.")
        else:
            await send_to(user_id, "Введите корректный код игры (4 цифры).")
        clear_user_state(user_id)
        return

    if state == "waiting_for_amount":
        if await process_balance_amount_input(user_id, message.text or ""):
            return

    if state == "waiting_for_house_count":
        if await process_house_count_input(user_id, message.text or ""):
            return

    if state == "wait_for_dice_sum":
        if await process_dice_sum_input(user_id, message.text or ""):
            return

    if state == "waiting_for_dice":
        try:
            dice_sum = int((message.text or "").strip())
            if dice_sum < 2 or dice_sum > 12:
                raise ValueError
        except ValueError:
            await send_to(user_id, "❗ Введите число от 2 до 12.")
            return

        user_states.pop(user_id, None)
        await resolve_landing(user_id, dice_sum)
        return

    text = (message.text or "").strip()
    if state is None:
        if text == "/баланс":
            await balance_menu(user_id)
            return
        if text == "/купить":
            await send_to(user_id, "🛒 Покупка доступна только при попадании на клетку после броска кубиков.")
            return
        if text == "/собственность":
            await property_menu(user_id)
            return
        if text == "/строить":
            if not is_player_turn(user_id):
                await send_to(user_id, "⏳ Сейчас не ваш ход.")
                return
            if not (turn_flags.get(user_id) or {}).get("can_build"):
                await send_to(user_id, "❗ В этом ходу нельзя строить.", keyboard=_turn_keyboard(user_id))
                return
            await show_build_menu(user_id)
            return
        if text == "/рента":
            await send_to(user_id, "💸 Рента оплачивается автоматически при попадании на чужую собственность.")
            return
        if text == "/конец_хода":
            await end_turn(user_id)
            return
        if text == "/завершить_игру":
            await end_game(user_id)
            return

    if text == "Начать":
        await show_start_menu(user_id, user_msg=message)
        return

    await send_to(user_id, "Введите команду/нажмите кнопку. Для старта отправьте «Начать».")


bot.run_forever()