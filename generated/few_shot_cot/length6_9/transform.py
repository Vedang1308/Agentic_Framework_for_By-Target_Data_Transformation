import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour components
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Group by date and hour, and aggregate the zone_016 values
    # Using mean to aggregate minute-level data into hourly buckets.
    # If an hour has no data, it will be NaN.
    grouped = df.groupby(['date_only', 'hour'])['zone_016'].mean()
    
    # 4. Pivot the data to have hours as columns
    # The index will be date_only, columns will be hour (0-23)
    pivoted = grouped.unstack(level='hour')
    
    # 5. Rename columns from 0-23 to 'Hr 1'-'Hr 24'
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    new_columns = {h: f'Hr {h+1}' for h in range(24)}
    pivoted = pivoted.rename(columns=new_columns)
    
    # 6. Reset index to make date_only a column
    pivoted = pivoted.reset_index()
    
    # 7. Format the date column as '%m/%d/%Y'
    pivoted['Date'] = pd.to_datetime(pivoted['date_only']).dt.strftime('%m/%d/%Y')
    
    # 8. Drop the temporary date_only column if it exists (it was reset to index)
    # Actually, reset_index creates a column named 'date_only'. We want 'Date'.
    # We created 'Date' above. We can drop 'date_only'.
    pivoted = pivoted.drop(columns=['date_only'])
    
    # 9. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 10. Ensure all target columns exist (fill missing hours with NaN if necessary)
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = pd.NA
            
    # 11. Sort by Date descending to match the sample order (01/02/2018 before 01/01/2018)
    # Convert Date to datetime for sorting, then back to string if needed, 
    # but since we formatted it, we can sort by the string if format is consistent, 
    # or better, sort by the original date_only before formatting.
    # Let's re-add date_only for sorting, then drop it.
    pivoted['date_sort'] = pd.to_datetime(pivoted['Date'])
    pivoted = pivoted.sort_values('date_sort', ascending=False)
    pivoted = pivoted.drop(columns=['date_sort'])
    
    # 12. Return the dataframe with exact target columns
    return pivoted[target_columns]