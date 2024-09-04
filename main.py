from telebot import TeleBot
from telebot import types
#from io import StringIO
from telebot import formatting
from telebot import util
from telebot import custom_filters
from telebot import State
from telebot.handler_backends import StatesGroup

import config
import messages
#import my_filters

bot = TeleBot(config.BOT_TOKEN)
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())


class CustomerSurveyStates(StatesGroup):
    full_name = State()
    contact_number = State()
    purpose_of_the_call = State()
    city = State()
    convenient_call_time = State()

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

@bot.message_handler(commands=["start"])
def handle_command_start(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.start_msg,
        parse_mode="HTML",
    )


@bot.message_handler(commands=["leave_a_message"])
def handle_leave_a_message_request_start_survey(message: types.Message):
    bot.set_state(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        state=CustomerSurveyStates.full_name,
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.customer_survey_name,
        parse_mode="HTML",
    )


@bot.message_handler(
    state=CustomerSurveyStates.full_name,
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
        state=CustomerSurveyStates.contact_number,
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
    state=CustomerSurveyStates.full_name,
    content_types=util.content_type_media,
)
def handle_wrong_user_name(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.customer_survey_wrong_name,
        parse_mode="HTML",
    )


@bot.message_handler(
    text=custom_filters.TextFilter(
        equals="отмена",
        ignore_case=True,
    ),
    state=all_customer_survey_states,
)
def handle_cancel_customer_survey(message: types.Message):
    visit_our_website_kb = get_visit_our_website_kb()
    with bot.retrieve_data(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
    ) as data:
        data.pop("full_name", "-")
        data.pop("contact_number", "-")
        data.pop("city","-")
        data.pop("convenient_call_time", "-")
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

if __name__ == '__main__':
    bot.enable_saving_states()
    #bot.enable_save_next_step_handlers(delay=2)
    #bot.load_next_step_handlers()
    bot.infinity_polling(skip_pending=True, allowed_updates=[])
