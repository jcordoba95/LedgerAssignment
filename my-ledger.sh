#!/bin/bash
python ledger.py --price-db prices_db \
-f index.ledger "$@"
