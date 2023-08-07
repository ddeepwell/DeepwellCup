#!/bin/bash

db_file=$1
table_file=$2

sqlite3 $db_file ".read ${table_file}"
