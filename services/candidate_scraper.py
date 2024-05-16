import asyncio
import aiohttp
from services.scraping_utils import search_for_candidate_name, search_for_candidate_headline, search_for_section

async def scrape_linkedin_profile(linkedin_id, session):
    """Scraping LinkedIn profile data asynchronously"""
    try:
        print(f'Scraping data for id: {linkedin_id}')
        profile_url = f"https://www.linkedin.com/in/{linkedin_id}/"

        async with session.get(profile_url) as response:
            if response.status == 404:
                print(f"Profile for {linkedin_id} not found (404)")
                return {"error": f"Profile for {linkedin_id} not found."}

            page_source = await response.text()

            # Scrape name, experiences, education from the LinkedIn profile
            try:
                name = search_for_candidate_name(page_source)
                if not name:
                    print("scraping failed due to session token not setup or expired")
                    return {"error": "Your Linkedin session token is not set up correctly or has expired"}

                headline = search_for_candidate_headline(page_source)
                education = search_for_section(page_source, "Education")
                experience = search_for_section(page_source, "Experience")
            except Exception as e:
                print(f"Error scraping details for {linkedin_id} : {e}")
                return {"error": f"Error searching for details for {linkedin_id}"}

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

async def main():
    linkedin_ids = [...]  # List of LinkedIn IDs to scrape
    async with aiohttp.ClientSession() as session:
        tasks = []
        for linkedin_id in linkedin_ids:
            task = asyncio.create_task(scrape_linkedin_profile(linkedin_id, session))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        print(results)

asyncio.run(main())