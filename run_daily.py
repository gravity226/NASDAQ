from datetime import datetime
from threading import Timer

def add_time():
    x=datetime.today()
    y=x.replace(second=x.second+5, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds+1

    return secs

def to_repeat():
    secs = add_time()
    t = Timer(secs, to_repeat)
    t.start()
