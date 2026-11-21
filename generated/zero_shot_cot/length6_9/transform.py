import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Date and Hour
    # Target Date format is %m/%d/%Y
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    # Target Hours are 1-24, pandas hour is 0-23. 
    # We map hour 0 -> 'Hr 1', hour 1 -> 'Hr 2', etc.
    df['Hour_Label'] = df['datetime'].dt.hour + 1
    
    # 3. Aggregate data
    # We group by Date and Hour_Label and take the mean of zone_016.
    # This handles multiple minute entries per hour.
    agg_df = df.groupby(['Date', 'Hour_Label'])['zone_016'].mean().reset_index()
    
    # 4. Pivot the data
    # Rows: Date, Columns: Hour_Label, Values: zone_016
    pivot_df = agg_df.pivot(index='Date', columns='Hour_Label', values='zone_016')
    
    # 5. Rename columns to match target schema 'Hr 1', 'Hr 2', ...
    # The columns are currently integers 1-24.
    pivot_df.columns = [f'Hr {int(col)}' for col in pivot_df.columns]
    
    # 6. Ensure all 24 hour columns exist, filling missing ones with NaN
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    pivot_df = pivot_df.reindex(columns=target_hour_cols)
    
    # 7. Reset index to make 'Date' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Sort by Date descending to match the sample order (01/02 before 01/01)
    # The sample shows 01/02/2018 then 01/01/2018.
    pivot_df = pivot_df.sort_values(by='Date', ascending=False).reset_index(drop=True)
    
    # 9. Define target columns
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # 10. Return the final dataframe
    return pivot_df[target_columns]