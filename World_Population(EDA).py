### World Population EDA

#### Objective:
'''
The primary goal of this is to analyze the world population dataset to uncover patterns, trends, and insights about global population growth over time. 
The dataset contains population data for different countries and continents from 1970 to 2022, 
allowing us to study historical population trends and current demographic distributions.

'''


#### Loading and understanding the data set
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"F:\Data Science (Analytics)\Pyhton\Pandas\world_population.csv")
pd.set_option('display.float_format', lambda x : '%.2f' % x) # converting scientific notation to standard decimal notation

df
print("Dataset Info: \n")
df.info()
print("Preview of the Dataset :")
df.head()
print('Statistics Summary :')
df.describe(include="all")

#### Cleaning data
# Checking for NULL Values

print("Missing Values:")
df.isnull().sum()
df.columns.to_list()
num_cols = ['2022 Population', '2020 Population', '2015 Population',
 '2010 Population', '2000 Population', '1990 Population', '1980 Population',
 '1970 Population', 'Area (km²)', 'Density (per km²)', 'Growth Rate']

for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

df.isnull().sum()
# checking for Duplicate values are there are not.

if df.duplicated().sum() > 0 :
    df.drop_duplicates(inplace=True)
    print(f"Duplicates : {df.duplicated().sum()}\n Duplicates Droped and data frame shape is: {df.shape}")
else:
    print(f"Duplicates : {df.duplicated().sum()}\n No changes done \n Data Frame Shape: {df.shape}")

#### Analyzing the Categorical and Numerical values 
df.dtypes
# Categorical columns

print("Unique values in Categorical Values:\n")

for cate_col in df.select_dtypes(include='object').columns :
    print(f"{cate_col} : {df[cate_col].nunique()} Unique Values")
# Numerical columns

print("Unique values in Numerical Values:\n")

for cate_col in df.select_dtypes(include='number').columns :
    print(f"{cate_col} : {df[cate_col].nunique()} Unique Values")
# df['Continent'].value_counts('Country')

Count_of_Continents = df.groupby('Continent')['Country'].nunique()
Count_of_Continents
# visualizing for the Categorical.

sns.countplot(x='Continent', data=df)
plt.title("Count of the Countries by the Continent")
plt.show()
# visualizing for the Numerical.

numeric_cols = df.select_dtypes(include='number').columns

df[numeric_cols].hist(bins=20, figsize=(15, 10))
plt.show()
# Outlier Detection.

sns.boxplot(data=df[numeric_cols])
plt.title("Outliers for Numeric Columns")
plt.show()
# Correlation

num_corr = df.select_dtypes(include='number')

print("Correlation :")
correlation = num_corr.corr()
correlation
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.rcParams['figure.figsize'] = (20, 7)
plt.title("Correlation Heatmap \n")
plt.show()
# Grouped analysis

Continent_grp = df.groupby('Continent')[['2022 Population', 'Area (km²)']].mean()

print("Average Population and Area by Continent \n")
print(Continent_grp )
Continent_grp.plot(kind='bar', figsize=(10, 5))
plt.title("Average Population and Area by Continent")
plt.show()
# Historical Analysis

population_col = [col for col in df.columns if 'Population' in col]
time_series = df.groupby('Continent')[population_col].mean()
time_series.T.plot(figsize=(15, 8))
plt.title("Population Trends over a Time period by Continent")
plt.xlabel = ('Year')
plt.ylabel = ('Avg. Population')
plt.legend(title = 'Continet')

plt.show()
# Outlier Analysis

if 'Area (km²)' in df.columns:
    df['Population_density'] = df['2022 Population'] / df['Area (km²)'] # Creating a Population_density column to store the Population Density 
    sns.histplot(df['Population_density'], kde=True)
    plt.title("Population Density Distribution")
    plt.show()
# Remove outliers for population density

print("Before Removing Outliers:", df.shape)

if 'Population_density' in df.columns:
    Q1 = df['Population_density'].quantile(0.25)
    Q3 = df['Population_density'].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(
        df['Population_density'] >= (Q1 - 1.5 * IQR)) &
        (df['Population_density'] >= (Q3 + 1.5 * IQR))]
    
print("After Removing Outliers:", df.shape)
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['Population_density'])
plt.title("Population Density (After Removing Outliers)")
plt.show()
top_countries = df.sort_values(by='2022 Population', ascending=False).head(10)
sns.barplot(x='2022 Population', y='Country', data=top_countries)
plt.title("Top 10 Countries by Population (2022)")
plt.show()
#### Document Findings
print("Key Insights: ")
print("1. Asia has the highest average population, followed by Africa.")
print("2. The population density distribution shows that smaller countries tend to have higher densities.")
print("3. Growth trends suggest significant population increases in developing regions.")
