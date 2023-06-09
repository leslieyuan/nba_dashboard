import datetime
import os
import sqlite3
import sys

import pandas as pd
import pyvibe as pv
from flask import Flask

app = Flask(import_name=__name__)
app.config["CACHE_TYPE"] = "null"
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = datetime.timedelta(seconds=1)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=10)


@app.route('/', methods=['GET', 'POST'])
def home():
    page = pv.Page()
    page.add_header("NBA WEST rank board")

    data = get_rank_data_from_db(west=True)
    columns = ['rank', 'team', 'win', 'loss']

    df = pd.DataFrame(data, columns=columns)
    page.add_pandastable(df)
    return page.to_html()


@app.route('/east', methods=['GET', 'POST'])
def east_rank():
    page = pv.Page()
    page.add_header("NBA EAST rank board")
    page.add

    data = get_rank_data_from_db(west=False)
    columns = ['rank', 'team', 'win', 'loss']

    df = pd.DataFrame(data, columns=columns)
    page.add_pandastable(df)
    return page.to_html()


@app.route('/pics', methods=['GET', 'POST'])
def pics():
    page = pv.Page()
    page.add_header("Pictures from AI")
    cc = page.add_container(grid_columns=3)
    card1 = cc.add_card()
    card2 = cc.add_card()
    card3 = cc.add_card()
    card4 = cc.add_card()
    card5 = cc.add_card()
    card6 = cc.add_card()

    card1.add_image(url='https://raw.githubusercontent.com/leslieyuan/leslieyuan.github.io/master/pics/cat_on_wall.png',
                   alt='cat on wall')
    card2.add_image(url='https://github.com/leslieyuan/leslieyuan.github.io/blob/master/pics/dolphin_1.png?raw=true',
                   alt='dolphin')
    card3.add_image(url='https://github.com/leslieyuan/leslieyuan.github.io/blob/master/pics/dolphin_2.png?raw=true',
                   alt='dolphin')
    card4.add_image(url='https://github.com/leslieyuan/leslieyuan.github.io/blob/master/pics/cat_1.png?raw=true',
                    alt='cat')
    card5.add_image(url='https://github.com/leslieyuan/leslieyuan.github.io/blob/master/pics/dolphin_3.png?raw=true',
                    alt='dolphin')
    card6.add_image(url='https://github.com/leslieyuan/leslieyuan.github.io/blob/master/pics/woman_1.png?raw=true',
                    alt='woman')

    return page.to_html()


def get_rank_data_from_db(west=True):
    data = []
    connection, cursor = None, None
    try:
        connection = sqlite3.connect('./service/rank.db')
        cursor = connection.cursor()
        if west:
            cursor.execute('SELECT rank, team, win, loss FROM t_nba_rank WHERE east_west=1')
        else:
            cursor.execute('SELECT rank, team, win, loss FROM t_nba_rank WHERE east_west=0')
        for rank, team, win, loss in cursor.fetchall():
            data.append([rank, team, win, loss])
    except Exception as ex:
        print(ex)
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

    return data


def daemonize(b_stat):
    if not b_stat:
        return
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
    os.chdir("/")
    os.setsid()
    os.umask(0)

    # second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()


if __name__ == '__main__':
    # run
    #daemonize(True)
    app.run(host='0.0.0.0', port=31758, debug=False)
