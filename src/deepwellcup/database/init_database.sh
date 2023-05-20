#!/bin/bash
# Initialize a database

if [ "$#" -eq 0 ]; then
    db_file='DeepwellCup.db'
elif [ "$#" -eq 1 ]; then
    db_file=$1
else
    echo "Incorrect number of arguments"
fi

DATABASE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
table_files=($(ls $DATABASE_DIR/*.txt))
for file in "${table_files[@]}"; do
    $DATABASE_DIR/add_table.sh $db_file $file
done
