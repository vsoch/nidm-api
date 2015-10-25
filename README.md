# nidm-api

* under development *

[documentation](http://nidm-api.readthedocs.org/)

This is an application to query and visualize nidm data structures, including workflow, experiment, and results. This repo contains a python module that can serve as a standalone application to work with [nidm-queries](https://github.com/incf-nidash/nidm-queries).

Functions will be provided to do the following:

- perform a query on an NIDM turtle file, returning the format of your choice (text and graphical)
- a web interface to generate a new query to add to the database
- validation of query data structures

#### Installation

      pip install git+git://github.com/incf-nidash/nidm-api.git

#### Quick Start
To start the server:

      nidm
      
See all valid queries at localhost:8088. To see a single query:


      localhost:8088/api/7950f524-90e8-4d54-ad6d-7b22af2e895d


Do a query:

      http://localhost:8088/api/query/7950f524-90e8-4d54-ad6d-7b22af2e895d?ttl=https://rawgithub.com/incf-nidash/nidm-api/master/example/nidm.ttl
    

#### Documentation
Please see [getting started](http://nidm-api.readthedocs.org/en/latest/getting-started.html) for how to run a local REST API, a server REST API, or use the module functions in your application to perform queries on NIDM results, workflow, and experiment data structures. We will be providing complete documentation at [readthedocs](http://nidm-api.readthedocs.org/)


#### Organization
The main python module contains scripts that are organized by the associated NIDM data structure, and you should follow the following convention:

 - [nidmapi/query.py](nidmapi/query.py): contains functions for working with [nidm-queries](https://github.com/incf-nidash/nidm-queries).
 - [nidmapi/app.py](nidmapi/app.py): the flask application used to serve the REST API, as well as provide graphical interfaces for generating new data structures, etc.
 - [nidmapi/utils.py](nidmapi/utils.py): General utility functions for file browsing, reading and writing, formatting, etc.
 - [nidmapi/scripts.py](nidmapi/scripts.py): The "entry point" for the command line executable installed with the module.
 - [nidmapi/experiment.py](nidmapi/experiment.py): nidm experiment functions
 - [nidmapi/results.py](nidmapi/results.py): nidm results functions
 - [nidmapi/workflow.py](nidmapi/workflow.py): nidm workflow functions


#### Quick Answers

##### How do I use this as a REST API?
You have several options. By installing the [nidm-api](https://github.com/incf-nidash/nidm-api) you will have a command line tool to immediately serve a localhost version of the REST API.  You could easily run this executable on a server to provide it to a larger group of people. We will also (likely) find a place to serve this officially.

##### How do I integrate queries into my application?
While this API is an executable, it is also a collection of functions organized around the different NIDM objects. You can easily import the same functions to perform the queries into your applications to use them without needing to get them via the REST API.
