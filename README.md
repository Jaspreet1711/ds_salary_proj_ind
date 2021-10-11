# Data Science Salary Predcition Project

# Data Collection
  
  ### GLassdoor Webscraper
  - I created this Web Scraper Glassdoor_Scraper_V2.py using Selenium Library in python to extract Data from Glassdoor Website about Jobs and Salary.
  - It will collect data and will give output in Excel Format.
  - Excel file will be downloaded in your system where you have saved Glassdoor_Scraper_V2.py
  
  ### Requirements to use Glassdoor_Scraper_V2:
  - Python Environment in your system (Anaconda)
  - Libraries used are - selenium, pandas & time
  - Chromedriver.exe should be installed in your system to use this code. [Click here](https://chromedriver.chromium.org/downloads) to install. Please ignore if you already have.
  - Change path in Glassdoor_Scraper_V2.py (Line 80) to your system's path where you have saved Chromedriver.exe      
        
        Glassdoor_Scraper_V2.py

        Created on 7th October 2021

       
        Author Details:
               
               Name            -  Jaspreet Singh
               Github Username -  Jaspreet1711
               Email ID        -  singhjaspreet1711@outlook.com

        Input:  
               1. Job Title
               2. Location
               3. Number of Pages you want to scrape
               4. Full Page Upload Speed in Seconds
               5. Output File Name (Excel)
               
        Output:
        All of these are columns in Excel Output
               1. company_name
               2. Job Title
               3. City 
               4. Salary 
               5. Company Rating 
               6. Job Post Age
               7. Job Description
               8. Company Size 
               9. Co Founded in 
               10. Company Type 
               11. Industry 
               12. Sector
               13. Revenue Earned
               14. Website 
