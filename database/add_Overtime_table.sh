#!/bin/bash

db_file=$1

sqlite3 $db_file \
"CREATE TABLE Overtime (
    Year            INTEGER (4) NOT NULL,
    Round           INTEGER (1) NOT NULL,
    IndividualID    INTEGER    REFERENCES Individuals (IndividualID)
                       NOT NULL,
    Overtime          INTEGER NOT NULL,
    PRIMARY KEY ( Year, Round, IndividualID )
);"
