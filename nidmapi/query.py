'''
query: part of the nidm-api
general functions to work with query
data structures for nidm-queries

'''

import os
import uuid
import rdflib
import rdfextras
rdfextras.registerplugins()
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO
from pandas import DataFrame
from nidmapi.utils import load_json, get_query_template


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
    #TODO: if a sparql query is provided, we should generate parameters from it
    #TODO: template validation
    if fields != None:    
    for key,value in fields.iteritems():
        if key in template:
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
