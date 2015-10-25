Development
===========

How do I contribute a new query?
--------------------------------
We will have a function in this API executable to generate a new data structure for adding to `nidm-query <https://github.com/incf-nidash/nidm-query>`_. This will work via command line, or via a web interface for you to input fields for your structure. We recommend that you use the generation functions to ensure accuracy in the format and fields of your data structure. You can then add it to the repo by submitting a pull request to add it. A pull request affords group discussion, and we will eventually have continuous integration that will run tests on your new query.


How do I develop the API?
-------------------------
You will want to fork the repo, clone the fork, and then run the flask application directly (so that it updates with changes to your code):


::

    git clone https://github.com/[username]/nidm-api
    cd nidm-api
    python setup.py install --user 
    python nidm/app.py



How does this work?
-------------------
Flask is a web framework (in python) that makes it ridiculously easy to do stuff with python in the browser. You can conceptually think of it like `Django <https://www.djangoproject.com/>`_ released wild and free from its mom's minivan. If you look at app.py, you will see a bunch of functions that return different views, and each view is associated with a particular url (with variables) that the user might want.  You should first `familiarize yourself with flask <flask.pocoo.org/docs/0.10/quickstart/>`_ before trying to develop with it.

Queries vs. API
'''''''''''''''
The queries are kept separate from the api itself, in the `nidm-query <https://github.com/incf-nidash/nidm-query>`_ repo. We did this because the world of writing sparql, and developing a web framework / API to serve the queries, are two separate things. A developer writing queries should be able to submit a PR to add a single file to the nidm-queries repo without needing to know about the nidm-api infrastructure. A developer working on the API shouldn't need to worry about the sparql side of things.

Application Logic
'''''''''''''''''
The basic application logic is as follows:

- The user installs the application with pip. This installs the python modules to the user's site-packages, but it also adds an executable, "nidm" to the users bin. This exectuable can be run to start the server instantly.
- Upon the creation of the server, the nidm-queries repo is downloaded to a temporary directory. This ensures that queries are up to date at the start of the server. If you are using the functions from within your application, you can download the repo to a location of your choice and specify the location in your application.
- The queries are json (ld) files. This just means they have a key called @context with some kind of stuff that semantic web folk understand. We are showing them as standard .json files because the .jsonld extension is not widely known, and could be confusing.
- The tool reads in all queries, and presents valid queries to the user at the base url of the server, localhost:8088. (Note that validation is not currently implemented). The user can select a query of choice based on the unique id, the "uid" variable in the json structure presented at localhost:8088.
- The user can then look at the details for a query by way of locahost:8088/api/[qid], or perform a query on a ttl file with localhost:8088/api/query/[qid]?ttl=[ttl_file]. The [ttl_file] can be a local path, or a URL. This is the extent of the tool thus far, it is still under development. 

Serving an API and web interfaces
---------------------------------
The url /api/[more-stuff-here] is linked up to serve a RESTful API, however the beauty of flask is that we can configure other URLs to do other interesting things. For example, /create might bring up an interactive web interface to write inputs to generate a new query object. /api/visual may be configured to return an interactive d3 or neo4j version of some part of the graph extracted from your ttl file. Having python and the infinite amount of web visualization technology at our fingertips makes the options really unlimited.
