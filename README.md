# Data Science Salary Predcition Project


# Data Collection

<p>I collected data using Webscraper from Glassdoor Website. I have extracted all the details of Data Science jobs from various cities and states across USA (Check folder "Data Collected USA"). I consolidated all the outputs into one Excel file mentioned below.</p> 
        
File Name -  DS Jobs in USA (Consolidated).xlsx
  
Source - [Glassdoor Website](www.glassdoor.com)
  
 --------------------------------------------------------------- 
 
  ### GLassdoor Webscraper
  
  1. I created this Web Scraper Glassdoor_Scraper_V2.py using Selenium Library in python to extract Data from Glassdoor Website about Jobs and Salary.
  2. It collected the data and gave output in Excel Format.
  3. Requirements to use Glassdoor_Scraper_V2:
      - Python Environment in your system (Anaconda)
      - Libraries used are - selenium, pandas & time
      - Chromedriver.exe should be installed in your system to use this code. [Click here](https://chromedriver.chromium.org/downloads) to install. Please ignore if you already have.
      - Change path in Glassdoor_Scraper_V2.py (Line 80) to your system's path where you have saved Chromedriver.exe      
  4. Excel file will be downloaded in your system where you have saved Glassdoor_Scraper_V2.py
 
       
         Glassdoor_Scraper_V2.py

         Created on 7th October 2021

         Author Details:
               
              Name            -  Jaspreet Singh
              Github Username -  Jaspreet1711
              Email ID        -  singhjaspreet1711@outlook.com
    
  
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

----------------------------------------------------------------------------
