# Ledger Python implementation
This is my first approach to [Ledger CLI](https://www.ledger-cli.org/) implementation on python

## Requirements

To be able to run this project you will need a Python 3.0 or above.

### Steps
    1. Verify you have a valid python 3.0 (or above) installation running on your pc
    2. Clone git repository
    3. Read usage and examples
    4. Start having fun!

## Usage/Examples

```bash
  python3 ledger.py [command] [flag] [flag_value] [filename]
```
Current supported commands:

| Command |  Description                                      |
|:--------|:--------------------------------------------------|
|register | Prints out ledger transactions and a running total|
|print    | Prints out ledger transactions in a textual format|

Current supported flags:
| Flag    |  Description                                        | Accepted values                                                           | Required |
|:--------|:----------------------------------------------------|:--------------------------------------------------------------------------|:---------|
|--sort   | Sort transactions based on the specified value      | **d** / **date**: Sort transactions by date, from the oldest to the newest| No       |


This is how it would look like a command that prints out transactions in a textual format ordered by date from our file called filename.ledger

```bash
  python3 ledger.py print --sort d filename.ledger
```



## File format

Transactions must be specified into the next format:

```
; [comment]
yyyy/mm/dd [Description]
    [Concept]:[Description]     [Amount]
    [Concept]:[Description]     [Amount]
    ...
yyyy/mm/dd [Description]
    [Concept]:[Description]     [Amount]
    [Concept]:[Description]     [Amount]
    ...
```

### Example
```
; Bitcoin trades
2012/11/29 Purchased bitcoins
	Asset:Bitcoin Wallet   	15 BTC
	Bank:Paypal		$-300
2012/11/29 Some bitcoin transaction
	Asset:Bitcoin Wallet   	13 BTC
	Bank:Paypal		$-200
```

There are already some files into the project for you to run tests or learn more about how file format works.

IMPORTANT: Note that there aren't blank lines between transactions

## Some considerations

Currently this project only supports transactions from one file at a time.


## Roadmap

- Balance command support (Already under development)
- --price-db flag support
- --file flag support


## Authors

- [@devcydo](https://www.github.com/devcydo)

