#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Сборка сайта-портфолио Вероники Ким.

Запуск:  python3 build.py
Результат: папка site/ (обычные HTML-файлы, можно выложить на любой хостинг).

Фото: положите файлы в site/photos/<галерея>/ (jpg, jpeg, png, webp) и
запустите сборку ещё раз. Пока папка пуста, показываются заглушки.
Файлы с именем stock-*.jpg: временные фото из интернета (Unsplash), на
сайте они помечены значком «сток». Перед публикацией замените своими.
Названия галерей: home, portrait, love-story, family, pregnancy, kids,
mountains, underwater, architecture, thirst, film, travel, editorial,
prints, about.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")
LANGS = ["ru", "kz", "en"]
HTML_LANG = {"ru": "ru", "kz": "kk", "en": "en"}

# ── Настройки ────────────────────────────────────────────────────────────
INSTAGRAM = "nananika.photographer"
TIKTOK = "nananika.photographer"
WHATSAPP = ""  # номер в формате 77001234567; пока пусто, кнопка WhatsApp скрыта
# Сезонный баннер на главной. Чтобы убрать, поставьте SHOW_BANNER = False.
SHOW_BANNER = True

# Адрес сайта в интернете: нужен для поисковиков (canonical, sitemap, превью ссылок)
SITE_URL = "https://nananika.vercel.app"
# Коды подтверждения из Google Search Console и Яндекс Вебмастера (вставить, когда будут)
GOOGLE_VERIFY = ""
YANDEX_VERIFY = ""

IG_DM = "https://ig.me/m/" + INSTAGRAM
IG_URL = "https://www.instagram.com/" + INSTAGRAM + "/"
TT_URL = "https://www.tiktok.com/@" + TIKTOK


import time
VER = str(int(time.time()))  # метка сборки: телефон не берёт старые стили и скрипты из кэша


def L(ru, kz, en):
    return {"ru": ru, "kz": kz, "en": en}


# ── Общие строки ─────────────────────────────────────────────────────────
S = {
    "name": L("Veronika Kim", "Veronika Kim", "Veronika Kim"),
    "name1": L("Veronika", "Veronika", "Veronika"),
    "name2": L("Kim", "Kim", "Kim"),
    "role": L("Фотограф. Алматы, Астана", "Фотограф. Алматы, Астана", "Photographer. Almaty, Astana"),
    "desc": L(
        "Вероника Ким, фотограф из Алматы: авторские портреты, чёрно-белая плёнка и ручная печать, съёмки в горах с дроном и под водой.",
        "Вероника Ким, алматылық фотограф: авторлық портреттер, ақ-қара таспа және қолмен басу, тауда дронмен және су астында түсірілім.",
        "Veronika Kim, a photographer based in Almaty: art portraits, black-and-white film and hand printing, mountain shoots with a drone, underwater photography."),
    "seo_home": L(
        "Veronika Kim (Вероника Ким) — фотограф в Алматы и Астане",
        "Veronika Kim (Вероника Ким) — Алматы мен Астанадағы фотограф",
        "Veronika Kim — photographer in Almaty and Astana, Kazakhstan"),
    "seo_suffix": L(" · Veronika Kim, фотограф в Алматы", " · Veronika Kim, Алматыдағы фотограф",
                    " · Veronika Kim, photographer in Almaty"),
    "seo_sign": L("Вероника Ким (Veronika Kim), фотограф: Алматы, Астана, выездные съёмки.",
                  "Вероника Ким (Veronika Kim), фотограф: Алматы, Астана, көшпелі түсірілімдер.",
                  "Veronika Kim, photographer: Almaty, Astana and on location."),
    "menu": L("Меню", "Мәзір", "Menu"),
    "close": L("Закрыть", "Жабу", "Close"),
    "home": L("Главная", "Басты бет", "Home"),
    "book": L("Заказать съёмку", "Түсірілімге жазылу", "Book a shoot"),
    "arch": L("Архитектура и дрон", "Сәулет және дрон", "Architecture & drone"),
    "art": L("Авторское", "Авторлық", "Personal work"),
    "shop": L("Магазин", "Дүкен", "Shop"),
    "about": L("Обо мне", "Мен туралы", "About"),
    "contacts": L("Контакты", "Байланыс", "Contact"),
    "all": L("Смотреть все", "Барлығын көру", "View all"),
    "included": L("Что входит", "Не кіреді", "What's included"),
    "price": L("Стоимость", "Бағасы", "Pricing"),
    "price_text": L("Стоимость по запросу", "Бағасы сұраныс бойынша", "Pricing on request"),
    "price_note": L(
        "Напишите мне в директ: расскажу о стоимости, свободных датах и помогу выбрать формат. Отвечаю сама.",
        "Директке жазыңыз: бағасын, бос күндерді айтып, форматты таңдауға көмектесемін. Өзім жауап беремін.",
        "Message me on Instagram: I'll share pricing and open dates and help you pick a format. I reply personally."),
    "ask": L("Узнать стоимость", "Бағасын білу", "Ask for pricing"),
    "order": L("Заказать", "Тапсырыс беру", "Order"),
    "write_ig": L("Написать в Instagram", "Instagram-ға жазу", "Message on Instagram"),
    "write_wa": L("Написать в WhatsApp", "WhatsApp-қа жазу", "Message on WhatsApp"),
    "more": L("Другие съёмки", "Басқа түсірілімдер", "Other shoots"),
    "more_art": L("Другие проекты", "Басқа жобалар", "Other projects"),
    "terms": L("Условия", "Шарттар", "Terms"),
    "where": L("Где", "Қайда", "Where"),
    "where_text": L("Алматы, Астана и выездные съёмки", "Алматы, Астана және көшпелі түсірілімдер", "Almaty, Astana and on location"),
    "booking": L("Запись", "Жазылу", "Booking"),
    "social": L("Соцсети", "Әлеуметтік желілер", "Social"),
    "soon": L("Скоро", "Жақында", "Soon"),
    "prev": L("Назад", "Артқа", "Prev"),
    "next": L("Вперёд", "Алға", "Next"),
    "rights": L("Все права защищены", "Барлық құқықтар қорғалған", "All rights reserved"),
    "top": L("Наверх", "Жоғарыға", "Back to top"),
    "statement": L(
        "Человек приносит свою личность. <em>Я создаю из неё искусство.</em>",
        "Адам өз тұлғасын алып келеді. <em>Мен одан өнер жасаймын.</em>",
        "You bring who you are. <em>I turn it into art.</em>"),
    "intro": L(
        "Авторские портреты, чёрно-белая плёнка и ручная печать в собственной проявочной, съёмки в горах с дроном и под водой.",
        "Авторлық портреттер, ақ-қара таспа және өз зертханамда қолмен басу, тауда дронмен және су астында түсірілім.",
        "Art portraits, black-and-white film hand-printed in my own darkroom, mountain shoots with a drone and underwater photography."),
    "banner_label": L("Сезонная съёмка", "Маусымдық түсірілім", "Seasonal"),
    "banner_title": L("Новогодний детский проект", "Жаңа жылдық балалар жобасы", "New Year kids' project"),
    "banner_text": L("13 и 20 декабря · Studio 73, зал Sharm · Алматы",
                     "13 және 20 желтоқсан · Studio 73, Sharm залы · Алматы",
                     "13 & 20 December · Studio 73, Sharm hall · Almaty"),
    "banner_cta": L("Записаться", "Жазылу", "Book a slot"),
}

TERMS = L(
    ["Предоплата 30% закрепляет дату", "Аренда студии оплачивается отдельно",
     "Фото готовы через 7–10 дней, видео через 14", "Все кадры в цветокоррекции, JPEG. Исходники не передаются",
     "Перенос возможен. При отмене менее чем за сутки предоплата не возвращается, если студию нельзя отменить",
     "Выезд в другие города: билеты и проживание за счёт клиента", "Визажиста и стилиста я не предоставляю"],
    ["30% алдын ала төлем күнді бекітеді", "Студия жалдау бөлек төленеді",
     "Фото 7–10 күнде, видео 14 күнде дайын болады", "Барлық кадрлар түс түзетуінен өтеді, JPEG. Бастапқы файлдар берілмейді",
     "Күнді ауыстыруға болады. Бір тәуліктен аз уақыт қалғанда бас тартсаңыз және студиядан бас тарту мүмкін болмаса, алдын ала төлем қайтарылмайды",
     "Басқа қалаларға шығу: билет пен тұру клиент есебінен", "Визажист пен стилист қызметін ұсынбаймын"],
    ["A 30% deposit secures the date", "Studio rental is paid separately",
     "Photos are ready in 7–10 days, video in 14", "Every frame is colour-graded, JPEG. RAW files are not provided",
     "Rescheduling is fine. If you cancel less than 24 hours ahead and the studio can't be refunded, the deposit is kept",
     "Other cities: travel and accommodation are covered by the client", "Make-up artist and stylist are not included"])

# ── Съёмки на заказ ──────────────────────────────────────────────────────
SERVICES = [
    {"slug": "portrait", "g": "portrait",
     "title": L("Портрет", "Портрет", "Portrait"),
     "lead": L("Индивидуальная съёмка: женский, мужской и деловой портрет. В студии или в городе.",
               "Жеке түсірілім: әйел, ер адам және іскерлік портрет. Студияда немесе қалада.",
               "A one-to-one session: women's, men's and business portraits. In the studio or in the city."),
     "facts": L(["1 час съёмки", "15 кадров в ретуши", "Фото и короткое видео", "Все удачные кадры в цветокоррекции"],
                ["1 сағат түсірілім", "15 кадр ретушьпен", "Фото және қысқа видео", "Барлық сәтті кадрлар түс түзетуімен"],
                ["1 hour of shooting", "15 retouched frames", "Photos and a short video", "All selected frames colour-graded"])},
    {"slug": "love-story", "g": "love-story",
     "title": L("Love story", "Love story", "Love story"),
     "lead": L("Съёмка для двоих: прогулка, город, горы или студия. Помогу с образом и подберу локацию.",
               "Екеуге арналған түсірілім: серуен, қала, тау немесе студия. Образ бен локация таңдауға көмектесемін.",
               "A session for two: a walk, the city, the mountains or a studio. I help with styling and location."),
     "facts": L(["1–1,5 часа", "До 2 локаций", "20–25 кадров в ретуши", "Все кадры в цветокоррекции", "Помощь с образом и локацией"],
                ["1–1,5 сағат", "2 локацияға дейін", "20–25 кадр ретушьпен", "Барлық кадрлар түс түзетуімен", "Образ бен локацияға көмек"],
                ["1–1.5 hours", "Up to 2 locations", "20–25 retouched frames", "All frames colour-graded", "Help with styling and location"])},
    {"slug": "family", "g": "family",
     "title": L("Семья", "Отбасы", "Family"),
     "lead": L("Камерная семейная съёмка до пяти человек, без суеты и заученных поз.",
               "Бес адамға дейінгі жайлы отбасылық түсірілім, асығыссыз және жаттанды позаларсыз.",
               "An intimate family session for up to five people, unhurried and without stock poses."),
     "facts": L(["1,5 часа", "25 кадров в ретуши", "До 5 человек, больше по договорённости"],
                ["1,5 сағат", "25 кадр ретушьпен", "5 адамға дейін, одан көп болса келісім бойынша"],
                ["1.5 hours", "25 retouched frames", "Up to 5 people, more by arrangement"])},
    {"slug": "pregnancy", "g": "pregnancy",
     "title": L("Беременность", "Жүктілік", "Maternity"),
     "lead": L("Съёмка в ожидании: спокойный темп, несколько образов, студия или натура.",
               "Сәби күту кезеңіндегі түсірілім: сабырлы қарқын, бірнеше образ, студия немесе табиғат.",
               "A maternity session at a calm pace, with several looks, in the studio or outdoors."),
     "facts": L(["1 час: 2 образа, 10 кадров в ретуши", "2 часа: 4 образа, 20 кадров в ретуши"],
                ["1 сағат: 2 образ, 10 кадр ретушьпен", "2 сағат: 4 образ, 20 кадр ретушьпен"],
                ["1 hour: 2 looks, 10 retouched frames", "2 hours: 4 looks, 20 retouched frames"])},
    {"slug": "kids", "g": "kids",
     "title": L("Дети", "Балалар", "Children"),
     "lead": L("Новорождённые, малыши до года и детские проекты. Формат подбираем под возраст и характер ребёнка.",
               "Жаңа туған сәбилер, бір жасқа дейінгі бөбектер және балалар жобалары. Форматты баланың жасы мен мінезіне қарай таңдаймыз.",
               "Newborns, babies under one and children's projects. The format is shaped around the child's age and temperament."),
     "facts": L(["Ньюборн в студии", "Лайфстайл с новорождённым дома", "Малыши 3–12 месяцев", "Сезонные детские проекты"],
                ["Студиядағы ньюборн", "Үйдегі жаңа туған сәбимен лайфстайл", "3–12 айлық бөбектер", "Маусымдық балалар жобалары"],
                ["Newborn in the studio", "Lifestyle with a newborn at home", "Babies 3–12 months", "Seasonal children's projects"])},
    {"slug": "mountains", "g": "mountains",
     "title": L("Горы с дроном", "Таудағы дрон", "Mountains & drone"),
     "lead": L("Прогулка в горах Алматы: фото и видео с дрона, от одного до пяти человек.",
               "Алматы тауларындағы серуен: дроннан фото мен видео, бір адамнан бес адамға дейін.",
               "A walk in the mountains above Almaty: drone photos and video for one to five people."),
     "facts": L(["Медеу и Шымбулак, Ой-Карагай по запросу", "Фото и видео с дрона", "1–5 человек",
                 "Съёмка до 16:00, пока хороший свет", "Бесплатный перенос из-за погоды", "Подскажу, что надеть"],
                ["Медеу мен Шымбұлақ, Ой-Қарағай сұраныс бойынша", "Дроннан фото мен видео", "1–5 адам",
                 "Жарық жақсы кезде, 16:00-ге дейін", "Ауа райына байланысты тегін ауыстыру", "Не кию керегін айтамын"],
                ["Medeu and Shymbulak, Oi-Qaragai on request", "Drone photos and video", "1–5 people",
                 "Shooting before 4 pm while the light is good", "Free rescheduling for bad weather", "Advice on what to wear"])},
    {"slug": "underwater", "g": "underwater",
     "title": L("Под водой", "Су астында", "Underwater"),
     "lead": L("Люди и подводный мир. Снимаю в поездках: Египет, Вьетнам, Таиланд.",
               "Адамдар және су асты әлемі. Сапарларда түсіремін: Мысыр, Вьетнам, Таиланд.",
               "People and the underwater world. I shoot on trips: Egypt, Vietnam, Thailand."),
     "facts": L(["Портреты и съёмка в движении под водой", "Подводный мир: рифы и их жители", "Даты привязаны к моим поездкам, пишите заранее"],
                ["Су астындағы портрет пен қозғалыстағы түсірілім", "Су асты әлемі: рифтер мен олардың тұрғындары", "Күндер сапарларыма байланысты, алдын ала жазыңыз"],
                ["Portraits and movement underwater", "The underwater world: reefs and their inhabitants", "Dates follow my trips, so write in advance"])},
]

ARCH = {
    "title": L("Архитектура и дрон", "Сәулет және дрон", "Architecture & drone"),
    "lead": L("Архитектура, интерьеры и объекты с воздуха. Для архитекторов, дизайнеров, отелей и застройщиков.",
              "Сәулет, интерьер және нысандарды әуеден түсіру. Сәулетшілерге, дизайнерлерге, қонақүйлер мен құрылыс компанияларына.",
              "Architecture, interiors and aerial views of sites. For architects, designers, hotels and developers."),
    "facts": L(["Экстерьеры и интерьеры", "Съёмка объектов с дрона: фото и видео", "От 2 часов съёмки", "Лицензирование кадров"],
               ["Экстерьер мен интерьер", "Нысандарды дронмен түсіру: фото мен видео", "2 сағаттан бастап", "Кадрларды лицензиялау"],
               ["Exteriors and interiors", "Aerial photo and video of sites", "From 2 hours of shooting", "Image licensing"]),
}

# ── Авторское ────────────────────────────────────────────────────────────
ART = [
    {"slug": "thirst-for-life", "g": "thirst",
     "title": L("Жажда жизни", "Өмірге құштарлық", "Thirst for Life"),
     "lead": L("Постановочный чёрно-белый проект с манекенами. Снят на плёнку.",
               "Манекендермен қойылған ақ-қара жоба. Таспаға түсірілген.",
               "A staged black-and-white project with mannequins. Shot on film."),
     "body": L(["Проект целиком снят на среднеформатную плёнку и проявлен вручную. Для меня это принципиально: плёнка не даёт спрятаться за количеством кадров.",
                "Серия опубликована на PhMuseum."],
               ["Жоба толығымен орта форматты таспаға түсіріліп, қолмен өңделген. Бұл мен үшін маңызды: таспа кадр санының артына тығылуға мүмкіндік бермейді.",
                "Серия PhMuseum платформасында жарияланған."],
               ["The whole project was shot on medium-format film and developed by hand. That matters to me: film leaves no room to hide behind the number of frames.",
                "The series is published on PhMuseum."])},
    {"slug": "film-darkroom", "g": "film",
     "title": L("Плёнка и даркрум", "Таспа және қараңғы бөлме", "Film & darkroom"),
     "lead": L("Чёрно-белый средний формат: Rolleiflex и Mamiya. Проявляю и печатаю сама, в собственной проявочной.",
               "Ақ-қара орта формат: Rolleiflex және Mamiya. Өз зертханамда өзім өңдеп, өзім басамын.",
               "Black-and-white medium format: Rolleiflex and Mamiya. I develop and print everything myself in my own darkroom."),
     "body": L(["Плёночный портрет: съёмка на ч/б плёнку 120, ручная проявка, сканы и серебряно-желатиновый отпечаток 30×40.",
                "Услуги проявочной: проявка плёнки 120 и ручная печать с ваших негативов."],
               ["Таспалы портрет: 120 ақ-қара таспаға түсіру, қолмен өңдеу, скандар және 30×40 күміс-желатинді басылым.",
                "Зертхана қызметтері: 120 таспаны өңдеу және сіздің негативтеріңізден қолмен басу."],
               ["Film portrait: shot on 120 black-and-white film, hand-developed, scanned and printed as a 30×40 silver gelatin print.",
                "Darkroom services: 120 film developing and hand printing from your negatives."])},
    {"slug": "editorial", "g": "editorial",
     "title": L("Авторский портрет", "Авторлық портрет", "Art portrait"),
     "lead": L("«Искусство видеть человека иначе». Не фотосессия, а работа, выросшая из личности человека.",
               "«Адамды басқаша көру өнері». Бұл фотосессия емес, адамның тұлғасынан туған жұмыс.",
               "“The art of seeing a person differently.” Not a photo session but a work that grows out of who you are."),
     "steps": L(["Личное письмо-приглашение", "Разговор о вас: что вами движет, что вы прячете и чем гордитесь",
                 "Я готовлю реквизит, фактуры и свет", "Творческая съёмка без готовых образов и шаблонных поз",
                 "Авторская работа. Результат заранее не известен никому"],
                ["Жеке шақыру хаты", "Сіз туралы әңгіме: сізді не жетелейді, нені жасырасыз, немен мақтанасыз",
                 "Мен реквизит, фактура және жарық дайындаймын", "Дайын образдарсыз және жаттанды позаларсыз шығармашылық түсірілім",
                 "Авторлық жұмыс. Нәтижесін алдын ала ешкім білмейді"],
                ["A personal letter of invitation", "A conversation about you: what drives you, what you hide, what you're proud of",
                 "I prepare props, textures and light", "A creative shoot with no ready-made looks or stock poses",
                 "An authored work. Nobody knows the result in advance"])},
    {"slug": "travel", "g": "travel",
     "title": L("Travel", "Саяхат", "Travel"),
     "lead": L("Кадры из поездок: люди, свет и места, к которым хочется вернуться.",
               "Сапарлардан кадрлар: адамдар, жарық және қайта оралғың келетін жерлер.",
               "Frames from the road: people, light and places worth returning to."),
     "body": L(["Отдельные кадры доступны для лицензирования и как принты для интерьера."],
               ["Жекелеген кадрларды лицензиялауға және интерьерге арналған принт ретінде алуға болады."],
               ["Selected frames are available for licensing and as interior prints."])},
]

# ── Магазин ──────────────────────────────────────────────────────────────
SHOP = [
    {"title": L("Плёночные отпечатки", "Таспадан басылымдар", "Darkroom prints"),
     "text": L("Ручная серебряно-желатиновая печать с моих негативов. Каждый лист печатаю сама.",
               "Өз негативтерімнен қолмен жасалған күміс-желатинді басылым. Әр парақты өзім басамын.",
               "Silver gelatin prints made by hand from my negatives. I print every sheet myself."),
     "facts": L(["Формат 30×40", "В наличии и под заказ", "Без рамы или в раме"],
                ["30×40 форматы", "Қолда бар және тапсырыспен", "Жақтаусыз немесе жақтаумен"],
                ["30×40 cm", "In stock and made to order", "Unframed or framed"])},
    {"title": L("Принты для интерьера", "Интерьерге арналған принттер", "Interior prints"),
     "text": L("Печать с цифровых кадров под ваш интерьер: размер и материал подбираем вместе.",
               "Сандық кадрлардан сіздің интерьеріңізге сай басып шығару: өлшем мен материалды бірге таңдаймыз.",
               "Prints from digital frames made for your space: we choose the size and material together."),
     "facts": L(["Постер", "Холст", "Баннер", "Только под заказ"],
                ["Постер", "Кенеп", "Баннер", "Тек тапсырыспен"],
                ["Poster", "Canvas", "Banner", "Made to order only"])},
    {"title": L("Сертификаты", "Сертификаттар", "Gift certificates"),
     "text": L("Подарок на любую съёмку. Получатель сам выбирает дату.",
               "Кез келген түсірілімге сыйлық. Күнді сыйлық иесі өзі таңдайды.",
               "A gift for any shoot. The recipient picks the date."),
     "facts": L(["Действует 6 месяцев", "Электронный: в WhatsApp или директ", "Печатный в крафт-конверте, бесплатно по запросу"],
                ["6 ай жарамды", "Электронды: WhatsApp немесе директ арқылы", "Крафт конверттегі баспа нұсқасы, сұраныс бойынша тегін"],
                ["Valid for 6 months", "Digital: sent via WhatsApp or Instagram", "Printed in a kraft envelope, free on request"])},
    {"title": L("Подписка", "Жазылым", "Subscription"), "soon": True,
     "text": L("Подписка на новые отпечатки и серии. Условия появятся здесь позже.",
               "Жаңа басылымдар мен серияларға жазылым. Шарттары кейінірек осында пайда болады.",
               "A subscription to new prints and series. Details will appear here later."),
     "facts": L([], [], [])},
]

ABOUT = L(
    ["Я Вероника Ким, фотограф из Алматы. Снимаю с 2017 года: на цифру и плёнку, с дрона и под водой.",
     "Мне интересен авторский подход: студийные сеты и арт-проекты, которые придумываю и собираю с нуля. В цифре люблю яркий, плотный цвет. На плёнке снимаю только чёрно-белый средний формат.",
     "У меня своя проявочная. Плёнку проявляю сама и сама печатаю отпечатки: от нажатия на спуск до готового листа работа остаётся в одних руках.",
     "Работаю в Алматы и Астане, езжу на выездные съёмки."],
    ["Мен Вероника Ким, алматылық фотографпын. 2017 жылдан бері түсіремін: сандық камераға және таспаға, дроннан және су астында.",
     "Маған авторлық көзқарас қызық: өзім ойлап тауып, нөлден құрастыратын студиялық сеттер мен арт-жобалар. Сандық фотода ашық, қанық түсті ұнатамын. Таспаға тек ақ-қара орта форматты түсіремін.",
     "Өз зертханам бар. Таспаны өзім өңдеп, басылымдарды өзім басамын: түсіру сәтінен дайын параққа дейін жұмыс бір қолда қалады.",
     "Алматы мен Астанада жұмыс істеймін, көшпелі түсірілімдерге шығамын."],
    ["I'm Veronika Kim, a photographer based in Almaty. I've been shooting since 2017: digital and film, from a drone and underwater.",
     "I'm drawn to authored work: studio sets and art projects that I invent and build from scratch. In digital I love bold, dense colour. On film I shoot black-and-white medium format only.",
     "I have my own darkroom. I develop the film and make the prints myself, so the work stays in one pair of hands from shutter to finished sheet.",
     "I work in Almaty and Astana and travel for shoots."])

ABOUT_GEAR = L(["Canon EOS R", "Rolleiflex, двухобъективная", "Mamiya, средний формат", "Дрон: фото и видео", "Подводный бокс"],
               ["Canon EOS R", "Rolleiflex, екі объективті", "Mamiya, орта формат", "Дрон: фото мен видео", "Су асты боксы"],
               ["Canon EOS R", "Rolleiflex twin-lens", "Mamiya medium format", "Drone: photo and video", "Underwater housing"])
ABOUT_NO = L("Большие свадьбы, тои и людные мероприятия я не снимаю. Небольшие события до 20 человек обсуждаем лично.",
             "Үлкен тойлар мен көп адам жиналатын іс-шараларды түсірмеймін. 20 адамға дейінгі шағын оқиғаларды жеке талқылаймыз.",
             "I don't shoot large weddings or crowded events. Small gatherings of up to 20 people can be discussed individually.")
LBL_GEAR = L("Техника", "Техника", "Equipment")
LBL_NO = L("Чего я не снимаю", "Нені түсірмеймін", "What I don't shoot")

PH_TINTS = ["#1b1b1e", "#242427", "#2a2320", "#1e2326", "#27201f", "#20241f", "#2d2d31"]

# ── Вспомогательное ──────────────────────────────────────────────────────
e = html.escape
_photo_cache = {}


def photos(g):
    if g not in _photo_cache:
        d = os.path.join(SITE, "photos", g)
        files = []
        if os.path.isdir(d):
            files = sorted(f for f in os.listdir(d)
                           if f.lower().rsplit(".", 1)[-1] in ("jpg", "jpeg", "png", "webp"))
        _photo_cache[g] = files
    return _photo_cache[g]


def lang_prefix(lang):
    """Русская версия живёт в корне сайта, остальные языки — в /kz/ и /en/."""
    return "" if lang == LANGS[0] else lang + "/"


class Ctx(object):
    def __init__(self, lang, path):
        self.lang = lang
        self.path = path
        depth = (1 if lang_prefix(lang) else 0) + (len(path.split("/")) if path else 0)
        self.root = "../" * depth
        self.desc = None    # описание страницы для поисковиков (берётся из вводного абзаца)
        self.image = None   # картинка для превью ссылки (первое фото страницы)

    def abs(self, path=None, lang=None):
        """Полный адрес страницы в интернете."""
        path = self.path if path is None else path
        return SITE_URL + "/" + lang_prefix(lang or self.lang) + (path + "/" if path else "")

    def t(self, d):
        return d[self.lang]

    def url(self, path, lang=None):
        # Чистые адреса: без index.html, с косой чертой на конце
        u = self.root + lang_prefix(lang or self.lang) + (path + "/" if path else "")
        return u or "./"


def tile(c, g, i, ratio, alt, lightbox=True):
    files = photos(g)
    if files and i < len(files):
        src = c.root + "photos/" + g + "/" + files[i]
        if c.image is None and not files[i].startswith("stock-"):
            c.image = "photos/" + g + "/" + files[i]
        img = '<img src="%s" alt="%s" loading="lazy"%s>' % (
            e(src), e(alt), "" if lightbox else ' style="aspect-ratio:%s"' % ratio)
        st = " stock" if files[i].startswith("stock-") else ""  # временное фото из интернета
        if lightbox:
            return '<a class="tile reveal%s" href="%s" data-lb>%s</a>' % (st, e(src), img)
        return '<div class="tile%s">%s</div>' % (st, img)
    return '<div class="tile ph%s" data-ph="%s %02d" style="aspect-ratio:%s;background:%s"></div>' % (
        " reveal" if lightbox else "", e(g), i + 1, ratio, PH_TINTS[(i * 3 + len(g)) % len(PH_TINTS)])


def gallery(c, g, alt, n=9):
    ratios = ["4/5", "3/2", "4/5", "1/1", "4/5", "3/2", "2/3", "4/5", "3/2", "4/5", "1/1", "3/2"]
    count = len(photos(g)) or n
    return '<div class="gallery">%s</div>' % "".join(
        tile(c, g, i, ratios[i % len(ratios)], alt) for i in range(count))


def cta(c, label_key="ask"):
    out = '<a class="btn" href="%s" target="_blank" rel="noopener">%s</a>' % (IG_DM, c.t(S[label_key]))
    if WHATSAPP:
        out += '<a class="btn ghost" href="https://wa.me/%s" target="_blank" rel="noopener">%s</a>' % (
            WHATSAPP, c.t(S["write_wa"]))
    return out


def facts(items, cls="facts"):
    tag = "ol" if "steps" in cls else "ul"
    return "<%s class=\"%s\">%s</%s>" % (tag, cls, "".join("<li>%s</li>" % e(x) for x in items), tag)


def rows(c, items):
    """items: [(path, title, description)]"""
    out = []
    for i, (path, title, desc) in enumerate(items):
        out.append('<a href="%s"><span class="n">%02d</span><span class="t">%s</span><span class="d">%s</span></a>' % (
            c.url(path), i + 1, e(title), e(desc)))
    return '<nav class="rows">%s</nav>' % "".join(out)


def price_block(c):
    return ('<div><h2 class="label">%s</h2><p class="big">%s</p><p class="note">%s</p>%s</div>' % (
        c.t(S["price"]), c.t(S["price_text"]), c.t(S["price_note"]), cta(c)))


NAV = [("book", "book"), ("arch", "architecture"), ("art", "art"), ("shop", "shop"), ("about", "about"),
       ("contacts", "contacts")]


OG_LOCALE = {"ru": "ru_RU", "kz": "kk_KZ", "en": "en_US"}
PARENTS = {"book": "book", "art": "art"}


def seo_head(c, title, full_title, desc, section):
    """Всё, что читают поисковики и ИИ: адрес страницы, языковые версии, превью, структурированные данные."""
    t = c.t
    url = c.abs()
    image = SITE_URL + "/" + (c.image or "assets/og.jpg")
    tags = ['<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
            '<link rel="canonical" href="%s">' % url]
    for lg in LANGS:
        tags.append('<link rel="alternate" hreflang="%s" href="%s">' % (HTML_LANG[lg], c.abs(lang=lg)))
    tags.append('<link rel="alternate" hreflang="x-default" href="%s">' % c.abs(lang=LANGS[0]))
    tags += [
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="Veronika Kim">',
        '<meta property="og:locale" content="%s">' % OG_LOCALE[c.lang],
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:title" content="%s">' % e(full_title),
        '<meta property="og:description" content="%s">' % e(desc),
        '<meta property="og:image" content="%s">' % image,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % e(full_title),
        '<meta name="twitter:description" content="%s">' % e(desc),
        '<meta name="twitter:image" content="%s">' % image,
    ]
    if GOOGLE_VERIFY:
        tags.append('<meta name="google-site-verification" content="%s">' % GOOGLE_VERIFY)
    if YANDEX_VERIFY:
        tags.append('<meta name="yandex-verification" content="%s">' % YANDEX_VERIFY)

    person = {
        "@type": "Person", "@id": SITE_URL + "/#person",
        "name": "Veronika Kim", "alternateName": ["Вероника Ким", "Ким Вероника"],
        "jobTitle": t(L("Фотограф", "Фотограф", "Photographer")),
        "description": t(S["desc"]), "url": SITE_URL + "/", "image": SITE_URL + "/assets/og.jpg",
        "sameAs": [IG_URL, TT_URL],
        "homeLocation": {"@type": "City", "name": "Almaty", "addressCountry": "KZ"},
        "knowsAbout": ["portrait photography", "fine art photography", "black-and-white film photography",
                       "darkroom printing", "drone photography", "underwater photography",
                       "architecture and interior photography"],
    }
    business = {
        "@type": "ProfessionalService", "@id": SITE_URL + "/#studio",
        "name": "Veronika Kim Photography", "alternateName": "Вероника Ким, фотограф",
        "url": SITE_URL + "/", "image": SITE_URL + "/assets/og.jpg", "description": t(S["desc"]),
        "founder": {"@id": SITE_URL + "/#person"},
        "address": {"@type": "PostalAddress", "addressLocality": "Almaty", "addressCountry": "KZ"},
        "areaServed": [{"@type": "City", "name": "Almaty"}, {"@type": "City", "name": "Astana"},
                       {"@type": "Country", "name": "Kazakhstan"}],
        "sameAs": [IG_URL, TT_URL],
        "availableLanguage": ["ru", "kk", "en"],
    }
    website = {"@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": "Veronika Kim",
               "inLanguage": [HTML_LANG[lg] for lg in LANGS], "publisher": {"@id": SITE_URL + "/#person"}}
    page = {"@type": "WebPage", "@id": url, "url": url, "name": full_title, "description": desc,
            "inLanguage": HTML_LANG[c.lang], "isPartOf": {"@id": SITE_URL + "/#site"},
            "about": {"@id": SITE_URL + "/#person"}, "primaryImageOfPage": image}
    graph = [website, person, business, page]
    if c.path:
        crumbs = [(t(S["home"]), c.abs(""))]
        parts = c.path.split("/")
        if len(parts) > 1 and parts[0] in PARENTS:
            crumbs.append((t(S[PARENTS[parts[0]]]), c.abs(parts[0])))
        crumbs.append((title, url))
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
        if c.path.startswith("book/") or c.path == "architecture":
            graph.append({"@type": "Service", "name": title, "description": desc, "url": url,
                          "serviceType": title, "provider": {"@id": SITE_URL + "/#studio"},
                          "areaServed": ["Almaty", "Astana"]})
    tags.append('<script type="application/ld+json">%s</script>' % json.dumps(
        {"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/"))
    return "\n".join(tags)


def seo_files():
    """sitemap.xml, robots.txt, llms.txt, картинка для превью и значок сайта."""
    from PIL import Image
    pages = sorted({os.path.relpath(d, SITE).replace(os.sep, "/") for d, _, fs in os.walk(SITE)
                    if "index.html" in fs})
    ru = [("" if p == "." else p) for p in pages if not (p + "/").startswith(("kz/", "en/"))]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    today = time.strftime("%Y-%m-%d")
    for path in ru:
        for lg in LANGS:
            c = Ctx(lg, path)
            out.append("<url><loc>%s</loc><lastmod>%s</lastmod>" % (c.abs(), today))
            for alt in LANGS:
                out.append('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (HTML_LANG[alt], c.abs(lang=alt)))
            out.append("</url>")
    out.append("</urlset>")
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "YandexBot", "Bingbot"]
    robots = "User-agent: *\nAllow: /\n\n" + "".join("User-agent: %s\nAllow: /\n\n" % b for b in bots)
    robots += "Sitemap: %s/sitemap.xml\n" % SITE_URL
    with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    ll = ["# Veronika Kim (Вероника Ким) — фотограф, Алматы и Астана, Казахстан", "",
          "> " + S["desc"]["ru"], "> " + S["desc"]["en"], "",
          "Вероника Ким снимает с 2017 года: цифра, чёрно-белая плёнка среднего формата (Rolleiflex, Mamiya), "
          "дрон и подводная съёмка. Своя проявочная: проявляет плёнку и печатает отпечатки вручную. "
          "Работает в Алматы и Астане, выезжает на съёмки в другие города и страны. "
          "Не снимает большие свадьбы и людные мероприятия.", "",
          "Запись и стоимость: личным сообщением в Instagram @%s (%s). Стоимость сообщается по запросу." % (INSTAGRAM, IG_URL),
          "Языки сайта: русский (/), қазақша (/kz/), English (/en/).", "",
          "## Съёмки на заказ / Book a shoot", ""]
    for x in SERVICES:
        ll.append("- [%s](%s): %s" % (x["title"]["ru"], Ctx("ru", "book/" + x["slug"]).abs(), x["lead"]["ru"]))
    ll.append("- [%s](%s): %s" % (S["arch"]["ru"], Ctx("ru", "architecture").abs(), ARCH["lead"]["ru"]))
    ll += ["", "## Авторские проекты / Personal work", ""]
    for x in ART:
        ll.append("- [%s](%s): %s" % (x["title"]["ru"], Ctx("ru", "art/" + x["slug"]).abs(), x["lead"]["ru"]))
    ll += ["", "## Ещё", "",
           "- [Магазин](%s): отпечатки из даркрума, принты для интерьера, сертификаты" % Ctx("ru", "shop").abs(),
           "- [Обо мне](%s)" % Ctx("ru", "about").abs(),
           "- [Контакты](%s)" % Ctx("ru", "contacts").abs(),
           "- [English version](%s)" % Ctx("en", "").abs(),
           "- Instagram: %s" % IG_URL, "- TikTok: %s" % TT_URL, ""]
    with open(os.path.join(SITE, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(ll))

    # Превью ссылки 1200×630 из обложки
    files = photos("home")
    if files:
        im = Image.open(os.path.join(SITE, "photos", "home", files[0])).convert("RGB")
        w, h = im.size
        nh = int(w * 630 / 1200.0)
        top = max(0, min(h - nh, int(h * .44 - nh * .45)))
        im.crop((0, top, w, top + nh)).resize((1200, 630), Image.LANCZOS).save(
            os.path.join(SITE, "assets", "og.jpg"), quality=86)
    with open(os.path.join(SITE, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#111112"/>'
                '<text x="32" y="43" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-weight="900" '
                'font-size="30" letter-spacing="-2" fill="#FA8030">VK</text></svg>')


def layout(c, title, body, section=""):
    t = c.t
    full_title = (title + t(S["seo_suffix"])) if title else t(S["seo_home"])
    desc = t(S["desc"])
    if c.desc:
        desc = c.desc.rstrip(". ") + ". " + t(S["seo_sign"])
    seo = seo_head(c, title, full_title, desc, section)
    langs = "".join('<a href="%s" lang="%s"%s>%s</a>' % (
        c.url(c.path, lg), HTML_LANG[lg], ' aria-current="true"' if lg == c.lang else "", lg) for lg in LANGS)
    main_links = "".join('<a href="%s"%s>%s</a>' % (
        c.url(p), ' aria-current="page"' if section == p else "", t(S[k])) for k, p in NAV)
    sub = "".join('<a href="%s">%s</a>' % (c.url("book/" + s["slug"]), t(s["title"])) for s in SERVICES)
    sub += "".join('<a href="%s">%s</a>' % (c.url("art/" + a["slug"]), t(a["title"])) for a in ART)
    wa = ('<p class="big"><a href="https://wa.me/%s">WhatsApp</a></p>' % WHATSAPP) if WHATSAPP else ""
    return """<!doctype html>
<html lang="{hl}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#111112">
{seo}
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Unbounded:wght@900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css?v={ver}">
</head>
<body id="top">
<header class="top">
  <a class="mono" href="{home}" aria-label="{name}">{mono}</a>
  <div class="top-right">
    <nav class="langs" aria-label="Language">{langs}</nav>
    <button class="menu-btn" aria-expanded="false" aria-controls="menu" data-open="{menu}" data-close="{close}">{menu}</button>
  </div>
</header>
<div class="menu" id="menu">
  <nav class="menu-main">{main_links}</nav>
  <nav class="langs menu-langs" aria-label="Language">{langs}</nav>
  <nav class="menu-sub">{sub}</nav>
</div>
<main>
{body}
</main>
<footer class="foot">
  <div class="foot-grid">
    <div><h2 class="label">{l_booking}:</h2><p class="big"><a href="{ig_dm}" target="_blank" rel="noopener">{write_ig}</a></p>{wa}</div>
    <div><h2 class="label">{l_social}:</h2><p class="big"><a href="{ig}" target="_blank" rel="noopener">Instagram</a><br><a href="{tt}" target="_blank" rel="noopener">TikTok</a></p></div>
    <div><h2 class="label">{l_where}:</h2><p class="big">{where}</p></div>
    <div><h2 class="label">{l_menu}:</h2><p class="big">{foot_links}</p></div>
  </div>
  <div class="foot-bottom"><span>© 2026 {name}. {rights}</span><a href="#top">{top}</a></div>
</footer>
<div class="lb" role="dialog" aria-modal="true"><span class="c"></span><button class="x">{close}</button><button class="p">← {prev}</button><img alt=""><button class="nx">{next} →</button></div>
<script src="{root}assets/app.js?v={ver}"></script>
</body>
</html>
""".format(
        hl=HTML_LANG[c.lang], ver=VER, title=e(full_title), desc=e(desc), seo=seo, root=c.root, home=c.url(""),
        name=e(t(S["name"])), mono=e(t(S["name1"])[0] + "—" + t(S["name2"])[0]), langs=langs,
        menu=t(S["menu"]), close=t(S["close"]), main_links=main_links, sub=sub, body=body,
        l_booking=t(S["booking"]), ig_dm=IG_DM, write_ig=t(S["write_ig"]), wa=wa,
        l_social=t(S["social"]), ig=IG_URL, tt=TT_URL, l_where=t(S["where"]), where=t(S["where_text"]),
        l_menu=t(S["menu"]),
        foot_links="<br>".join('<a href="%s">%s</a>' % (c.url(p), t(S[k])) for k, p in NAV[:4]),
        rights=t(S["rights"]), top=t(S["top"]), prev=t(S["prev"]), next=t(S["next"]))


def write(c, title, body, section=""):
    out = os.path.join(SITE, lang_prefix(c.lang).strip("/"), *(c.path.split("/") if c.path else []))
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(layout(c, title, body, section))


def page_head(c, title, lead, eyebrow="", eyebrow_path=None):
    eb = ""
    if eyebrow:
        inner = '<a href="%s">%s</a>' % (c.url(eyebrow_path), e(eyebrow)) if eyebrow_path else e(eyebrow)
        eb = '<p class="eyebrow">%s</p>' % inner
    c.desc = lead
    back = '<a class="back" href="%s">← %s</a>' % (c.url(eyebrow_path or ""), c.t(S["prev"]))
    return '<header class="page-head">%s%s<h1>%s</h1><p class="lead">%s</p></header>' % (back, eb, e(title), e(lead))


# ── Страницы ─────────────────────────────────────────────────────────────
def cover_html(c):
    """Первый экран: home/01 для широкого экрана, home/02 (если есть) для телефона."""
    files = photos("home")
    if not files:
        return tile(c, "home", 0, "auto", c.t(S["name"]), lightbox=False)
    base = c.root + "photos/home/"
    src = ""
    if len(files) > 1:
        src = '<source media="(max-width: 760px)" srcset="%s">' % e(base + files[1] + "?v=" + VER)
    return '<picture class="tile">%s<img src="%s" alt="%s"></picture>' % (src, e(base + files[0] + "?v=" + VER), e(c.t(S["name"])))


def drift_thumb(g, f):
    """Лёгкая копия кадра для плывущего ряда: телефону не нужно двигать фото в 2000 px."""
    from PIL import Image
    out_dir = os.path.join(SITE, "photos", "drift")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    im = Image.open(os.path.join(SITE, "photos", g, f)).convert("RGB")
    im.thumbnail((560, 560))
    im.save(os.path.join(out_dir, g + ".jpg"), quality=82)
    return im.size


def home(lang):
    c = Ctx(lang, "")
    t = c.t
    # (галерея, путь, подпись, колонка, ширина, пропорция, отступ сверху, поверх надписи?)
    A = {a["slug"]: a for a in ART}
    V = {s["slug"]: s for s in SERVICES}
    # (галерея, путь, подпись, колонка, ширина, пропорция, отступ сверху)
    cells = [
        ("editorial", "art/editorial", t(A["editorial"]["title"])),
        ("mountains", "book/mountains", t(V["mountains"]["title"])),
        ("kids", "book/kids", t(V["kids"]["title"])),
        ("underwater", "book/underwater", t(V["underwater"]["title"])),
        ("portrait", "book/portrait", t(V["portrait"]["title"])),
        ("architecture", "architecture", t(S["arch"])),
        ("love-story", "book/love-story", t(V["love-story"]["title"])),
        ("travel", "art/travel", t(A["travel"]["title"])),
    ]
    scatter = []
    for g, path, label in cells:
        files = photos(g)
        if not files:
            continue
        w, h = drift_thumb(g, files[0])
        scatter.append('<div class="drift-item"><a href="%s"><img src="%s" width="%d" height="%d" alt="%s" decoding="async"></a></div>' % (
            c.url(path), e(c.root + "photos/drift/" + g + ".jpg?v=" + VER), w, h, e(label)))
    banner = ""
    if SHOW_BANNER:
        banner = ('<section class="banner"><div><h2 class="label">%s</h2><p class="big">%s</p><p>%s</p></div>'
                  '<a class="btn" href="%s" target="_blank" rel="noopener">%s</a></section>' % (
                      t(S["banner_label"]), t(S["banner_title"]), t(S["banner_text"]), IG_DM, t(S["banner_cta"])))
    body = """
<div class="home" id="home">
<section class="stage">
  <div class="splash">{cover}</div>
  <h1 class="wordmark" aria-label="{name}"><span>{n1}</span><span>{n2}</span></h1>
  <div class="drift">{scatter}</div>
</section>
<div class="home-content">
<p class="statement">{statement}</p>
{banner}
<div class="block-head"><h2>{book}</h2><a href="{book_url}">{all}</a></div>
{book_rows}
<div class="block-head"><h2>{art}</h2><a href="{art_url}">{all}</a></div>
{art_rows}
<div class="block-head"><h2>{shop}</h2><a href="{shop_url}">{all}</a></div>
{shop_rows}
<section class="split"><div class="wide prose"><h2 class="label">{about}</h2><p class="big">{intro}</p>
<a class="btn ghost" href="{about_url}">{about}</a></div></section>
</div>
</div>
""".format(
        cover=cover_html(c),
        scatter="".join(scatter), name=e(t(S["name"])), n1=t(S["name1"]), n2=t(S["name2"]),
        statement=t(S["statement"]), banner=banner, all=t(S["all"]),
        book=t(S["book"]), book_url=c.url("book"),
        book_rows=rows(c, [("book/" + s["slug"], t(s["title"]), t(s["lead"])) for s in SERVICES]
                       + [("architecture", t(S["arch"]), t(ARCH["lead"]))]),
        art=t(S["art"]), art_url=c.url("art"),
        art_rows=rows(c, [("art/" + a["slug"], t(a["title"]), t(a["lead"])) for a in ART]),
        shop=t(S["shop"]), shop_url=c.url("shop"),
        shop_rows=rows(c, [("shop", t(x["title"]), t(x["text"])) for x in SHOP[:3]]),
        about=t(S["about"]), intro=t(S["intro"]), about_url=c.url("about"))
    write(c, "", body)


def book_index(lang):
    c = Ctx(lang, "book")
    t = c.t
    body = page_head(c, t(S["book"]), t(S["price_note"]))
    body += rows(c, [("book/" + s["slug"], t(s["title"]), t(s["lead"])) for s in SERVICES]
                 + [("architecture", t(S["arch"]), t(ARCH["lead"]))])
    body += '<section class="split"><div><h2 class="label">%s</h2>%s</div>%s</section>' % (
        t(S["terms"]), facts(t(TERMS)), price_block(c))
    write(c, t(S["book"]), body, "book")


def service(lang, s):
    c = Ctx(lang, "book/" + s["slug"])
    t = c.t
    body = page_head(c, t(s["title"]), t(s["lead"]), t(S["book"]), "book")
    body += gallery(c, s["g"], t(s["title"]))
    body += '<section class="split"><div><h2 class="label">%s</h2>%s</div>%s</section>' % (
        t(S["included"]), facts(t(s["facts"])), price_block(c))
    body += '<div class="block-head"><h2>%s</h2><a href="%s">%s</a></div>' % (t(S["more"]), c.url("book"), t(S["all"]))
    body += rows(c, [("book/" + x["slug"], t(x["title"]), t(x["lead"])) for x in SERVICES if x is not s][:3])
    write(c, t(s["title"]), body, "book")


def architecture(lang):
    c = Ctx(lang, "architecture")
    t = c.t
    body = page_head(c, t(ARCH["title"]), t(ARCH["lead"]))
    body += gallery(c, "architecture", t(ARCH["title"]))
    body += '<section class="split"><div><h2 class="label">%s</h2>%s</div>%s</section>' % (
        t(S["included"]), facts(t(ARCH["facts"])), price_block(c))
    write(c, t(ARCH["title"]), body, "architecture")


def art_index(lang):
    c = Ctx(lang, "art")
    t = c.t
    body = page_head(c, t(S["art"]), t(S["intro"]))
    body += rows(c, [("art/" + a["slug"], t(a["title"]), t(a["lead"])) for a in ART])
    write(c, t(S["art"]), body, "art")


def art_page(lang, a):
    c = Ctx(lang, "art/" + a["slug"])
    t = c.t
    body = page_head(c, t(a["title"]), t(a["lead"]), t(S["art"]), "art")
    body += gallery(c, a["g"], t(a["title"]), 12 if a["slug"] == "thirst-for-life" else 9)
    if "steps" in a:
        left = facts(t(a["steps"]), "facts steps")
        left += '<p class="statement" style="padding-left:0;padding-bottom:0;font-size:clamp(24px,3vw,44px)">%s</p>' % t(S["statement"])
        body += '<section class="split"><div>%s</div>%s</section>' % (left, price_block(c))
    else:
        prose = "".join("<p>%s</p>" % e(p) for p in t(a["body"]))
        right = ""
        if a["slug"] in ("film-darkroom", "travel"):
            right = price_block(c)
        body += '<section class="split"><div class="prose">%s</div>%s</section>' % (prose, right)
    body += '<div class="block-head"><h2>%s</h2><a href="%s">%s</a></div>' % (t(S["more_art"]), c.url("art"), t(S["all"]))
    body += rows(c, [("art/" + x["slug"], t(x["title"]), t(x["lead"])) for x in ART if x is not a])
    write(c, t(a["title"]), body, "art")


def shop(lang):
    c = Ctx(lang, "shop")
    t = c.t
    body = page_head(c, t(S["shop"]), t(SHOP[0]["text"]))
    cards = []
    for i, x in enumerate(SHOP):
        soon = x.get("soon")
        cards.append('<article class="card">%s<div class="card-body">%s<h2>%s</h2><p>%s</p>%s%s</div></article>' % (
            tile(c, "prints", i, "3/2", t(x["title"]), lightbox=False),
            '<span class="soon">%s</span>' % t(S["soon"]) if soon else "",
            e(t(x["title"])), e(t(x["text"])),
            facts(t(x["facts"])) if t(x["facts"]) else "",
            "" if soon else cta(c, "order")))
    body += '<div class="cards">%s</div>' % "".join(cards)
    write(c, t(S["shop"]), body, "shop")


def about(lang):
    c = Ctx(lang, "about")
    t = c.t
    paras = t(ABOUT)
    body = page_head(c, t(S["about"]), paras[0])
    body += '<section class="split" style="padding-top:0"><div class="narrow">%s</div><div class="wide prose">%s</div></section>' % (
        tile(c, "about", 0, "4/5", t(S["name"]), lightbox=False), "".join("<p>%s</p>" % e(p) for p in paras[1:]))
    body += '<section class="split"><div><h2 class="label">%s</h2>%s</div><div><h2 class="label">%s</h2><p class="big">%s</p></div></section>' % (
        t(LBL_GEAR), facts(t(ABOUT_GEAR)), t(LBL_NO), e(t(ABOUT_NO)))
    write(c, t(S["about"]), body, "about")


def contacts(lang):
    c = Ctx(lang, "contacts")
    t = c.t
    body = page_head(c, t(S["contacts"]), t(S["price_note"]))
    c.desc = t(S["contacts"]) + ": Instagram @" + INSTAGRAM + ", TikTok @" + TIKTOK + ". " + t(S["where_text"])
    body += ('<section class="split" style="padding-top:0"><div><h2 class="label">Instagram</h2>'
             '<p class="big"><a href="%s" target="_blank" rel="noopener">@%s</a></p>%s</div>'
             '<div><h2 class="label">TikTok</h2><p class="big"><a href="%s" target="_blank" rel="noopener">@%s</a></p>'
             '<h2 class="label" style="margin-top:36px">%s</h2><p class="big">%s</p></div></section>' % (
                 IG_URL, INSTAGRAM, cta(c, "write_ig"), TT_URL, TIKTOK, t(S["where"]), t(S["where_text"])))
    body += '<section class="split"><div class="wide"><h2 class="label">%s</h2>%s</div></section>' % (
        t(S["terms"]), facts(t(TERMS)))
    write(c, t(S["contacts"]), body, "contacts")


def main():
    for lang in LANGS:
        home(lang)
        book_index(lang)
        for s in SERVICES:
            service(lang, s)
        architecture(lang)
        art_index(lang)
        for a in ART:
            art_page(lang, a)
        shop(lang)
        about(lang)
        contacts(lang)
    seo_files()
    n = sum(len(fs) for _, _, fs in os.walk(SITE) if any(x.endswith(".html") for x in fs))
    print("Готово: site/ (%d файлов)" % n)


if __name__ == "__main__":
    main()
