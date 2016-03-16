Requests-NBER
=============

Requests-NBER is a custom `Requests <http://requests.readthedocs.org/en/latest/>`_ class to log onto `NBER.org <https://www.nber.org>`_, the website of the American Economic Association.


Installation
------------

*Available soon!*
	
.. code-block:: bash

	$ pip install requests_nber


Documentation
-------------

Detailed documentation available at `www.erinhengel.com/software/requests-nber <http://www.erinhengel.com/software/requests-nber/>`_. 


Quickstart
----------

The ``NBER`` class logs onto `NBER.org <https://www.nber.org>`_ and establishes a connection with the host.
The ``session`` attribute returns a
`Request Session object <http://requests.readthedocs.org/en/latest/user/advanced/#session-objects>`_
with all the methods of the main `Requests API <http://requests.readthedocs.org/en/latest/>`_.


.. code-block:: python

    >>> from requests_nber import NBER
	
    # Establish NBER connection object.
    >>> deets = {'username': 'someuser', 'password': 'XXXX'}
    >>> conn = NBER(login=deets)
	
    # Download the HTML of the paper with document id t1.
    >>> doc_id = 't1'
    >>> html = conn.html(id=doc_id)
	
    # Download the document PDF.
    >>> pdf = conn.pdf(id=doc_id, file='article.pdf')
    
    # Download the bibliographic information.
    >>> biblio = conn.ref(id=doc_id)
	>>> biblio['doi']
	'10.3386/t0001'
    >>> biblio['author']
    'Seppo Honkapohja and Takatoshi Ito'

