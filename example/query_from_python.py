#!/usr/bin/python

from nidm.query import Queries, do_query

alltypes = Queries()

len(alltypes.queries)
#7

res = Queries(components="results")
len(res.queries)

#6

# What am I looking at?
# res.queries holds all queries as a list in json, for iterating over
# res.query_dict is a query lookup based on a unique id
# res.store is the (temp) location of your query files

# Select a query from results that we like
qid = "7950f524-90e8-4d54-ad6d-7b22af2e895d"

# Here is a ttl file that I want to query, nidm-results
ttl_file = "nidm.ttl"

result = do_query(ttl_file=ttl_file,query=res.query_dict[qid]["sparql"])

# The result is a pandas data frame. I can turn it into other things too
result = result.to_dict(orient="records")
