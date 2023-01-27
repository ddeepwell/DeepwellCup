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

$DATABASE_DIR/add_Individuals_table.sh $db_file
$DATABASE_DIR/add_StanleyCupSelections_table.sh $db_file
$DATABASE_DIR/add_StanleyCupResults_table.sh $db_file
$DATABASE_DIR/add_Series_table.sh $db_file
$DATABASE_DIR/add_SeriesSelections_table.sh $db_file
$DATABASE_DIR/add_SeriesResults_table.sh $db_file
$DATABASE_DIR/add_OtherPoints_table.sh $db_file
$DATABASE_DIR/add_Overtime_table.sh $db_file
