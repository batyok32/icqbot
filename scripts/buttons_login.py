from django.conf import settings
import json
import time
import string
import logging
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
from bot.filter import Filter
from random import randrange, choice, random
from main.models import Client, VpnKey
from datetime import date, datetime, timedelta
from django.db.models import Count, F, Value
from datetime import datetime, timedelta


default_markup = [
    [{"text": "Список", "callbackData": "list"}],
    [{"text": "Добавить", "callbackData": "add"}],
    [{"text": "Удалить", "callbackData": "delete"}],
    [{"text": "Посмотреть", "callbackData": "see"}],
    [{"text": "Изменить", "callbackData": "edit"}],
    #
    [{"text": "Заблокировать клиента", "callbackData": "lock"}],
    [{"text": "Разблокировать клиента", "callbackData": "unlock"}],
    #
    [{"text": "Оплатить клиента", "callbackData": "pay"}],
    [{"text": "Добавить выключенные дни", "callbackData": "closed_days"}],
]

add_buttons_markup = [
    [{"text": "Добавить клиента", "callbackData": "add_client", "style": "primary"}],
    [{"text": "Добавить впн", "callbackData": "add_vpn", "style": "primary"}],
]

list_buttons_markup = [
    [
        {
            "text": "1. Список клиентов и впнов",
            "callbackData": "list_all",
            "style": "primary",
        }
    ],
    [{"text": "2. Список впнов", "callbackData": "list_all_2", "style": "primary"}],
    [{"text": "3. Список пустых", "callbackData": "list_all_3", "style": "primary"}],
    [
        {
            "text": "4. Список просроченных",
            "callbackData": "list_all_4",
            "style": "primary",
        }
    ],
    [
        {
            "text": "5. Список неоплаченных",
            "callbackData": "list_all_5",
            "style": "primary",
        }
    ],
    [
        {
            "text": "6. Список заблокированных",
            "callbackData": "list_all_6",
            "style": "primary",
        }
    ],
]

# +

styles_all = (
    "Все типы стилей",
    [
        [{"text": "primary style", "callbackData": "nothing", "style": "primary"}],
        [{"text": "attention style", "callbackData": "nothing", "style": "attention"}],
        [{"text": "base style", "callbackData": "nothing", "style": "base"}],
    ],
)
#

adding_client_text = """
/add_client
Batyr
30
android / ios
150
yes
"""

adding_vpn_text = """
/add_vpn
1
30
android / ios
150
yes
"""

delete_client_text = """
/deleteclient 1
"""
delete_client_text_2 = """
/deletevpn b55
"""

see_client_text = """
/user 1
"""
see_vpn_text_2 = """
/vpn b55
"""

adding_errorly_text = """
/add_vpn | /add_client
1
30
android / ios
150
yes
"""

edit_vpn_text = """
/edit b5
"""


def sender(
    bot,
    chat_id=None,
    query_id=None,
    markup=None,
    message="",
    text="",
    alert=False,
    url="",
    separate_message="",
    parseMode="",
):
    logging.info(f"Invoked sender with args: {locals()}")
    if separate_message:
        if parseMode:
            bot.send_text(chat_id=chat_id, text=separate_message, parse_mode=parseMode)
        else:
            bot.send_text(chat_id=chat_id, text=separate_message)
    if markup:
        bot.send_text(
            chat_id=chat_id, text=message, inline_keyboard_markup=json.dumps(markup)
        )
    if query_id:
        bot.answer_callback_query(
            query_id=query_id, text=text, show_alert=alert, url=url
        )


def get_answer_by_text(bot, event):
    print("EVENT DATA", event.data)
    answer = "Привет!"
    markup = default_markup
    return sender(bot, chat_id=event.from_chat, message=answer, markup=markup)


def show_add_buttons(bot, event):
    answer = "Что добавить?"
    markup = add_buttons_markup
    return sender(bot, chat_id=event.from_chat, message=answer, markup=markup)


def show_list_buttons(bot, event):
    answer = "Что?"
    markup = list_buttons_markup
    return sender(bot, chat_id=event.from_chat, message=answer, markup=markup)


def show_delete_buttons(bot, event):
    sender(bot, chat_id=event.from_chat, separate_message=delete_client_text)
    return sender(bot, chat_id=event.from_chat, separate_message=delete_client_text_2)


def show_see_buttons(bot, event):
    sender(bot, chat_id=event.from_chat, separate_message=see_client_text)
    return sender(bot, chat_id=event.from_chat, separate_message=see_vpn_text_2)


def show_edit_buttons(bot, event):
    return sender(bot, chat_id=event.from_chat, separate_message=edit_vpn_text)


# CUSTOM


def list_users(bot, event):
    clients = Client.objects.all()

    sender(
        bot,
        chat_id=event.data["message"]["chat"]["chatId"],
        query_id=event.data["queryId"],
        separate_message=f"Clients: {clients}",
    )


def throw_back_to_adding(bot, event, message):
    bot.send_text(chat_id=event.data["chat"]["chatId"], text=message)
    bot.send_text(chat_id=event.data["chat"]["chatId"], text=adding_errorly_text)


def add_user(bot, event):
    print("ADDING USER")
    if "text" in event.data:
        if "/add_client" in event.data["text"]:
            text = event.data["text"][11:]
            data = text.split("\n")
            print("DATA", data)
            #
            name = data[1]
            time = data[2]
            mobile = data[3]
            price = data[4]
            paid = data[5]
            #
            if paid == "yes":
                paid = True
            else:
                paid = False
            #
            if not price:
                price = 150
            #
            client = Client.objects.create(name=name)
            client.save()
            print("CLIENT", client.id)
            #
            vpnkey = VpnKey.objects.filter(client__isnull=True).distinct().first()
            print("VPN KEY", vpnkey)
            vpnkey.client = client
            vpnkey.time = time
            vpnkey.start_date = datetime.now()
            vpnkey.finish_date = datetime.now() + timedelta(days=int(time))
            vpnkey.mobile = mobile
            vpnkey.price = int(price)
            vpnkey.paid = paid
            print("VPN KEY", vpnkey)
            vpnkey.save()
            #
            sender(
                bot,
                chat_id=event.data["chat"]["chatId"],
                separate_message=f"""
ID: {client.id}
Имя: {client.name}
Время: {time}
Время включения: {vpnkey.start_date}
Время выключения: {vpnkey.finish_date}
Код клиента: {vpnkey.name}
Устройство: {mobile}
Оплачено: {paid}
Цена: {price}
                """,
            )

        elif "/add_vpn" in event.data["text"]:
            text = event.data["text"][8:]
            data = text.split("\n")
            #
            id = data[1]
            time = data[2]
            mobile = data[3]
            price = data[4]
            paid = data[5]
            #
            if paid == "yes":
                paid = True
            else:
                paid = False
            #
            if not price:
                price = 150
            #
            client = Client.objects.get(id=id)
            #
            vpnkey = VpnKey.objects.filter(client__isnull=True).distinct().first()
            vpnkey.client = client
            vpnkey.time = time
            vpnkey.start_date = datetime.now()
            vpnkey.finish_date = datetime.now() + timedelta(days=int(time))
            vpnkey.mobile = mobile
            vpnkey.price = int(price)
            vpnkey.paid = paid
            vpnkey.save()
            #
            sender(
                bot,
                chat_id=event.data["chat"]["chatId"],
                separate_message=f"""
ID: {client.id}
Имя: {client.name}
Время: {time}
Время включения: {vpnkey.start_date}
Время выключения: {vpnkey.finish_date}
Код клиента: {vpnkey.name}
Устройство: {mobile}
Оплачено: {paid}
Цена: {price}
                """,
            )
        else:
            message = "Ты забыл прислать данные :)"
            throw_back_to_adding(bot, event, message)

    elif event.data["callbackData"] == "add_client":
        print("ADDING CLIENT")
        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=adding_client_text,
        )

    elif event.data["callbackData"] == "add_vpn":
        print("ADDING VPN")
        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=adding_vpn_text,
        )


def list_all(bot, event):
    if event.data["callbackData"] == "list_all":
        clients = Client.objects.all()
        big_text = ""
        for client in clients:
            vpns = VpnKey.objects.filter(client=client)
            vpns_text = ""
            for vpn in vpns:
                vpns_text += f"""
VPN:               *{vpn.name}*
Оплачено:          *{vpn.paid}*
Осталось времени:  *{vpn.remaining_days}*
Устройство:        {vpn.mobile}
Заблокировано:     {vpn.locked}
Время на открытие: {vpn.time}
Время открытия:    {vpn.start_date}
Время окончания:   {vpn.finish_date}
"""
            big_text += f"""
\nКлиент: {client.id}
------------------
{vpns_text}
"""
        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=big_text,
            parseMode="MarkdownV2",
        )
    elif event.data["callbackData"] == "list_all_2":
        vpns = VpnKey.objects.filter(client__isnull=False)
        big_text = ""
        for vpn in vpns:
            big_text += f"""
VPN:               *{vpn.name}*
------------------
Клиент:            *{vpn.client.id}*
Осталось времени:  *{vpn.remaining_days}*
Оплачено:          *{vpn.paid}*
Устройство:        {vpn.mobile}
Заблокировано:     {vpn.locked}
Время на открытие: {vpn.time}
Время открытия:    {vpn.start_date}
Время окончания:   {vpn.finish_date}
"""
        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=big_text,
            parseMode="MarkdownV2",
        )
    #
    elif event.data["callbackData"] == "list_all_3":
        vpns = VpnKey.objects.filter(client__isnull=True)
        big_text = ""
        for vpn in vpns:
            big_text += f"""{vpn.name}, """
        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=big_text,
            parseMode="MarkdownV2",
        )
    #
    elif event.data["callbackData"] == "list_all_4":
        vpns = VpnKey.objects.all()
        expired = []
        for v in vpns:
            if v.remaining_days <= 1:
                print("V[pn", v)
                expired.append(v)
        big_text = ""
        if len(expired) >= 1:
            print("PRINTING EXPIRED", expired)
            for vpn in expired:
                big_text += f"""
VPN:               *{vpn.name}*
------------------
Клиент:            *{vpn.client.id}*
Осталось времени:  __*{vpn.remaining_days}*__
Оплачено:          _*{vpn.paid}*_
Устройство:        {vpn.mobile}
Заблокировано:     {vpn.locked}
Время на открытие: {vpn.time}
Время открытия:    {vpn.start_date}
Время окончания:   {vpn.finish_date}
    """

        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=big_text,
            parseMode="MarkdownV2",
        )
    elif event.data["callbackData"] == "list_all_5":
        vpns = VpnKey.objects.filter(paid=False, client__isnull=False)

        big_text = ""
        if len(vpns) >= 1:
            print("PRINTING EXPIRED", vpns)
            for vpn in vpns:
                big_text += f"""
VPN:               *{vpn.name}*
Оплачено:          _*{vpn.paid}*_
------------------
Клиент:            *{vpn.client.id}*
Осталось времени:  __*{vpn.remaining_days}*__
Устройство:        {vpn.mobile}
Заблокировано:     {vpn.locked}
Время на открытие: {vpn.time}
Время открытия:    {vpn.start_date}
Время окончания:   {vpn.finish_date}
    """

        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=big_text,
            parseMode="MarkdownV2",
        )
    elif event.data["callbackData"] == "list_all_6":
        vpns = VpnKey.objects.filter(locked=True, client__isnull=False)

        big_text = ""
        if len(vpns) >= 1:
            print("PRINTING EXPIRED", vpns)
            for vpn in vpns:
                big_text += f"""
VPN:               *{vpn.name}*
Заблокировано:     _*{vpn.locked}*_
Осталось времени:  __*{vpn.remaining_days}*__
Оплачено:     {vpn.paid}
------------------
Клиент:            *{vpn.client.id}*
Устройство:        {vpn.mobile}
Время на открытие: {vpn.time}
Время открытия:    {vpn.start_date}
Время окончания:   {vpn.finish_date}
    """

        sender(
            bot,
            chat_id=event.data["message"]["chat"]["chatId"],
            separate_message=big_text,
            parseMode="MarkdownV2",
        )


def delete(bot, event):
    if "text" in event.data:
        if "/deleteclient" in event.data["text"]:
            text = event.data["text"][13:]
            data = text.split("\n")
            print("DATA", data)
            #
            name = data[0]

            client = Client.objects.get(id=name)
            client.delete()

            #
            sender(
                bot,
                chat_id=event.data["chat"]["chatId"],
                separate_message="Успешно! Клиент удален.",
            )

        elif "/deletevpn" in event.data["text"]:
            text = event.data["text"][10:]
            data = text.split("\n")
            print("DATA", data)

            #
            name = data[0]
            #
            vpnkey = VpnKey.objects.get(name=name)
            vpnkey.client = None
            #
            vpnkey.save()
            #
            sender(
                bot,
                chat_id=event.data["chat"]["chatId"],
                separate_message=f"Успешно! {id} - теперь свободен!",
            )
        else:
            message = "Ты забыл прислать данные :)"
            bot.send_text(chat_id=event.data["chat"]["chatId"], text=message)
            show_delete_buttons()


def see(bot, event):
    if "text" in event.data:
        if "/user" in event.data["text"]:
            text = event.data["text"][5:]
            data = text.split("\n")
            print("DATA", data)
            #
            id = data[0]

            client = Client.objects.get(id=id)
            big_text = ""
            vpns = VpnKey.objects.filter(client=client)
            vpns_text = ""
            for vpn in vpns:
                vpns_text += f"""
VPN:               *{vpn.name}*
Оплачено:          *{vpn.paid}*
Осталось времени:  *{vpn.remaining_days}*
Устройство:        {vpn.mobile}
Заблокировано:     {vpn.locked}
Время на открытие: {vpn.time}
Время открытия:    {vpn.start_date}
Время окончания:   {vpn.finish_date}
"""
            big_text += f"""
\nКлиент: {client.id}
------------------
{vpns_text}
"""
            sender(
                bot,
                chat_id=event.data["chat"]["chatId"],
                separate_message=big_text,
                parseMode="MarkdownV2",
            )

            #

        elif "/vpn" in event.data["text"]:
            text = event.data["text"][5:]
            data = text.split("\n")
            print("DATA", data)
            #
            name = data[0]

            big_text = ""
            try:
                vpn = VpnKey.objects.get(name=name, client__isnull=False)
                print("VPN", vpn)
                vpns_text = ""
                big_text += f"""
VPN:               *{vpn.name}*
------------------
Клиент:            *{vpn.client.id}*
Осталось времени:  *{vpn.remaining_days}*
Оплачено:          *{vpn.paid}*
Устройство:        {vpn.mobile}
Заблокировано:     {vpn.locked}
Время на открытие: {vpn.time}
Время открытия:    {vpn.start_date}
Время окончания:   {vpn.finish_date}
"""

                sender(
                    bot,
                    chat_id=event.data["chat"]["chatId"],
                    separate_message=big_text,
                    parseMode="MarkdownV2",
                )
            except:
                sender(
                    bot,
                    chat_id=event.data["chat"]["chatId"],
                    separate_message="This user is free or unexist!",
                )

        else:
            message = "Ты забыл прислать данные :)"
            bot.send_text(chat_id=event.data["chat"]["chatId"], text=message)
            show_see_buttons()


def edit(bot, event):
    print("EDITING VPN")
    if "text" in event.data:
        if "/edit" in event.data["text"]:
            text = event.data["text"][6:]
            data = text.split("\n")
            #
            name = data[0]
            if len(data) > 2:
                id = data[1]
                start_date = data[2]
                finish_date = data[3]
                mobile = data[4]
                price = data[5]
                paid = data[6]
                locked = data[7]
                #
                if paid == "yes" or paid == "True":
                    paid = True
                else:
                    paid = False
                #
                if locked == "yes" or locked == "True":
                    locked = True
                else:
                    locked = False

                #
                try:
                    client = Client.objects.get(id=id)
                    vpnkey = VpnKey.objects.get(name=name)
                    vpnkey.client = client
                    vpnkey.start_date = start_date
                    vpnkey.finish_date = finish_date
                    vpnkey.mobile = mobile
                    vpnkey.price = int(price)
                    vpnkey.paid = paid
                    vpnkey.locked = locked
                    vpnkey.save()
                    sender(
                        bot,
                        chat_id=event.data["chat"]["chatId"],
                        separate_message=f"""
Успешно!!!
VPN: {vpnkey.name}
------------------------
ID: {client.id}
Имя: {client.name}
Время включения: {vpnkey.start_date}
Время выключения: {vpnkey.finish_date}
Устройство: {mobile}
Оплачено: {paid}
Заблокировано: {locked}
Цена: {price}
                    """,
                    )
                except:
                    sender(
                        bot,
                        chat_id=event.data["chat"]["chatId"],
                        separate_message="Что-то не правильно!",
                    )
                #

            else:
                vpnkey = VpnKey.objects.get(name=name, client__isnull=False)
                message = f"""
/edit b5
{vpnkey.client.id} //client-id
{vpnkey.start_date} //start-date
{vpnkey.finish_date} //finish-date
{vpnkey.mobile} //mobile
{vpnkey.price} //price
{vpnkey.paid} //paid
{vpnkey.locked} //locked
                """
                sender(
                    bot,
                    chat_id=event.data["chat"]["chatId"],
                    separate_message=message,
                )
        else:
            message = "Ты забыл прислать данные :)"
            bot.send_text(chat_id=event.data["chat"]["chatId"], text=message)
            bot.send_text(chat_id=event.data["chat"]["chatId"], text=edit_vpn_text)


def launch_handlers(bot):
    #
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=show_add_buttons, filters=Filter.callback_data("add")
        )
    )
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=add_user, filters=Filter.callback_data_regexp(r"add_")
        )
    )
    bot.dispatcher.add_handler(
        MessageHandler(callback=add_user, filters=Filter.regexp(r"^/add"))
    )

    #
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=show_list_buttons, filters=Filter.callback_data("list")
        )
    )

    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=list_all, filters=Filter.callback_data_regexp(r"list_all")
        )
    )
    #
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=show_delete_buttons, filters=Filter.callback_data("delete")
        )
    )
    bot.dispatcher.add_handler(
        MessageHandler(callback=delete, filters=Filter.regexp(r"^/delete"))
    )
    #
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=show_see_buttons, filters=Filter.callback_data("see")
        )
    )
    bot.dispatcher.add_handler(
        MessageHandler(callback=see, filters=Filter.regexp(r"^/user"))
    )
    bot.dispatcher.add_handler(
        MessageHandler(callback=see, filters=Filter.regexp(r"^/vpn"))
    )

    #
    bot.dispatcher.add_handler(
        BotButtonCommandHandler(
            callback=show_edit_buttons, filters=Filter.callback_data("edit")
        )
    )
    bot.dispatcher.add_handler(
        MessageHandler(callback=edit, filters=Filter.regexp(r"^/edit"))
    )
