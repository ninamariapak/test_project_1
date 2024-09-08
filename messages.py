from telebot import formatting


start_msg = formatting.format_text(
    formatting.format_text(
        "Вас приветствует бот-помощник менеджера",
        formatting.hlink("Дзен.", "https://dzen.ru"),
        separator=" ",
    ),
    formatting.format_text(
        "Нажмите",
        formatting.hbold("/leave_a_message,"),
        "я запишу Ваше сообщение, и менеджер перезвонит.",
        separator=" ",
    ),
)

customer_survey_name = formatting.format_text(
    formatting.format_text("Укажите Ваше имя."),
    formatting.format_text(
        "Например,",
        formatting.hitalic("Нина"),
        "или",
        formatting.hitalic("Нина Сергеевна."),
        separator=" ",
    ),
)

#name_not_okay_try_again_msg = ("Непонятно. Укажите текстом.")


customer_survey_share_contact_number = formatting.format_text(
        formatting.format_text(
            "{full_name}, нажмите",
            formatting.hbold("отправить контакт"),
            "на клавиатуре ниже, чтобы я смог записать Ваш номер.",
            separator=" ",
        ),
        formatting.format_text(
        "Если кликнете",
            formatting.hitalic("отмена,"),
            "наша беседа прервется, и я буду в печали.",
            separator=" ",
        ),
)

customer_survey_wrong_name = formatting.format_text(
    formatting.format_text("Не понимаю."),
    formatting.format_text("Укажите текстом, пожалуйста."),
    formatting.format_text(
        "Например,",
        formatting.hitalic("Нина"),
        "или",
        formatting.hitalic("Нина Сергеевна."),
        separator=" ",
    ),
)

#name_ok_share_contact_number_msg = ("Укажите Ваш номер телефона")


customer_survey_cancel_msg = formatting.format_text(
    "Жаль, что нам пришлось прерваться",
    formatting.format_text(
        "В любое время нажмите",
        formatting.hbold("/leave_a_message,"),
        "я запишу Ваше сообщение, и менеджер перезвонит.",
        separator=" ",
    ),
)

visit_our_website_msg = formatting.format_text(
    "+ Бесплатный тест,",
    formatting.format_text("+ наши преимущества,"),
    formatting.format_text("+ видеофрагменты,"),
    formatting.format_text("+ клубы - "),
    formatting.format_text("все это в одном клике от Вас на нашем сайте!"),
)

customer_survey_purpose_of_the_call_msg = ("Что желаете узнать у менеджера?")

customer_survey_invalid_contact_msg = formatting.format_text(
    formatting.format_text(
        "Не понимаю. Нажмите",
        formatting.hbold("отправить контакт"),
        "на клавиатуре ниже, и я запишу Ваш номер.",
        "Так уж я запрограммирован.",
        separator=" ",
    ),
    formatting.format_text(
        "Кликнув",
            formatting.hitalic("отмена,"),
            "можно отменить отправку заявки.",
            separator=" ",
    ),
)

customer_survey_ask_for_city_msg = formatting.format_text(
    formatting.format_text("В каком Вы городе?"),
    formatting.format_text(
        "Напишите одним словом. Например,",
        formatting.hbold("Волгоград."),
        separator=" ",
    ),
    formatting.format_text("Это чтобы менеджер знал(а) Ваш часовой пояс."),
)

#customer_survey_city_ok_send_final_msg = formatting.format_text()

customer_survey_city_not_ok = formatting.format_text(
    "Напишите город текстом, пожалуйста.",
    formatting.format_text(
        "Например,",
        formatting.hbold("Волгоград."),
        separator=" ",
    ),
)