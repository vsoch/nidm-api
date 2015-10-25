from nidm.query import get_query_directory, validate_queries, make_lookup, do_query
from flask import Flask, render_template, request
from flask_restful import Resource, Api
from werkzeug import secure_filename
import tempfile
import shutil
import random
import os


# SERVER CONFIGURATION ##############################################
class NIDMServer(Flask):

    def __init__(self, *args, **kwargs):
            super(NIDMServer, self).__init__(*args, **kwargs)

            # update queries on start of application
            self.query_dir = get_query_directory()
            self.query_json = validate_queries(self.query_dir)
            self.query_dict = make_lookup(self.query_json,key_field="uid")

app = NIDMServer(__name__)
api = Api(app)    

# API VIEWS #########################################################
class apiIndex(Resource):
    """apiIndex
    Main view for REST API to display all available queries
    """
    def get(self):
        query_json = app.query_json
        return query_json

class apiQueryMeta(Resource):
    """apiQueryMeta
    return complete meta data for specific query
    """
    def get(self, qid):
        return {qid: app.query_dict[qid]}

class apiDoQuery(Resource):
    """apiDoQuery
    return result of query on ttl file
    Paramters
    =========
    qid: str
        the uid associated with the query
    ttl: str
        the url of the turtle file
    """
    def get(self, qid, output_format):
        ttl = request.args.get('ttl')
        try:
            result = do_query(ttl_file=ttl,
                     query=app.query_dict[qid]["sparql"])
            result = result.to_dict(orient="records")
            return {"uid": qid,
                "result": result}
        except:
            return {"message": "invalid input for query type.",
                    qid: app.query_dict[qid]}

              
# Add all resources
api.add_resource(apiIndex,'/')
api.add_resource(apiQueryMeta,'/api/<string:qid>')
api.add_resource(apiDoQuery,'/api/<string:output_format>/<string:qid>')

# WEB INTERFACE VIEWS ##############################################

#TODO will write

# RUNNING ##########################################################


# This is how the command line version will run
def start(port=8088):
    app.run(host="0.0.0.0",debug=True,port=port)
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
