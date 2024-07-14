#! /usr/bin/env bash

curl -X POST localhost:8000/stop?node_id=$1
