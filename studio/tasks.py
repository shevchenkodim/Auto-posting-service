from Auto_posting_service.celery import app

@app.task
def live_journal_task(a, b):
    c = a + b
    return c

@app.task
def telegram_task(a, b):
    c = a + b
    return c
