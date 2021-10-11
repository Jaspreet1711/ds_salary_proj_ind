"""
Glassdoor Web Scraper

Created on 7th October 2021

Author Details:
               Name            -  Jaspreet Singh
               Github Username -  Jaspreet1711
               Email ID        -  singhjaspreet1711@outlook.com

Change Path in line 80 according to your system path where chromedriver.exe is saved
Download Chromerdriver.exe from 
https://chromedriver.chromium.org/downloads
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
from time import localtime, strftime
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)

def gl_scrap():
    
    # Details and Info of Scraping
    print(bcolors.BOLD + "This function will fetch details from Glassdoor Website uptill pages given by you of various openings of any role or job title within a location given by you.")
    print("Details will be fetched in excel format.")
    print(" ")
    
    print("You will be required to download chromedriver.exe from the link mentioned below: ")
    print("https://chromedriver.chromium.org/downloads")
    print("Copy & paste the downloaded chromedriver.exe in the same folder where you have saved this Glassdoor_Scraper.py file")
    print(bcolors.WARNING + "Change the Path (in code line 80 in Glassdoor_Scraper.py) to your system path where you have saved the chromediver.exe")
    print(bcolors.OKGREEN + "Your output excel will be saved in same folder.")
    print(" ")
    
    time.sleep(1)
    
    # Inputs for Scraping
    Job_or_Role = str(input("Enter the Job_title or Role: "))
    Location = str(input("Enter the location: "))
    Pgs = int(input("Enter num of pages you want to scrape: "))
    print(" ")
    
    print("Depending upon your Internet Speed decide second(s) to wait before page fully uploads")
    print("3 Seconds are ideal. Go for 4 or 5 Seconds if your Internet Speed is really slow.")
    print("If you have fast Internet 2 Seconds are appropriate")
    Secs = int(input("Enter Second(s) for page load time: "))
    Output_DF_Name = str(input("Enter the Output file name you want to save: "))
    
    print(" ")
    print(" ")
    
    # Calculating approx time for Scraping and collecting data in excel format
    minutes = str(round((((((Secs/1.5)*30)*Pgs) + (Secs*4))/60) + 3)) 
    print(bcolors.WARNING + "It will take approximately "+minutes+" mins to scrape through 5 pages with all details into dataframe" )
    print(" ")
    print(" ")
    
    #Scraping Starts after taking all the Inputs (Remember to change path below according to your system)
    print(bcolors.OKGREEN + "Opening_the_Glassdoor_Website_in_ChromeBrowser")
    path = 'C:/Users/Jaspreet Singh/Desktop/DS_Projects/ds_sal_proj_backup/chromedriver.exe' # CHANGE THIS PATH 
    driver = webdriver.Chrome(path) # selecting the browser to be opened
    driver.get("https://www.glassdoor.com/blog/tag/job-search/") # selecting the website
    print(bcolors.OKBLUE + driver.title)   # getting the title in web page

    time.sleep(1)

    # Searching Job Title or Role 
    print(bcolors.OKGREEN + "Searching_for_Job_Entered_by_you")
    try:
        search_job = driver.find_element_by_id("sc.keyword")
        search_job.send_keys(Job_or_Role)
        search_job.send_keys(Keys.RETURN)
        print(bcolors.WARNING + "Job_is_Successfully_Searched")
    except:
        print(bcolors.FAIL + "Job_Search_Failed")
        time.sleep(Secs)
        driver.close()
    
    # Searching Location
    time.sleep(Secs)
    print(bcolors.OKGREEN + "It_will_search_Jobs_on_location_entered")
    try:
        see_all = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-test='jobs-location-see-all-link']"))
            )
        
        actions = ActionChains(driver)
        actions.click(see_all)
        actions.perform()
        time.sleep(1)
    
        search_loc = driver.find_element_by_id("sc.location")
        search_loc.send_keys(Location)
        search_loc.send_keys(Keys.RETURN)
        print(bcolors.BOLD + "Wait_for_few_seconds_as_page_loading_takes_time_while_searching_jobs_on_location")
        time.sleep(Secs*4)    
    except:
        print(bcolors.FAIL + "Failed_on_searching_jobs_on_Location")
        time.sleep(Secs)
    
    print(" ")
    print(" ")
    
    #Looking for Left and Right Arrow to Navigate through Pages.
    print(bcolors.BOLD + "Finding_Page_Number_Change_Elements_on_WebPage")
    print(bcolors.OKGREEN + "It_Will_first_Let_Login-Pop-up_Trigger_and_Close_it_for_smooth_Scraping_ahead")
    
    left_arrow = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-test='pagination-prev']"))
        )
    right_arrow = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-test='pagination-next']"))
        ) 
    
    # Closing the login Pop Up before collecting the Data. It will change the page to trigger the pop up and close it.
    try:            
        right_arrow.click()
        print(bcolors.OKGREEN + "Waiting_for_Login_Pop-up")
        time.sleep(Secs/2)
        cross = 'svg[class="SVGInline-svg modal_closeIcon-svg"]'
        cross_loc = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, cross))
            )
        cross_loc.click()
        print(bcolors.WARNING + "Login_Pop_up_Closed_Successfully")
        print(bcolors.WARNING + "Page_Numbers_Element_Found_Successfully")
       
    except:
        print(bcolors.FAIL + "Failed_to_Find_Page_Numbers_Elements_on_WebPage")
        time.sleep(4)
        driver.close()
    
    # Page Numbers requested (Input) can be more than Total Pages Available for that Job in given Location. It can give error to avoid that we will first check and rectify it. 
    Pages_Tray = driver.find_element_by_css_selector("div[data-test='page-x-of-y']").text.split(" ")
    Available_Pgs = int(Pages_Tray[3])
    Extra_Pgs = Pgs - Available_Pgs
    if Pgs > Available_Pgs:
        print(bcolors.FAIL + "Pages requested by you i.e. "+str(Pgs)+" are more than Total Number of Pages i.e."+str(Available_Pgs))
        print(bcolors.WARNING + "We will reduce the Pages requested by you to Total Pages Available")
        time.sleep(3)
        Pgs = Pgs - Extra_Pgs
        print("Done revised Pages to Scrape Input to "+str(Pgs))
        time.sleep(2)
    else:
        pass

    print(" ")
    print(" ")

########################################################################################################################################################
    
    #Data Collection will start from Page 1
    print(bcolors.OKBLUE + "Now_Scraping_will_start_from_page-1_till_page-"+str(Pgs))    
    
    #Variables to be collected of the job (Basically these are all columns in output Excel it will get)
    company_name = []
    designation = []
    city = []
    salary = []
    rating = []
    posted = []
    
    jd =[]
    size = []
    founded = []
    co_type = []
    industry = []
    sector = []
    revenue = []
    website = []

    #Starts from Page-1 
    left_arrow.click()
    time.sleep(Secs)
    print(" ")
    print(bcolors.OKGREEN + "Collecting_all_Job_Opening_Details_on_Page-1 - In Element Form")
    try:
        ul = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-test='jlGrid']"))
            )
            
        jobs_list = ul.find_elements_by_tag_name("li")
        
        co = []
        des = []
        cit = []
        sal = []
        rat = []
        pos = []
        
        for openings in jobs_list:
            try:
                co.append(openings.find_element_by_css_selector("div[class = 'd-flex justify-content-between align-items-start']"))
            except:
                co.append("NA")
                    
            try:
                des.append(openings.find_element_by_css_selector("a[class='css-h3hi0t jobLink css-1rd3saf eigr9kq1']"))
            except Exception:
                des.append(openings.find_element_by_css_selector("a[class='jobLink css-1rd3saf eigr9kq1']"))    
            except:
                des.append("NA")

            try:    
                cit.append(openings.find_element_by_css_selector("span[class='css-1buaf54 pr-xxsm css-iii9i8 e1rrn5ka4']"))    
            except:
                cit.append("NA")

            try:    
                sal.append(openings.find_element_by_css_selector("span[data-test='detailSalary']"))
            except:
                sal.append("NA")

            try:
                rat.append(openings.find_element_by_css_selector("span[class=' css-srfzj0 e1cjmv6j0']"))
            except:
                rat.append("NA")

            try:    
                pos.append(openings.find_element_by_css_selector("div[data-test='job-age']"))
            except:
                pos.append("NA")
    
    except:
        print(bcolors.FAIL + "Error_in_locating_element(s)_on_page-1")
          
        
    print(bcolors.OKGREEN + "Extracting_Text_from_Elements_collected_in_Page-1")
        
    try:
        for i in co:
            try:
                company_name.append(i.text)
            except:
                company_name.append(i)
    
        for i in des:
            try:
                designation.append(i.text)
            except:
                designation.append(i)
            
        for i in cit:
            try:
                city.append(i.text)
            except:
                city.append(i)
                
        for i in sal:
            try:
                salary.append(i.text)    
            except:
                salary.append(i)
                
        for i in rat:
            try:
                rating.append(i.text)
            except:
                rating.append(i)
                
        for i in pos:
            try:
                posted.append(i.text)
            except:
                posted.append(i)       
        
        print(bcolors.WARNING + "All_Details_Retrieved_Successfully_from_page-1")          
        
    except:
        print(bcolors.FAIL + "Failed_to_retrieve_Details_from_page-1")
    
    #It will Start Clicking on each job to get data out of it.
    print(bcolors.OKCYAN + "Getting_JobDescription_on_page-1_Wait_for_Few_More_Seconds")
        
    for opening in jobs_list:
        opening.click()
        time.sleep(Secs/1.5)
        try:
            jd.append(driver.find_element_by_css_selector("div[class='jobDescriptionContent desc']").text)
        except:
            jd.append("NA")
        try:
            ov = driver.find_elements_by_css_selector("span[class='css-1ff36h2 e1pvx6aw0']")
            if len(ov) == 6:
                size.append(ov[0].text)
                founded.append(ov[1].text)
                co_type.append(ov[2].text)
                industry.append(ov[3].text)
                sector.append(ov[4].text)
                revenue.append(ov[5].text)
            elif len(ov) == 5:
                size.append(ov[0].text)
                founded.append("NA")
                co_type.append(ov[1].text)
                industry.append(ov[2].text)
                sector.append(ov[3].text)
                revenue.append(ov[4].text)
            elif len(ov) == 3:
                size.append(ov[0].text)
                founded.append("NA")
                co_type.append(ov[1].text)
                industry.append("NA")
                sector.append("NA")
                revenue.append(ov[2].text)
            else:
                size.append("NA")
                founded.append("NA")
                co_type.append("NA")
                industry.append("NA")
                sector.append("NA")
                revenue.append("NA")
        except:
            size.append("NA")
            founded.append("NA")
            co_type.append("NA")
            industry.append("NA")
            sector.append("NA")
            revenue.append("NA")
        try:
            www = driver.find_element_by_css_selector("div[class='m-0 pt-sm pb']")
            url = www.find_element_by_tag_name("a")
            website.append(url.get_attribute('href'))
        except:
            website.append("NA")       

    page_num = 1    

    # Now, it will collect from rest of the pages using Loop Function. Page Numbers to scrape requested (Input) are placed in end limit of Range mentioned below
    # As page-1 doesn't require Right Click we cannot place page-1 in loop.
    for i in range(1,Pgs):
        right_arrow.click()
        time.sleep(Secs)
        
        page_num = page_num + 1
        
        print(" ")
        print(bcolors.OKGREEN + "Collecting_all_Job_Opening_Details_on_Page-"+str(page_num)+" - In Element Form")
        try:
            ul = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-test='jlGrid']"))
                )
            
            jobs_list = ul.find_elements_by_tag_name("li")
        
            co = []
            des = []
            cit = []
            sal = []
            rat = []
            pos = []
        
            for openings in jobs_list:
                try:
                    co.append(openings.find_element_by_css_selector("div[class = 'd-flex justify-content-between align-items-start']"))
                except:
                    co.append("NA")
                    
                try:
                    des.append(openings.find_element_by_css_selector("a[class='css-h3hi0t jobLink css-1rd3saf eigr9kq1']"))
                except Exception:
                    des.append(openings.find_element_by_css_selector("a[class='jobLink css-1rd3saf eigr9kq1']"))    
                except:
                    des.append("NA")

                try:    
                    cit.append(openings.find_element_by_css_selector("span[class='css-1buaf54 pr-xxsm css-iii9i8 e1rrn5ka4']"))    
                except:
                    cit.append("NA")

                try:    
                    sal.append(openings.find_element_by_css_selector("span[data-test='detailSalary']"))
                except:
                    sal.append("NA")

                try:
                    rat.append(openings.find_element_by_css_selector("span[class=' css-srfzj0 e1cjmv6j0']"))
                except:
                    rat.append("NA")

                try:    
                    pos.append(openings.find_element_by_css_selector("div[data-test='job-age']"))
                except:
                    pos.append("NA")
    
        except:
            print(bcolors.FAIL + "Error_in_locating_element(s)_on_page-"+str(page_num))
          
        
        print(bcolors.OKGREEN + "Extracting_Text_from_Elements_collected_in_Page-"+str(page_num))    
        
       
        
        try:
            for i in co:
                try:
                    company_name.append(i.text)
                except:
                    company_name.append(i)
    
            for i in des:
                try:
                    designation.append(i.text)
                except:
                    designation.append(i)
            
            for i in cit:
                try:
                    city.append(i.text)
                except:
                    city.append(i)
                
            for i in sal:
                try:
                    salary.append(i.text)    
                except:
                    salary.append(i)
                
            for i in rat:
                try:
                    rating.append(i.text)
                except:
                    rating.append(i)
                
            for i in pos:
                try:
                    posted.append(i.text)
                except:
                    posted.append(i)       
        
            print(bcolors.WARNING + "All_Details_Retrieved_Successfully_from_page-"+str(page_num))          
        
        except:
            print(bcolors.FAIL + "Failed_to_retrieve_Details_from_page-"+str(page_num))
    
        #Will Start Clicking on each job to get data out of it.
        print(bcolors.OKCYAN + "Getting_JobDescription_on_page-"+str(page_num)+"_Wait_for_Few_More_Seconds")
        
        for opening in jobs_list:
            opening.click()
            time.sleep(Secs/1.5)
            try:
                jd.append(driver.find_element_by_css_selector("div[class='jobDescriptionContent desc']").text)
            except:
                jd.append("NA")
            try:
                ov = driver.find_elements_by_css_selector("span[class='css-1ff36h2 e1pvx6aw0']")
                if len(ov) == 6:
                    size.append(ov[0].text)
                    founded.append(ov[1].text)
                    co_type.append(ov[2].text)
                    industry.append(ov[3].text)
                    sector.append(ov[4].text)
                    revenue.append(ov[5].text)
                elif len(ov) == 5:
                    size.append(ov[0].text)
                    founded.append("NA")
                    co_type.append(ov[1].text)
                    industry.append(ov[2].text)
                    sector.append(ov[3].text)
                    revenue.append(ov[4].text)
                elif len(ov) == 3:
                    size.append(ov[0].text)
                    founded.append("NA")
                    co_type.append(ov[1].text)
                    industry.append("NA")
                    sector.append("NA")
                    revenue.append(ov[2].text)
                else:
                    size.append("NA")
                    founded.append("NA")
                    co_type.append("NA")
                    industry.append("NA")
                    sector.append("NA")
                    revenue.append("NA")
            except:
                size.append("NA")
                founded.append("NA")
                co_type.append("NA")
                industry.append("NA")
                sector.append("NA")
                revenue.append("NA")
            try:
                www = driver.find_element_by_css_selector("div[class='m-0 pt-sm pb']")
                url = www.find_element_by_tag_name("a")
                website.append(url.get_attribute('href'))
            except:
                website.append("NA")    
            
#####################################################################################################################################################
    
    # Arranging Data in Data Frame
    print(" ")
    print(bcolors.WARNING + "Scraping_Job_Done_for_all_"+str(Pgs)+"_Page(s)")
    
    print(" ")
    print(" ")
    print(bcolors.OKGREEN + "Arranging data in DataFrame")
    
    time.sleep(1)

    company_name = company_name
    designation = designation
    city = city
    salary = salary
    company_rating = rating
    job_post_age = posted
    
    Job_description = jd
    Company_Size = size 
    Co_Founded_in = founded 
    Company_Type = co_type 
    Industry = industry 
    Sector = sector 
    Revenue_Earned = revenue
    Website = website 

    Output_DF = pd.DataFrame(
    {'Company_Name': company_name,
     'Job Title': designation,
     'Location': city,
     'Salary': salary,
     'Company_Rating': company_rating,
     'Job_Post_Age': job_post_age,
     'Company_Size': Company_Size,
     'Co_Founded_in': Co_Founded_in,
     'Company_Type': Company_Type,
     'Industry': Industry,
     'Sector': Sector,
     'Revenue_Earned': Revenue_Earned,
     'Website': Website,
     'Data_Collected_on': time.strftime("%d-%m-%Y %H:%M", localtime()),
     'Job_Description': Job_description
    })
    
    print(" ")
    print(" ")
    print(bcolors.WARNING + "DataFrame is made successfully and named "+Output_DF_Name+" with all the details.")
    print(bcolors.WARNING + "Output will be saved in excel format in your system.")
    print(" ")
    print(" ")

    datatoexcel = pd.ExcelWriter(Output_DF_Name+'.xlsx')
    
    Output_DF.to_excel(datatoexcel)

    try:
        datatoexcel.save()
        print(bcolors.WARNING + Output_DF_Name+".xlsx is Successfully Saved in your system.")
        print(bcolors.WARNING + "Check your folder with Excel File named - "+Output_DF_Name+".xlsx")
    except:
        print(bcolors.Fail + "Error: In saving"+Output_DF_Name+".xlsx")
        print(bcolors.Fail + "May be same name file already exsist in your system.")
        
    time.sleep(Secs)
    driver.close()             
    
        
    