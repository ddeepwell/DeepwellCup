#!/bin/bash

db_file=$1

sqlite3 $db_file \
"CREATE TABLE StanleyCupResults (
    Year             INT (4)      PRIMARY KEY
                                  UNIQUE
                                  NOT NULL,
    EastWinner       VARCHAR (40) NOT NULL,
    WestWinner       VARCHAR (40) NOT NULL,
    StanleyCupWinner VARCHAR (40),
    Games            INT (1) 
);"
