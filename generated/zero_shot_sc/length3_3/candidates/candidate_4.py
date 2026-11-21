import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a long format (minute-level) 
    to a wide format (daily hourly aggregates).
    """
    # 1. Parse the date column
    df = source.copy()
    df['parsed_date'] = pd.to_datetime(df['date'])
    
    # 2. Extract date part and hour part
    df['date_key'] = df['parsed_date'].dt.date
    df['hour'] = df['parsed_date'].dt.hour
    
    # 3. Map hour to target column names
    # Convention observed: Hour 0 (midnight) -> 'Hour 24', Hour 1 -> 'Hour 1', ..., Hour 23 -> 'Hour 23'
    def map_hour(h):
        if h == 0:
            return 'Hour 24'
        else:
            return f'Hour {h}'
    
    df['hour_label'] = df['hour'].apply(map_hour)
    
    # 4. Aggregate
    # Group by date and hour label, calculate mean of zone_016
    # Using mean is standard for time-series downsampling. 
    # If there are NaNs in the group, mean will ignore them if skipna=True (default).
    # If the entire group is NaN, result is NaN.
    agg_df = df.groupby(['date_key', 'hour_label'])['zone_016'].mean()
    
    # 5. Pivot/Unstack to wide format
    df_pivot = agg_df.unstack(fill_value=np.nan)
    
    # 6. Format the date index to string '%m/%d/%Y'
    df_pivot.index = df_pivot.index.strftime('%m/%d/%Y')
    
    # 7. Reset index to make date a column
    df_result = df_pivot.reset_index()
    df_result.rename(columns={'index': 'date'}, inplace=True)
    
    # 8. Define target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (some might be missing if no data for that hour)
    for col in target_columns[1:]:
        if col not in df_result.columns:
            df_result[col] = np.nan
            
    # 10. Select and order columns verbatim
    df_result = df_result[target_columns]
    
    return df_result