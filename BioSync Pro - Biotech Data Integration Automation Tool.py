import sqlite3
import pandas as pd
import logging
import click
import os 

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def create_sqlite_db(db_name):
    try:
        # Connect to SQLite database (or create if it doesn't exist)
        conn = sqlite3.connect(f"{db_name}.db")
        cursor = conn.cursor()

        # Drop the existing table if it exists
        cursor.execute('DROP TABLE IF EXISTS sample_data')

        # Create a new sample table with appropriate columns
        cursor.execute('''CREATE TABLE sample_data (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            type TEXT,
                            description TEXT
                          )''')
        print(f"Database '{db_name}.db' updated with a new table 'sample_data'.")

        # Query to check the structure of the table
        cursor.execute("PRAGMA table_info(sample_data)")
        columns = cursor.fetchall()
        print("Table Structure: ")
        for col in columns:
            print(col)

        # Clean up
        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Failed to create database '{db_name}': {e}")
        raise


def connect_to_sqlite_db(db_name):
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(f"{db_name}.db")
        print(f"Connected to SQLite database '{db_name}.db' successfully.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to database '{db_name}': {e}")
        raise


def input_biotech_data():
    data = []
    n = int(input("Enter the number of biotech samples you want to input: "))

    for i in range(n):
        print(f"\nEntering data for sample {i+1}:")

        sample_id = get_valid_input("Enter Sample ID: ", int)
        name = get_valid_input("Enter Sample Name: ", str, lambda x: all(char.isalnum() or char in [' ', '_'] for char in x))
        sample_type = get_valid_input("Enter Sample Type (e.g., DNA, Protein, Cell): ", str, lambda x: x in ["DNA", "Protein", "Cell"])
        description = input("Enter a brief description: ")

        data.append((sample_id, name, sample_type, description))

    return pd.DataFrame(data, columns=['id', 'name', 'type', 'description'])

def get_valid_input(prompt, expected_type, condition=lambda x: True):
    while True:
        try:
            user_input = input(prompt)
            value = expected_type(user_input)
            if not condition(value):
                raise ValueError
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {expected_type.__name__}.")

def insert_data_to_db(conn, data, table_name, csv_filename):
    try:
        # Insert data into the database
        data.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Data inserted successfully into table '{table_name}'.")

        # Get the absolute path to the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Combine the script directory with the CSV filename to get the absolute file path
        csv_file_path = os.path.join(script_dir, csv_filename)
        
        # Export data to the CSV file using the absolute file path
        data.to_csv(csv_file_path, index=False)
        print(f"Data exported to '{csv_file_path}'.")
    except Exception as e:
        logging.error(f"Error inserting data into '{table_name}': {e}")
        raise

@click.command()
@click.option('--db_name', default='my_database', help='Database name')
def main(db_name):
    # Create the database and insert data as usual
    create_sqlite_db(db_name)
    conn = connect_to_sqlite_db(db_name)
    biotech_data = input_biotech_data()

    # Allow the user to input the CSV file name
    csv_filename = input("Enter the name for the CSV file (e.g., biotech_data.csv): ")

    # Call the function to insert data and export it to CSV with the specified filename
    insert_data_to_db(conn, biotech_data, 'sample_data', csv_filename)
    print(f"Data has been exported to {csv_filename}")

if __name__ == "__main__":
    main()
