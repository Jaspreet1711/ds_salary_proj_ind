"""
Created on Mon Oct 11 "21:24:07 2021

@author: Jaspreet Singh
"""
#--Setting up the Environment --#

#Importing Libraries
import pandas as pd
import numpy as np

# Uploading the Data Collected
ds_df = pd.read_excel("C:/Users/Jaspreet Singh/Desktop/DS_Projects/ds_sal_proj/DS Jobs in USA (Consolidated).xlsx")     
print("Data Uploaded")
print("Numbers of rows and columns are "+str(ds_df.shape))
print(" ")

#-- Data Cleaning Proceeds --#

# Checking irrelevant Columns
print("Colummn Names in the Data")
print(ds_df.columns)
print(" ")

## Removing 1st Column as it is of no use. 
ds_df = ds_df.drop("Unnamed: 0", 1)
ds_df = ds_df.drop("Job_Description", 1)
print("Removing 1st Column and Job_Description as it is of no use.")
print(ds_df.columns)
print(" ")     
print("Numbers of rows and columns are "+str(ds_df.shape))
print(" ")

# Checking Missing Values (it includes all blank and NA Values in the Data)
print("Total Missing Values Column wise")
print(ds_df.isnull().sum())
print(" ")

# Cleaning "Salary" Variable
Sal_Null_Values = ds_df.Salary.isnull().sum()
print("Numbers rows with missing value in Salary Column = "+str(Sal_Null_Values))
print(" ")

## All rows with NA and Blank values in Salary columns wiil be removed
ds_df = ds_df[ds_df['Salary'].notna()]
print("After removing all the rows with Missing values in Salary Column")
print("Numbers of rows and columns in data are "+str(ds_df.shape)) 
print(" ")

## Spliting Salary Variable to get proper int dtype
salary_sr = ds_df.Salary.apply(lambda x: x.split('(')[0])
salary_sr = salary_sr.apply(lambda x: x.replace('$', '').replace('K', ''))

## Making Hourly Column (as some salaries are given per hour and majourity are per annum)
ds_df['Hourly']  = ds_df.Salary.apply(lambda x: 1 if 'per hour' in x.lower() else 0)
ds_df['Hourly'] = pd.to_numeric(ds_df['Hourly'])

## Removing per hour text from Salary 
salary_sr = salary_sr.apply(lambda x: x.lower().replace('per hour', '')) 

## Creating two new columns Minimum Salary and Maximum Salary by splitting the range
ds_df['Min_Sal'] = salary_sr.apply(lambda x: x.split(' - ')[0])

### We are creating this func to extract Max Salary such that there are few values in Salary Column without the range so we will have same minimum value in maximum 
def extract_max(r):
    l = r.split(' ')
    if len(l) == 4:
        return l[2]
    else:
        return l[0]
        
ds_df['Max_Sal'] = salary_sr.apply(lambda x: extract_max(x))

ds_df['Min_Sal'] = pd.to_numeric(ds_df['Min_Sal'])
ds_df['Max_Sal'] = pd.to_numeric(ds_df['Max_Sal'])

## Creating Average Column of Min and Max Salary.
### Converting Hourly Salary into per annum to standardize the data.
def hours_to_annum(r):
    if r['Hourly'] == 1:
        return (((r['Min_Sal'] + r['Max_Sal']) / 2) *40 * 52) / 1000  # I have multiplied average by working hours in a week i.e. 40 Hours and by Total Weeks in a year i.e. 52 Weeks
    else:
        return (r['Min_Sal'] + r['Max_Sal']) / 2
    
ds_df['Average_Salary'] = ds_df.apply(lambda x: hours_to_annum(x), axis = 1)

print("We have cleaned the Salary Details and Extracted 'Average_Salary' in the data for each job")
print("Numbers of rows and columns in data are "+str(ds_df.shape))
print(" ") 
print("Colummns in the Data after cleaning are:")
print(ds_df.columns)
print(" ")

# Cleaning "Location" Variable
Loc_Null_Values = ds_df.Location.isnull().sum()
print("Numbers rows with missing value in Location Column = "+str(Loc_Null_Values))
print(" ")

## Spliting "Location" to get state codes
### Checking Unique Values before spliting
Loc_Values = ds_df['Location'].unique()
print("All unique text in Location Column are: ")
print(Loc_Values)
print(" ")

### Creating function to split as some rowz have Full State Name only or City, County & State Name.
def state(r):
    l = r.split(',')
    if len(l) == 2:
        return l[1]
    elif len(l) == 3:
        return l[2]
    else:
        return l[0]
    
ds_df['State_Code'] = ds_df['Location'].apply(lambda x: state(x))
State_Values = ds_df['State_Code'].unique()
print("All unique text in State Column are: ")
print(State_Values )
print(" ")

### Replacing Full State Name to State Code
ds_df['State_Code'] = ds_df['State_Code'].apply(lambda x: x.replace("Florida", "FL").replace("Colorado", "CO").replace("North Carolina", "NC").replace("Arizona", "AZ").replace("Utah", "UT").replace(" ", ""))

State_Values = ds_df['State_Code'].unique()
print("Cleaning Complete for 'State_Code' Column")
print("All final unique text in State Column are: ")
print(State_Values )
print(" ")

# "Co_Founded_in" Variable
founded_null_values = ds_df['Co_Founded_in'].isnull().sum()
print("Numbers rows with missing value in Co_Founded_in Column = "+str(founded_null_values))
print(" ")

ds_df['Age_of_Co'] = ds_df['Co_Founded_in'].apply(lambda x: x if x == "NA" else 2021 - x)

print("Calculated 'Age_of_Co' using 'Co_Founded_in' column")
print(" ")

# Extracting State Name in a column from State_Code

statescodes_to_names = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
      
ds_df["State_Name"] = ds_df["State_Code"].replace(statescodes_to_names)

print("Added State_Name Column for better analyses")
print(" ")

print("Final Data Shape is Rows by Columns: "+str(ds_df.shape))
print(" ")

# Making Technique Column

def Techniques(r):
    r = str(r)
    if "machine" in r.lower() or "ml" in r.lower():
        return "AI, Machine Learning"
    elif "deep" in r.lower():
        return "AI, ML, Deep Learning"
    elif "nlp" in r.lower() or "natural" in r.lower() or "nlu" in r.lower():
        return "AI, ML, DL, Natural Language Processing"
    else:
        return "AI"
    
ds_df['Technique_Focused'] = ds_df["Job Title"].apply(Techniques)

# Making Senior or not Column
    
def Senior(r):
    r = str(r)
    if "senior" in r.lower() or "sr" in r.lower() or "lead" in r.lower():
        return 1
    else:
        return 0
    
ds_df['Senior_in_Title_y/n'] = ds_df['Job Title'].apply(Senior)

# Making Remote Column

def Remote(r):
    r = str(r)
    if "remote" in r.lower():
        return 1
    else:
        return 0

ds_df['Remote_work_y/n'] = ds_df['Job Title'].apply(Remote)

# Downloading Cleaned data in csv format

ds_df.to_csv("Salary_Data_Cleaned_USA.csv", index = False)

print("Downloaded cleaned data set in your file named 'Salary_Data_Cleaned_USA.csv'")



   