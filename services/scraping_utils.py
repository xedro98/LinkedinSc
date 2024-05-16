from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
from pyvirtualdisplay import Display
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from webdriver_manager.chrome import ChromeDriverManager
from settings import LINKEDIN_ACCESS_TOKEN, LINKEDIN_ACCESS_TOKEN_EXP, HEADLESS

# Setting up the options
options = Options()
if HEADLESS.lower() != "false":
    options.add_argument("--headless=new")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors=yes')
options.add_argument("--log-level=3")
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')

# Setting up service
service = Service(ChromeDriverManager().install())

def find_by_xpath_or_None(driver, *xpaths):
    """Returns the text inside an element by its xPath."""
    for xpath in xpaths:
        try:
            return driver.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            continue
    return None

def search_for_candidate_name(driver):
    """Search for the profile's name on the page."""
    try:
        name = find_by_xpath_or_None(driver, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1',
                                      '/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1')
        return name
    except Exception as e:
        print(f"Error finding name: {e}")
    return None

def search_for_candidate_headline(driver):
    """Search for the profile's headline on the page."""
    try:
        headline = find_by_xpath_or_None(driver, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]',
                                             '/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]')
        return headline
    except Exception as e:
        print(f"Error finding headline: {e}")
    return None

def search_for_section(driver, section_name, min_index=2, max_index=8):
    """Search for a section's content by section name on the page."""
    try:
        sectionIndex = min_index
        found_elements = {'positions': [], 'institutions': [], 'dates': []}

        def add_elements(position, institution, date):
            if position: found_elements['positions'].append(position)
            if institution: found_elements['institutions'].append(institution)
            if date: found_elements['dates'].append(date)

        while sectionIndex <= max_index:
            section_title = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[2]/div/div/div/h2/span[1]')
            if section_title == section_name:
                elementIndex = 1
                if section_name == "Experience":
                    while True:
                        target_element_position = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/div/div/div/div/span[1]',
                                                                       f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[2]/ul/li[1]/div/div[2]/div/a/div/div/div/div/span[1]',
                                                                       f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[2]/ul/li[1]/div/div[2]/div/a/div/div/div/div/div/span[1]',
                                                                       f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/div/span[1]/span[1]')
                        target_element_institution = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/span[1]/span[1]',
                                                                           f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/a/div/div/div/div/span[1]',
                                                                           f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/a/div/div/div/div/span[1]')
                        target_element_date = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/span[2]/span[1]',
                                                                    f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/a/span[1]/span[1]',
                                                                    f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/div/span[2]/span[1]')
                        if not target_element_position:
                            break
                        add_elements(target_element_position, target_element_institution, target_element_date)
                        elementIndex += 1
                if section_name == "Education":
                    while True:
                        target_element_position = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/a/span[1]/span[1]',
                                                                       f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/a/span[1]/span[1]')
                        target_element_institution = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/a/div/div/div/div/span[1]',
                                                                           f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/a/div/div/div/div/span[1]')
                        target_element_date = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/a/span[2]/span[1]',
                                                                    f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/a/span[2]/span[1]')
                        if not target_element_position:
                            break
                        add_elements(target_element_position, target_element_institution, target_element_date)
                        elementIndex += 1
                break
            sectionIndex += 1
        return found_elements
    except Exception as e:
        print(f"Error finding section: {e}")
        return None

def search_for_candidate_profile_picture(driver):
    """Search for the profile's picture URL on the page."""
    try:
        wait = WebDriverWait(driver, 10)
        profile_picture_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.pv-top-card-profile-picture__image--show')))
        profile_picture_url = profile_picture_element.get_attribute('src')
        return profile_picture_url
    except Exception as e:
        print(f"Error finding profile picture: {e}")
    return None

def extract_linkedin_profile(linkedin_url):
    """Extract LinkedIn profile information."""
    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(linkedin_url)
        sleep(1)

        # Adding cookies
        driver.add_cookie({"name": "li_at", "value": LINKEDIN_ACCESS_TOKEN, "domain": ".www.linkedin.com", "expiry": int(LINKEDIN_ACCESS_TOKEN_EXP)})
        driver.add_cookie({"name": "liap", "value": LINKEDIN_ACCESS_TOKEN, "domain": ".www.linkedin.com", "expiry": int(LINKEDIN_ACCESS_TOKEN_EXP)})
        driver.get(linkedin_url)

        profile = {
            "Name": search_for_candidate_name(driver),
            "Headline": search_for_candidate_headline(driver),
            "Profile Picture": search_for_candidate_profile_picture(driver),
            "Experience": search_for_section(driver, "Experience", 2, 8),
            "Education": search_for_section(driver, "Education", 2, 8),
        }

        driver.quit()
        return profile
    except Exception as e:
        print(f"Error extracting LinkedIn profile: {e}")
        return None

def extract_linkedin_profiles_concurrently(linkedin_urls, concurrency=4):
    """Extract multiple LinkedIn profiles concurrently."""
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(extract_linkedin_profile, linkedin_urls))
    return results

# Example usage
if __name__ == "__main__":
    linkedin_urls = ["https://www.linkedin.com/in/some-profile/", "https://www.linkedin.com/in/another-profile/"]
    profiles = extract_linkedin_profiles_concurrently(linkedin_urls, concurrency=4)
    for profile in profiles:
        print(profile)
