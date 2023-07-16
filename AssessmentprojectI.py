import requests
from bs4 import BeautifulSoup

def get_filmography(actor_name):
    # Prepare the URL
    base_url = 'https://github.com'
    search_url = base_url + '/search?q=' + actor_name.replace(' ', '+') + '+filmography&type=Repositories'

    # Send a GET request to the search URL
    response = requests.get(search_url)
    response.raise_for_status()

    # Parse the HTML content of the search results page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the link to the actor's filmography repository
    repo_link = soup.select_one('ul.repo-list .v-align-middle')
    if not repo_link:
        return "No filmography found for the actor."

    # Retrieve the filmography repository page
    repo_url = base_url + repo_link['href']
    response = requests.get(repo_url)
    response.raise_for_status()

    # Parse the HTML content of the filmography repository page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the filmography content in the repository
    filmography_content = soup.select_one('.file-box .js-navigation-container')

    # Extract the film titles from the content
    film_titles = [title.text.strip() for title in filmography_content.select('.js-navigation-open')]

    return film_titles

# Test the function
actor_name = input("Enter the name of an actor: ")
filmography = get_filmography(actor_name)

if isinstance(filmography, str):
    print(filmography)
else:
    print(f"Filmography of {actor_name} (in descending order):")
    for film_title in filmography:
        print(film_title)

