from app import  AboutYou,db, initialize_timetable
from app import app
from sqlalchemy import inspect  # Import the inspect function to examine the database schema

with app.app_context():
  

  """
  
    print("Table 'about_me' has been deleted.")
    db.create_all()  # Create all tables
    initialize_timetable()  # Populate Timetable with default rows

    # Inspect database tables
    inspector = inspect(db.engine)  # Inspect the database schema
    print("Tables in the database:")
    print(inspector.get_table_names())  # Get all the table names
    # Print table details
    print("Columns in the 'about_me' table:")
    columns = inspector.get_columns('about_me')  # Replace 'about_me' with your table name
    for column in columns:
        print(f"Name: {column['name']}, Type: {column['type']}")

    rows = AboutYou.query.all()
    print(rows,"          :hope")

    # Print each row's values
    for row in rows:
        print(f"ID: {row.id}, Name: {row.name}, Bio: {row.bio}")"""
