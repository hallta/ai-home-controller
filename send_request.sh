#!/bin/bash

# add more files that indicate the state of the garage:
#  - garage door closed
#    - garage with car no cars in it 
#    - garage with car 1 in it
#    - garage with car 2 in it
#    - garage with car 3 in it
#    - garage with car 1,2 in it
#    - garage with car 1,3 in it
#    - garage with car 2,3 in it
#    - garage with car 1,2,3 in it
#  - garage door open
#    - garage with car no cars in it 
#    - garage with car 1 in it
#    - garage with car 2 in it
#    - garage with car 3 in it
#    - garage with car 1,2 in it
#    - garage with car 1,3 in it
#    - garage with car 2,3 in it
#    - garage with car 1,2,3 in it



#cat garage.prompt| ollama run llava
#cat garage.prompt| ollama run qwen3-vl:8b
cat garage.prompt| ollama run qwen3-vl:30b 

#model="llama3"
#model="llava"
#
#curl -X POST http://localhost:11434/api/generate -d "{
#  \"model\": \"${model}\",
#  \"prompt\": \"a photoreaslistic image of a caat wearing a santa hat.\"
#}" | perl -MJSON -lne '$r = $r . decode_json($_)->{"response"}; END{print $r}'