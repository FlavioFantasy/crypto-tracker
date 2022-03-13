# crypto-tracker
a tracker for crypto portfolio

### Setup env
```bash
$ python3 -m venv venv

    linux: source venv/bin/activate
    win: .\venv\Scripts\activate.bat

$ pip install -r requirements.txt
$ pip install -e .

cp config.ini.template config.ini

$ tracker setup_all # create db and tables
```

### Use
```
$ tracker --help
Usage: tracker [OPTIONS] COMMAND [ARGS]...

  Set of commands to handle the db app

Options:
  --help  Show this message and exit.

Commands:
  add_coin              Add a coin to the db
  add_deposit           Add the deposit of coin to the db (transaction in)
  add_withdraw          Add the withdraw of coin to the db (transaction out)
  list_coins            List all coins.
  list_deposits         List all deposits.
  list_withdraws        List all withdraws.
  setup_all             Setup the app (create db)
  update_all            Do all updates necessary (coin_balances, prices...
  update_coin_balances  Add the coin balances in the db if needed (based...
  update_prices         Add the coins price for each date in the db if...
  update_tot_balances   Add the total balances of the portfolio (eur and...
```

## Examples
```bash
# add the coin you are interested in
$ tracker add_coin BTC Bitcoin bitcoin

# add deposit (or withdraws)
$ tracker add_deposit BTC 0.03 2021-11-26

# update manually
$ tracker update_coin_balances
$ tracker update_prices
$ tracker update_tot_balances

# or update all together
$ tracker update_all
```