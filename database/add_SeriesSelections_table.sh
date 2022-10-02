#!/bin/bash

db_file=$1

sqlite3 $db_file \
"CREATE TABLE SeriesSelections (
    YearRoundSeriesID INTEGER      REFERENCES Series (YearRoundSeriesID) 
                                   NOT NULL,
    IndividualID      INTEGER      REFERENCES Individuals (IndividualID) 
                                   NOT NULL,
    TeamSelection     VARCHAR (40),
    GameSelection     INTEGER (1),
    PlayerSelection   VARCHAR (40),
    PRIMARY KEY (
        YearRoundSeriesID,
        IndividualID
    )
);"
