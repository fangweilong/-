# -*- coding:utf-8 -*-

import requests
import datetime

# 今天的日期
today = datetime.datetime.today()

thisYear = today.year
nextYear = today.year + 1

# 接口地址
holidayUrl = "https://timor.tech/api/holiday/year/{}?type=Y&week=N"

# 下一个节假日
nextHolidayUrl = "https://timor.tech/api/holiday/next/{}?type=Y&week=Y".format(today.date())

# 假期的数组，不包含周末
holidaysAllJson = {}

printStr = "[高级摸鱼办提醒您]:今天是{}周{}.\n" \
           "工作再累，一定不要忘记摸鱼哦！有事没事起身去茶水间，去厕所，去廊道走走别老在工位上坐着，钱是老板的,但命是自己的。\n".format(
    datetime.datetime.strftime(today, '%Y年%m月%d日'), today.weekday())

printEndStr = "工作996，生病ICU。\n" \
              "工作955，work–life balance。\n" \
              "工作 944，生活为先."


# 计算今天以后的节假日
def todayAfterHolidays():
    global printStr
    for key in holidaysAllJson.keys():
        holidayDate = datetime.datetime.strptime(holidaysAllJson[key].get("time")[0], '%Y-%m-%d')
        if today < holidayDate:
            distanceDays = (holidayDate - today).days
            printStr += "距离{}年{}还有{}天\n".format(holidayDate.year, key, distanceDays)


# 获取今年的假期，包含周日和调休
def getHolidays():
    global holidaysAllJson, holidayUrl

    # 首先判断下个节假日是不是明年的
    nextHolidaysJson = requests.get(nextHolidayUrl).json()
    if nextHolidaysJson.get("code") == 0:
        nextHolidayData = nextHolidaysJson.get("holiday").get("date")
        nextHolidayYear = datetime.datetime.strptime(nextHolidayData, '%Y-%m-%d').year
        if thisYear < nextHolidayYear:
            holidayUrl = holidayUrl.format(nextYear)
        else:
            holidayUrl = holidayUrl.format(thisYear)
    else:
        print("获取远程失败")
        return

    holidaysJson = requests.get(holidayUrl).json()

    if holidaysJson.get("code") == 0:
        holidaysTypeJson = holidaysJson.get("type")
        for key, val in holidaysTypeJson.items():
            if val.get("type") == 2:
                holidayName = val.get("name")
                if holidayName in holidaysAllJson.keys():
                    holiday = holidaysAllJson[holidayName]
                    holiday.get("time").append(key)
                    holidaysAllJson[holidayName] = holiday
                else:
                    holiday = {"time": [key], "week": val.get("week")}
                    holidaysAllJson[holidayName] = holiday


if __name__ == '__main__':
    getHolidays()
    todayAfterHolidays()

    print(printStr + printEndStr)
