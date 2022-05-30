#!/bin/bash

db_file=$1

sqlite3 $db_file \
"CREATE TABLE StanleyCupSelections (
    IndividualID        INTEGER      REFERENCES Individuals (IndividualID) 
                                     NOT NULL,
    Year                INTEGER      NOT NULL,
    EastSelection       VARCHAR (40),
    WestSelection       VARCHAR (40),
    StanleyCupSelection VARCHAR (40),
    GameSelection       INTEGER,
    PRIMARY KEY (
        IndividualID,
        Year
    )
);"
