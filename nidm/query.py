'''
query: part of the nidm-api
general functions to work with query
data structures for nidm-queries

'''

import os
import re
import stat
import uuid
import json
import numpy
import rdflib
import shutil
import tempfile
import rdfextras
rdfextras.registerplugins()
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from git import Repo
from glob import glob
from pandas import DataFrame
from nidm.utils import load_json, get_query_template, has_internet_connectivity, \
find_directories, set_permissions

def generate_query_template(output_dir=None,template_path=None,fields=None):
    '''generate_query_template
    Parameters
    ==========
    output_dir: str
        full path to output directory for json data structure.
        if none specified, will not save the data structure
    template_path: str
        path to json file to use as a template. Only should be
        specified if the user has reason to use a custom template
        default is the standard provided by nidm-api.    
    fields: dict (optional)
        a dictionary with fields that correspond to template keys.
        if provided, template will be filled with keys. Possible values
        include 
    Returns
    =======
    template: json (dict)
        A python dictionary (json) that can be filled with
        new query information
    '''
    if template_path == None:
        template = get_query_template()        
    template = load_json(template)

    # Each template is given a uid
    uid = str(uuid.uuid4())   
    template["uid"] = uid

    # the user has provided data to fill template
    #TODO: template validation
    if fields != None:    
        for key,value in fields.iteritems():
           if key in template:
              # Parameters are generated from sparql query based on "SELECT" line
              if key == "sparql":
                  template["parameters"],template["sparql"] = format_sparql(value)
              else:
                  template[key] = value

    # the user wants to save to file
    if output_dir != None:
        save_query_template(template,output_dir)
    return template


def save_query_template(template,output_dir):
    '''generate_query_template
    Parameters
    ==========
    output_dir: string path
        full path to output directory for json data structure.
        the template filename is generated from the uid variable
    Returns
    =======
    success: boolean
        True if save was successful, false otherwise
    '''
    filepath = "%s/%s.json" %(output_dir,template["uid"])
    try:
        json.dump(template,open(filepath,"wb"))
        return True
    except:
        return False

def do_query(ttl_file,query,rdf_format="turtle",serialize_format="csv",output_df=True):
    g = rdflib.Graph()
    g.parse(ttl_file,format=rdf_format)
    result = g.query(query)   
    result = result.serialize(format=serialize_format)    
    if output_df == True:
        result = StringIO(result)
        return DataFrame.from_csv(result,sep=",")
    else:
        return result


def make_lookup(query_list,key_field):
    '''make_lookup
    returns dict object to quickly look up query based on uid
    Parameters
    ==========
    query_list: list 
        a list of query (dict objects)
    key_field: str
        the key in the dictionary to base the lookup key
    Returns
    =======
    query_dict: dict
        dict (json) with key as "key_field" from query_list 
    '''
    lookup = dict()
    for single_query in query_list:
        lookup_key = single_query[key_field]
        lookup[lookup_key] = single_query
    return lookup

def validate_queries(query_dir,queries=None):
    '''validate_queries
    returns json object with query data structures, and
    a field 'valid' to describe if query was valid
    Parameters
    ==========
    queries: list 
        a list of full paths to json files, each a query
    query_dir: str
        full path to a nidm-query repo
    Returns
    =======
    queries: json
        dict (json) with all read in queries available
    from nidm-query, provided by API
    '''
    #TODO: validation should include testing sparql,
    # as well as if fields possible to return are
    # possible given the query. It would be more ideal
    # to remove these "hard coded" options and have them
    # derived directly from the query at runtime
    if queries == None:
        query_folders = find_directories(query_dir)
        query_paths = find_queries(query_folders)
    queries = read_queries(query_paths)
    #TODO: need to decide how to validate :)
    return queries


def get_query_directory(tmpdir=None):
    '''get_query_directory:
    Download queries repo to tmp directory
    Parameters
    ==========
    tmpdir: str
        path to directory to download queries to
    '''
    if tmpdir == None:
        tmpdir = tempfile.mkdtemp()
    # Check for internet connection
    if has_internet_connectivity():
        print "Updating queries at %s" %(tmpdir)
        download_queries(tmpdir)  
    return tmpdir

def find_queries(query_folders,search_pattern="*.json"):
    '''find_queries
    searches one or more folders for valid queries, meaning
    json files. In the case of multiple directories, will
    append the folder name as a variable to indicate the type
    Parameters
    ==========
    query_folders: list or str
        one or more full paths to directories with json objects
    search_pattern: str
        pattern for glob to use to find query objects
        default is "*.json"
    Returns
    =======
    queries: list
        a list of full paths to query object files
    '''
    queries = []
    if isinstance(query_folders,str):
        query_folders = [query_folders]
    for query_folder in query_folders:
        queries = queries + glob("%s/%s" %(query_folder,search_pattern))
    return queries


def read_queries(query_paths):
    '''read_queries
    Read in a list of query (json) objects.
    Parameters
    ==========
    query_paths: list
    a list of full paths to query objects to read
    Returns
    =======
    queries_: list
        dict to be served as json describing queries available
        a "type" variable is added to indicate folder query was found in
    '''
    queries = []
    for query_path in query_paths:
        ext = os.path.splitext(query_path)[1]
        if ext == ".json":
            query_type = query_path.split("/")[-2]
            uid = query_path.split("/")[-1].replace(ext,"")
            tmp = json.load(open(query_path,"rb"))
            # sparql should be joined into single string
            tmp["sparql"] = "\n".join(tmp["sparql"])  
            tmp["type"] = query_type
            tmp["uid"] = uid    
            queries.append(tmp)
        else:
            print "Skipping file %s, extension is not .json" %(query_path)
    return queries

# Currently hard coded for query repo, if we have more
# data types can be changed to a variable
def download_queries(destination):
    '''download_queries
    Download queries repo to a destination
    Parameters
    ==========
    destination:
       the full path to download the repo to
    '''
    repo = Repo.clone_from("https://github.com/incf-nidash/nidm-query.git",destination)
    return repo


def format_sparql(sparql_text):
    '''format_sparql
    split sparql text into a list, and 
    extract parameter options from select.
    '''
    lines = sparql_text.split("\n")
    lines = [line.strip("\r") for line in lines]
    params = []
    # Find any lines with select and extract variables from it
    expression = re.compile("select")
    param_expression = re.compile(r"([#?]\w+)\b")
    for line in lines:
        if expression.search(line.lower()):
            if param_expression.search(line):
                params = params + param_expression.findall(line)
    params = numpy.unique(params).tolist() 
    return params,lines

