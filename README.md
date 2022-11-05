# crypto-tracker
a tracker for crypto portfolio

## Initialize app
```bash
# create and activate venv (optional, but recomended)
$ python3 -m venv venv

linux: source venv/bin/activate
win:   .\venv\Scripts\activate.bat

# ------------------------------------------------------------------

# install
$ pip install -r requirements.txt
$ pip install -e .

# configure app
cp config.ini.template config.ini
# edit config.ini

# create db and tables
$ tracker init-db
```

## App structure
```
$ tracker help

Usage: tracker [OPTIONS] COMMAND [ARGS]...
                                          
    Set of commands to handle the db app  
                                          
Subcommands:                              
  - balance                      All regarding balances                                                                                      
    - list-coin-lasts            List last coin balances                                                                                     
    - list-tot-by-date           List total (EUR) balance by date                                                                            
  - coin                         All regarding coins                                                                                         
    - add                        Add a coin to the db                                                                                        
    - list                       List all coins                                                                                              
  - deposit                      All regarding deposits                                                                                      
    - add                        Register the deposit of a coin (transaction in)                                                             
    - list                       List all deposits                                                                                           
  - init-db                      Setup the app, creating sqlite db file and db tables                                                        
  - monthly-update               Add all missing data (coin_balances, prices and total_balances) and the eur graph and send Telegram messages
  - withdrawal                   All regarding withdrawals                                                                                   
    - add                        Register the withrawal of a coin (transaction out)
    - list                       List all withdrawals

```

## Usage examples
```bash
# add the coin you are interested in
$ tracker coin add BTC Bitcoin bitcoin

# add deposit (or withdrawal)
$ tracker deposit add BTC 0.03 2021-11-26

# update all data and send recap graph
$ tracker monthly-update
```