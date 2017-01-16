FROM solr:6.2.1

MAINTAINER Joshy Cyriac <j.cyriac@gmail.com>

# Copy schema json and test data
COPY scripts/schema.json /opt/solr
COPY scripts/solr_test_data_mr.csv /opt/solr

# Starts solr, creates core, add schema, post test data and shutdown
RUN /opt/solr/bin/solr start && \
    /opt/solr/bin/solr create_core -c grouping && \
    curl -X POST -H 'Content-type:application/json' -d @schema.json http://localhost:8983/solr/grouping/schema && \
    curl "http://localhost:8983/solr/grouping/update/csv?stream.file=/opt/solr/solr_test_data_mr.csv&separator=;&stream.contentType=text/plain;charset=utf-8" && \
    /opt/solr/bin/solr stop
