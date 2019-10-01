import datetime


CHECKMARK = "fas fa-check-square"
RED_X = "&#10060;"


class Table:
    def __init__(self, name, ts):
        self.name = name
        self.ts = ts

        # compare ts of the table vs today
        if ts < datetime.date.today().strftime("%Y-%m-%d 00:00:00"):
            # table was not updated today
            self.good_to_go = False
        else:
            self.good_to_go = True


class Workflow:
    def __init__(self, name, updated_tf):
        self.name = name
        # updated_tf comes through as a string from redcap, convert too bool
        if updated_tf == "True":
            self.good_to_go = True
        else:
            self.good_to_go = False
