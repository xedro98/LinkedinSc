from selenium import webdriver
from time import sleep
from services.scraping_utils import (
    options, service, search_for_candidate_name, search_for_candidate_headline, 
    search_for_section, search_for_candidate_profile_picture, add_session_cookie
)
from pyvirtualdisplay import Display
from concurrent.futures import ThreadPoolExecutor
import json
from multiprocessing import Pool

def scrape_linkedin_profile(linkedin_ids):
    """Scraping LinkedIn profile data for multiple profiles"""
    try:
        with Pool(processes=len(linkedin_ids)) as pool:
            results = pool.map(scrape_profile_worker, linkedin_ids)
        
        return results
    except Exception as e:
        print(f"Error fetching details for profiles: {e}")
        return {"error": f"Error fetching profile details"}
    
def scrape_profile_worker(linkedin_id):
    try:
        display = Display(visible=0, size=(1920, 1080))
        display.start()

        # Setup Selenium WebDriver
        driver = webdriver.Chrome(service=service, options=options)

        # Load cookies from the file
        add_session_cookie(driver)

        print(f'Scraping data for id: {linkedin_id}')

        # LinkedIn URL for the profile
        profile_url = f"https://www.linkedin.com/in/{linkedin_id}/"

        # Navigate to the LinkedIn profile
        driver.get(profile_url)

        if "/404" in driver.current_url or "Page not found" in driver.page_source:
            driver.quit()
            display.stop()
            print(f"Profile for {linkedin_id} not found (404)")
            return {"error": f"Profile for {linkedin_id} not found."}

        sleep(1)

        # Scrape name, headline, education, experience, and profile picture URL from the LinkedIn profile
        try:
            name = search_for_candidate_name(driver)
            if not name:
                driver.quit()
                display.stop()
                print("scraping failed due to session token not setup or expired")
                return {"error": "Your Linkedin session token is not set up correctly or has expired"}
            headline = search_for_candidate_headline(driver)
            education = search_for_section(driver, "Education")
            experience = search_for_section(driver, "Experience")
            profile_picture_url = search_for_candidate_profile_picture(driver)
        except Exception as e:
            print(f"Error scraping details for {linkedin_id} : {e}")
            driver.quit()
            display.stop()
            return {"error": f"Error searching for details for {linkedin_id}"}

        driver.quit()
        display.stop()
        print(f"Finished fetching details for profile {linkedin_id} successfully")
        return {
            "linkedin_id": linkedin_id,
            "name": name,
            "headline": headline,
            "education": education,
            "experience": experience,
            "profile_picture_url": profile_picture_url,
        }
    except Exception as e:
        print(f"Error fetching details for {linkedin_id} : {e}")
        return {"error": f"Error fetching profile details for {linkedin_id}"}


