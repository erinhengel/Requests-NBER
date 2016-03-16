# -*- coding: utf-8 -*-

import sys
import traceback
import re
import getpass
from bs4 import BeautifulSoup
import requests
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class NotFoundError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg
    
    def __str__(self):
        return repr('{} {}'.format(self.expr, self.msg))

class NBER(object):
    """ Creates a custom Requests class to authenticate AEAweb user.
        Requests Session object stored in session attribute for reuse.
    """
    
    def __init__(self, login={}):
        
        # Ask for username and password if not supplied.
        if 'username' not in login:
            login['username'] = input('username: ')
        if 'password' not in login:
            login['password'] = getpass.getpass(stream=sys.stderr, prompt='password: ')
        
        login['post_login_url'] = None
        
        # Start session and store in session attribute.
        self.session = requests.Session()
        
        # Root site.
        nber_site = 'https://www.nber.org'
        nber_login = '{}/login/login'.format(nber_site)
        
        post = self.session.post(nber_login, data=login)

        # Save destination URL.
        self.url = nber_site
    
    def number(self, id):
        """ Find correct report number from document's webpage. """
        
        # Go to webpage of given ID.
        request = self.session.get('{}/papers/{}'.format(self.url, id))
        soup = BeautifulSoup(request.text, 'html.parser')
        
        # If webpage does not exit, return NotFoundError error.
        title = soup.title.text
        if title == 'Paper Not Found' or title == 'Page Missing':
            raise NotFoundError(id, 'not found.')
        
        # Correct report number is in meta data of returned html. 
        number = soup.find(attrs={'name':'citation_technical_report_number'})['content']
        return number
    
    def html(self, id):
        """ Download html of document's webpage. """
        request = requests.get('{}/papers/{}'.format(self.url, self.number(id=id)))
        return request.text
        
    def pdf(self, id, file=None):
        """ Download PDF of document.
            If file supplied, save to local disk. """
            
        request = self.session.get('{}/papers/{}.pdf'.format(self.url, self.number(id=id)))
        if 'application/pdf' in request.headers['Content-Type']:
            mypdf = request.content
            if file:
                with open(file, 'wb') as fh:
                    fh.write(mypdf)
            return mypdf
        # If webpage does not exit, return NotFoundError error.
        else:
            raise NotFoundError(number, 'PDF not found.')
    
    # Return bibliographic information for document.
    def ref(self, id, published=False, standardised=False):
        """ Download bibliographic data of document. """
        
        # Set up BibTeX parser.
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        
        # Get correct document report number.
        number = self.number(id=id)
        
        # Get bibtex file and parse.
        request = requests.get('{}/papers/{}.bib'.format(self.url, number))
        text = request.content.decode('utf8').replace(u'\xa0', u' ')
        bibtex = bibtexparser.loads(text, parser=parser).entries[0]
        
        # If 'published' keyword is true, fetch information on where document
        # was eventually published.
        if published:
            request = requests.get('{}/papers/{}'.format(self.url, number))
            soup = BeautifulSoup(request.text, 'html.parser')
            bibtex['published'] = soup.find(attrs={'id': 'published_line'})
            
            # Clean up returned text (get rid of extra spaces).
            if bibtex['published']:
                bibtex['published'] = ' '.join(bibtex['published'].text.strip().split())
        
        # If 'standardised' keyword is true, return dictionary with common keywords.
        if standardised:
            standard = {
                'NberID': bibtex['ID'][4:],
                'Abstract': ' '.join(bibtex['abstract'].strip().split()),
                'Month': bibtex['month'].strip(),
                'Year': int(bibtex['year']),
                'Title': ' '.join(bibtex['title'].strip().split()),
                'Authors': []
            }
            
            # All authors appear to be separated by 'and'.
            authors = bibtex['author'].split(' and ')
            for author in authors:
                standard['Authors'].append({'Name': author})
            
            # Sometimes, the 'month' keyword returns the year for documents released
            # in January.
            if re.match('^\d{4}$', standard['Month']):
                standard['Month'] = 'January'
            
            if 'published' in bibtex:
                standard['Published'] = bibtex['published']
            
            bibtex = standard
        
        return bibtex

