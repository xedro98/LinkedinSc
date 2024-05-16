from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from settings import LINKEDIN_ACCESS_TOKEN, LINKEDIN_ACCESS_TOKEN_EXP, HEADLESS

# Setting up the options
options = Options()
if HEADLESS != "False":
    options.add_argument("--headless=new")
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors=yes')
options.add_argument("--log-level=3")

# Add a random user-agent string
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
]
options.add_argument(f"user-agent={random.choice(user_agent_list)}")

# Setting up service
service = Service(ChromeDriverManager().install(), log_output='nul')

def find_by_xpath_or_None(driver, *xpaths):
    """Returns the text inside an element by its XPath"""
    for xpath in xpaths:
        try:
            return driver.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            continue
    return None

def search_for_candidate_name(driver):
    """Search for profile's name in the page"""
    try:
        name = find_by_xpath_or_None(driver, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1','/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/span/a/h1')
        return name
    except Exception as e:
        print(f"Error finding name: {e}")
    return None

def search_for_candidate_headline(driver):
    """Search for profile's headline in the page"""
    try:
        headline = find_by_xpath_or_None(driver, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]','/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]')
        return headline
    except Exception as e:
        print(f"Error finding headline: {e}")
    return None

def search_for_section(driver, section_name, min_index=2, max_index=8):
    """Search for a section's content by section name in the page"""
    try:
        # Initialize variables
        sectionIndex = min_index
        found_elements = {
            'positions': [],
            'institutions': [],
            'dates': []
        }

        # Function to add found elements to the dictionary
        def add_elements(position, institution, date):
            if position: found_elements['positions'].append(position)
            if institution: found_elements['institutions'].append(institution)
            if date: found_elements['dates'].append(date)

        # Loop through sections until "section_title" section is found
        while sectionIndex <= max_index:
            # Check if the section title matches "section_name"
            section_title = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[2]/div/div/div/h2/span[1]')
            if section_title == section_name:
                # Experience
                elementIndex = 1
                if section_name == "Experience":
                    while True:
                        target_element_position = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/div/div/div/div/span[1]', f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[2]/ul/li[1]/div/div[2]/div/a/div/div/div/div/span[1]', f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[2]/ul/li[1]/div/div[2]/div/a/div/div/div/div/div/span[1]', f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div/div/span[1]/span[1]')
                        target_element_institution = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/span[1]/span[1]', f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/a/div/div/div/div/span[1]', f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/a/div/div/div/div/span[1]')
                        target_element_date = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/span[2]/span[1]')
                        if target_element_position is None: break
                        add_elements(target_element_position, target_element_institution, target_element_date)
                        elementIndex += 1
                elif section_name == "Education":
                    while True:
                        target_element_institution = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/span[1]/span[1]', f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/a/div/div/div/div/span[1]')
                        target_element_position = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/span[2]/span[1]', f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/a/div/div/div/div/span[2]')
                        target_element_date = find_by_xpath_or_None(driver, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{sectionIndex}]/div[3]/ul/li[{elementIndex}]/div/div[2]/div[1]/div/span[3]/span[1]')
                        if target_element_institution is None: break
                        add_elements(target_element_position, target_element_institution, target_element_date)
                        elementIndex += 1
                break
            sectionIndex += 1
        return found_elements
    except Exception as e:
        print(f"Error searching for section: {e}")
    return None

def search_for_profile_picture(driver):
    """Search for profile's picture in the page"""
    try:
        picture_url = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[1]/div[1]/button/img').get_attribute("src")
        return picture_url
    except NoSuchElementException:
        return None

def add_session_cookie(driver):
    driver.get('https://www.linkedin.com')
    driver.add_cookie({'name': 'li_at', 'value': LINKEDIN_ACCESS_TOKEN, 'domain': '.linkedin.com'})
