import configparser
import datetime
import sqlite3
import threading
import time

from selenium import webdriver
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler


class RankUpdater(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.__scheduler = BackgroundScheduler()
        self.__config = configparser.ConfigParser()
        self.__config.read('update_config.ini')

    def __update(self):
        now_time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        print('start update on {}'.format(now_time))

        chrome_driver_path = self.__config.get('update', 'chromedriver')
        interval = self.__config.getint('update', 'interval')
        nba_div_class = self.__config.get('update', 'nba_div_class')

        driver = webdriver.Chrome(chrome_driver_path)
        driver.get('https://www.nba.com/standings')
        driver.implicitly_wait(10)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        update_data = []
        # 找到排名表格
        for i, east_west in enumerate(soup.findAll('div', {'class': str(nba_div_class)})):
            # 跳过east
            if i == 0:
                print('no east')
                continue
            for j, row in enumerate(east_west.findAll('tr')):
                # 跳过表头
                if j == 0:
                    print('no first line')
                    continue
                all_td = row.findAll('td')
                span_td = all_td[0].findAll('span')
                rank = span_td[0].text.strip()
                team = span_td[1].text.strip() + ' ' + span_td[2].text.strip()
                win = all_td[1].text.strip()
                loss = all_td[2].text.strip()

                update_data.append([rank, win, loss, team])
                #print('rank {:2} | team {:30} | win {:4} | loss {:4}'.format(rank, team, win, loss))
        # close chrome
        driver.quit()

        self.__update_db(update_data)

    def __update_db(self, rank_list):
        if not isinstance(rank_list, list):
            raise Exception('update only use list')
        try:
            connection = sqlite3.connect('./rank.db')
            cursor = connection.cursor()
            cursor.executemany('INSERT OR REPLACE INTO t_nba_rank(rank, win, loss, team) VALUES(?,?,?,?)', rank_list)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as ex:
            print("update e error, {}".format(ex))
        print('update db success')

    def do_jobs(self):
        interval = self.__config.getint('update', 'interval')
        self.__scheduler.add_job(self.__update, trigger='interval', minutes=interval, next_run_time=datetime.datetime.now())
        self.__scheduler.start()


if __name__ == '__main__':
    obj = RankUpdater()
    obj.do_jobs()
    while True:
        time.sleep(60 * 60)

