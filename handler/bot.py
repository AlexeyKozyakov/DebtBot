import re

from telegram import Update, Message
from telegram.constants import MessageEntityType
from telegram.ext import Application, ContextTypes, filters, MessageHandler, CommandHandler

import core.debts

TOKEN = '6135723229:AAG3QoWuJPiD830Rw-FL1nfhGCrqV85yxiM'

EXPRESSION_REGEXP = '((\d+\s*(\*|\/|\+|\-)\s*)+(\d+\s*))|\d+'


def __get_first_mentioned_user(message: Message):
    for entity in message.entities:
        if entity.type == MessageEntityType.MENTION:
            return message.text[entity.offset + 1:entity.offset + entity.length]
    return None


def __get_simple_math_expression(text: str):
    match = re.search(EXPRESSION_REGEXP, text)
    if match is None:
        return match
    return match.group()


async def process_message(update: Update, _: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user.username
    mentioned_user = __get_first_mentioned_user(message)
    if mentioned_user is None:
        return
    is_incoming = 'мне' in message.text.lower()
    debt_expression = __get_simple_math_expression(message.text)
    if debt_expression is None:
        return
    amount = int(eval(debt_expression))
    from_user, to_user = (mentioned_user, user) if is_incoming else (user, mentioned_user)
    if from_user == to_user:
        return
    if amount <= 0:
        return
    core.debts.create_debt(from_user, to_user, amount)
    await message.reply_text(f"долг записан: @{from_user}->@{to_user} {amount}")


async def calculate_debts(update: Update, _: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    total_debts = core.debts.calculate_total_debts(user)
    if not total_debts:
        message = 'Нет долгов'
    else:
        message = ""
        for user, debt in total_debts.items():
            is_incoming = debt < 0
            if is_incoming:
                message += f'@{user} мне {-debt}. \n'
            else:
                message += f'Я @{user} {debt}. \n'
    await update.message.reply_text(message)


async def pay_debts(update: Update, _: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    mentioned_user = __get_first_mentioned_user(update.message)
    if mentioned_user is None:
        core.debts.mark_all_debts_as_payed(user)
        message = 'Все долги погашены'
    else:
        core.debts.mark_debts_as_payed(user, mentioned_user)
        message = f'Долги с @{mentioned_user} погашены'
    await update.message.reply_text(message)


def start_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    application.add_handler(CommandHandler("calculate", calculate_debts))
    application.add_handler(CommandHandler("pay", pay_debts))
    # TODO: Debts history
    application.run_polling()
