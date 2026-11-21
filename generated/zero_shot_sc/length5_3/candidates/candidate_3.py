import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source time-series data into a daily profile format.
    Source has 10-minute intervals. Target has 24 hourly averages per day.
    """
    # 1. Parse the date column to datetime
    # The source format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date string for grouping and formatting, and hour for pivoting
    # We group by the calendar date
    df['date_only'] = df['parsed_date'].dt.date
    # Extract hour (0-23)
    df['hour'] = df['parsed_date'].dt.hour
    
    # 3. Group by date and hour, and calculate the mean of cerc_logger_1
    # This aggregates the 10-minute intervals into hourly averages
    daily_hourly = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the table
    # Index: date_only
    # Columns: hour (0-23)
    # Values: cerc_logger_1 (mean)
    pivoted = daily_hourly.pivot(index='date_only', columns='hour', values='cerc_logger_1')
    
    # 5. Ensure all 24 hours are present as columns (fill NaN if an hour is missing for a day)
    # The columns will be integers 0, 1, ..., 23
    expected_hours = list(range(24))
    for h in expected_hours:
        if h not in pivoted.columns:
            pivoted[h] = np.nan
            
    # Reorder columns to be 0-23
    pivoted = pivoted[expected_hours]
    
    # 6. Rename columns to value1, value2, ..., value24
    # Hour 0 -> value1, Hour 1 -> value2, ...
    new_col_names = [f'value{i+1}' for i in range(24)]
    pivoted.columns = new_col_names
    
    # 7. Reset index to make 'date_only' a column
    pivoted = pivoted.reset_index()
    
    # 8. Format the date column to '%m/%d/%Y'
    # Convert date object back to string with specific format
    pivoted['date'] = pivoted['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 9. Drop the temporary 'date_only' column
    pivoted = pivoted.drop(columns=['date_only'])
    
    # 10. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 11. Ensure column order and return
    # Sort by date? The sample output isn't strictly sorted, but usually, deterministic output is good.
    # The sample shows 05/08, 05/07, 03/10... which is mixed. 
    # I will not enforce a specific sort order as the prompt doesn't specify it, 
    # but typically groupby preserves some order. To be safe, I'll just return the dataframe.
    
    return pivoted[target_columns]