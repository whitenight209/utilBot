from cgv import generate_telegram_message

if __name__ == "__main__":
    items = [{"date": '10', "value": "test12321321"}, {"date": '20', "value": "test2"}, {"date": '30', "value": "test3"}]
    print(generate_telegram_message(items))
