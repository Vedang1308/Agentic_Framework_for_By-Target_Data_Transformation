import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    # The format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Prepare for pivoting
    # The target columns are 'Hr 1' to 'Hr 24'.
    # Hour 0 corresponds to 'Hr 1', Hour 1 to 'Hr 2', etc.
    df['hr_label'] = df['hour'] + 1
    
    # 4. Pivot the data
    # We group by date_only and spread the values across hr_label columns.
    # Using mean() to aggregate if there are multiple readings per hour.
    # If there are NaNs, mean will ignore them if there is at least one valid number.
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hr_label', 
        values='zone_016', 
        aggfunc='mean'
    )
    
    # 5. Rename columns to match target schema exactly
    # Columns are currently integers 1-24. We need 'Hr 1', 'Hr 2', ...
    pivot_df.columns = [f'Hr {col}' for col in pivot_df.columns]
    
    # 6. Reset index to make date_only a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Format the date column
    # Target format is '%m/%d/%Y' with leading zeros (e.g., 01/02/2018)
    pivot_df['Date'] = pivot_df['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 8. Select and order columns
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # Ensure all expected columns exist. If a date doesn't have data for a specific hour, 
    # pivot_table creates NaN automatically. If a column is missing (e.g., no data for Hr 24 at all), 
    # we might need to reindex, but pivot_table usually keeps the column structure if defined.
    # However, pivot_table only creates columns for observed values. 
    # To be safe and ensure all Hr 1-24 columns exist even if empty:
    for col in target_columns:
        if col == 'Date':
            continue
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    return pivot_df[target_columns]