import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import PredefinedResponse, db

# Load the CSV file
csv_file_path = 'data.csv'  # Adjust the path to your CSV file
data = pd.read_csv(csv_file_path)

# Database setup
DATABASE_URI = 'sqlite:///database.db'  # Ensure this matches your Flask app's configuration
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Iterate over the CSV rows
for index, row in data.iterrows():
    # Create an instance of the PredefinedResponse model for each row
    response = PredefinedResponse(response_text=row['response_text'], keyword=row['keyword'])
    # Add each instance to the session
    session.add(response)

# Commit the session to save all instances to the database
session.commit()

# Close the session
session.close()

print("Data uploaded successfully.")
