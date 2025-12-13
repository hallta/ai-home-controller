#!/bin/bash

docker build -t llm-test:0.1.0 .
docker run -p 5432:5432 -d --shm-size="6g" --memory="6g" --cpus="4" --net=bridge -it llm-test:0.1.0
