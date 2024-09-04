from telebot.types import Message
from telebot import custom_filters
from telebot.custom_filters import (
    SimpleCustomFilter,
    AdvancedCustomFilter,
    TextFilter,
)

import itertools

class AreEntitiesInMessage(SimpleCustomFilter):
    key = "are_entities_in_message"

    def check(self, message: Message):
        if message.entities:
            return True
        else:
            return


class ContainsOneOfWordsFilter(AdvancedCustomFilter):
    key = "contains_one_of_words"

    def check(self, message: Message, words:str):
        text = message.text or message.caption
        if not text:
            return False
        else:
            text_lower=text.lower()
            return any(word.lower() in text_lower for word in words)


class UpdatedTextFilter(TextFilter):
    def check(self, obj):
        if isinstance(obj, Message):
            text=obj.text or obj.caption
            if text is None:
                return False
        return super().check(obj)