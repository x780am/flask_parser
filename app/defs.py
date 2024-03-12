
import calendar
import datetime
def get_now_unix():
    return str(calendar.timegm(datetime.datetime.utcnow().utctimetuple()))



if __name__ == "__main__":
    pass
