#-*- coding: utf-8 -*-

"""
Requests-NBER is a custom Requests class to log onto NBER.org, the website of the
National Bureau for Economic Research. Basic usage for returning a Requests session
object:
    
    >>> import requests_nber
    >>> deets = {'username': 'someuser', 'password': 'XXXX'}
    >>> conn = requests_nber.NBER(login=deets)
    >>> s = conn.session
    
The NBER class contains methods to download the webpage HTML, PDF
and bibliographic information of papers released as NBER working papers.
    
    >>> import requests_nber
    >>> doc_id = 't1'
    >>> conn = requests_nber.NBER(login=deets)
    >>> html = conn.html(id=doc_id)
    >>> ref = conn.ref(id=doc_id)
    >>> pdf = conn.pdf(id=doc_id, file='article.pdf')
    
Full documentation at <http://www.erinhengel.com/software/requests-nber>.

:copyright: (c) 2016 by Erin Hengel.
:license: Apache 2.0, see LICENSE for more details.
"""

__title__ = 'requests_nber'
__version__ = '0.0.1'
__author__ = 'Erin Hengel'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2016 Erin Hengel'


from .nber import *
