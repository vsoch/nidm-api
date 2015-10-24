# nidm-api

* under development *

This is an application to query and visualize nidm data structures, including workflow, experiment, and results. This repo contains a python module that can serve as a standalone application to work with [nidm-queries](https://github.com/incf-nidash/nidm-queries).

Functions will be provided to do the following:

- perform a query on an NIDM turtle file, returning the format of your choice (text and graphical)
- a web interface to generate a new query to add to the database
- validation of query data structures

#### Organization
The main python module contains scripts that are organized by the associated NIDM data structure, and you should follow the following convention:

 - [nidmapi/query.py](nidmapi/query.py): contains functions for working with [nidm-queries](https://github.com/incf-nidash/nidm-queries).
 - [nidmapi/app.py](nidmapi/app.py): the flask application used to serve the REST API, as well as provide graphical interfaces for generating new data structures, etc.
 - [nidmapi/utils.py](nidmapi/utils.py): General utility functions for file browsing, reading and writing, formatting, etc.
 - [nidmapi/scripts.py](nidmapi/scripts.py): The "entry point" for the command line executable installed with the module.
 - [nidmapi/experiment.py](nidmapi/experiment.py): nidm experiment functions
 - [nidmapi/results.py](nidmapi/results.py): nidm results functions
 - [nidmapi/workflow.py](nidmapi/workflow.py): nidm workflow functions

Nothing is yet developed fully enough for testing, this is simply a skeleton.


#### Documentation

Documentation will be provided to answer the following questions:

#### How do I use this as a REST API?
You have several options. By installing the [nidm-api](https://github.com/incf-nidash/nidm-api) you will have a command line tool to immediately serve a localhost version of the REST API.  You could easily run this executable on a server to provide it to a larger group of people. We will also (likely) find a place to serve this officially.

##### How do I contribute a new query?
We will have a function in this API executable to generate a new data structure for adding to [nidm-queries](https://github.com/incf-nidash/nidm-queries). This will work via command line, or via a web interface for you to input fields for your structure. We recommend that you use the generation functions to ensure accuracy in the format and fields of your data structure. You can then add it to the repo by submitting a pull request to add it. A pull request affords group discussion, and we will eventually have continuous integration that will run tests on your new query.

#### How do I integrate queries into my application?
While this API is an executable, it is also a collection of functions organized around the different NIDM objects. You can easily import the same functions to perform the queries into your applications to use them without needing to get them via the REST API.

More documentation and details will come, for now it's time to code!

