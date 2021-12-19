import sys, time
from bs4 import BeautifulSoup
import requests
from lib.telegram import send_message_to_chpark
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)


def parse_digital_black_smith(target_date):
    url = "https://digital-blacksmithshop.com/program/calendar?v2=1"
    response = requests.get(url)
    if response.status_code != 200:
        return
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    dates = soup.select("table.table_program_calendar > tr > td")
    for date in dates:
        if not date.select_one("div.date_num_active"):
            continue
        date = int(date.select_one("div.date_num_active").text.strip())
        if date == target_date:
            message = f'black smith date {date} target date {target_date} to date matched'
            logger.debug(message)
            send_message_to_chpark(message)


if __name__ == "__main__":
    target_day = sys.argv[1]
    logging_directory = sys.argv[2]

    logFile = 'black_smith-' + time.strftime("%Y%m%d-%H%M%S") + '.log'
    handler = RotatingFileHandler(f'{logging_directory}/{logFile}', mode='a',
                                  maxBytes=50*1024*1024, backupCount=3, encoding=None, delay=False)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    while True:
        logger.debug("start parse digital black smith")
        parse_digital_black_smith(target_day)
        time.sleep(60)


