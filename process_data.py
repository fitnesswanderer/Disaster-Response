import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    Loads data from messages and categories datasets, returns merged dataframe
    """
    messages = pd.read_csv('messages.csv', dtype = str) 
    categories = pd.read_csv('categories.csv', dtype = str)  
    df = pd.merge(messages, categories, on=["id"])
    return df
    pass


def clean_data(df):
     """
     Takes dataframe of categories, splits every string, and extracts a category
    out of each string in form of 1 and 0 matrix, returns cleaned dataset
    """
     # create a dataframe of the 36 individual category columns
 
     categories = df.categories.str.split(';', expand=True)
     # select the first row of the categories dataframe
     row = categories.iloc[0]
    # use this row to extract a list of new column names for categories using lambda function
     category_colnames = row.apply(lambda x : x[:-2])
    # rename the columns of `categories`
     categories.columns = category_colnames
    #Convert category values to just numbers 0 or 1.
    #Iterate through the category columns in df to keep only the last character of each string (the 1 or 0).
     for column in categories:
        # set each value to be the last character of the string
         categories[column] = categories[column].str[-1]
        # convert column from string to numeric
         categories[column] = categories[column].astype(int) 
    #Replace categories column in df with new category columns.
    #Drop the categories column from the df dataframe since it is no longer needed.
     df = df.drop(columns=['categories'])
    # concatenate the original dataframe with the new `categories` dataframe
     df = pd.concat([df,categories],axis = 1)
    # check number of duplicates
     df.duplicated(keep="first").sum()
    # drop duplicates
     df.drop_duplicates(keep="first",inplace=True)
    # check number of duplicates
     df.duplicated(keep="first").sum()

     pass


def save_data(df, database_filename):
    engine = create_engine('sqlite:///DisasterCategories.db')
    df.to_sql('DisasterCategories', engine, index=False)
    pass  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
