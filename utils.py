from datetime import datetime, timedelta


def normalize_data(data):
    return {key: value for key, value in data.items() if value is not None}  # eliminamos los valores None


def get_yesterday_date():
    return datetime.utcnow() - timedelta(1)


def get_today_date():
    return datetime.utcnow()


def get_formatted_date(date):
    return datetime.strftime(date, '%Y-%m-%d')
