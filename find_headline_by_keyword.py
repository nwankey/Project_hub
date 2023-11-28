# For lists contained in a csv file
import csv
import pandas as pd

# # define source of data
def find_headline_by_keyword():
    df = pd.read_csv('CrimeNews_headlines.csv')
    # print(df)
    headlines = df['Headline'].tolist()

    keyword = input("Enter Keyword:")

    found = False
    for headline in headlines:
        if keyword.lower() in headline.lower():
            print(f'found, {headline}')
            found = True

    if not found:
        print(f"No headlines found containing '{keyword}'")


find_headline_by_keyword()








# # inspect data and note column headings(if source is .csv)
#     print(data)

# # assign values
# headlines = data['column_name'].tolist()

# keyword = input("Enter Keyword:")

# # iterate over headlines
# found = False
# for headline in headlines:
#     if keyword.lower() in headline.lower():      #convert str to lower case
#         print(f'found, {headline}')
#         found = True
#         break

# if not found:
#     print(f"No headlines found containing '{keyword}'")



# Example usage:
    