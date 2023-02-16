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

$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'Individuals.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'StanleyCupSelections.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'StanleyCupResults.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'Series.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'SeriesSelections.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'SeriesResults.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'OtherPoints.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'OvertimeSelections.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'OvertimeResults.txt'
$DATABASE_DIR/add_table.sh $db_file $DATABASE_DIR/'Nicknames.txt'