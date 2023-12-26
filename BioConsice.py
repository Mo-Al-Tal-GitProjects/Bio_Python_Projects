import argparse
import pandas as pd
import plotly.express as px
from datetime import datetime
from tabulate import tabulate

def main_menu():
    parser = argparse.ArgumentParser(description="Protein Concentration Data Tool")
    parser.add_argument("-e", "--enter", help="Enter new protein concentration data", action="store_true")
    parser.add_argument("-v", "--view", help="View entered data", action="store_true")
    parser.add_argument("-z", "--visualize", help="Visualize data", action="store_true")
    parser.add_argument("-s", "--summary", help="Statistical summary", action="store_true")
    parser.add_argument("-save", "--save_data", help="Save data", action="store_true")
    parser.add_argument("-l", "--load", help="Load data", action="store_true")
    args = parser.parse_args()

    if args.enter:
        enter_data()
    elif args.view:
        view_data()
    elif args.visualize:
        visualize_data()
    elif args.summary:
        statistical_summary()
    elif args.save_data:
        save_data()
    elif args.load:
        load_data()
    else:
        parser.print_help()


# Initialize an empty DataFrame instead of a list
protein_data = pd.DataFrame(columns=["sample_id", "concentration", "date"])

def enter_sample_id():
    return input("Enter sample identifier: ")


def enter_concentration():
    while True:
        try:
            concentration = float(input("Enter concentration: "))
            if 0 <= concentration <= 1000:  # Example range check
                return concentration
            else:
                print("Concentration out of valid range (0-1000).")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def enter_measurement_date():
    while True:
        date_entry = input("Enter date of measurement (YYYY-MM-DD): ")
        try:
            datetime.strptime(date_entry, '%Y-%m-%d')
            return date_entry
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def enter_data():
    global protein_data  # Use the global DataFrame
    print("\n--- Enter Protein Concentration Data ---")
    while True:
        sample_id = enter_sample_id()
        concentration = enter_concentration()
        date = enter_measurement_date()

        # Append to DataFrame
        protein_data = protein_data.append({
            "sample_id": sample_id,
            "concentration": concentration,
            "date": date
        }, ignore_index=True)

        if input("Enter more data? (yes/no): ").lower() != 'yes':
            break


def view_data():
    if protein_data.empty:
        print("No data available.")
    else:
        print("\n--- Entered Protein Concentration Data ---")
        print(tabulate(protein_data, headers='keys', tablefmt='pretty'))

    
def visualize_data():
    if protein_data.empty:
        print("No data to visualize.")
        return

    print("Select plot type:")
    print("1. Line Plot")
    print("2. Histogram")
    print("3. Box Plot")
    print("4. Scatter Plot with Trend Line")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        visualize_line_plot()
    elif choice == '2':
        visualize_histogram()
    elif choice == '3':
        visualize_box_plot()
    elif choice == '4':
        visualize_scatter_plot()
    else:
        print("Invalid choice.")


def visualize_line_plot():
    sorted_data = protein_data.sort_values(by='date')
    fig = px.line(sorted_data, x='date', y='concentration', markers=True, title='Protein Concentration Over Time')
    fig.update_layout(xaxis_title='Date', yaxis_title='Concentration')
    fig.show()

def visualize_histogram():
    fig = px.histogram(protein_data, x='concentration', nbins=20, title='Distribution of Protein Concentrations')
    fig.update_layout(xaxis_title='Concentration', yaxis_title='Frequency')
    fig.show()

def visualize_box_plot():
    fig = px.box(protein_data, y='concentration', title='Box Plot of Protein Concentrations')
    fig.update_layout(yaxis_title='Concentration')
    fig.show()

def visualize_scatter_plot():
    fig = px.scatter(protein_data, x=protein_data.index, y='concentration', trendline='ols', title='Scatter Plot of Protein Concentrations')
    fig.update_layout(xaxis_title='Sample Number', yaxis_title='Concentration')
    fig.show()

def statistical_summary():
    if protein_data.empty:
        print("No data available for analysis.")
        return

    print("\n--- Statistical Summary ---")
    description = protein_data['concentration'].describe()
    median = protein_data['concentration'].median()
    mode = protein_data['concentration'].mode().iloc[0]
    skewness = protein_data['concentration'].skew()
    kurtosis = protein_data['concentration'].kurt()

    summary = pd.DataFrame({'Metric': ['Mean', 'Median', 'Mode', 'Standard Deviation', 'Skewness', 'Kurtosis'],
                            'Value': [description['mean'], median, mode, description['std'], skewness, kurtosis]})
    print(summary.to_string(index=False))


def save_data():
    if protein_data.empty:
        print("No data to save.")
        return

    file_name = input("Enter filename to save data (CSV format): ")
    if not file_name.endswith('.csv'):
        file_name += '.csv'
    protein_data.to_csv(file_name, index=False)
    print(f"Data saved to {file_name}.")

def load_data():
    file_name = input("Enter filename to load data from: ")
    try:
        global protein_data
        protein_data = pd.read_csv(file_name)
        print(f"Data loaded from {file_name}.")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        print("There was an error loading the file. Please check the filename and file contents.")


def main():
    main_menu()

if __name__ == "__main__":
    main()
