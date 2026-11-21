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
    
    # 3. Map hour to target column name
    # Hypothesis: Hour 1 = 1am (01:00), ..., Hour 23 = 11pm (23:00), Hour 24 = 12am (00:00)
    def map_hour_to_col(h):
        if h == 0:
            return 'Hour 24'
        else:
            return f'Hour {h}'
            
    df['hour_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Aggregate
    # Group by date and hour column, take the mean of the value
    agg_df = df.groupby(['date_only', 'hour_col'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='date_only', columns='hour_col', values='zone_016_cooling_sp')
    
    # 6. Ensure all 24 hour columns exist
    target_hours = [f'Hour {i}' for i in range(1, 25)]
    for h in target_hours:
        if h not in pivot_df.columns:
            pivot_df[h] = np.nan
            
    # 7. Format date back to string MM/DD/YYYY
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%m/%d/%Y')
    pivot_df = pivot_df.reset_index().rename(columns={'index': 'date'})
    
    # 8. Select and order columns
    target_columns = ['date'] + target_hours
    result_df = pivot_df[target_columns]
    
    # 9. Ensure correct data types if necessary, though pandas usually handles float/int conversion automatically
    # The target schema specifies specific int64/float64 types. 
    # Usually, returning the DataFrame is sufficient, but let's ensure no strict type mismatches cause issues.
    # The problem statement says "Return a DataFrame with the same schema...". 
    # We will rely on pandas default behavior which usually results in float64 for aggregated data with NaNs.
    
    return result_df