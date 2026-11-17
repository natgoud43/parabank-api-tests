# Parabank API Tests
![Parabank API test suite](https://github.com/natgoud43/parabank-api-tests/actions/workflows/tests.yml/badge.svg)

Pytest + requests tests for the [Parabank](https://parabank.parasoft.com) demo bank's REST API.

## What the suite checks
- Existing customer response holds customer first name
- Every account returned for a customer belongs to that customer (customerId matches)
- Unknown customer id returns code 404 (not found).Expected by REST convention; see Known issues
- Negative id (-1) returns 400 (bad request); a non-numeric id (abc) returns 404 (no such path)

## Known issues (by design: xfail)
- For customer id "0" and "99999999" Parabank returns code 400

## Design notes
- **Assert rules, not snapshots.** Shared public demo server: data changes all the time, so tests check rules that always hold, not current values like counts or balances
- **One session for the whole run.** Headers are set once and one connection is reused for the whole run
- **Strict xfail.** Known issues are xfail(raises=AssertionError), so unrelated errors still show; xfail_strict makes an unexpected pass fail loudly

## How to run
```
pip install -r requirements.txt
python -m pytest
```