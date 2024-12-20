import telebot
from telebot import types
import requests
from langchain_community.chat_models.gigachat import GigaChat
from googleapiclient.discovery import build

# апи тг
API_TOKEN = '7837833423:AAEfuJRWqqRXAZmZH_WSMZot36f74PwZRMI'
bot = telebot.TeleBot(API_TOKEN)

#апи ютуб
api_key = 'AIzaSyBNz_fL0Kr7HeypshoI3pqXOdALo-1D4aE'
youtube = build('youtube', 'v3', developerKey=api_key)

#апи гигачад
giga = GigaChat(credentials="Y2Q1NWRhY2EtMjM0Zi00YmYzLTkwY2UtY2RjMjQ4YjA4OGYxOjBiNWMxNDI2LWU0OTQtNDk4YS1iODA1LWNhOWUyYTk1MDgzNw==",verify_ssl_certs=False)

def search_youtube(topic):
    request = youtube.search().list(
        part="snippet",
        maxResults=1,
        q=topic,
        type='video',
        order='relevance'
    )
    response = request.execute()
    return response['items'][0]['id']['videoId']

# Данные по классам, предметам и темам
data = {
    "5 класс": {
        "Математика 📐": [
            "Натуральные числа",
            "Сложение и вычитание натуральных чисел",
            "Умножение и деление натуральных чисел",
            "Порядок действий",
            "Обыкновенные дроби",
            "Десятичные дроби",
            "Проценты",
            "Геометрические фигуры (прямоугольник, квадрат)",
            "Периметр и площадь прямоугольника и квадрата",
            "Единицы измерения длины, массы, времени",
            "Решение задач на движение, работу, стоимость"
        ],
        "Русский язык 📚": [
            "Фонетика и графика",
            "Лексика и фразеология",
            "Морфемика и словообразование",
            "Грамматическая основа предложения",
            "Части речи (имя существительное, имя прилагательное, глагол)",
            "Орфография и пунктуация",
            "Развитие речи (сочинения, изложения)"
        ],
        "Литература 📖": [
            "Введение в литературу",
            "Устное народное творчество (сказки, пословицы, поговорки)",
            "Древнерусская литература",
            "Русская классическая литература XIX века (Пушкин, Лермонтов, Гоголь)",
            "Современная русская литература XX века (Чехов, Бунин, Шолохов)",
            "Зарубежная литература (Андерсен, Дефо, Свифт)",
            "Анализ литературных произведений"
        ],
        "Английский язык 🇬🇧": [
            "Алфавит и произношение",
            "Основные грамматические конструкции (Present Simple, Past Simple)",
            "Личные местоимения и формы глагола to be",
            "Вопросительные и отрицательные предложения",
            "Предлоги места и времени",
            "Модальные глаголы (can, must, should)",
            "Чтение и понимание текстов",
            "Аудирование и говорение"
        ],
        "История 📜": [
            "История Древнего мира (Древний Египет, Греция, Рим)",
            "Средневековье (крестовые походы, феодализм)",
            "Новое время (открытие Америки, Реформация)",
            "История России до XVIII века (Киевская Русь, Московское княжество)",
            "Исторические личности и события"
        ],
        "Обществознание 🏛️": [
            "Человек и общество",
            "Права и обязанности граждан",
            "Государственное устройство Российской Федерации",
            "Основы экономики (товар, деньги, рынок)",
            "Социальные группы и их взаимодействие",
            "Культура и духовные ценности общества"
        ],
        "География 🌍": [
            "Планета Земля и её оболочка",
            "Карты и атласы",
            "Материки и океаны",
            "Природные зоны Земли",
            "Население мира",
            "Страны и регионы мира",
            "Климат и погода"
        ]
    },
    "6 класс": {
        "Математика 📐 ": [
            "Делимость чисел",
            "Признаки делимости",
            "Простые и составные числа",
            "НОД и НОК",
            "Пропорции и отношения",
            "Масштаб",
            "Координатная плоскость",
            "Положительные и отрицательные числа",
            "Сравнение чисел",
            "Модуль числа",
            "Решение уравнений",
            "Геометрия: углы, треугольники, многоугольники"
        ],
        "Русский язык 📚": [
            "Повторение фонетики и графики",
            "Словоизменение и формообразование",
            "Имя существительное (падежи, склонения)",
            "Имя прилагательное (склонение, согласование)",
            "Местоимения (личные, притяжательные, указательные)",
            "Наречие",
            "Союз",
            "Частица",
            "Предлог",
            "Развитие речи (описание, рассуждение, повествование)"
        ],
        "Литература 📖": [
            "Введение в литературу",
            "Литературные жанры (эпос, лирика, драма)",
            "Поэзия (Пушкин, Лермонтов, Есенин)",
            "Проза (Гоголь, Тургенев, Чехов)",
            "Зарубежная литература (Шекспир, Диккенс, Андерсен)",
            "Анализ литературных произведений"
        ],
        "Английский язык 🇬🇧": [
            "Повседневные ситуации общения (в магазине, в школе, дома)",
            "Описание внешности и характера людей",
            "Времена года и погода",
            "Путешествия и транспорт",
            "Еда и напитки",
            "Present Continuous",
            "Past Continuous",
            "Future Simple",
            "Условные предложения (First Conditional)",
            "Артикли (a/an, the)"
        ],
        "История 📜": [
            "История средних веков (Византия, крестовые походы, Великие географические открытия)",
            "История нового времени (Реформация, Просвещение, Великая французская революция)",
            "Россия в XVI-XVII веках (Иван Грозный, Смутное время, Петр I)",
            "Исторические личности и события"
        ],
        "Обществознание 🏛️": [
            "Личность и общество",
            "Социализация личности",
            "Семья и семейные отношения",
            "Трудовая деятельность и профессия",
            "Права ребенка",
            "Экономическая жизнь общества",
            "Политическая система государства"
        ],
        "География 🌍": [
            "Атмосфера и климат",
            "Гидросфера (океаны, моря, реки, озера)",
            "Литосфера (горные породы, рельеф)",
            "Биосфера (животные и растения разных регионов)",
            "Региональная география (Европа, Азия, Африка)",
            "Население мира (этнические группы, миграция)"
        ],
        "Биология 🧬": [
            "Клетка – структурная единица организма",
            "Ткани растений и животных",
            "Органы и системы органов",
            "Питание и пищеварение у растений и животных",
            "Дыхательная система",
            "Кровеносная система",
            "Выделительная система",
            "Нервная система",
            "Опорно-двигательная система"
        ],
        "Физика 🔬": [
            "Физические величины и единицы измерения",
            "Механическое движение",
            "Скорость и ускорение",
            "Силы в природе (гравитация, трение, упругость)",
            "Законы Ньютона",
            "Работа и энергия",
            "Тепловые явления (температура, теплопередача)",
            "Агрегатные состояния вещества"
        ]
    },
    "7 класс": {
       "Алгебра 📐": [
            "Числовые выражения",
            "Буквенные выражения",
            "Уравнения первой степени",
            "Линейные неравенства",
            "Системы линейных уравнений",
            "Степень с натуральным показателем",
            "Одночлены и многочлены",
            "Формулы сокращенного умножения",
            "Разложение многочленов на множители"
        ],
        "Геометрия 📏": [
            "Начальные геометрические сведения",
            "Треугольники",
            "Параллельные прямые",
            "Сумма углов треугольника",
            "Окружность и круг",
            "Подобные треугольники",
            "Площадь треугольников и четырехугольников"
        ],
        "Русский язык 📚": [
            "Повторение изученного материала",
            "Лексика и фразеология",
            "Состав слова",
            "Имя числительное",
            "Глагол",
            "Причастие",
            "Деепричастие",
            "Наречие",
            "Предлог",
            "Союз",
            "Частица",
            "Междометие",
            "Словосочетание",
            "Простое предложение",
            "Сложное предложение"
        ],
        "Литература 📖": [
            "Литературный процесс",
            "Теория литературы",
            "Древнерусская литература",
            "Классицизм",
            "Сентиментализм",
            "Романтизм",
            "Реализм",
            "Зарубежная литература"
        ],
        "Английский язык 🇬🇧": [
            "Школьная жизнь",
            "Досуг и хобби",
            "Путешествия",
            "Здоровье и спорт",
            "Present Perfect",
            "Past Perfect",
            "Future Perfect",
            "Passive Voice",
            "Reported Speech",
            "Modal Verbs (must, have to, should)"
        ],
        "История 📜": [
            "История средних веков",
            "Эпоха Возрождения",
            "Начало Нового времени",
            "Россия в XVII веке",
            "История стран Европы и Азии в XV-XVIII веках"
        ],
        "Обществознание 🏛️": [
            "Человек и общество",
            "Экономика",
            "Политика",
            "Право",
            "Культура",
            "Социум и социальные институты"
        ],
        "География 🌍": [
            "Землеведение",
            "Атмосферная циркуляция",
            "Климатические пояса",
            "Почвы и почвенные ресурсы",
            "Минеральные ресурсы",
            "Население мира",
            "Хозяйственная деятельность человека"
        ],
        "Биология 🧬": [
            "Растения",
            "Животные",
            "Грибы",
            "Бактерии",
            "Вирусы",
            "Эволюционное учение",
            "Экологические факторы и экосистемы"
        ],
        "Физика 🔬": [
            "Механическое движение",
            "Законы сохранения импульса и энергии",
            "Работа и мощность",
            "Давление твердых тел, жидкостей и газов",
            "Архимедова сила",
            "Тепловые явления",
            "Электрический ток"
        ],
        "Химия 🧪": [
            "Введение в химию",
            "Строение атомов",
            "Периодическая таблица элементов",
            "Химические связи",
            "Валентность",
            "Закон сохранения массы веществ",
            "Типы химических реакций"
        ]
    },
    "8 класс": {
        "Алгебра 📐": [
            "Рациональные числа",
            "Квадратные корни",
            "Степень с рациональным показателем",
            "Алгебраические дроби",
            "Преобразования алгебраических выражений",
            "Уравнения второй степени",
            "Система уравнений второй степени",
            "Неравенства второй степени",
            "Прогрессии (арифметическая и геометрическая)"
        ],
        "Геометрия 📏": [
            "Четырёхугольники",
            "Многоугольники",
            "Вписанные и описанные окружности",
            "Подобие фигур",
            "Метрические соотношения в треугольнике",
            "Прямоугольный параллелепипед",
            "Объём прямоугольного параллелепипеда",
            "Куб"
        ],
        "Русский язык 📚": [
            "Синтаксис простого предложения",
            "Служебные части речи",
            "Словосочетания",
            "Сложносочинённые предложения",
            "Сложноподчинённые предложения",
            "Бессоюзные сложные предложения",
            "Предложения с разными видами связи",
            "Пунктуация в простом предложении",
            "Языковые нормы"
        ],
        "Литература 📖": [
            "Литературный процесс конца XVIII - начала XIX века",
            "Золотой век русской литературы",
            "Серебряный век русской литературы",
            "Советская литература",
            "Постсоветская литература",
            "Зарубежная литература XIX-XX веков"
        ],
        "Английский язык 🇬🇧": [
            "Будущее время (Future Tenses)",
            "Условные предложения (Second Conditional)",
            "Косвенная речь (Reported Speech)",
            "Пассивный залог (Passive Voice)",
            "Модальные глаголы (could, would, might)",
            "Артикли (the definite article, the indefinite article)",
            "Прилагательные и наречия (degrees of comparison)",
            "Герундий и инфинитив"
        ],
        "История 📜": [
            "Новая история (XVI-XVIII вв.)",
            "Просвещение и революции",
            "Наполеоновские войны",
            "Россия в XVIII-XIX веках",
            "Отмена крепостного права",
            "Первая мировая война",
            "Революции 1917 года"
        ],
        "Обществознание 🏛️": [
            "Социальная структура общества",
            "Социализация личности",
            "Молодёжь в современном обществе",
            "Этнические общности и межнациональные отношения",
            "Права и свободы человека",
            "Гражданское общество",
            "Государство и право"
        ],
        "География 🌍": [
            "Литосфера и рельеф Земли",
            "Атмосфера и климат",
            "Гидросфера",
            "Биосфера",
            "Природные зоны",
            "Географическая оболочка",
            "Экономическая география"
        ],
        "Биология 🧬": [
            "Основы цитологии",
            "Обмен веществ и превращение энергии",
            "Размножение и развитие организмов",
            "Наследственность и изменчивость",
            "Генетика",
            "Эволюционная теория",
            "Экология"
        ],
        "Физика 🔬": [
            "Законы движения Ньютона",
            "Импульс тела",
            "Энергия",
            "Законы сохранения энергии",
            "Работа и мощность",
            "Механические колебания и волны",
            "Звуковые волны",
            "Магнитное поле"
        ],
        "Химия 🧪": [
            "Валентность",
            "Типы химической связи",
            "Ковалентная связь",
            "Ионная связь",
            "Металлическая связь",
            "Водородная связь",
            "Реакции ионного обмена",
            "Окислительно-восстановительные реакции"
        ]
    },
    "9 класс": {
        "Алгебра 📐": [
            "Квадратичная функция",
            "Решение квадратных уравнений",
            "Теорема Виета",
            "Прогрессии: арифметическая и геометрическая",
            "Степень с рациональным показателем",
            "Системы линейных уравнений и неравенств",
            "Графики функций",
            "Элементы комбинаторики и теории вероятностей"
        ],
        "Геометрия 📏": [
            "Векторы в пространстве",
            "Скалярное произведение векторов",
            "Координаты вектора",
            "Метод координат в пространстве",
            "Площади многоугольников",
            "Объемы многогранников",
            "Подобные фигуры",
            "Правильные многогранники"
        ],
        "Русский язык 📚": [
            "Повторение орфографии и пунктуации",
            "Сложносочинённые предложения",
            "Сложноподчинённые предложения",
            "Бессоюзные сложные предложения",
            "Прямая и косвенная речь",
            "Лексика и фразеология",
            "Словообразование",
            "Стилистические особенности текста"
        ],
        "Литература 📖": [
            "А.С. Пушкин («Евгений Онегин», «Медный всадник»)",
            "М.Ю. Лермонтов («Герой нашего времени»)",
            "Н.В. Гоголь («Ревизор», «Мертвые души»)",
            "И.А. Бунин («Темные аллеи»)",
            "Максим Горький («На дне»)",
            "Александр Блок (лирика)"
        ],
        "Английский язык 🇬🇧": [
            "Времена глаголов (Present Perfect, Past Continuous и др.)",
            "Условные предложения (Conditionals)",
            "Модальные глаголы",
            "Диалоги и монологи на бытовые и учебные темы",
            "Написание эссе и писем",
            "Выполнение тестов по грамматике и лексике"
        ],
        "История📜": [
            "Первая мировая война",
            "Октябрьская революция 1917 года",
            "Между двумя мировыми войнами",
            "Вторая мировая война и её итоги",
            "Революция 1905–1907 годов",
            "Февральская и Октябрьская революции 1917 года",
            "Гражданская война и интервенция",
            "Советское государство в 1920-е годы"
        ],
        "Обществознание🏛️": [
            "Государство и его функции",
            "Формы правления и политические режимы",
            "Избирательная система",
            "Конституционное право",
            "Административное право",
            "Уголовное право и правонарушения",
            "Основные экономические понятия",
            "Рынок труда и безработица",
            "Инфляция и денежная политика"
        ],
        "География 🌍": [
            "Население мира",
            "Природные ресурсы и их использование",
            "Мировое хозяйство",
            "Европа",
            "Азия",
            "Северная Америка",
            "Экологические проблемы",
            "Глобализация экономики",
            "Международная торговля"
        ],
        "Биология 🧬": [
            "Строение клетки",
            "Обмен веществ и энергии в клетке",
            "Деление клеток",
            "Законы Менделя",
            "Наследственность и изменчивость",
            "Генетические карты",
            "Дарвинизм",
            "Микроэволюция и макроэволюция"
        ],
        "Физика 🔬": [
            "Импульс тела",
            "Работа и энергия",
            "Закон сохранения импульса",
            "Идеальный газ",
            "Первое начало термодинамики",
            "Тепловые машины",
            "Электрическое поле",
            "Постоянный ток",
            "Магнитное поле"
        ],
        "Химия 🧪": [
            "Периодический закон и периодическая таблица элементов",
            "Ковалентная связь",
            "Ионная связь",
            "Реакции ионного обмена",
            "Скорость химических реакций",
            "Концентрация растворов",
            "Способы выражения концентрации"
        ]
    },
    "10 класс": {
        "Алгебра и начала анализа 📐": [
            "Линейная функция",
            "Квадратичная функция",
            "Основные тригонометрические функции (синус, косинус, тангенс)",
            "Обратные тригонометрические функции",
            "Свойства степеней",
            "Арифметический корень",
            "Определение логарифма",
            "Логарифмические уравнения и неравенства",
            "Понятие производной",
            "Правила дифференцирования",
            "Первообразная и неопределенный интеграл",
            "Определенный интеграл и его свойства",
            "Основы комбинаторики",
            "Вероятность событий",
            "Предел последовательности",
            "Непрерывность функции"
        ],
        "Стереометрия 💩": [
            "Основные понятия стереометрии",
            "Аксиомы стереометрии и основные теоремы",
            "Параллельность прямых и плоскостей",
            "Перпендикулярность прямой и плоскости",
            "Перпендикулярность плоскостей",
            "Взаимное расположение прямых и плоскостей в пространстве",
            "Многогранники",
            "Призма",
            "Пирамида",
            "Вписанные и описанные тела"
        ],
        "Русский язык 📚": [
            "Лексическое значение слова",
            "Омонимы, синонимы, антонимы",
            "Звуковые особенности русского языка",
            "Слоговая структура слова",
            "Морфемы и их типы",
            "Способы образования новых слов",
            "Простое предложение",
            "Сложное предложение",
            "Правописание гласных и согласных",
            "Знаки препинания в сложном предложении",
            "Нормы современного русского литературного языка",
            "Стилистическая окраска слов"
        ],
        "Литература 📖": [
            "Творчество Пушкина, Лермонтова, Гоголя",
            "Романы Достоевского и Толстого",
            "Поэзия Серебряного века (Блок, Ахматова, Маяковский)",
            "Проза Бунина, Куприна, Горького",
            "Произведения Шолохова, Булгакова, Солженицына",
            "Постмодернизм в литературе (Сорокин, Пелевин)",
            "Тематика и проблематика произведений",
            "Художественные средства выразительности"
        ],
        "Английский язык 🇬🇧": [
            "Времена глаголов (Present Perfect, Past Continuous)",
            "Модальные глаголы",
            "Чтение адаптированных текстов",
            "Извлечение основной информации из текста",
            "Диалоги и монологи на заданную тему",
            "Участие в дискуссиях",
            "Написание эссе и писем",
            "Оформление деловых документов",
            "Прослушивание аудиоматериалов",
            "Восприятие устной речи носителей языка"
        ],
        "История 📜": [
            "Реформация и Контрреформация",
            "Первая мировая война",
            "Октябрьская революция и Гражданская война в России",
            "Вторая мировая война и её последствия",
            "Холодная война и распад СССР"
        ],
        "Обществознание 🏛️": [
            "Социальная структура общества",
            "Роль личности в истории",
            "Семья и брак",
            "Образование и наука",
            "Государство и его функции",
            "Политические партии и движения",
            "Конституционное право",
            "Уголовное право",
            "Рыночная экономика",
            "Трудовые отношения"
        ],
        "География 🌍": [
            "Литосфера и рельеф Земли",
            "Гидросфера и климатические пояса",
            "Этнический состав населения",
            "Миграции и урбанизация",
            "Минеральные ресурсы",
            "Водные и лесные ресурсы",
            "Евразия",
            "Северная Америка",
            "Экологические проблемы",
            "Проблемы устойчивого развития"
        ],
        "Биология 🧬": [
            "Строение клетки",
            "Метаболизм клеток",
            "Законы Менделя",
            "Генотип и фенотип",
            "Теория эволюции Дарвина",
            "Видообразование",
            "Взаимодействие организмов в экосистемах",
            "Антропогенное воздействие на природу",
            "Опорно-двигательная система",
            "Кровеносная и лимфатическая системы"
        ],
        "Физика 🔬": [
            "Динамика",
            "Закон сохранения импульса",
            "Идеальный газ",
            "Первый закон термодинамики",
            "Электрическое поле",
            "Магнитное поле",
            "Геометрическая оптика",
            "Волновая оптика",
            "Фотоны и фотоэффект",
            "Корпускулярно-волновой дуализм"
        ],
        "Химия 🧪": [
            "Электронные оболочки",
            "Периодический закон Менделеева",
            "Ковалентная связь",
            "Ионная связь",
            "Концентрация растворов",
            "Коллоидные системы",
            "Электролиты и неэлектролиты",
            "Скорость химических реакций",
            "Углеводороды",
            "Функциональные группы органических соединений"
        ],
        "Информатика 💻": [
            "Базовые алгоритмы сортировки и поиска",
            "Языки программирования высокого уровня (Python, C++)",
            "Компьютерные сети",
            "Интернет-технологии",
            "Информационные модели",
            "СУБД и SQL-запросы",
            "Шифрование данных",
            "Защита от вирусов и хакерских атак",
            "Нейронные сети и машинное обучение",
            "Применение ИИ в различных областях"
        ],
        "Экономика 📊": [
            "Предложение и спрос",
            "Эластичность спроса и предложения",
            "Валовый внутренний продукт (ВВП)",
            "Инфляция и безработица",
            "Фондовый рынок",
            "Банковская система",
            "Внешняя торговля",
            "Международные экономические организации",
            "Налогово-бюджетная политика",
            "Монетарная политика Центрального банка"
        ],
        "Право ⚖️": [
            "Конституция Российской Федерации",
            "Права и свободы граждан",
            "Договорные обязательства",
            "Наследственное право",
            "Преступления против личности",
            "Наказания за преступления",
            "Административные правонарушения",
            "Ответственность за административные проступки",
            "Трудовой договор",
            "Охрана труда"
        ]
    },
    "11 класс": {
        "Алгебра и начала анализа📐": [
            "Функции и их свойства",
            "Производная функции",
            "Интегралы",
            "Показательная и логарифмическая функции",
            "Тригонометрические функции",
            "Ряды и последовательности",
            "Комбинаторика и вероятность",
            "Комплексные числа"
        ],
        "Стереометрия 💩": [
           "Прямые и плоскости в пространстве",
            "Углы между прямыми и плоскостями",
            "Расстояния в пространстве",
            "Объём и площадь поверхности многогранников",
            "Цилиндр",
            "Конус",
            "Сфера и шар",
            "Сечения многогранников и тел вращения",
            "Вписанные и описанные тела",
            "Координатный метод в стереометрии",
            "Векторы в пространстве",
            "Применение стереометрии в задачах на построение и доказательство"
        ],
        "Русский язык 📚": [
            "Синтаксис и пунктуация",
            "Орфография",
            "Морфология",
            "Функциональные стили",
            "Тексты и работа с информацией",
            "Подготовка к ЕГЭ"
        ],
        "Литература 📖": [
            "Русская литература XIX века",
            "Литература второй половины XIX века",
            "Серебряный век русской литературы",
            "Русская литература XX века",
            "Зарубежная литература",
            "Анализ художественного текста"
        ],
        "Английский язык 🇬🇧": [
            "Грамматика",
            "Лексика",
            "Чтение и перевод текстов",
            "Письменная речь",
            "Аудирование и говорение",
            "Подготовка к ЕГЭ"
        ],
        "История 📜": [
            "История России XX века",
            "Мировая история XX века",
            "История России XXI века",
            "Тенденции развития мировой цивилизации",
            "Подготовка к ЕГЭ"
        ],
        "Обществознание🏛️": [
            "Человек и общество",
            "Социальные отношения",
            "Экономика",
            "Политика и право",
            "Мировая политика и глобализация",
            "Подготовка к ЕГЭ"
        ],
        "Физика 🔬": [
            "Электродинамика",
            "Квантовая физика",
            "Оптика",
            "Элементы теории относительности",
            "Атомная и ядерная физика",
            "Подготовка к ЕГЭ"
        ],
        "Химия 🧪": [
            "Органическая химия",
            "Химия живых систем",
            "Общая химия",
            "Металлы и неметаллы",
            "Подготовка к ЕГЭ"
        ],
        "Информатика 💻": [
            "Основы программирования",
            "Компьютерные сети",
            "Базы данных",
            "Моделирование и анализ данных",
            "Подготовка к ЕГЭ"
        ],
        "Экономика 📊": [
            "Основы рыночной экономики",
            "Финансовая система",
            "Экономическая политика государства",
            "Международная экономика",
            "Роль России в мировой экономике"
        ],
        "Право ⚖️": [
            "Конституционное право",
            "Гражданское право",
            "Административное и уголовное право",
            "Трудовое право",
            "Международное право",
            "Подготовка к ЕГЭ"
        ]
    }
}


selected_grade = None  
#старт+генерация кнопок классов
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for grade in data.keys():
        markup.add(types.KeyboardButton(grade))
    bot.send_message(message.chat.id, "Выбери класс:", reply_markup=markup)
    
#обработка выбора класса + генерация кнопок предметов
@bot.message_handler(func=lambda message: message.text in data.keys())
def select_subject(message):
    global selected_grade
    selected_grade = message.text  # Устанавливаем класс
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in data[selected_grade].keys():
        markup.add(types.KeyboardButton(subject))
    markup.add(types.KeyboardButton("⏮️ На главную ⏮️"))
    bot.send_message(message.chat.id, f"Ты выбрал {selected_grade}. Теперь выбери предмет:", reply_markup=markup)

@bot.message_handler(func=lambda message: selected_grade and message.text in data[selected_grade].keys())
def select_topic(message):
    global selected_grade
    selected_subject = message.text
    
    if selected_grade and selected_subject in data[selected_grade]:
        topics = data[selected_grade][selected_subject]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for topic in topics:
            markup.add(types.KeyboardButton(topic))
        markup.add(types.KeyboardButton("⏮️ На главную ⏮️"))
        bot.send_message(message.chat.id, f"Ты выбрал {selected_subject}. Теперь выбери тему:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, начни сначала командой /start")

@bot.message_handler(func=lambda message: selected_grade and any(message.text in topics for topics in data[selected_grade].values()))
def show_topic_content(message):
    global selected_grade
    selected_topic = message.text
    selected_subject = None
    
    # Находим выбранный предмет
    for subject, topics in data[selected_grade].items():
        if selected_topic in topics:
            selected_subject = subject
            break

    if selected_subject:
        mess = giga.invoke(f"Дай сведения по теме {selected_topic} предмета {selected_subject} для ученика {selected_grade} класса. Ответ не более 100 слов и без приветствий")
        tasks = giga.invoke(f"Придумай 3 задания по теме {selected_topic} предмета {selected_subject} для ученика {selected_grade} класса для проработки материала. Без приветсвий, просто задания. После каждого задания на следующей строчке дай правильный ответ на него, выделив его звездочками с каждой стороны")
        video_id = search_youtube(selected_topic + " " + selected_grade + " класс")
        bot.send_message(message.chat.id, f"Ты выбрал тему: {selected_topic}. Вот материал для изучения этой темы: https://www.youtube.com/watch?v={video_id}")
        bot.send_message(message.chat.id,mess.content)
        bot.send_message(message.chat.id,tasks.content)
    else:
        bot.send_message(message.chat.id, "Тема не найдена. Пожалуйста, начни сначала командой /start")
    
@bot.message_handler(func=lambda message: message.text == "⏮️ На главную ⏮️")
def go_back(message):
    send_welcome(message)
# работает бесконечно(вроде)
bot.polling(none_stop=True)
