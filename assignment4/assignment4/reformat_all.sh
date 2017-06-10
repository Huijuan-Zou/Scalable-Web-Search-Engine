#!/bin/bash

python -m assignment4.Reformatter assignment2Pro/data/info_ret.xml --job_path=assignment4/idf_jobs/  --num_partitions=1
python -m assignment4.Reformatter assignment2Pro/data/info_ret.xml --job_path=assignment4/docs_jobs/ --num_partitions=3
python -m assignment4.Reformatter assignment2Pro/data/info_ret.xml --job_path=assignment4/invindex_jobs/ --num_partitions=3
