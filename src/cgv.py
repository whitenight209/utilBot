from bs4 import BeautifulSoup
import requests
from lib.telegram import send_message_to_chpark
import time
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
import logging

logger = logging.getLogger(__name__)


def check_move_exists(movie_name, target_date):
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
            logger.debug(months)
            logger.debug(f'target month {date.month} not include')
            return
        logger.debug(days)
        logger.debug(str('%02d' % date.day))
        if str('%02d' % date.day) not in days:
            logger.debug(f'target day {date.day} not include')
            return

        items = soup.select("div > div.sect-showtimes > ul > li")
        for li in items:
            movie_already_show = li.select_one("div.info-movie > a > strong").text.strip()
            if movie_already_show != movie_name:
                continue

            logger.debug(movie_already_show)
            for theater in li.select("div.type-hall"):
                theater_type = theater.select_one("div.info-hall > ul > li").text.strip()
                if theater_type == 'IMAX LASER 2D':
                    theater_times = [{'time': screen_time.select_one('em').text.strip(), 'state': screen_time.select_one('span').text.strip()}
                                     for screen_time in theater.select("div.info-timetable > ul > li")]
                    for theater_time in theater_times:
                        logger.debug(theater_time['time'])
                        logger.debug(theater_time['state'])

                    if len(theater_time) > 0:
                        # send telegram message to bot
                        return True
        return False


if __name__ == "__main__":
    deploy_mode = sys.argv[1]
    target_date = sys.argv[2]
    logging_directory = sys.argv[3]
    message_send_count = 0
    logFile = "cgv_" + time.strftime("%Y%m%d-%H%M%S") + '.log'

    logger.setLevel(logging.DEBUG)
    if deploy_mode == 'production':
        handler = RotatingFileHandler(f'{logging_directory}/{logFile}', mode='a',
                                      maxBytes=50*1024*1024, backupCount=3, encoding=None, delay=False)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        logger.addHandler(logging.StreamHandler(sys.stdout))
    while True:
        if check_move_exists("스파이더맨-노 웨이 홈", target_date, 1):
            message_send_count += 1
        time.sleep(60)
        if message_send_count == 3:
            break
