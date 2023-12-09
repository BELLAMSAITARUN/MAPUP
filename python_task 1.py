#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
def generate_car_matrix(dataframe):
    # Pivot the dataframe to get a matrix-like structure
    car_matrix = dataframe.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0 and set diagonal values to 0
    car_matrix = car_matrix.fillna(0).astype(int)
    car_matrix.values[[range(car_matrix.shape[0])]*2] = 0

    return car_matrix

def get_type_count(df):

    # Create a new column 'car_type' based on the conditions
    df['car_type'] = pd.cut(df['car'], bins=[float('-inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Count occurrences of each car type and return as a dictionary
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

def get_bus_indexes(df):
  
    # Calculate the mean of the 'bus' column
    mean_bus = df['bus'].mean()

    # Find the indexes where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()

    return bus_indexes
def filter_routes(df):
  
    # Group by 'route' and calculate the average 'bus' value for each route
    route_avg_bus = df.groupby('route')['bus'].mean()

    # Filter routes where the average 'bus' value is greater than 7
    filtered_routes = route_avg_bus[route_avg_bus > 7].index.tolist()

    return filtered_routes

def multiply_matrix(matrix):
    
    # Create a copy of the input matrix to avoid modifying the original
    modified_matrix = matrix.copy()

    # Apply custom conditions to modify values
    modified_matrix[matrix > 20] *= 0.75
    modified_matrix[(matrix <= 20) & (matrix > 0)] *= 1.25

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix



def time_check(df):
    
    # Assuming the timestamp columns are named 'startDay', 'startTime', 'endDay', 'endTime'
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Group by unique (`id`, `id_2`) pairs and check if timestamps cover a full 24-hour and 7 days
    time_check_series = df.groupby(['id', 'id_2'])['start_datetime', 'end_datetime'].apply(
        lambda x: (x['end_datetime'].max() - x['start_datetime'].min()) == pd.Timedelta(days=7))

    return time_check_series






# In[ ]:




