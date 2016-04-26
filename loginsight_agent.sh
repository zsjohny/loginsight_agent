#!/bin/bash
#Download install agent scripts
wget http://loginsight:loginsight@download.loginsight.cn/loginsight_agent.tar.gz
tar fvxz loginsight_agent.tar.gz
cd loginsight_agent
python loginsight_agent.py
