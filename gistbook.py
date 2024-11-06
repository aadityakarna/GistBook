import requests
import openai
import time


# Function to get Google search results using an API (e.g., Google's Programmable Search Engine)
def get_google_results(query, num_results, api_key, cx):
    search_results = []
    try:

        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "num": num_results,
            "key": api_key,
            "cx": cx
        }

        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('items', []):
                link = item.get('link')
                if link:
                    search_results.append(link)
                    if len(search_results) >= num_results:
                        break
            time.sleep(1)  # Delay to avoid rate-limiting
        else:
            print(f"Failed to retrieve search results: {response.status_code}")
        return search_results
    except Exception as e:
        print(f"Error occurred during Google search API call: {e}")
        return []



def get_gist_from_links(links, language):
    try:
        prompt = f"Summarize the information from the following links in {language} in about 100 words:\n"
        for link in links:
            prompt += f"{link}\n"

        # Set up your OpenAI API key
        openai.api_key = 'Your-Openai-API-key'

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error occurred during OpenAI request: {e}")
        return "Failed to retrieve gist."


# Main function
def main():
    try:
        keyword = input("Enter the keywords you want to get gist information about: ")
        language = input("Enter the preferred language: ")

        # Google API details (replace with your own API key and search engine ID)
        google_api_key = "Google-API-key"
        search_engine_id = "Search-Engine-id"


        links = get_google_results(keyword, 10, google_api_key, search_engine_id)

        if not links:
            print("No valid links found.")
            return

       
        gist = get_gist_from_links(links, language)

        print("\nGist of the information:\n")
        print(gist)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
