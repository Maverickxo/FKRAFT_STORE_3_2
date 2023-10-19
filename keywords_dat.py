HELP = """
🛒 Добро пожаловать в наш магазин! 🛍️

- Чтобы добавить товар в корзину, просто нажмите кнопку с названием товара.
- Если вы хотите добавить несколько экземпляров одного товара, просто нажмите кнопку несколько раз.

- Чтобы уменьшить количество товара или удалить его из корзины, нажмите появившуюся кнопку с соответствующим действием.
- Количество выбранного товара отображается в скобках.

📦 *Корзина:\n- Предварительный просмотр содержимого вашей корзины.\n
🗑️ Очистить корзину:\n- Полная очистка корзины. Все добавленные товары будут удалены.\n
💳 После формирования заказа:\nВы получите актуальные реквизиты для оплаты. После успешной оплаты, ‼️пришлите ваш заказ и чек‼️ >>> @KRAFT_ZAKAZ.\n
📞 Обратная связь:\nЕсли у вас возникли вопросы или вам требуется помощь, обратитесь к администрации:\n├─@blockmor\n├─@Maverik_Xo\n├─@ZalehvatSky\n
📬 Для получения трека >>>>>> @KRAFT_CT_BOT !*\n
Приятных покупок!
"""

TEXT_RULES = """
👇Все заказы только через 👇
❗️@KRAFT_STORE_BOT❗️

Оплата только по реквизитам к заказу❗️

- Будьте внимательны , работают мошенники!

┌─Минимальный заказ 4500 рублей 
│ 
│├─Отправка заказов в течение недели!
│   └─ Отправка стандарт +600р
│   └─ Отправка экспресс +1200р (в течение 24 часов)
│      └─ Раздача треков по запросу через бот: @KRAFT_CT_BOT
│         └─ Трек появится в базе как только почта примет посылку
│         └─ Отслеживайте все перемещения через бот
│         └─ Трек доступен после прибытия посылки на вручение
│
│├─ Скидки:
│   └─ Опт 15% от 130т(пересчет автоматом)
│   └─ Купоны в магазине 5-10% рандомно(одноразовые)
│
│├─ Заказ:
││    └─ После оплаты перешлите сообщение с заказом + чек
││         └─ Получите подтверждение
│├─ НЕ ПРИНИМАЮТСЯ:
│       └─ Скрины заказа
│       └─ Номер заказа 
│       └─ Редактированные сообщения заказа
│
│├─ Страховка посылки:
│   └─ Независимо от этой опции снимайте видео распаковки!
│─ Дополнительная информация в чате и в канале магазина.
└─ Нажимая кнопку │ОЗНАКОМЛЕН│ вы принимаете правила магазина.
"""

help_text = """
Список доступных команд для администратора:

Команды общего назначения:
/dice: Кубики
/dice_list: Список пользователей по кубам
/help: Инструкция (доступна всем)
/start: Вызвать правила (доступна всем)
/reset: Сброс состояния бота (для мудаков, доступно всем, 3 раза подряд)
/ck_coupon: Проверка купона (доступна всем)
/rank_system: Информация о системе репутации(R)

Команды управления балансом:
/get_balance: Узнать свой баланс(PRIVATE)
/checkbalance: Узнать баланс пользователя(ADM)
/get_user_balance: Узнать баланс пользователей(список)
/add_user_balance: Пополнить баланс пользователя(список)
/deposit: Пополнить баланс пользователя(ответом на сообщение)
/gopstop <деньги>: Отнять у пользователя денег 
/send <деньги>: Отправка денег со своего счета

Команды управления пользователями:
/users_count: Количество подписчиков бота
/block_list: Список долбоебов
/user_list: Список юзеров доступных на бан
/rating <число>: Топ пользователей в рейтинге

Управление товарами:
/toggle_product: Переключение статуса товара (включение/выключение)
/edit_product_price: Редактировать цену товара
/add_product: Добавление нового товара
/products_to_delete: Удаление товара
/status <номер заказа>: Узнать номер заказа

Управление купонами:
/weekend_coupons: Случайные купоны на выходные
/adm_get_coupons <процент>: Взять случайный купон с указанным процентом скидки.
/add_coupon <имя> <процент>: Добавить именной купон с указанным процентом скидки.
/add_coupon_pack <количество купонов> <процент скидки>: Добавить новые купоны в базу
/add_coupon_off_time: Добавить бессрочный купон
/list_coupon_of_time: Список бессрочных купонов
/del_coupon_off_time: Удалить бессрочный купон

Команды управления магазином и рассылкой:
/response_store: Ответ на вопрос в магазин
/speak_store: Рассылка всем в магазине
/speak_chat: Отправка от мимени бота репутации
/technical_works: Технические работы

"""

ALERT_TEXT = """
После совершения *ОПЛАТЫ*, перешлите на *@KRAFT_ZAKAZ*
*следующую информацию о вашем заказе:* 

1.Сообщение с заказом (❕_в том виде в котором вы его получили_❕) без редактирования и прочих фантазий.
PS - тыкните в сообщение (❕переслать❕)

❕- Просим предоставить именно текст, а не скриншоты.❕

2.*Чек об оплате можно в любом виде*

*Для отслеживания посылки используйте -  @KRAFT_CT_BOT*

*Подпишитесь на канал магазина  - @krafturpharmacyinfo*
"""


COUPON_TEXT = """
Уважаемые друзья, коллеги, товарищи, соратники!!!
Скидочные купоны от нашего любимого магазина

"""

INFO = """
🛍️ *KRAFT STORE BOT - версия 3.5.2563* 🛍️

    [rel: Дата: 16.10.2023]\n
    [feedback](https://t.me/Maver1ckxo) : @Maver1ckxo\n

"""
