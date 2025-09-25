import datetime


def compare_dates(sub_date: datetime.datetime) -> int | bool:
    if sub_date:
        date = str(sub_date).split(' ')[0].split('-')
        last_date = datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        remaining_date = str(last_date - datetime.date.today())
        try:
            days = int(remaining_date.split(' ')[0])
            return days
        except:
            return False