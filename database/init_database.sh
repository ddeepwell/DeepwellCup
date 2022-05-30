#!/bin/bash

db_file='DeepwellCup.db'

./add_Individuals_table.sh $db_file
./add_StanleyCupSelections_table.sh $db_file
./add_StanleyCupResults_table.sh $db_file
./add_Series_table.sh $db_file
./add_SeriesSelections_table.sh $db_file
./add_SeriesResults_table.sh $db_file
# ./add_OtherPoints_table.sh $db_file
