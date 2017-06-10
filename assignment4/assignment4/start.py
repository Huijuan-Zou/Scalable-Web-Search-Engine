#!/usr/bin/env python3
import os

def main():
    os.system("python -m assignment3.Coordinator \
              --mapper_path=./assignment4/mr_apps/invindex_mapper.py \
               --reducer_path=./assignment4/mr_apps/invindex_reducer.py --job_path=./assignment4/invindex_jobs \
                --num_reducers=3"
              )
    os.system("python -m assignment3.Coordinator --mapper_path=./assignment4/mr_apps/docs_mapper.py \
               --reducer_path=./assignment4/mr_apps/docs_reducer.py --job_path=./assignment4/docs_jobs \
                --num_reducers=3")
    os.system("python -m assignment3.Coordinator --mapper_path=./assignment4/mr_apps/idf_mapper.py \
               --reducer_path=./assignment4/mr_apps/idf_reducer.py --job_path=./assignment4/idf_jobs \
                --num_reducers=1")
if __name__ == "__main__":
    main()
