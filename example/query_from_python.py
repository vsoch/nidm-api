#!/usr/bin/python

from nidm.query import get_query_directory, validate_queries, make_lookup, do_query

# Get updated queries, validate, and generate a lookup dict:
query_dir = get_query_directory()
query_json = validate_queries(query_dir)
query_dict = make_lookup(query_json,key_field="uid")

# Let's use the query to get coordinates
qid = "7950f524-90e8-4d54-ad6d-7b22af2e895d"

# Here is a ttl file that I want to query, nidm-results
ttl_file = "nidm.ttl"

result = do_query(ttl_file=ttl_file,query=query_dict[qid]["sparql"])

# The result is a pandas data frame. I can turn it into other things too
result = result.to_dict(orient="records")
