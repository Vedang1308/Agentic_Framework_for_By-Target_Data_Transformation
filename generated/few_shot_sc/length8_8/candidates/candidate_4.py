import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse the date column to extract the month
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    
    # Identify hourly columns
    hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # Melt the dataframe to long format
    # id_vars keeps 'month', value_vars are the hourly columns
    melted = df.melt(id_vars=['month'], value_vars=hour_cols, var_name='hour_label', value_name='value')
    
    # Extract the hour number from the column name (e.g., 'Hour 1' -> 1)
    melted['hour'] = melted['hour_label'].str.extract(r'(\d+)').astype(int)
    
    # Group by month and hour, and calculate the mean of the values
    # Using mean because the target values match the constant input values, 
    # implying an average profile rather than a sum.
    grouped = melted.groupby(['month', 'hour'])['value'].mean().reset_index()
    
    # Pivot the table so that months become columns and hours become the index
    pivot_df = grouped.pivot(index='hour', columns='month', values='value')
    
    # Rename month integers to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df = pivot_df.rename(columns=month_names)
    
    # Reset index to bring 'hour' back as a column
    pivot_df = pivot_df.reset_index()
    
    # Sort by hour to ensure the order 1, 2, ..., 24
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # Define the exact target column order
    target_columns = ['hour'] + [month_names[i] for i in range(1, 13)]
    
    return pivot_df[target_columns]