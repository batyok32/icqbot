from bot.bot import Bot
from bot.handler import MessageHandler
from .buttons_login import get_answer_by_text, launch_handlers, list_users
from bot.filter import Filter


# TOKEN = "001.3580860311.4179257138:1006878718" #your token here
TOKEN = "001.4169137757.1244010991:1009179039"  # your token here

bot = Bot(token=TOKEN)


# def message_cb(bot, event):
#     print("EVENT DATA", event.data)
#     # if event.text == "start":
#     # print("LAUNCHING")
#     # else:
#     #     print("HAY DO")


def run():
    # bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
    bot.dispatcher.add_handler(
        MessageHandler(callback=get_answer_by_text, filters=Filter.regexp(r"^/start"))
    )

    # bot.dispatcher.add_handler(
    #     CommandHandler(callback=get_answer_by_text, filters=Filter.command("start"))
    # )
    launch_handlers(bot)
    bot.start_polling()
    bot.idle()
