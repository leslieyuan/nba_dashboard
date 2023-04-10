# nba_dashboard
<img width="1544" alt="image" src="https://user-images.githubusercontent.com/2480615/230000782-20f7e594-a1c9-4c14-b664-566a11f652a3.png">

a very simple web show the rank of NBA on regular season.

route / display west.

route /east display east.

use [PyVibe](https://github.com/pycob/pyvibe)

# dependencies
install newest [Chrome](https://www.google.com/chrome/)

install [ChromeDriver](https://chromedriver.chromium.org/downloads) of the same as Chrome version

other python dependents in directory `deploy`, will auto install when deploy the app.

# config
the config file on server/update_config.ini default be like:
```shell
[update]
interval=60
chromedriver=/Users/leslieyuan/Downloads/chromedriver_mac64/chromedriver
nba_div_class=Crom_container__C45Ti crom-container
```

1.interval means how often you want the rank board to update.

2.chromedriver is your server's chromedriver absolutely path.

3.nba_div_class is the website on NBA official when we get the data, it may changed some day.

# deploy
unzip the package, run
```shell
sh deploy/deploy.sh [debug]
```
the server will run on 31758 port by default, and the rank_updater server will run on background.

# debug
when run
```shell
sh deploy/deploy.sh debug
```
the web app will not run background, but the **rank_updater server not**.

