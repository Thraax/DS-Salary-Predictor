# import tools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
sns.set(style='darkgrid')

# Read the cleaned data
data = pd.read_csv('cleaned-DataAnalyst.csv')

# Take a look at the fundamental measurements
data.describe()

# Take a look at the distribution of the numerical data we have


# Exclude '-1' From rating
rating = data.Rating.apply(lambda x: x if x != -1 else None)
sns.histplot(rating)
plt.title("Distribution of Ratings")

# Distribution of salaries
fig, axs = plt.subplots(ncols=3, figsize=(11, 8))
sns.histplot(data.max_salary, bins=10, ax=axs[0])
axs[0].set_title('Max salary distribution')
axs[0].set_xlabel('')
axs[0].set_ylabel('')

sns.histplot(data.min_salary, bins=10, ax=axs[1])
axs[1].set_title('Min salary distribution')
axs[1].set_xlabel('')
axs[1].set_ylabel('')

sns.histplot(data.avg_salary, bins=10, ax=axs[2])
axs[2].set_title('Average salary distribution')
axs[2].set_xlabel('')
axs[2].set_ylabel('')

fig.supxlabel('Salary')
fig.supylabel('Count')
fig.tight_layout()

# Distribution of companies ages
# Exclude '-1' From ages
age = data.age.apply(lambda x: x if x > 0 else None)
sns.histplot(age)

# Start counting categorical variables

# Count States, which state need more data analysts?
data['state'].value_counts().plot(kind='bar')

# Count level, Is companies need more seniors or juniors?
data['level'].value_counts().plot(kind='pie')

# Count industry, Which industry need more data analyst?
data['Industry'].value_counts().head(10).plot(kind='bar')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.4)

sns.barplot(data['Industry'].value_counts().head(10))

# Count title, What is the required titles for data analysis job?
data['title_simp'].value_counts().plot(kind='pie')
plt.ylabel("")

# Count type of ownership, What is the most type of companies require data analysts?
data['Type of ownership'].value_counts().plot(kind='bar')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.5)

# Get the most required tool
tools = []
count = []

for col in data.columns:
    if col.split('_')[0] == 't':
        tools.append(col.split('_')[1])
        count.append(np.sum(data[col]))

# plot the results
sns.barplot(x=tools, y=count, order=count.sort())
plt.title("Most required tools")
plt.xlabel("Tools")
plt.ylabel("Count")

# Start look for correlations

df = data[['Rating', 'desc_len', 'same state', 'Competitors', 'avg_salary', 'age']]
sns.heatmap(df.corr(), annot=True)

# What is the top 10 states with higher salaries?

pd.pivot_table(data, index='state', values='avg_salary').sort_values(by='avg_salary', ascending=False).head(10) \
    .plot(kind='barh')

plt.xlabel("Salary")
plt.ylabel("State")
plt.title("Top 10 states in salaries")
plt.legend(["Average salary"])

# What is the top 10 industries with higher salaries?

pd.pivot_table(data, index='Industry', values='avg_salary').sort_values(by='avg_salary', ascending=False).head(10) \
    .plot(kind='barh')

plt.xlabel("Salary")
plt.ylabel("industries")
plt.title("Top 10 industries in salaries")
plt.legend(["Average salary"])

# What is the top 10 sectors with higher salaries?

pd.pivot_table(data, index='Sector', values='avg_salary').sort_values(by='avg_salary', ascending=False).head(10) \
    .plot(kind='barh')

plt.xlabel("Salary")
plt.ylabel("Sectors")
plt.title("Top 10 industries in salaries")
plt.legend(["Average salary"])

# Present the salary according to title job and the level (jr / sr / manager)

pd.pivot_table(data, index=['title_simp', 'level'], values='avg_salary').sort_values(by='avg_salary', ascending=False) \
 .plot(kind='barh')

plt.xlabel("Title and level")
plt.ylabel("Average salary")
plt.title("Top 10 industries in salaries")
plt.legend(["Average salary"])

