from dotenv import load_dotenv
from os import getenv

load_dotenv(override=True)

# Correct the spelling of 'ACCESS'
LINKEDIN_ACCESS_TOKEN = getenv('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_ACCESS_TOKEN_EXP = getenv('LINKEDIN_ACCESS_TOKEN_EXP')
HEADLESS = getenv('HEADLESS')