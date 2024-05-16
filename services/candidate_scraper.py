from selenium import webdriver
from time import sleep
from services.scraping_utils import options, service, search_for_candidate_name, search_for_candidate_headline, search_for_section, add_session_cookie
from concurrent.futures import ThreadPoolExecutor
import json
from multiprocessing import Pool
import random
from fake_useragent import UserAgent
import time

def scrape_linkedin_profile(linkedin_ids):
    """Scraping LinkedIn profile data for multiple profiles"""
    try:
        with Pool(processes=len(linkedin_ids)) as pool:
            results = pool.map(scrape_profile_worker, linkedin_ids)
        
        return results
    except Exception as e:
        print(f"Error fetching details for profiles: {e}")
        return {"error": f"Error fetching profile details"}
    

def simulate_human_scroll(driver):
    # Get the current scroll position
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to a random position
        new_height = random.uniform(0.2 * last_height, 0.8 * last_height)
        driver.execute_script(f"window.scrollTo(0, {new_height});")

        # Wait for a random time between 0.5 and 2 seconds
        time.sleep(random.uniform(0.5, 2))

        # Check if the page has been scrolled to the bottom
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Simulate mouse movements
    actions = webdriver.ActionChains(driver)
    for _ in range(3):
        x = random.randint(100, driver.get_window_size()['width'] - 100)
        y = random.randint(100, driver.get_window_size()['height'] - 100)
        actions.move_by_offset(x, y)
        actions.perform()
        time.sleep(random.uniform(0.5, 2))

def random_delay():
    time.sleep(random.uniform(2, 10))

def scrape_profile_worker(linkedin_id):
    try:
        # Setup Selenium WebDriver
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f'user-agent={user_agent}')
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
            print(f"Profile for {linkedin_id} not found (404)")
            return {"error": f"Profile for {linkedin_id} not found."}

        random_delay()  # Add random delay

        # Scrape name, experiences, education from the LinkedIn profile
        try:
            name = search_for_candidate_name(driver)
            if not name:
                driver.quit()
                print("scraping failed due to session token not setup or expired")
                return {"error": "Your Linkedin session token is not set up correctly or has expired"}

            simulate_human_scroll(driver)  # Simulate human scrolling and mouse movements
            random_delay()  # Add random delay

            headline = search_for_candidate_headline(driver)
            education = search_for_section(driver, "Education")
            experience = search_for_section(driver, "Experience")
        except Exception as e:
            print(f"Error scraping details for {linkedin_id} : {e}")
            return {"error": f"Error searching for details for {linkedin_id}"}

        driver.quit()
        print(f"finished fetching details for profile {linkedin_id} successfully")
        return {
            "linkedin_id": linkedin_id,
            "name": name,
            "headline": headline,
            "education": education,
            "experience": experience,
        }
    except Exception as e:
        print(f"Error fetching details for {linkedin_id} : {e}")
        return {"error": f"Error fetching profile details for {linkedin_id}"}