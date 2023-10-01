study_groups = {
    '12': 'М3О-312Б-21',
    '14': 'М3О-314Б-21',
    '21': 'М3О-321Б-21',
}
c1 = "Констр и Арх+МК (1, 2)"
c2 = "DataSc и Надежность (3, 4)"
c3 = "Арх+МК и DataSc (2, 3)"
c4 = "Констр и Надежность (1, 4)"
fullC1 = "Технология производства средств информационно-вычислительной техники и Микроконтроллеры"
fullC2 = "Информационная теория оценок и Надежность информационных систем"
fullC3 = "Микроконтроллеры и Информационная теория оценок"
fullC4 = "Технология производства средств информационно-вычислительной техники и Надежность информационных систем"

bOptions = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "label": "На сегодня",
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "На завтра",
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Расписание до конца недели",
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Расписание на следующую неделю",
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Расписание в определенный день",
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Расписание в определенную неделю",
                },
                "color": "primary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": "Сменить группу",
                },
                "color": "secondary"
            },
            {
                "action": {
                    "type": "text",
                    "label": "Сменить цепочки",
                },
                "color": "secondary"
            }
        ],
    ],
}

bChains = {
    "inline": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "label": c1,
                },
                "color": "secondary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": c2,
                },
                "color": "secondary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": c3,
                },
                "color": "secondary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": c4,
                },
                "color": "secondary"
            }
        ],
    ]
}
bGroups = {
    "inline": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "label": study_groups['12'],
                },
                "color": "secondary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": study_groups['14'],
                },
                "color": "secondary"
            }
        ],
        [
            {
                "action": {
                    "type": "text",
                    "label": study_groups['21'],
                },
                "color": "secondary"
            }
        ],
    ]
}

bExit = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "label": "в главное меню",
                },
                "color": "primary"
            }
        ],
    ]
}

return_codes = {
    201: 'Created - Создано',
    202: 'Accepted - Принято',
    203: 'Non-Authoritative Information - Неавторитетная информация',
    204: 'No Content - Нет контента',
    205: 'Reset Content - Сброшенное содержимое',
    206: 'Partial Content - Частичное содержимое',
    300: 'Multiple Choices - Несколько вариантов',
    301: 'Moved Permanently - Перемещено навсегда',
    302: 'Found - Найдено',
    303: 'See Other - Смотрите другое',
    304: 'Not Modified - Не изменен',
    305: 'Use Proxy - Используйте прокси',
    307: 'Temporary Redirect - Временный редирект',
    308: 'Permanent Redirect - Постоянное перенаправление (experimental)',
    400: 'Bad Request - Плохой запрос',
    401: 'Unauthorized - Неавторизован',
    402: 'Payment Required - Требуется оплата',
    403: 'Forbidden - Запрещено',
    404: 'Not Found - Не найдено',
    405: 'Method Not Allowed - Метод не разрешен',
    406: 'Not Acceptable - Неприемлемый',
    407: 'Proxy Authentication Required - Требуется прокси-аутентификация',
    408: 'Request Timeout - Таймаут запроса',
    409: 'Conflict - Конфликт',
    410: 'Gone - Исчез',
    411: 'Length Required - Требуется длина',
    412: 'Precondition Failed - Предварительное условие не выполнено',
    413: 'Request Entity Too Large - Сущность запроса слишком большая',
    414: 'Request-URI Too Long - Запрос-URI Слишком длинный',
    415: 'Unsupported Media Type - Неподдерживаемый медиа тип',
    428: 'Precondition Required - Требуется предварительное условие',
    429: 'Too Many Requests - Слишком много запросов',
    431: 'Request Header Fields Too Large - Слишком большие поля заголовка запроса',
    444: 'No Response - Нет ответа (Nginx)',
    451: 'Unavailable For Legal Reasons - Недоступен по юридическим причинам',
    500: 'Internal Server Error - Внутренняя ошибка сервера',
    501: 'Not Implemented - Не реализован',
    502: 'Bad Gateway - Плохой шлюз',
    503: 'Service Unavailable - Служба недоступна',
    504: 'Gateway Timeout - Таймаут шлюза',
    505: 'HTTP Version Not Supported - Версия HTTP не поддерживается',
    510: 'Not Extended - Не расширен',
}

daysInMonths = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}
monthName_to_No = {
    'января': 1,
    'январь': 1,
    'февраля': 2,
    'февраль': 2,
    'марта': 3,
    'март': 3,
    'апреля': 4,
    'апрел': 4,
    'мая': 5,
    'май': 5,
    'июня': 6,
    'июнь': 6,
    'июля': 7,
    'июль': 7,
    'августа': 8,
    'август': 8,
    'сентября': 9,
    'сентябрб': 9,
    'октября': 10,
    'октябрь': 10,
    'ноября': 11,
    'ноябрь': 11,
    'декабря': 12,
    'декабрь': 12,
}
time_to_pairNo = {
    '09': '1',
    '10': '2',
    '13': '3',
    '14': '4',
    '16': '5',
    '18': '6',
}

greetings = [
    "привет",
    "добрый день",
    "доброго дня",
    "добрый вечер",
    "доброе утро",
    "доброго вечера",
    "доброго утра",
    "доброго утреца",
    "доброй ночи",
    "доброго времени суток",
    "хаюхай",
    "хай",
    "здарова",
    "здорова",
    "здаров",
    "здоров",
    "здравствуй",
    "здравствуйте",
    "здраствуй",
    "здраствуйте",
    "здрасте",
    "вечер в хату",
    "салют",
    "мое почтение",
    "здравия желаю",
    "ку",
]

gratitudes = [
    "спасибо",
    "от души",
    "благодар",
    "должник",
    "признател",
]

response_to_gratitude = [
    "Пожалуйста!",
    "Всегда пожалуйста",
    "Обращайся!",
    "На здоровье!",
    "Рад стараться!",
    "Бро, все ради тебя <3",
]

swearings = [
    "гандон",
    "сука",
    "сучка",
    "пидарас",
    "пидорас",
    "пидор",
    "пидр",
    "урод",
    "придурок",
    "дибил",
    "дебил",
    "дэбил",
    "лох",
    "дурак",
    "глупый",
    "тупой",
    "тварь",
]

farewell = [
    "пока",
    "до скорого",
    "спокойной ночи",
    "доброй ночи",
    "до свидания",
    "увидимся",
    "давай тогда",
    "прощай",
]