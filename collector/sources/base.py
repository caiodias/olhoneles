from datetime import datetime

from logging import exception

import urllib
from urllib2 import urlopen, URLError, HTTPError
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import and_

from models import Legislator, Supplier, Expense

import models
Session = models.initialize('sqlite:///data.db')

def parse_money(string):
    string = string.replace('.', '')
    string = string.replace(',', '.')
    return float(string)

def parse_date(string):
    return datetime.strptime(string, '%d/%m/%Y').date()

class BaseCollector(object):
    debug = True

    def update_legislators(self):
        exception('Not implemented.')

    def update_data(self, year = datetime.now().year):
        exception('Not implemented.')

    def retrieve_uri(self, uri, data = None):
        resp = None

        try:
            if data == None:
                resp = urlopen(uri)
            else:
                resp = urlopen(uri, urllib.urlencode(data))
        except HTTPError, e:
            if e.getcode() != 404:
                raise HTTPError(e)
        except URLError:
            exception('Unable to retrieve: %s' % (uri))

        if resp == None:
            return None

        return BeautifulSoup(resp.read())

    def get_element_from_uri(self, uri, element, attrs = {}, data = None):
        content = self.retrieve_uri (uri, data)
        return content.find(element, attrs)