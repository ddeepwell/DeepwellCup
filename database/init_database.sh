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

$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'Individuals'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'StanleyCupSelections'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'StanleyCupResults'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'Series'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'SeriesSelections'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'SeriesResults'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'OtherPoints'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'OvertimeSelections'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'OvertimeResults'
