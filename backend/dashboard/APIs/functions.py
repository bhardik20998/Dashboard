from .constants import db
import pandas as pd
import re

def SaveDataframe(df, collection_name):


    try:

        collection = db[collection_name]

        # Convert DataFrame to a list of dictionaries
        data_list = df.to_dict(orient='records')

        # Insert data into MongoDB collection
        collection.insert_many(data_list)

        return True
    except:
        return False
    
def FetchDataframe(collection_name):
    # Replace with your MongoDB collection name
    collection = db[collection_name]  

    # Fetch data from the collection
    return pd.DataFrame(list(collection.find()))

def delete_all_entries(collection_name):
    # Replace with your MongoDB collection name
    collection = db[collection_name]  

    # Delete all documents in the collection
    result = collection.delete_many({})

    # Return the number of documents deleted
    return result.deleted_count


    
def UpdateDataFrame(collection_name,df):
    collection = db[collection_name]
    result = collection.delete_many({})
    try:

        collection = db[collection_name]

        # Convert DataFrame to a list of dictionaries
        data_list = df.to_dict(orient='records')

        # Insert data into MongoDB collection
        collection.insert_many(data_list)

        return True
    except:
        return False
    
def SortColumn(df, column):
    
    
    return sortArrayParan(df,column)
def SortArray(array):
    sorted_numeric_values = sorted( int(re.search(r'\d+', bucket).group()) if re.search(r'\d+', bucket) else None for bucket in array)

    # Remove None values (where re.search returned None) before sorting
    sorted_numeric_values = [value for value in sorted_numeric_values if value is not None]

    # Sort numeric values in ascending order and create sorted score buckets
    sorted_score_buckets = [
        f'<={value}' if '<=' in str(bucket) else
        f'>{value}' if '>' in str(bucket) else
        f'[{value}]' for value, bucket in zip(sorted_numeric_values, array)
    ]
    
    return sorted_score_buckets




def sortArrayParan(df, name):

    

    
    df[name] =  pd.Series(inner(df[name].tolist()))
    return df

def inner(array):

        for i, element in enumerate(array):
            if '<' in element:
                element_with_less_than = array.pop(i)
                break

        for i, element in enumerate(array):
            if '>' in element:
                element_with_greater_than = array.pop(i)
                break
        array.pop(len(array)-1)
        # SortArray(array)
    
            # Initialize an empty list to store the result
        result = []

        # Iterate over corresponding elements in arrays and sum them
        result=([element_with_less_than]+ array+ [element_with_greater_than]+["Total"])
            
        return result
