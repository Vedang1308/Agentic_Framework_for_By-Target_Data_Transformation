import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    source = source.copy()
    source['date_parsed'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    # The target 'Date' is just the date part
    source['date_only'] = source['date_parsed'].dt.date
    # The target hours are 1-24, corresponding to 0-23 in 24h clock
    source['hour'] = source['date_parsed'].dt.hour
    
    # 3. Aggregate data
    # Group by date and hour, taking the mean of the sensor values
    # This handles multiple readings per hour
    agg_df = source.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the table
    # Rows: date_only, Columns: hour, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='cerc_logger_1')
    
    # 5. Rename columns to match target schema ('Hr 1' to 'Hr 24')
    # Map hour 0 -> 'Hr 1', hour 1 -> 'Hr 2', ..., hour 23 -> 'Hr 24'
    pivot_df.columns = [f'Hr {h + 1}' for h in pivot_df.columns]
    
    # 6. Ensure all 24 hour columns exist, filling missing with NaN
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    for col in target_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 7. Reset index to make 'date_only' a column again
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'Date'})
    
    # 8. Format the Date column to '%m/%d/%Y'
    # Since 'Date' is currently a datetime.date object or similar, we format it
    pivot_df['Date'] = pivot_df['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 9. Select and order columns exactly as required
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # Sort by Date to match typical output expectations (optional but good practice)
    # Convert to datetime for sorting, then back to string if needed, 
    # but since we formatted as strings, we can sort by the original parsed date if we kept it.
    # However, the target sample is not strictly sorted chronologically in the snippet provided (05/08, 05/07, 03/10...).
    # Usually, deterministic order is preferred. Let's sort by Date descending or ascending?
    # The sample shows 05/08 then 05/07. This looks like Descending order.
    # Let's sort by Date descending.
    
    # To sort correctly, we need to parse the date string back to datetime for sorting, 
    # or use the original parsed date if we had kept it. 
    # Let's re-parse for sorting.
    pivot_df['Date_parsed'] = pd.to_datetime(pivot_df['Date'], format='%m/%d/%Y')
    pivot_df = pivot_df.sort_values(by='Date_parsed', ascending=False).drop(columns=['Date_parsed'])
    
    # Final selection
    df = pivot_df[target_columns]
    
    return df[target_columns]