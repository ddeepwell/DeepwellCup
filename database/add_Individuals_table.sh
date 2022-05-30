#!/bin/bash

db_file=$1

sqlite3 $db_file \
"CREATE TABLE Individuals (
    IndividualID INTEGER      PRIMARY KEY AUTOINCREMENT
                              UNIQUE
                              NOT NULL,
    FirstName    VARCHAR (20) NOT NULL,
    LastName     VARCHAR (20) NOT NULL
);"
