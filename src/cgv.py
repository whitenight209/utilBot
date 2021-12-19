from bs4 import BeautifulSoup
import requests
from lib.telegram import send_message_to_chpark
import time
import sys
from datetime import datetime

def check_move_exists(movie_name, target_date, theater_code):
    url = f'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx/iframeTheater.aspx?areacode=01&theatercode=0013&date={target_date}&screencodes=&screenratingcode=&regioncode='
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        date_items = soup.select("#slider > div:nth-child(1) > ul > li")
        months = [item.select_one("div > a > span").text.strip()[:-1] for item in date_items]
        days = [item.select_one("div > a > strong").text.strip() for item in date_items]
        date = datetime.strptime(target_date, "%Y%m%d")

        if str(date.month) not in months:
            print(months)
            print(f'target month {date.month} not include')
            return
        print(days)
        print(str('%02d' % date.day))
        if str('%02d' % date.day) not in days:
            print(f'target day {date.day} not include')
            return

        items = soup.select("div > div.sect-showtimes > ul > li")
        for li in items:
            movie_already_show = li.select_one("div.info-movie > a > strong").text.strip()
            if movie_already_show != movie_name:
                continue
            print(movie_already_show)
            return send_message_to_chpark(movie_name)
        return False


if __name__ == "__main__":
    target_date = sys.argv[1]
    message_send_count = 0
    while True:
        if check_move_exists("듄", target_date, 1):
            message_send_count += 1
        time.sleep(60)
        if message_send_count == 3:
            break
