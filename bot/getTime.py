import datetime

    #Convert string into an operatable time object
def todatetime(t):
    return datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')

    #Return time delta
def timeDif (t, k):
    return t-k

    #Convert the time delta into a separated integer -- hours, minutes, seconds
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return (hours-8), minutes, seconds

    #A function that:
    #Given a time in a string format '%Y-%m-%dT%H:%M:%S'
    #Returns a displayable arrival message with the time and time difference
def stringTime(t):
    if len(t)==0:
        return "No more bus services available"
    t = todatetime(t)
    dif = timeDif(t,datetime.datetime.now())
    hours, minutes, seconds = convert_timedelta(dif)
    if seconds > 30:
        minutes+=1
    if hours < 0:
        message = 'Arrived'
        return message
    elif hours == 0:
        if minutes == 1 or minutes == 0:
            message = "Coming in " + str(minutes) + " minute "
            return message
        else:
            message = "Coming in " + str(minutes) + " minutes"
            return message
    else:
        message = "Coming in "+ str(hours) + " hours " + str(minutes) + " minutes "
        return message
