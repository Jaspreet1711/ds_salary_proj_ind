from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
from itertools import chain
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

def glassdoor_pg5():
    
    print(bcolors.BOLD + "This function will fetch details from Glassdoor Website uptill 5 pages of various openings of any role or job title within a location given by you.")
    print("Details will be fetched in excel format.")
    print(" ")
    print(" ")
    
    Job_or_Role = str(input("Enter the Job_title or Role: "))
    Location = str(input("Enter the location: "))
    print("Depending upon your Internet Speed decide second(s) to wait before page fully uploads")
    print("3 Seconds are ideal. Go for 4 or 5 Seconds if your Internet Speed is really slow.")
    print("If you have fast Internet 2 Seconds are appropriate")
    Secs = int(input("Enter Second(s) for page load time: "))
    Output_DF_Name = str(input("Enter the Output file name you want to save: "))
    print(" ")
    print(" ")
    minutes = str(round((((((Secs/1.5)*30)*5) + (Secs*4))/60) + 2)) 
    print("It will take approximately "+minutes+" mins to scrape through 5 pages with all details into dataframe" )
    print(" ")
    print(" ")
    
    print("Opening_the_Glassdoor_Website_in_ChromeBrowser")
    path = 'c:/Users/Jaspreet Singh/Desktop/DS_Projects/Test_Project/ds_salary_proj_ind/chromedriver.exe'
    driver = webdriver.Chrome(path) # selecting the browser to be opened
    driver.get("https://www.glassdoor.com/blog/tag/job-search/") # selecting the website
    print(bcolors.OKBLUE + driver.title)   # getting the title in web page

    time.sleep(1)

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
    print(bcolors.BOLD + "Finding_Page_Numbers_Elements_on_WebPage")
    print(bcolors.OKGREEN + "It_Will_first_Let_Login-Pop-up_Trigger_and_Close_it_for_smooth_Scraping_ahead")
    try:        
        page_nums = []
        for n in range(1,6):
            P = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.LINK_TEXT, str(n)))
                )
            page_nums.append(P)
        
        page_1 = page_nums[0]
        page_2 = page_nums[1]
        page_3 = page_nums[2]
        page_4 = page_nums[3]
        page_5 = page_nums[4]
    
        page_2.click()
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
        
    print(" ")
    print(" ")
    print(bcolors.OKBLUE + "Now_Scraping_will_start_from_page-1_till_page-5")    
      
    #Page_1
    page_1.click()
    time.sleep(Secs)
    print(" ")
    print(bcolors.OKGREEN + "Collecting_all_Job_Opening_Details_on_Page-1 - In Element Form")
    try:
        ul = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-test='jlGrid']"))
            )
        
        jobs_list = ul.find_elements_by_tag_name("li")
        
        co_1 = []
        des_1 = []
        cit_1 = []
        sal_1 = []
        rat_1 = []
        pos_1 = []
        
        for openings in jobs_list:
            try:
                co_1.append(openings.find_element_by_css_selector("div[class = 'd-flex justify-content-between align-items-start']"))
            except:
                co_1.append("NA")

            try:
                des_1.append(openings.find_element_by_css_selector("a[class='css-h3hi0t jobLink css-1rd3saf eigr9kq1']"))
            except Exception:
                des_1.append(openings.find_element_by_css_selector("a[class='jobLink css-1rd3saf eigr9kq1']"))    
            except:
                des_1.append("NA")

            try:    
                cit_1.append(openings.find_element_by_css_selector("span[class='css-1buaf54 pr-xxsm css-iii9i8 e1rrn5ka4']"))    
            except:
                cit_1.append("NA")

            try:    
                sal_1.append(openings.find_element_by_css_selector("span[data-test='detailSalary']"))
            except:
                sal_1.append("NA")

            try:
                rat_1.append(openings.find_element_by_css_selector("span[class=' css-srfzj0 e1cjmv6j0']"))
            except:
                rat_1.append("NA")

            try:    
                pos_1.append(openings.find_element_by_css_selector("div[data-test='job-age']"))
            except:
                pos_1.append("NA")
    
    except:
        print(bcolors.FAIL + "Error_in_locating_element(s)_on_page-1")
          
        
    print(bcolors.OKGREEN + "Extracting_Text_from_Elements_collected_in_Page-1")    
    try:
        company_name_1 = []
        for i in co_1:
            try:
                company_name_1.append(i.text)
            except:
                company_name_1.append(i)
            
        designation_1 = []
        for i in des_1:
            try:
                designation_1.append(i.text)
            except:
                designation_1.append(i)
            
        city_1 = []
        for i in cit_1:
            try:
                city_1.append(i.text)
            except:
                city_1.append(i)
                
        salary_1 = []
        for i in sal_1:
            try:
                salary_1.append(i.text)    
            except:
                salary_1.append(i)
                
        rating_1 = []
        for i in rat_1:
            try:
                rating_1.append(i.text)
            except:
                rating_1.append(i)
                
        posted_1 = []
        for i in pos_1:
            try:
                posted_1.append(i.text)
            except:
                posted_1.append(i)       
        
        print(bcolors.WARNING + "All_Details_Retrieved_Successfully_from_page-1")          
        
    except:
        print(bcolors.FAIL + "Failed_to_retrieve_Details_from_page-1")
    
    print(bcolors.OKCYAN + "Getting_JobDescription_on_page-1_Wait_for_Few_More_Seconds")
    jd_1 =[]    
    for opening in jobs_list:
        try:
            opening.click()
            time.sleep(Secs/1.5)  
            jd_1.append(driver.find_element_by_css_selector("div[class='jobDescriptionContent desc']").text)
        except:
            jd_1.append("NA")
        
    #Page_2
    page_2.click()
    time.sleep(Secs)
    print(" ")
    print(bcolors.OKGREEN + "Collecting_all_Job_Opening_Details_on_Page-2 - In Element Form")
    try:
        ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-test='jlGrid']"))
            )
        
        jobs_list = ul.find_elements_by_tag_name("li")
        
        co_2 = []
        des_2 = []
        cit_2 = []
        sal_2 = []
        rat_2 = []
        pos_2 = []

        for openings in jobs_list:
            try:
                co_2.append(openings.find_element_by_css_selector("div[class = 'd-flex justify-content-between align-items-start']"))
            except:
                co_2.append("NA")
            
            try:
                des_2.append(openings.find_element_by_css_selector("a[class='css-h3hi0t jobLink css-1rd3saf eigr9kq1']"))
            except Exception:
                des_2.append(openings.find_element_by_css_selector("a[class='jobLink css-1rd3saf eigr9kq1']"))    
            except:
                des_2.append("NA")
            
            try:
                cit_2.append(openings.find_element_by_css_selector("span[class='css-1buaf54 pr-xxsm css-iii9i8 e1rrn5ka4']"))
            except:
                cit_2.append("NA")
            
            try:
                sal_2.append(openings.find_element_by_css_selector("span[data-test='detailSalary']"))
            except:
                sal_2.append("NA")

            try:
                rat_2.append(openings.find_element_by_css_selector("span[class=' css-srfzj0 e1cjmv6j0']"))
            except:
                rat_2.append("NA")
            
            try:
                pos_2.append(openings.find_element_by_css_selector("div[data-test='job-age']"))
            except:
                pos_2.append("NA")
    
    except:
        print(bcolors.FAIL + "Error_in_locating_element(s)_on_page-2")
          
    print(bcolors.OKGREEN + "Extracting_Text_from_Elements_collected_in_Page-2")
    try:
        company_name_2 = []
        for i in co_2:
            try:
                company_name_2.append(i.text)
            except:
                company_name_2.append(i)
            
        designation_2 = []
        for i in des_2:
            try:
                designation_2.append(i.text)
            except:
                designation_2.append(i)
            
        city_2 = []
        for i in cit_2:
            try:
                city_2.append(i.text)
            except:
                city_2.append(i)
                
        salary_2 = []
        for i in sal_2:
            try:
                salary_2.append(i.text)    
            except:
                salary_2.append(i)
                
        rating_2 = []
        for i in rat_2:
            try:
                rating_2.append(i.text)
            except:
                rating_2.append(i)
                
        posted_2 = []
        for i in pos_2:
            try:
                posted_2.append(i.text)
            except:
                posted_2.append(i)
        
        print(bcolors.WARNING + "All_Details_Retrieved_Successfully_from_page-2")           
    
    except:
        print(bcolors.FAIL + "Failed_to_retrieve_Details_from_page-2")
    
    print(bcolors.OKCYAN + "Getting_JobDescription_on_page-2_Wait_for_Few_More_Seconds")
    jd_2 =[]    
    for opening in jobs_list:
        try:
            opening.click()
            time.sleep(Secs/1.5)
            jd_2.append(driver.find_element_by_css_selector("div[class='jobDescriptionContent desc']").text)
        except:
            jd_2.append("NA")
            
    #Page_3
    page_3.click()
    time.sleep(Secs)
    print(" ")
    print(bcolors.OKGREEN + "Collecting_all_Job_Opening_Details_on_Page-3 - In Element Form")
    try:
        ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-test='jlGrid']"))
            )
        
        jobs_list = ul.find_elements_by_tag_name("li")
        co_3 = []
        des_3 = []
        cit_3 = []
        sal_3 = []
        rat_3 = []
        pos_3 = []

        for openings in jobs_list:
            try:
                co_3.append(openings.find_element_by_css_selector("div[class = 'd-flex justify-content-between align-items-start']"))
            except:
                co_3.append("NA")

            try:
                des_3.append(openings.find_element_by_css_selector("a[class='css-h3hi0t jobLink css-1rd3saf eigr9kq1']"))
            except Exception:
                des_3.append(openings.find_element_by_css_selector("a[class='jobLink css-1rd3saf eigr9kq1']"))    
            except:
                des_3.append("NA")

            try:
                cit_3.append(openings.find_element_by_css_selector("span[class='css-1buaf54 pr-xxsm css-iii9i8 e1rrn5ka4']"))    
            except:
                cit_3.append("NA")

            try:
                sal_3.append(openings.find_element_by_css_selector("span[data-test='detailSalary']"))
            except:
                sal_3.append("NA")

            try:
                rat_3.append(openings.find_element_by_css_selector("span[class=' css-srfzj0 e1cjmv6j0']"))
            except:
                rat_3.append("NA")

            try:
                pos_3.append(openings.find_element_by_css_selector("div[data-test='job-age']"))
            except:
                pos_3.append("NA")
    
    except:
        print(bcolors.FAIL + "Error_in_locating_element(s)_on_page-3")
          
        
    print(bcolors.OKGREEN + "Extracting_Text_from_Elements_collected_in_Page-3")
    try:
        company_name_3 = []
        for i in co_3:
            try:
                company_name_3.append(i.text)
            except:
                company_name_3.append(i)
            
        designation_3 = []
        for i in des_3:
            try:
                designation_3.append(i.text)
            except:
                designation_3.append(i)
            
        city_3 = []
        for i in cit_3:
            try:
                city_3.append(i.text)
            except:
                city_3.append(i)
                
        salary_3 = []
        for i in sal_3:
            try:
                salary_3.append(i.text)    
            except:
                salary_3.append(i)
                
        rating_3 = []
        for i in rat_3:
            try:
                rating_3.append(i.text)
            except:
                rating_3.append(i)
                
        posted_3 = []
        for i in pos_3:
            try:
                posted_3.append(i.text)
            except:
                posted_3.append(i)
        
        print(bcolors.WARNING + "All_Details_Retrieved_Successfully_from_page-3")           
    
    except:
        print(bcolors.FAIL + "Failed_to_retrieve_Details_from_page-3")    
    
    print(bcolors.OKCYAN + "Getting_JobDescription_on_page-3_Wait_for_Few_More_Seconds")
    jd_3 =[]    
    for opening in jobs_list:
        try:
            opening.click()
            time.sleep(Secs/1.5)
            jd_3.append(driver.find_element_by_css_selector("div[class='jobDescriptionContent desc']").text)
        except:
            jd_3.append("NA")
            
    #Page_4
    page_4.click()
    time.sleep(Secs)
    print(" ")
    print(bcolors.OKGREEN + "Collecting_all_Job_Opening_Details_on_Page-4 - In Element Form")
    try:
        ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-test='jlGrid']"))
            )
    
        jobs_list = ul.find_elements_by_tag_name("li")
        co_4 = []
        des_4 = []
        cit_4 = []
        sal_4 = []
        rat_4 = []
        pos_4 = []

        for openings in jobs_list:
            try:
                co_4.append(openings.find_element_by_css_selector("div[class = 'd-flex justify-content-between align-items-start']"))
            except:
                co_4.append("NA")

            try:
                des_4.append(openings.find_element_by_css_selector("a[class='css-h3hi0t jobLink css-1rd3saf eigr9kq1']"))
            except Exception:
                des_4.append(openings.find_element_by_css_selector("a[class='jobLink css-1rd3saf eigr9kq1']"))    
            except:
                des_4.append("NA")

            try:
                cit_4.append(openings.find_element_by_css_selector("span[class='css-1buaf54 pr-xxsm css-iii9i8 e1rrn5ka4']"))    
            except:
                cit_4.append("NA")

            try:
                sal_4.append(openings.find_element_by_css_selector("span[data-test='detailSalary']"))
            except:
                sal_4.append("NA")

            try:
                rat_4.append(openings.find_element_by_css_selector("span[class=' css-srfzj0 e1cjmv6j0']"))
            except:
                rat_4.append("NA")

            try:
                pos_4.append(openings.find_element_by_css_selector("div[data-test='job-age']"))
            except:
                pos_4.append("NA")
    
    except:
        print(bcolors.FAIL + "Error_in_locating_element(s)_on_page-4")
          
        
    print(bcolors.OKGREEN + "Extracting_Text_from_Elements_collected_in_Page-4")    
    try:
        company_name_4 = []
        for i in co_4:
            try:
                company_name_4.append(i.text)
            except:
                company_name_4.append(i)
            
        designation_4 = []
        for i in des_4:
            try:
                designation_4.append(i.text)
            except:
                designation_4.append(i)
            
        city_4 = []
        for i in cit_4:
            try:
                city_4.append(i.text)
            except:
                city_4.append(i)
                
        salary_4 = []
        for i in sal_4:
            try:
                salary_4.append(i.text)    
            except:
                salary_4.append(i)
                
        rating_4 = []
        for i in rat_4:
            try:
                rating_4.append(i.text)
            except:
                rating_4.append(i)
                
        posted_4 = []
        for i in pos_4:
            try:
                posted_4.append(i.text)
            except:
                posted_4.append(i)

        print(bcolors.WARNING + "All_Details_Retrieved_Successfully_from_page-4")           
    
    except:
        print(bcolors.FAIL + "Failed_to_retrieve_Details_from_page-4")    
    
    print(bcolors.OKCYAN + "Getting_JobDescription_on_page-4_Wait_for_Few_More_Seconds")
    jd_4 =[]    
    for opening in jobs_list:
        try:
            opening.click()
            time.sleep(Secs/1.5)
            jd_4.append(driver.find_element_by_css_selector("div[class='jobDescriptionContent desc']").text)
        except:
            jd_4.append("NA")
            
    #Page_5
    page_5.click()
    time.sleep(Secs)
    print(" ")
    print(bcolors.OKGREEN + "Collecting_all_Job_Opening_Details_on_Page-5 - In Element Form")
    try:
        ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[data-test='jlGrid']"))
            )
    
        jobs_list = ul.find_elements_by_tag_name("li")
        co_5 = []
        des_5 = []
        cit_5 = []
        sal_5 = []
        rat_5 = []
        pos_5 = []

        for openings in jobs_list:
            try:
                co_5.append(openings.find_element_by_css_selector("div[class = 'd-flex justify-content-between align-items-start']"))
            except:
                co_5.append("NA")

            try:
                des_5.append(openings.find_element_by_css_selector("a[class='css-h3hi0t jobLink css-1rd3saf eigr9kq1']"))
            except Exception:
                des_5.append(openings.find_element_by_css_selector("a[class='jobLink css-1rd3saf eigr9kq1']"))    
            except:
                des_5.append("NA")

            try:
                cit_5.append(openings.find_element_by_css_selector("span[class='css-1buaf54 pr-xxsm css-iii9i8 e1rrn5ka4']"))    
            except:
                cit_5.append("NA")

            try:
                sal_5.append(openings.find_element_by_css_selector("span[data-test='detailSalary']"))
            except:
                sal_5.append("NA")

            try:
                rat_5.append(openings.find_element_by_css_selector("span[class=' css-srfzj0 e1cjmv6j0']"))
            except:
                rat_5.append("NA")

            try:
                pos_5.append(openings.find_element_by_css_selector("div[data-test='job-age']"))
            except:
                pos_5.append("NA")
    
    except:
        print(bcolors.FAIL + "Error_in_locating_element(s)_on_page-5")
          
        
    print(bcolors.OKGREEN + "Extracting_Text_from_Elements_collected_in_Page-5")    
    try:
        company_name_5 = []
        for i in co_5:
            try:
                company_name_5.append(i.text)
            except:
                company_name_5.append(i)
            
        designation_5 = []
        for i in des_5:
            try:
                designation_5.append(i.text)
            except:
                designation_5.append(i)
            
        city_5 = []
        for i in cit_5:
            try:
                city_5.append(i.text)
            except:
                city_5.append(i)
                
        salary_5 = []
        for i in sal_5:
            try:
                salary_5.append(i.text)    
            except:
                salary_5.append(i)
                
        rating_5 = []
        for i in rat_5:
            try:
                rating_5.append(i.text)
            except:
                rating_5.append(i)
                
        posted_5 = []
        for i in pos_5:
            try:
                posted_5.append(i.text)
            except:
                posted_5.append(i)

        print(bcolors.WARNING + "All_Details_Retrieved_Successfully_from_page-5")           
    
    except:
        print(bcolors.FAIL + "Failed_to_retrieve_Details_from_page-5")    
    
    print(bcolors.OKCYAN + "Getting_JobDescription_on_page-5_Wait_for_Few_More_Seconds")
    jd_5 =[]    
    for opening in jobs_list:
        try:
            opening.click()
            time.sleep(Secs/1.5)
            jd_5.append(driver.find_element_by_css_selector("div[class='jobDescriptionContent desc']").text)
        except:
            jd_5.append("NA")
            
    
    print(" ")
    print(bcolors.WARNING + "Scraping_Job_Done_for_all_5_Pages")
    
    print(" ")
    print(" ")
    print(bcolors.OKGREEN + "Arranging data in DataFrame")

    company_name = list(chain(company_name_1, company_name_2, company_name_3, company_name_4, company_name_5))
    designation = list(chain(designation_1, designation_2, designation_3, designation_4, designation_5))
    city = list(chain(city_1, city_2, city_3, city_4, city_5))
    salary = list(chain(salary_1, salary_2, salary_3, salary_4, salary_5))
    company_rating = list(chain(rating_1, rating_2, rating_3, rating_4, rating_5))
    job_post_age = list(chain(posted_1, posted_2, posted_3, posted_4, posted_5))
    job_description = list(chain(jd_1, jd_2, jd_3, jd_4, jd_5))

    Output_DF = pd.DataFrame(
    {'Company_Name': company_name,
     'Job Title': designation,
     'Location': city,
     'Salary': salary,
     'Company_Rating': company_rating,
     'Job_Post_Age': job_post_age,
     'Data_Collected_on': time.strftime("%d-%m-%Y %H:%M", localtime()),
     'Job_Description': job_description
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
