import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Aggregate data
    # Group by date and hour, take the mean of zone_016 to handle multiple rows per hour
    # and ignore NaNs.
    aggregated = df.groupby(['date_only', 'hour'])['zone_016'].mean().reset_index()
    
    # 4. Pivot the data
    # Index: date_only, Columns: hour, Values: zone_016
    pivoted = aggregated.pivot(index='date_only', columns='hour', values='zone_016')
    
    # 5. Rename columns from 0-23 to 'Hr 1'-'Hr 24'
    # The pivot columns are integers 0, 1, ..., 23
    pivoted.columns = [f'Hr {i+1}' for i in pivoted.columns]
    
    # 6. Reset index to make date_only a column
    pivoted = pivoted.reset_index()
    
    # 7. Format the date column
    # Convert date_only (which is now a column) to datetime again to format, 
    # or just format the date object directly.
    # Since it's a date object, we can use apply or strftime if we convert back to datetime.
    pivoted['Date'] = pd.to_datetime(pivoted['date_only']).dt.strftime('%m/%d/%Y')
    
    # 8. Drop the intermediate date_only column if it exists (it was the index, now reset)
    # Actually, reset_index creates 'date_only'. We want 'Date'.
    pivoted = pivoted.drop(columns=['date_only'])
    
    # 9. Sort by Date descending as per sample output
    pivoted = pivoted.sort_values(by='Date', ascending=False).reset_index(drop=True)
    
    # 10. Define target columns
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # Ensure all Hr columns exist, filling missing ones with NaN if necessary
    for col in target_columns[1:]:
        if col not in pivoted.columns:
            pivoted[col] = np.nan
            
    # Return with exact column order
    return pivoted[target_columns]