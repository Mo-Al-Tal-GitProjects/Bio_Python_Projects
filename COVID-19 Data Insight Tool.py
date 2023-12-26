import matplotlib.pyplot as plt

# Function to input COVID-19 data manually
def input_covid_data():
    dates = []
    cases = []
    while True:
        date = input("Enter date (YYYY-MM-DD) or 'done' to finish: ")
        if date.lower() == 'done':
            break
        try:
            cases_count = int(input("Enter the number of confirmed cases: "))
            dates.append(date)
            cases.append(cases_count)
        except ValueError:
            print("Invalid input. Please enter a valid date and cases count.")
    return dates, cases

# Function to create a line chart for COVID-19 cases
def create_covid_chart(dates, cases):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, cases, marker='o', linestyle='-', color='b')
    plt.title("COVID-19 Cases Over Time")
    plt.xlabel("Date")
    plt.ylabel("Confirmed Cases")
    plt.xticks(rotation=45)
    plt.tight_layout()

# Function to save the chart to a file
def save_chart_to_file(dates, cases, filename):
    create_covid_chart(dates, cases)
    plt.savefig(filename)
    print(f"Chart saved as '{filename}'.")

def load_data_from_file():
    filename = input("Enter the filename to load (e.g., data.csv): ")
    try:
        data = pd.read_csv(filename)
        return data['Date'].tolist(), data['Cases'].tolist()
    except Exception as e:
        print(f"Error loading file: {e}")
        return [], []

def export_data_to_file(dates, cases):
    filename = input("Enter the filename to save (e.g., data.csv): ")
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Cases'])
        for date, case in zip(dates, cases):
            writer.writerow([date, case])
    print(f"Data exported to '{filename}'.")

def data_summary(dates, cases):
    total_cases = sum(cases)
    average_cases = total_cases / len(cases) if cases else 0
    print(f"Total Cases: {total_cases}\nAverage Cases per Day: {average_cases}")

def filter_data_by_date(dates, cases):
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    filtered_dates = []
    filtered_cases = []
    for date, case in zip(dates, cases):
        if start_date <= date <= end_date:
            filtered_dates.append(date)
            filtered_cases.append(case)
    return filtered_dates, filtered_cases

def load_multiple_data_sets():
    data_sets = []
    labels = []
    while True:
        choice = input("Do you want to load a data set? (yes/no): ")
        if choice.lower() == 'no':
            break
        elif choice.lower() == 'yes':
            filename = input("Enter the filename to load (e.g., data.csv): ")
            label = input("Enter a label for this data set: ")
            try:
                data = pd.read_csv(filename)
                dates = pd.to_datetime(data['Date']).tolist()
                cases = data['Cases'].tolist()
                data_sets.append((dates, cases))
                labels.append(label)
            except Exception as e:
                print(f"Error loading file: {e}")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    return data_sets, labels

def compare_multiple_data_sets():
    data_sets, labels = load_multiple_data_sets()
    if not data_sets:
        print("No data sets loaded for comparison.")
        return

    plt.figure(figsize=(12, 8))
    for (dates, cases), label in zip(data_sets, labels):
        plt.plot(dates, cases, marker='o', linestyle='-', label=label)
    plt.title("Comparison of COVID-19 Cases Across Different Data Sets")
    plt.xlabel("Date")
    plt.ylabel("Confirmed Cases")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def user_menu():
    dates, cases = [], []
    while True:
        print("\nCOVID-19 Data Visualizer Menu")
        print("1. Input Data Manually")
        print("2. Load Data from File")
        print("3. View Chart")
        print("4. Save Chart to File")
        print("5. Export Data to File")
        print("6. View Data Summary")
        print("7. Filter Data by Date")
        print("8. Compare Multiple Data Sets")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            dates, cases = input_covid_data()
        elif choice == '2':
            dates, cases = load_data_from_file()
        elif choice == '3' and dates:
            create_covid_chart(dates, cases)
            plt.show()
        elif choice == '4' and dates:
            filename = input("Enter the filename (e.g., chart.png): ")
            save_chart_to_file(dates, cases, filename)
        elif choice == '5' and dates:
            export_data_to_file(dates, cases)
        elif choice == '6' and dates:
            data_summary(dates, cases)
        elif choice == '7' and dates:
            dates, cases = filter_data_by_date(dates, cases)
        elif choice == '8':
            compare_multiple_data_sets()
        elif choice == '9':
            break
        else:
            print("Invalid choice or no data available.")

if __name__ == "__main__":
    user_menu()
