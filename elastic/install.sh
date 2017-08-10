#!/bin/bash
#
# Created by Umanga Bista.
#
##
rm -r apps
mkdir apps

echo "installing trec_eval"
tar xvf trec_eval_latest.tar.gz
mv trec_eval.9.0 apps/
cd apps/trec_eval.9.0
make
cd ../../

# es
echo "installing elasticsearch"
tar xvf elasticsearch-5.5.1.tar
mv elasticsearch-5.5.1 apps/
echo """network.host: _eth0_
network.bind_host: 0.0.0.0
http.port: 9200
""" >> apps/elasticsearch-5.5.1/config/elasticsearch.yml

# kibana
echo "installing kibana"
tar xvf kibana-5.5.1-linux-x86_64.tar.gz
mv kibana-5.5.1-linux-x86_64 apps/
echo """server.host: 0.0.0.0
server.port: 5601
""" >> apps/kibana-5.5.1-linux-x86_64/config/kibana.yml

echo "Installation completed !!!"
