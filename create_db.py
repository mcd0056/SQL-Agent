from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer

# Assuming engine is your SQLAlchemy engine connected to the SQLite database
engine = create_engine('sqlite:///database.db')
metadata = MetaData()

# Define the table structure
predefined_responses = Table('predefined_responses', metadata,
                             Column('id', Integer, primary_key=True),
                             Column('response_text', String),
                             Column('keyword', String))

# Create the table if it does not exist
metadata.create_all(engine)