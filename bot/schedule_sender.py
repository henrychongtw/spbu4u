# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sqlite3
from datetime import datetime, timedelta

import telebot

from bot.bots_constants import release_token
from bot import get_json_day_data, create_schedule_answer, \
    is_full_place, send_long_message


def schedule_sender(db_path="Bot.db"):
    bot = telebot.TeleBot(release_token)
    sql_con = sqlite3.connect(db_path)
    cursor = sql_con.cursor()
    cursor.execute("""SELECT id
                      FROM user_data
                      WHERE sending = 1""")
    data = cursor.fetchall()
    cursor.close()
    sql_con.close()

    tomorrow_moscow_datetime = datetime.today() + timedelta(days=1, hours=3)
    tomorrow_moscow_date = tomorrow_moscow_datetime.date()
    for user_data in data:
        user_id = user_data[0]
        json_day = get_json_day_data(user_id, tomorrow_moscow_date)
        full_place = is_full_place(user_id)
        answer = create_schedule_answer(json_day, full_place, user_id)
        if "Выходной" in answer:
            continue
        print(user_id, answer)
        try:
            answer = "Расписание на завтра:\n\n" + answer
            send_long_message(bot, answer, user_id)
        except Exception as err:
            print(err)
            continue


if __name__ == '__main__':
    schedule_sender()