import argparse
import os
from textwrap import indent
import requests
from datetime import datetime
from tqdm import tqdm
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
from news_summary_generator import NewsSummaryGenerator
from html_content_extractor import HTMLContentExtractor
import json

init(autoreset=True)

# Hacker News API endpoints
TOP_STORIES_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
ITEM_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

def get_top_stories():
    response = requests.get(TOP_STORIES_URL)
    response.raise_for_status()
    return response.json()

def get_item(item_id):
    response = requests.get(ITEM_URL.format(item_id))
    response.raise_for_status()
    return response.json()

def get_website(url):
    response = requests.get(url)
    response.raise_for_status()
    return HTMLContentExtractor.extract_main_content(response.text)

def get_highest_score_story(stories):
    highest_score = 0
    highest_score_story = None
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_item, story_id): story_id for story_id in stories}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing stories"):
            try:
                story = future.result()
                if story['score'] > highest_score:
                    highest_score = story['score']
                    highest_score_story = story
            except Exception as e:
                print(f"{Fore.RED}An error occurred while processing story {futures[future]}: {e}")
                
    return highest_score_story

def main(args):
    try:
        api_token = os.environ.get('HF_API_TOKEN')  # Retrieve API token from environment
        if args.id:
            highest_score_story = get_item(args.id)
        else:
            top_stories = get_top_stories()
            highest_score_story = get_highest_score_story(top_stories)

        if highest_score_story:
            print(f"{Fore.GREEN}Title: {Fore.CYAN}{highest_score_story['title']}")
            print(f"{Fore.GREEN}Score: {Fore.CYAN}{highest_score_story['score']}")
            print(f"{Fore.GREEN}Date: {Fore.CYAN}{datetime.fromtimestamp(highest_score_story['time']).date()}")
            print(f"{Fore.GREEN}URL: {Fore.CYAN}{highest_score_story.get('url', 'No URL')}")

            # Initialize the NewsSummaryGenerator
            generator = NewsSummaryGenerator(model_name="mistralai/Mistral-7B-Instruct-v0.2", 
                                             api_token=api_token)
            # Get the website content and generate the summary
            summary = generator.generate_summary(get_website(highest_score_story.get('url'))) if highest_score_story.get('url') else "No URL"
            
            print(f"{Fore.GREEN}LLM-Powered Summary: \n{Fore.CYAN}{json.dumps(summary, indent=4).encode('latin1').decode('unicode_escape').encode('utf-16', 'surrogatepass').decode('utf-16')}") 
            
            # with open('data.json', 'w') as f:
            #     json.dump(summary, f, indent=4)
        else:
            print("No stories found.")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--id', type=int, help='ID of the specific news item to fetch')
    
    args = parser.parse_args()
    main(args)
