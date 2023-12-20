import os
import requests
import logging

# Requesting Data
BASE_URL =  f"http://www.omdbapi.com/"
API_KEY = os.environ['API_KEY']
GIT_API_KEY = os.environ['GIT_API_KEY']
ISSUE_NUMBER = os.getenv('ISSUE_NUMBER')
movie_title = os.getenv('MOVIE_TITLE')
owner = "JordanIKlein"
repo = "OMDB_API"

def retrieve_movie_data():
    url = BASE_URL + f"?t={movie_title}&apikey={API_KEY}&plot=full"
    headers = {'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers)
    #Response always returns 200 status code. Look for Response key in JSON.
    if response.status_code == 200:
        response_json = response.json()
        if response_json["Response"] == "True":
            logging.info("Successfully found movie...")
            #Extract Movie Information
            # Extract specific information
            title = response_json['Title']
            released = response_json['Released']
            director = response_json['Director']
            actors = response_json['Actors']
            runtime = response_json['Runtime']
            genre = response_json['Genre']
            plot = response_json['Plot']
            extracted_text = f"Title: {title}\nReleased: {released}\nDirector: {director}\nActors: {actors}\nRuntime: {runtime}\nGenre: {genre}\nPlot: {plot}\n"
            creating_issue_comment(extracted_text)
        else:
            logging.info("Movie not found. Returning issue comment with response...")
            creating_issue_comment("Movie not found, perhaps try a different spelling?")
    else: 
        print(response.status_code)    

def creating_issue_comment(text):
    # GitHub API endpoint for creating a comment on an issue
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{ISSUE_NUMBER}/comments"
    # Comment data
    comment_data = {
        "body": text
    }
    # Headers with authentication
    headers = {
        "Authorization": f"Bearer {GIT_API_KEY}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Make the API request to create a comment
    response = requests.post(url.format(owner=owner, repo=repo, issue_number=ISSUE_NUMBER), json=comment_data, headers=headers)

    # Check the response status
    if response.status_code == 201:
        print("Comment created successfully.")
        #Close issue
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def closing_an_issue():
    # GitHub API endpoint for issues
    github_api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{ISSUE_NUMBER}'

    # GitHub personal access token for authentication
    access_token = 'your_personal_access_token'

    # Headers for the request, including the authorization header with the token
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    # Payload to close the issue
    payload = {
        'state': 'closed'
    }
    # Make the PATCH request to close the issue
    response = requests.patch(
        github_api_url.format(owner=owner, repo=repo, issue_number=ISSUE_NUMBER),
        headers=headers,
        json=payload
    )
    # Check the response status
    if response.status_code == 200:
        logging.info(f"Issue {ISSUE_NUMBER} closed successfully")
    else:
        logging.info(f'Failed to close issue #{ISSUE_NUMBER}. Status code: {response.status_code}, Response: {response.json()}')

def main():
    retrieve_movie_data()

if __name__ == "__main__":
    main()
