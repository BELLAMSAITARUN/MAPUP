#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

def calculate_distance_matrix(df):

    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance').fillna(0)
    return distance_matrix


def unroll_distance_matrix(result_matrix):

    unrolled_df = result_matrix.unstack().reset_index(name='distance')
    return unrolled_df

def find_ids_within_ten_percentage_threshold(unrolled_df, reference_id, threshold=10):

    reference_avg_distance = unrolled_df.loc[unrolled_df['id_start'] == reference_id, 'distance'].mean()
    min_threshold = reference_avg_distance - (reference_avg_distance * threshold / 100)
    max_threshold = reference_avg_distance + (reference_avg_distance * threshold / 100)

    similar_ids_df = unrolled_df[(unrolled_df['distance'] >= min_threshold) & (unrolled_df['distance'] <= max_threshold)]
    return similar_ids_df

def calculate_toll_rate(unrolled_df):
   
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_rate'
        unrolled_df[column_name] = unrolled_df['distance'] * rate_coefficient

    return unrolled_df
import pandas as pd

def calculate_time_based_toll_rates(toll_rate_df):
    
    # Define time ranges and discount factors
    time_ranges = [
        {'start': '00:00:00', 'end': '10:00:00', 'weekday_factor': 0.8, 'weekend_factor': 0.7},
        {'start': '10:00:00', 'end': '18:00:00', 'weekday_factor': 1.2, 'weekend_factor': 0.7},
        {'start': '18:00:00', 'end': '23:59:59', 'weekday_factor': 0.8, 'weekend_factor': 0.7}
    ]

    # Initialize columns for discounted rates
    for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
        toll_rate_df[f'discounted_{vehicle_type}_rate'] = 0.0

    # Apply discount factors based on time ranges
    for time_range in time_ranges:
        start_time = pd.to_datetime(time_range['start']).time()
        end_time = pd.to_datetime(time_range['end']).time()

        # Weekday discount factor
        weekday_filter = (toll_rate_df['start_time'].dt.time >= start_time) & (toll_rate_df['end_time'].dt.time <= end_time) & (toll_rate_df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        toll_rate_df.loc[weekday_filter, 'time_factor'] = time_range['weekday_factor']

        # Weekend discount factor
        weekend_filter = (toll_rate_df['start_time'].dt.time >= start_time) & (toll_rate_df['end_time'].dt.time <= end_time) & (toll_rate_df['start_day'].isin(['Saturday', 'Sunday']))
        toll_rate_df.loc[weekend_filter, 'time_factor'] = time_range['weekend_factor']

        # Apply discount factors to each vehicle type
        for vehicle_type in ['moto', 'car', 'rv', 'bus', 'truck']:
            column_name = f'discounted_{vehicle_type}_rate'
            rate_column_name = f'{vehicle_type}_rate'
            toll_rate_df.loc[weekday_filter, column_name] = toll_rate_df.loc[weekday_filter, rate_column_name] * time_range['weekday_factor']
            toll_rate_df.loc[weekend_filter, column_name] = toll_rate_df.loc[weekend_filter, rate_column_name] * time_range['weekend_factor']

    return toll_rate_df





