# Evidence Board

## Running the DB (PostgreSQL and PgAdmin)

```bash
docker compose up -d
```

## Running the API

```bash
python3.12 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
pip install -e .
python evidence/main.py
```

## Running the UI

```bash
cd board
npm install
npm run dev
```