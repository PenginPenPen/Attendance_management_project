import datetime
today = datetime.date.today()
week_lsit=['月','火','水','木','金','土','日']
print(week_lsit[(today.weekday())])
