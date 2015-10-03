__author__ = 'christopherrivera'

import sqlalchemy as sa
from sqlalchemy import Column, Table, MetaData,create_engine
from sqlalchemy.dialects.mysql import *
from sqlalchemy.sql.expression import insert