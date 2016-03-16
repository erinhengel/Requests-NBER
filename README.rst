Requests-AEAweb
===============

Requests-AEAweb is a custom `Requests <http://requests.readthedocs.org/en/latest/>`_ class to log onto `AEAweb.org <https://www.aeaweb.org>`_, the website of the American Economic Association.


Installation
------------
	
.. code-block:: bash

	$ pip install requests_aeaweb


Documentation
-------------

Detailed documentation available at `www.erinhengel.com/software/requests-aeaweb <http://www.erinhengel.com/software/requests-aeaweb/>`_. 


Quickstart
----------

The ``AEAweb`` class logs onto `AEAweb.org <https://www.aeaweb.org>`_ and establishes a connection with the host.
The ``session`` attribute returns a
`Request Session object <http://requests.readthedocs.org/en/latest/user/advanced/#session-objects>`_
with all the methods of the main `Requests API <http://requests.readthedocs.org/en/latest/>`_.


.. code-block:: python

    >>> from requests_aeaweb import AEAweb
	
    # Establish AEAweb connection object.
    >>> deets = {'username': 'someuser', 'password': 'XXXX'}
    >>> conn = AEAweb(login=deets)
	
    # Use session attribute to access Requests methods.
    >>> url = '{}/articles.php'.format(conn.url)
    >>> payload = {'doi': '10.1257/aer.20130626'}
    >>> request = conn.session.get(url, params=payload)
    >>> request.status_code
    200
	
    # Do stuff with your request object.
    >>> from bs4 import BeautifulSoup
    >>> soup = BeautifulSoup(request.text, 'html.parser')
    >>> soup.title
    'AEAweb: AER (106,3) p. 525 - University Differences in the Graduation of Minorities in STEM Fields: Evidence from California'


The ``AER`` subclass contains the ``html``, ``pdf`` and ``ref`` methods to download the webpage HTML, PDF and bibliographic
information of articles published in the *American Economic Review*.

.. code-block:: python
    
    >>> from requests_aeaweb import AER
	
    # Establish AEAweb connection object via AER.
    >>> conn = AER(login=deets)
	
    # Download the HTML of the article with document id 10.1257/aer.20140289.
    >>> doc_id = '10.1257/aer.20140289'
    >>> html = conn.html(id=doc_id)
	
    # Download the document PDF.
    >>> pdf = conn.pdf(id=doc_id, file='article.pdf')
    
    # Download the bibliographic information.
    >>> biblio = conn.ref(id=doc_id)
    >>> biblio['Authors']
    [{'Affiliation': 'Johns Hopkins U', 'Name': 'Korinek, Anton'}, {'Affiliation': 'MIT', 'Name': 'Simsek, Alp'}]

