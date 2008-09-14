__all__ = (
    'Rtm',
    'RtmLog',
    )

import new
import logging
import urllib
from md5 import md5


from twisted.internet import reactor
from twisted.internet import defer

from ttm.proxy import getProxy
from ttm.api import API

import simplejson

logging.basicConfig()
RtmLog = logging.getLogger(__name__)
RtmLog.setLevel(logging.INFO)

SERVICE_URL = 'http://api.rememberthemilk.com/services/rest/'
AUTH_SERVICE_URL = 'http://www.rememberthemilk.com/services/auth/'


class RtmError(Exception): pass

class RtmApiError(RtmError): pass

class AuthStateMachine(object):

    class NoData(RtmError): pass

    def __init__(self, states):
        self.states = states
        self.data = {}

    def dataReceived(self, state, datum):
        if state not in self.states:
            raise RtmError, "Invalid state <%s>" % state
        self.data[state] = datum

    def get(self, state):
        if state in self.data:
            return self.data[state]
        else:
            raise AuthStateMachine.NoData, 'No data for <%s>' % state

class Rtm():

    def __init__(self, apiKey, secret, token=None, validator=None):
        self.apiKey = apiKey
        self.secret = secret
        self.authInfo = AuthStateMachine(['frob', 'token'])
        self.proxy = getProxy(self)

        self.validationFunction = validator

        # this enables one to do 'rtm.tasks.getList()', for example
        for prefix, attributes in API.items():
            setattr(self, prefix,
                    RtmApiCategory(self, "rtm." + prefix, attributes))

        if token:
            self.authInfo.dataReceived('token', token)

    def _sign(self, params):
        "Sign the parameters with MD5 hash"
        pairs = ''.join(['%s%s' % (k,v) for k,v in self._sortedItems(params)])
        return md5(self.secret+pairs).hexdigest()

    def _sortedItems(self, dictionary):
        "Return a list of (key, value) sorted based on keys"
        keys = dictionary.keys()
        keys.sort()
        for key in keys:
            yield key, dictionary[key]

    def _openURL(self, url, queryArgs=None):
        if queryArgs:
            url = url + '?' + urllib.urlencode(queryArgs)
        RtmLog.debug("URL> %s", url)
        return self.proxy.getPage(url)

    def readJson(self, json):
        RtmLog.debug("JSON> response: \n%s" % json)

        data = DottedDict('ROOT', simplejson.loads(json))
        rsp = data.rsp

        if rsp.stat == 'fail':
            raise RtmApiError, 'API call failed - %s (%s)' % (
                rsp.err.msg, rsp.err.code)
        else:
            return rsp

    def handleApiError(self, f):
        RtmLog.debug("API> got exception: %s", f.getTraceback())
        f.trap(RtmApiError)

    def get(self, **params):
        "Get the XML response for the passed `params`."
        params['api_key'] = self.apiKey
        params['format'] = 'json'
        params['api_sig'] = self._sign(params)

        return self._openURL(SERVICE_URL, params).addCallback(self.readJson).addErrback(self.handleApiError)

    def getNewFrob(self):
        rsp = self.get(method='rtm.auth.getFrob')
        return rsp.addCallback(lambda d: self.initFrob(d.frob))

    def initFrob(self, frob):
        self.authInfo.dataReceived('frob', frob)
        RtmLog.debug("Auth> initialized frob to %s", frob)
        return frob

    def getAuthURL(self, frob = None):
        RtmLog.debug("Auth> asking for Auth URL with frob = %s", frob)
        if frob is None:
            try:
                frob = self.authInfo.get('frob')
            except AuthStateMachine.NoData:
                return self.getNewFrob().addCallback(self.getAuthURL)

        params = {
            'api_key': self.apiKey,
            'perms'  : 'delete',
            'frob'   : frob
            }
        params['api_sig'] = self._sign(params)
        url = AUTH_SERVICE_URL + '?' + urllib.urlencode(params)
        RtmLog.debug("Auth> auth url computed : %s", url)

        if self.validationFunction is not None:
            RtmLog.debug("Validate> using custom validator")
            return self.validationFunction(url)
        else:
            RtmLog.debug("Validate> skipping validation")
            return defer.succeed(url)

    def getToken(self):
        RtmLog.debug("getToken> getting token")
        frob = self.authInfo.get('frob')
        rsp = self.get(method='rtm.auth.getToken', frob=frob)
        return rsp.addCallback(lambda d: self.initToken(d.auth.token))

    def initToken(self, token):
        self.authInfo.dataReceived('token', token)
        return token

    def ensureValidToken(self):
        try:
            token = self.authInfo.get('token')
        except AuthStateMachine.NoData:
            token = None

        if token is not None:
            return defer.succeed(token)
        else:
            return self.getAuthURL().addCallback(lambda res: self.getToken())

class RtmApiCategory:
    "See the `API` structure and `RTM.__init__`"

    def __init__(self, rtm, prefix, attributes):
        self.rtm = rtm
        self.prefix = prefix

        for name in attributes.keys():
            definition = attributes[name]
            if type(definition) is dict:
                setattr(self, name, RtmApiCategory(self.rtm, self.prefix + '.' + name, definition))
            else:
                aname = '%s.%s' % (self.prefix, name)
                rargs, oargs = definition
                func = self.makeMethod(aname, rargs, oargs)
                setattr(self, name, func) 

    def makeMethod(self, name, required, optional):
        return lambda **params: self.callMethod(name, required, optional, **params)

    def callMethod(self, aname, rargs, oargs, **params):
        # Sanity checks
        for requiredArg in rargs:
            if requiredArg not in params:
                raise TypeError, 'Required parameter (%s) missing' % requiredArg

        for param in params:
            if param not in rargs + oargs:
                warnings.warn('Invalid parameter (%s)' % param)

        return self.rtm.get(method=aname,
                            auth_token=self.rtm.authInfo.get('token'),
                            **params)

class DottedDict(object):
    "Make dictionary items accessible via the object-dot notation."

    def __init__(self, name, dictionary):
        self._name = name

        if type(dictionary) is dict:
            for key, value in dictionary.items():
                if type(value) is dict:
                    value = DottedDict(key, value)
                elif type(value) in (list, tuple) and key != 'tag':
                    value = [DottedDict('%s_%d' % (key, i), item)
                             for i, item in self._indexed(value)]
                setattr(self, key, value)

    def _indexed(self, seq):
        index = 0
        for item in seq:
            yield index, item
            index += 1

    def __repr__(self):
        children = [c for c in dir(self) if not c.startswith('_')]
        return 'dotted <%s> : %s' % (
            self._name,
            ', '.join(children))
