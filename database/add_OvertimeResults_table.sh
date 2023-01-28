#!/bin/bash

db_file=$1

sqlite3 $db_file \
"CREATE TABLE OvertimeResults (
    Year            INTEGER (4) UNIQUE NOT NULL,
    Round           INTEGER (1) NOT NULL,
    Overtime          INTEGER NOT NULL,
    PRIMARY KEY ( Year, Round )
);"
