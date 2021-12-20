import telegram


def get_token():
    return ""


def get_chat_id():
    return "1706764133"


def send_message_to_chpark(message):
    try:
        bot = telegram.Bot(token=get_token())
        bot.sendMessage(chat_id=get_chat_id(), text=message)
        print("sending message to chpark")
    except Exception as e:
        print(e)
        return False
    return True
