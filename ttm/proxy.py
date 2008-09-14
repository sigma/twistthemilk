__all__ = (
    'getProxy',
    )

from collections import deque

from twisted.internet import task
from twisted.web.client import getPage
from twisted.internet import defer

class RtmProxy():
    def __init__(self):
        self.queue = deque()
        self.loop = task.LoopingCall(self._getNextPage)
        self.loop.start(1.0) # call every second

    def _getNextPage(self):
        if len(self.queue) != 0:
            d = self.queue.pop()
            d.callback(None)

    def getPage(self, url):
        d = defer.Deferred()
        d.addCallback(lambda ignored: getPage(url))
        self.queue.appendleft(d)
        return d

RtmProxies = dict()

def getProxy(rtm):
    if rtm.apiKey in RtmProxies.keys():
        return RtmProxies[rtm.apiKey]
    else:
        proxy = RtmProxy()
        RtmProxies[rtm.apiKey] = proxy
        return proxy
