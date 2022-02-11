# import tools
import pandas as pd

pd.set_option("display.max_rows", None)
# Read the data
data = pd.read_csv('DataAnalyst.csv')

# Drop unammed column
data = data.drop(['Unnamed: 0'], axis=1)

# Clean the salary estimate
data['Salary Estimate'].value_counts()
data = data[data['Salary Estimate'] != '-1']
# Remove (Glass door) from the word
salary = data['Salary Estimate'].apply(lambda x: x.split(" ")[0])
# replace the K with 000
salary = salary.apply(lambda x: x.replace('$', "").replace('K', "000"))

# Get the min and max salary and the average
min_salary = salary.apply(lambda x: int(x.split('-')[0]))
max_salary = salary.apply(lambda x: int(x.split('-')[1]))
avg_salary = min_salary + max_salary / 2

data['min_salary'] = min_salary
data['max_salary'] = max_salary
data['avg_salary'] = avg_salary

# Update the company name column and remove the " \n + rating "
data['Company Name'] = data['Company Name'].astype('str')
data["Company Name"] = data["Company Name"].apply(lambda x: x.split("\n")[0])

# Split the headquarters and location
data['same state'] = data.apply(lambda x: 1 if x['Location'] == x['Headquarters'] else 0, axis=1)

# Extract the state of company as new feature

data['state'] = data.Location.apply(lambda x: 'CO' if 'CO' in x else x.split(',')[1])

# Age of company
data['age'] = data.Founded.apply(lambda x: x if x < 1 else 2022 - x)

# Extract tools from job description
data['t_python'] = data['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)  # Python
data['t_stat'] = data['Job Description'].apply(lambda x: 1 if 'statistics' in x.lower() else 0)  # Statistics
data['t_tableau'] = data['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)  # tableau
data['t_powerbi'] = data['Job Description'].apply(lambda x: 1 if 'power bi' in x.lower() else 0)  # Power BI
data['t_sql'] = data['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)  # SQL
data['t_excel'] = data['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)  # Excel

# Clean the categorical columns that contain -1
data['Sector'].replace({'-1': 'na'}, inplace=True)
data['Type of ownership'].replace({'-1': 'na'}, inplace=True)
data['Industry'].replace({'-1': 'na'}, inplace=True)
data['Revenue'].replace({'-1': 'na / Non-Applicable'}, inplace=True)


# Extract the required level (Senior/Junior)
def extract_level(description):
    if 'sr' in description.lower() or 'senior' in description.lower() or 'lead' in description.lower() or 'principal' in description.lower():
        return 'sr'

    elif 'jr' in description.lower() or 'junior' in description.lower() or 'entery' in description.lower() or 'intern' in description.lower():
        return 'jr'

    else:
        return 'na'


data['level'] = data['Job Description'].apply(extract_level)


# Extract the title
def extract_title(title):
    if 'data science' in title.lower() or 'data scientist' in title.lower():
        return 'data scientist'

    elif 'manager' in title.lower():
        return 'manager'

    elif 'analyst' in title.lower():
        return 'analyst'

    elif 'machine learning' in title.lower() or 'machine learning engineer' in title.lower():
        return 'mle'

    elif 'director' in title.lower():
        return 'director'


data['title_simp'] = data['Job Title'].apply(extract_title)

# Get the length of description as new feature
data['desc_len'] = data['Job Description'].apply(lambda x: len(x))

# Get the number of competitors as new feature
data['Competitors'] = data['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)

data.to_csv('cleaned-DataAnalyst.csv', index=False)
