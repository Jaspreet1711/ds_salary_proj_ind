# Data Science Salary Predcition Project


## Data Collection

<p>I collected data using Webscraper from Glassdoor Website. I have extracted all the details of Data Science jobs from various cities and states across USA (Check folder "Data Collected Using Glassdoor_Scraper" in the same repository). I consolidated all the outputs into one Excel file mentioned below.</p> 
        
File Name -  DS Jobs in USA (Consolidated).xlsx
  
Source - [Glassdoor Website](https://www.glassdoor.com/Job/index.htm)
  
 --------------------------------------------------------------- 
 
  #### GLassdoor Webscraper
  
  1. I created this Web Scraper <strong>Glassdoor_Scraper_V2.py</strong> using Selenium Library in python to extract Data from Glassdoor Website about Jobs and Salary.
  2. It collects the data and give output in Excel Format.
  3. Requirements and Settings to use Glassdoor_Scraper_V2:
       - Python Environment in your system (Anaconda)
       - Python Libraries used and need to be pip install are:
           -  selenium
           -  pandas 
           -  time
       - Copy & Paste all the codes in Glassdoor_Scraper_V2.py in any python ide (Like Spyder, Jupyter Notebook) and save it as .py or .ipynb file in your system.
       - Chromedriver.exe should be installed in your system to run this code. [Click here](https://chromedriver.chromium.org/downloads) to install. Please ignore if you already have.
       - Change path in Glassdoor_Scraper_V2.py (Line 80) to your system's path where you have saved Chromedriver.exe      
  4. Excel file will be downloaded in your system where you have saved Glassdoor_Scraper_V2.py or .ipynb .
  5. Take a look at Jupyter Notebook in the reposotory name "Data Collection using - Glassdoor_Scraper.ipynb" for your reference on how to use this Web Scraper.     
  6. Check the Inputs we need to give while running this Web Scraper in Python and Output(Details) we will get after code runs successfully.
       |              INPUTS                |     OUTPUTS    |     
       | :--------------------------------- |:-------------- |
       | Job Title                          | Company Name   | 
       | Location                           | Job Title      |
       | Number of Pages you want to scrape | City           |
       | Full Page Upload Speed in Seconds  | Salary         |
       | Output File Name (Excel)           | Company Rating |
       |                                    | Job Post Age   |
       |                                    | Job Description|
       |                                    | Company Size   |
       |                                    | Co Founded in  |
       |                                    | Company Type   |
       |                                    | Industry       |
       |                                    | Sector         |
       |                                    | Revenue Earned |
       |                                    | Website        |

  <em>OUTPUTS mentioned above are columns in Excel File that you will get as an Output using the Glassdoor_Scraper_V2.py</em>

----------------------------------------------------------------------------


## Data Cleaning

<p>Data we got using Scaper "DS Jobs in USA (Consolidated).xlsx" was cleaned. So, that we could analyse Salary offered in Data Science accross United States of America. Data mentioned in the Scraping output is not in numeric form and standardized (Like salaries ar mention in Per annum and Per hour bases under the Same Column).</p>

#### Dropped Columns
2 Columns were removed:
        <li>1. Unamed 0 - it is the indexing while getting the output in dataframe format using pandas in Web Scraping Code (Glassdoor_Scraper_V2.py). </li>
        <li>2. Job_Description - We will not be doing any analyses on the basis of Job Description because i found Job Description of various jobs were empty or not giving full description as required by the companies. So, it didn't make any sense for me to analyse based on missing Description. For example "Python" in Programming Language Skill required for a Job was not mentioned in majourity of the Job Descriptions but there can be a possibility that Jobs with Empty or missing Job Description would have required Python programming language from the desired candidate.</li> 
