import time
import requests
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


def web_scraper():

    data = []
    # Initialize Chrome webdriver 
    driver = webdriver.Chrome()  

    # Load the initial page
    url = 'https://www.washingtonpost.com/local/public-safety/'
    driver.get(url)

    # Wait for the "load more" button to appear and click it multiple times
    for headlines in range(50):  
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'inline-flex'))
            )
            load_more_button.click()
            time.sleep(1)  
            page_source = driver.page_source  

        except Exception as e:
            print(f"Error: {e}")
            break
    
    # if response.status_code == 200:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    headlines = soup.find_all('h3')
    dates = soup.find_all('span', class_='wpds-c-iKQyrV')
    for headline, date in zip(headlines, dates):
            headline_text = headline.text.strip()
            date_text = date.text.strip()
            data.append({'Date of Post': date_text, 'Headline': headline_text})
    # else:
    #     print(response.status_code)
    
    # Save data to a CSV file
    csv_file = 'CrimeNews_headlines.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Date of Post', 'Headline'])
        writer.writeheader()
        writer.writerows(data)

    print(f"Data has been saved to {csv_file}")
    print(data)
    
    # Close the webdriver
    driver.quit()


def sentiment_analysis():
    
    
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Read the CSV file containing the texts
    file_name = 'CrimeNews_headlines.csv'  
    df = pd.read_csv(file_name)

    # Perform sentiment analysis for each headline
    sentiment_scores = []
    for idx, row in df.iterrows():
        scores = sia.polarity_scores(row['Headline'])
        scores['Headline'] = row['Headline']
        scores['Date of Post'] = row['Date of Post']
        sentiment_scores.append(scores)

    # Add sentiment scores to the DataFrame
    sentiment_df = pd.DataFrame(sentiment_scores)

    # Display the DataFrame with sentiment scores
    print(sentiment_df)

    # save file to csv
    csv_file = 'sentiment_scores.csv'
    sentiment_df.to_csv(csv_file, index=False)

    print(f"Data has been saved to {csv_file}")


def sentiment_analysis_timeseries():


    file_name = 'sentiment_scores.csv'  
    data = pd.read_csv(file_name)


    df_all = pd.DataFrame(data)
    df = df_all.drop('Headline', axis=1)
    df['Date of Post'] = pd.to_datetime(df['Date of Post'])  
    # average_scores = df.groupby('Date of Post')['pos'].mean().reset_index()
    # average_scores = df.groupby('Date of Post')['neg'].mean().reset_index()
    # average_scores = df.groupby('Date of Post')['neu'].mean().reset_index()
    average_scores = df.groupby('Date of Post').mean().reset_index()


    plt.figure(figsize=(20, 6))

    # Plot compound scores against dates
    plt.plot(average_scores['Date of Post'], average_scores['compound'], marker='o', linestyle='-', label='compound Score', color='b')
    # plt.plot(average_scores['Date of Post'], average_scores['neg'], marker='o', linestyle='-', label='Negative Score', color='r')
    # plt.plot(average_scores['Date of Post'], average_scores['neu'], marker='o', linestyle='-', label='Neutral Score', color='y')

    plt.title('Average Sentiment Scores Over Time')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)  
    plt.tight_layout()

    plt.show()




web_scraper()
sentiment_analysis()
sentiment_analysis_timeseries()