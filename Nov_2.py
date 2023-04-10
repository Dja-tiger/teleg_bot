import requests
import time
import telebot
from auth_data import tocen
from bs4 import BeautifulSoup as BS

# Создаем словарь для хранения старых цен продуктов
old_prices = {}

tocen = tocen

def telegram_bot(tocen):

    bot = telebot.TeleBot(tocen)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет друг")

    @bot.message_handler(content_types=["text"])
    def send_message(message):

        # context.job_queue.run_repeating(send_message(message), interval=10, first=0)
        if message.text.lower() == "price":
            try:
                while True:
                    url = "https://api.digiseller.ru/api/shop/products"
                    params = {
                        "transp": "cors",
                        "format": "json",
                        "lang": "ru-RU",
                        "seller_id": "1112881",
                        "category_id": "0",
                        "order": "name",
                        "currency": "RUB",
                        "rows": "500"
                    }

                    # Создаем список продуктов, которые будут отслеживаться
                    url1 = 'https://efrhew333.exaccess.com/'
                    response1 = requests.get(url1)
                    soup = BS(response1.text, "lxml")
                    tracked_products = [link.text for link in soup.select('div#digiseller-exaccess a')]

                    global old_prices
                    response = requests.get(url, params=params)

                    if response.status_code == 200:
                        products = response.json()["product"]
                        prices = {}

                        # Создаем словарь цен для текущего запроса
                        for product in products:
                            prices[product["name"]] = product["price"]

                        # Сравниваем цены текущего запроса с ценами предыдущего запроса
                        for product_name in tracked_products:
                            old_price = old_prices.get(product_name)
                            price = prices.get(product_name)
                            if old_price is not None and price is not None and old_price != price:
                                messagee = f"Изменение цены у продукта '{product_name}' с {old_price} на {price}"
                                bot.send_message(message.chat.id, text=messagee)

                            # else:

                            #     messageee = f"Не было изменение цены у продукта '{product_name}' с {old_price} на {price}"
                            #     bot.send_message(message.chat.id, text=messageee)

                        # Сохраняем цены текущего запроса в качестве старых цен для следующего запроса
                        old_prices = prices
                        time.sleep(600)

                    else:
                        print(f"Ошибка запроса: {response.status_code}")

            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, "Damn... Something was wrong..")

        else:
            bot.send_message(message.chat.id, "неправильная команда")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(tocen)

