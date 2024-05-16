import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from services.scraping_utils import options, service, search_for_candidate_name, search_for_candidate_headline, search_for_section, add_session_cookie

# Add the constants for the LinkedIn access token and headless mode
LINKEDIN_ACCESS_TOKEN = "AQEDASR_V5cE4jaLAAABj3o87OAAAAGPnklw4E0Ah8qAU6n5YIY9SSWluVuPJ7q78KD_r_PmszI5s0UCMzqfnfpBvVGe6Ejz6KGCKokf11BsOkP7MHqxqOgL4EMiguE6XYNDvZkW4KxumfuK4ApcQ6MI"
HEADLESS = False

async def scrape_linkedin_profile(linkedin_id):
    """Scrape LinkedIn profile data asynchronously."""
    try:
        # Setup Selenium WebDriver
        chrome_options = Options()
        if HEADLESS:
            chrome_options.add_argument("--headless")
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Load cookies
        driver.get('https://www.linkedin.com')
        add_session_cookie(driver, LINKEDIN_ACCESS_TOKEN)
        driver.refresh()

        print(f'Scraping data for id: {linkedin_id}')

        # LinkedIn URL for the profile
        profile_url = f"https://www.linkedin.com/in/{linkedin_id}/"

        # Navigate to the LinkedIn profile
        driver.get(profile_url)

        if "/404" in driver.current_url or "Page not found" in driver.page_source:
            driver.quit()
            print(f"Profile for {linkedin_id} not found (404)")
            return {"error": f"Profile for {linkedin_id} not found."}

        await asyncio.sleep(1)

        # Scrape name, experiences, education from the LinkedIn profile
        try:
            name = search_for_candidate_name(driver)
            if not name:
                driver.quit()
                print("Scraping failed due to session token not setup or expired")
                return {"error": "Your LinkedIn session token is not set up correctly or has expired"}
            headline = search_for_candidate_headline(driver)
            education = search_for_section(driver, "Education")
            experience = search_for_section(driver, "Experience")
        except Exception as e:
            print(f"Error scraping details for {linkedin_id}: {e}")
            return {"error": f"Error searching for details for {linkedin_id}"}

        driver.quit()

        print(f"Finished fetching details for profile {linkedin_id} successfully")
        return {
            "linkedin_id": linkedin_id,
            "name": name,
            "headline": headline,
            "education": education,
            "experience": experience,
        }

    except Exception as e:
        print(f"Error fetching details for {linkedin_id}: {e}")
        return {"error": f"Error fetching profile details for {linkedin_id}"}
