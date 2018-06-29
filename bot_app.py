# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from bot import bot
from app import create_app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        bot.remove_webhook()
        bot.polling(none_stop=True, interval=0)
