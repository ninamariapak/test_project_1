from telebot import TeleBot
from telebot import types
#from io import StringIO
from telebot import formatting
from telebot import util
from telebot import custom_filters
from telebot import State
from telebot.handler_backends import StatesGroup
#from telebot.states.sync.middleware import StateMiddleware

import config
import messages
from config import get_admin_ids
import my_filters

bot = TeleBot(config.BOT_TOKEN)
#bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextContainsFilter())


class CustomerSurveyStates(StatesGroup):
    full_name = State()
    contact_number = State()
    purpose_of_the_call = State()
    city = State()

all_customer_survey_states = CustomerSurveyStates().state_list

def get_share_contact_kb():
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    share_contact_button = types.KeyboardButton(
        text="Отправить номер телефона",
        request_contact=True,
    )
    cancel_button = types.KeyboardButton(text="Отмена")
    keyboard.add(share_contact_button, cancel_button)
    return keyboard


def get_visit_our_website_kb():
    kb = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(
        text="Посетите наш сайт",
        url="https://dzen.ru/"
    )
    kb.add(url_button)
    return kb

def get_purpose_of_the_call_kb():
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    services_button = types.KeyboardButton(text="Курсы")
    camps_button = types.KeyboardButton(text="Лагеря")
    test_button = types.KeyboardButton(text="Записаться на тестирование")
    vacancies_button = types.KeyboardButton(text="Цены")
    a_little_bit_of_everything_button = types.KeyboardButton(text="Обо всем понемногу")
    other_button = types.KeyboardButton(text="Другое")
    keyboard.add(services_button, camps_button, test_button, vacancies_button, a_little_bit_of_everything_button, other_button)
    return keyboard


@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.start_msg,
        parse_mode="HTML",
    )


@bot.message_handler(commands=["user_and_chat_id"])
def handle_user_and_chat_id_request(message: types.Message):
    text = f"{message.chat.id}"
    bot.send_message(
        message.chat.id,
        text=text,
    )

@bot.message_handler(commands=["leave_a_message"])
def handle_leave_a_message_request_start_survey(message: types.Message):
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=CustomerSurveyStates.full_name.name,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.customer_survey_name,
        parse_mode="HTML",
    )

#Реакции на имя пользователя

@bot.message_handler(
    state=CustomerSurveyStates.full_name.name,
    content_types=["text"],
)
def handle_user_name(message: types.Message):
    full_name = message.text
    share_contact_kb = get_share_contact_kb()
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        full_name=full_name,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=CustomerSurveyStates.contact_number.name,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.customer_survey_share_contact_number.format(
            full_name=formatting.hbold(full_name),
        ),
        parse_mode="HTML",
        reply_markup=share_contact_kb,
    )

@bot.message_handler(
    state=CustomerSurveyStates.full_name.name,
    content_types=util.content_type_media,
)
def handle_wrong_user_name(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.customer_survey_wrong_name,
        parse_mode="HTML",
    )

#Реакции на контакт

@bot.message_handler(
    content_types=["contact"],
    state=CustomerSurveyStates.contact_number.name,
)
def handle_contact_number_ask_for_purpose(message: types.Message):
    contact_number=message.contact
    purpose_of_the_call_kb = get_purpose_of_the_call_kb()
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        contact_number=contact_number,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=CustomerSurveyStates.purpose_of_the_call.name,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.customer_survey_purpose_of_the_call_msg,
        #parse_mode="HTML",
        reply_markup=purpose_of_the_call_kb,
    )


@bot.message_handler(
    content_types=["text"],
    state=CustomerSurveyStates.contact_number.name,
)
def handle_cancel_contact_number(message: types.Message):
    visit_our_website_kb = get_visit_our_website_kb()
    share_contact_kb = get_share_contact_kb()
    if message.text.lower() == "отмена":
        with bot.retrieve_data(
                user_id=message.from_user.id,
                chat_id=message.chat.id,
        ) as data:
            data.pop("full_name", "-")
            data.pop("contact_number", "-")
            data.pop("purpose_of_the_call", "-")
            data.pop("city", "-")
        bot.set_state(
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            state=0,
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.customer_survey_cancel_msg,
            parse_mode="HTML",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.visit_our_website_msg,
            parse_mode="HTML",
            reply_markup=visit_our_website_kb,
        )
    elif message.text.lower != "отмена":
        bot.send_message(
            chat_id=message.chat.id,
            text=messages.customer_survey_invalid_contact_msg,
            parse_mode="HTML",
            reply_markup=share_contact_kb,
        )


#Реакции на цель обращения

@bot.message_handler(
    content_types=["text"],
    state=CustomerSurveyStates.purpose_of_the_call.name,
)
def handle_purpose_of_the_call_ask_for_city(message: types.Message):
    purpose_of_the_call = message.text
    bot.add_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        purpose_of_the_call=purpose_of_the_call,
    )
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=CustomerSurveyStates.city.name,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.customer_survey_ask_for_city_msg,
        parse_mode="HTML",
        reply_markup=types.ReplyKeyboardRemove(),
    )

#Реакции на город + итоги опроса

#Формирование итогов для юзера и админа
def prepare_result_msg_text(data: dict, message: types.Message):
    full_name=data.get("full_name", " ")
    contact_number=data.get("contact_number", " ")
    purpose_of_the_call=data.get("purpose_of_the_call", " ")

    text = formatting.format_text(
        "Спасибо! Все записал и отправил менеджеру.",
        formatting.format_text(
            "Имя:",
            formatting.hcode(full_name),
            separator=" ",
        ),
        formatting.format_text(
            "Контактный номер:",
            formatting.hcode(contact_number),
            separator=" ",
        ),
        formatting.format_text(
            "Цель звонка:",
            formatting.hcode(purpose_of_the_call),
            separator=" ",
        ),
        formatting.format_text(
            "Город:",
            formatting.hcode(message.text),
            separator=" ",
        ),
        "С минуты на минуту он(а) Вам позвонит.",
        formatting.format_text(
            "В любое время можете нажать",
            formatting.hbold("/leave_a_message,"),
            "и я запишу Ваше новое сообщение.",
            separator=" ",
        ),
        separator="\n",
    )
    return text


def prepare_result_msg_text_for_admin(data: dict, message: types.Message):
    full_name=data.get("full_name", " ")
    contact_number=data.get("contact_number", " ")
    purpose_of_the_call=data.get("purpose_of_the_call", " ")

    text = formatting.format_text(
        "У Вас новое обращение.",
        formatting.format_text(
            "Имя:",
            formatting.hcode(full_name),
            separator=" ",
        ),
        formatting.format_text(
            "Контактный номер:",
            formatting.hcode(contact_number),
            separator=" ",
        ),
        formatting.format_text(
            "Цель звонка:",
            formatting.hcode(purpose_of_the_call),
            separator=" ",
        ),
        formatting.format_text(
            "Город:",
            formatting.hcode(message.text),
            separator=" ",
        ),
    )
    return text

#Отправка итогов юзеру и админу
@bot.message_handler(
    content_types=["text"],
    state=CustomerSurveyStates.city.name,
)
def handle_city_ok_send_final_msgs(message: types.Message):
    visit_our_website_kb = get_visit_our_website_kb()
    admin_chat_id = get_admin_ids()
    user_text="text"
    admin_text="text for admin"
    with bot.retrieve_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    ) as data:
        user_text = prepare_result_msg_text(data, message)
        admin_text = prepare_result_msg_text_for_admin(data, message)
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=0,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=user_text,
        parse_mode="HTML",
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.visit_our_website_msg,
        parse_mode="HTML",
        reply_markup=visit_our_website_kb,
    )
    bot.send_message(
        chat_id=admin_chat_id,
        text=admin_text,
        parse_mode="HTML",
    )




if __name__ == '__main__':
    bot.enable_saving_states()
    #bot.enable_save_next_step_handlers(delay=2)
    #bot.load_next_step_handlers()
    bot.infinity_polling(skip_pending=True, allowed_updates=[])
