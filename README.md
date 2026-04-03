# Project-Album

Album project built with Flask.

## Requirements

- Python 3
- `pip`

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run the app

Initialize the database:

```bash
python3 -m flask --app album init-db
```

Start the development server:

```bash
python3 -m flask --app album run --debug
```

Open the app in your browser at:

```text
http://127.0.0.1:5000
```

## Notes

- The database is stored in `database.db`.
- Running `init-db` resets the database because it recreates all tables.
