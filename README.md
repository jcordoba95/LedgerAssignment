# Ledger Assignment

> Ledger

This is my implementation of a Ledger in python supporting the commands "--price-db", "-f", "--sort", "balance", "print" and "register"

## Install

This project uses [python](https://www.python.org/) and libraries contained in the "requirements.txt" file. Go check them out if you don't have them locally installed.

```sh
$ pip install -r requirements.txt
```

## Usage
To execute the Ledger run the following command to execute the .sh file:

```sh
$ ./my-ledger.sh
# This by itself does nothing. You must run it with other commands.
```

### Commands
These are the following commands supported by the Ledger:
#### Print
The print command prints out ledger transactions in a textual format that can be parsed by Ledger. 
```sh
$ ./my-ledger.sh print
```
#### Register
The register command displays all the postings occurring in a single account, line by line.
```sh
$ ./my-ledger.sh register
```
#### Balance
The balance command takes no extra arguments and shows the current balance in every account.
```sh
$ ./my-ledger.sh balance
```
### Flags
This is the only supported flag by the ledger:
#### Sort
"--sort date" sorts the "print" and "register" command's transactions by date.
For example this is the command needed to be ran in order to sort the "print" transactions by date:

```sh
$ ./my-ledger.sh --sort date print
```


## License

