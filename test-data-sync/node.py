import uuid
import vectorclock

class Node(object):
    def __init__(self, name=None):
        if id:
            self.name = name
        else:
            # generates from host ID, sequence number, and current time
            self.name = uuid.uuid1()

        self.clock = vectorclock.VectorClock()

    def __str__(self):
        return self.name
