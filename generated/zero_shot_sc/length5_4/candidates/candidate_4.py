import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with columns ['date', 'zone_016'] 
    into a target DataFrame with daily hourly aggregates.
    """
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date (for grouping) and hour (for pivoting)
    df['day'] = df['parsed_date'].dt.date
    df['hour'] = df['parsed_date'].dt.hour
    
    # 3. Aggregate: Mean of zone_016 for each day and hour
    # Using mean to handle multiple minutes per hour
    agg_df = df.groupby(['day', 'hour'])['zone_016'].mean()
    
    # 4. Pivot/Unstack: Hours become columns
    # This creates a DataFrame with MultiIndex or single index 'day' and columns 0-23
    pivot_df = agg_df.unstack('hour')
    
    # 5. Rename columns to value1...value24
    # The columns are currently 0, 1, ..., 23. We want value1...value24.
    pivot_df.columns = [f'value{i+1}' for i in pivot_df.columns]
    
    # 6. Sort by date descending (as seen in target sample: 01/02 before 01/01)
    pivot_df = pivot_df.sort_index(ascending=False)
    
    # 7. Reset index to make 'day' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Format the date column to '%m/%d/%Y'
    # Convert back to string format
    pivot_df['date'] = pivot_df['day'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 9. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 10. Return the dataframe with exact target columns
    return pivot_df[target_columns]