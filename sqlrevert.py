#
# SQL Revert: Reverse the impact of SQL statements 
#             In other words, generate SQL that will reverse the DML actions of SQL input to this utility
#             In a session, this can be managed by transactions (rollback, commit, etc.)
#             Across sessions which can span days or any amount of time, there is no "automatic" way of 
#             reversing the DML results. 
#             - Oracle does provide flashback features which help you generate such reverse/undo SQL
#               - But these are not always available to developers and also there is no database-agnostic
#                 way of generating such "undo" sql, hence this utility
#             We plan to use sqlparse library to parse the SQL
#
# Version 1. 
#     This will attempt reverse INSERT statments only. At this point, we only attempt standard/simple
#     INSERT statements of the form 'INSERT INTO tablename (column1, column2, ...) VALUES (value1, value2, ...) 
#

import os
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
import re

def get_table_name(psql):
    into_seen = False
    for tok in psql.tokens:
        if tok.value == " ":
            # print("Found whitespace")
            continue
        if into_seen:
            table_name = str(tok).split(' ', 1)[0]
            into_seen = False
            return table_name
        elif tok.ttype is Keyword and tok.value.upper() == 'INTO':
            into_seen = True

def get_column_names(psql):
    into_seen = False
    past_tablename = False
    for tok in psql.tokens:
        if past_tablename:
            # remove parenthesis
            tmp_str = re.sub('\(', '', column_string[0])
            tmp_str = re.sub('\)', '', tmp_str)
            tmp_str = re.sub(',', '', tmp_str)
            col_list = tmp_str.split(' ')
            # print(col_list)
            return col_list
        else:
            if tok.value == " ":
                # print("Found whitespace")
                continue
            if into_seen:
                table_name = str(tok).split(' ', 1)[0]
                column_string = str(tok).split(' ', 1)[1:]
                past_tablename = True
                into_seen = False
            elif tok.ttype is Keyword and tok.value.upper() == 'INTO':
                into_seen = True

def get_column_values(psql):
    values_seen = False
    past_tablename = False
    for tok in psql.tokens:
        if values_seen:
            if tok.value == " ":
                # print("Found whitespace")
                continue
            column_string = tok.value
            # print(column_string)
            # remove parenthesis
            tmp_str = re.sub('\(', '', column_string)
            tmp_str = re.sub('\)', '', tmp_str)
            tmp_str = re.sub(',', '', tmp_str)
            value_list = tmp_str.split(' ')
            past_tablename = True
            # print(value_list)
            return value_list
        else:
            if tok.ttype is Keyword and tok.value.upper() == 'VALUES':
                values_seen = True

def gen_DELETE_for_INSERT(in_table_name, in_column_names, in_column_values):
    DELETE_str = "DELETE FROM " + in_table_name + " WHERE 1 = 1 "
    ctr = 0
    for column_name in in_column_names:
        DELETE_str += " AND " + column_name + " = " + in_column_values[ctr]
        ctr += 1
    return DELETE_str    

INSERT_sqlstr = 'INSERT INTO tableX (name, id, gender, dob, cob, cor) VALUES ("Vinu", 1, "Male", "01-01-2018", "India", "America")'

# Get the first SQL statement only
parsed_INSERT_sqlstr = sqlparse.parse(INSERT_sqlstr)[0]; 
# print(parsed_INSERT_sqlstr)
# print(type(parsed_INSERT_sqlstr))

insert_into_this_table = get_table_name(parsed_INSERT_sqlstr)
# print(insert_into_this_table)

column_names = get_column_names(parsed_INSERT_sqlstr)
# print(column_names)

column_values = get_column_values(parsed_INSERT_sqlstr)
# print(column_values)

if (len(column_names) != len(column_values)):
    print("Mismatched number of columns and values!!")

DELETE_for_INSERT = gen_DELETE_for_INSERT(insert_into_this_table, column_names, column_values)
print(INSERT_sqlstr)
print(DELETE_for_INSERT)
