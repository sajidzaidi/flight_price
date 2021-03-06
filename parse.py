import json
from datetime import datetime

from flightprice import FlightInfo


def to_flight_info(tr, lst):
    out = []
    for f in lst:
        of = tr(f)
        if of is not None:
            out.append(of)
    return out

def southwest(text):
    flights = json.loads(text)
    def tr(f):
        # f = {'depart_time': '6:05 AM', 'stops': 'Nonstop', 'price': '$227', 'name': 'outbound_flightRow_1', 'arrive_time': '9:40 AM'}
        dt = datetime.strptime(f['depart_time'], '%I:%M %p')
        at = datetime.strptime(f['arrive_time'], '%I:%M %p')
        pr = f['price'].strip('$ ')
        if len(pr) == 0:
            return None

        if f['stops'] == 'Nonstop':
            ns = 0
        else:
            ns = int(f['stops'][0])

        return FlightInfo('southwest', dt.time(), at.time(), int(pr), ns, 0)

    return to_flight_info(tr, flights)


def hipmunk(text):
    flights = json.loads(text)

    def to_time(tstr):
        if ',' in tstr:
            parts = tstr.partition(',')
            dt = datetime.strptime(parts[2].strip(), '%I:%M%p').time()
            return (dt, parts[0].strip())
        else:
            dt = datetime.strptime(tstr, '%I:%M%p').time()
            return (dt, None)

    def tr(f):
        # f = {"arrive_time": "6:33pm", "depart_time": "3:16pm", "name": "Multiple AirlinesUnitedAlaska", "price": "838", "stops": "1 stop"}
        dt, dday = to_time(f['depart_time'])
        at, aday = to_time(f['arrive_time'])
        add_days = 1 if aday != dday else 0
        pr = int(f['price'])

        if f['stops'] == 'nonstop':
            ns = 0
        else:
            ns = int(f['stops'][0])

        return FlightInfo(f['name'], dt, at, pr, ns, add_days)

    return to_flight_info(tr, flights)


def bing(text):
    flights = json.loads(text)

    def to_time(tstr):
        return datetime.strptime(tstr + 'm', '%I:%M%p').time()

    def tr(f):
        # f = {"airline": "United", "arrive_time": "9:00a", "depart_time": "5:30a", "price": "$295", "stops": "0"}
        dt = to_time(f['depart_time'])
        at = to_time(f['arrive_time'])
        pr = int(f['price'].strip('$'))
        ns = int(f['stops'])

        return FlightInfo(f['airline'], dt, at, pr, ns, 0)

    return to_flight_info(tr, flights)
