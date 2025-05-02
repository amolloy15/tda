import time
import datetime
import yfinance as yf
import pandas as pd

from legacy.email import send


def main():
    spy = yf.Ticker('SPY')
    while True:
        data = spy.history('5d', '1d')
        data = cvtDF(data)

        emailBody = getEmailStr(data)

        if False:
            send(['amolloy.15@gmail.com'], 'monitoring', emailBody)
        else:
            print(emailBody)

        nextWeekday = getNextWeekday()
        nextCheck = datetime.datetime.combine(nextWeekday, datetime.time(hour=2))

        diff = (nextCheck - datetime.datetime.now()).total_seconds()
        print(f'Sleeping for {diff} until {nextCheck}')
        break
        time.sleep(diff)


def cvtDF(data: pd.DataFrame) -> dict:
    outDict = {}
    day0 = {}
    day1 = {}
    day2 = {}

    data = data.to_dict()

    day0['Close'] = data['Close'][list(data['Close'])[-3]]
    day0['date'] = list(data['Open'])[-3].to_pydatetime()

    day1['Open'] = data['Open'][list(data['Open'])[-2]]
    day1['Close'] = data['Close'][list(data['Close'])[-2]]
    day1['date'] = list(data['Open'])[-2].to_pydatetime()

    day2['Open'] = data['Open'][list(data['Open'])[-1]]
    day2['Close'] = data['Close'][list(data['Close'])[-1]]
    day2['date'] = list(data['Open'])[-1].to_pydatetime()

    outDict['day0'] = day0
    outDict['day1'] = day1
    outDict['day2'] = day2

    return outDict


def getEmailStr(data: dict) -> str:
    date0 = data['day0']['date'].date()
    day0Close = round(data['day0']['Close'], 2)

    date1 = data['day1']['date'].date()
    day1Close = round(data['day1']['Close'], 2)
    day1Change = round(data['day1']['Close'] - data['day0']['Close'], 2)
    day1Pct = round(day1Change / data['day1']['Open'] * 100, 2)

    date2 = data['day2']['date'].date()
    day2Close = round(data['day2']['Close'], 2)
    day2Change = round(data['day2']['Close'] - data['day1']['Close'], 2)
    day2Pct = round(day2Change / data['day2']['Open'] * 100, 2)

    outStr = ''
    outStr += f'{date0} close: {day0Close}\n'
    outStr += f'\t\tchange: {day1Change} | {day1Pct}%\n'
    outStr += f'{date1} close: {day1Close}\n'
    outStr += f'\t\tchange: {day2Change} | {day2Pct}%\n'
    outStr += f'{date2} close: {day2Close}'

    return outStr


def getNextWeekday(now: datetime.datetime = datetime.datetime.now()) -> datetime.date:
    nextWeekday = now.date() + datetime.timedelta(days=1)

    while nextWeekday.weekday() in [5, 6]:  # skip Saturday and Sunday
        nextWeekday = nextWeekday + datetime.timedelta(days=1)

    return nextWeekday


if __name__ == '__main__':
    main()
