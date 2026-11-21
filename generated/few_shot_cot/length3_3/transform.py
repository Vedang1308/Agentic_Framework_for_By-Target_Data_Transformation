import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date part for grouping and hour for bucketing
    df['date_part'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map source hour (0-23) to target hour label (1-24)
    # Convention inferred from sample: 
    # Source Hour 0 (00:xx) -> Target 'Hour 24'
    # Source Hour 1 (01:xx) -> Target 'Hour 1'
    # ...
    # Source Hour 23 (23:xx) -> Target 'Hour 23'
    def map_hour(h):
        if h == 0:
            return 24
        else:
            return h
            
    df['target_hour'] = df['hour'].apply(map_hour)
    
    # 4. Aggregate by date and target hour
    # Using mean as the aggregation function, consistent with typical load profile transformations
    # and the fact that sample values (67.9) remain similar (implying no multiplication by 60).
    agg_df = df.groupby(['date_part', 'target_hour'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: date_part, Columns: target_hour, Values: zone_016
    pivot_df = agg_df.pivot(index='date_part', columns='target_hour', values='zone_016')
    
    # 6. Rename columns to 'Hour 1', 'Hour 2', ..., 'Hour 24'
    pivot_df.columns = [f'Hour {int(col)}' for col in pivot_df.columns]
    
    # 7. Ensure all 24 hour columns exist, filling missing ones with NaN
    expected_hours = [f'Hour {i}' for i in range(1, 25)]
    for col in expected_hours:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 8. Format the date index to '%m/%d/%Y'
    pivot_df.index = pd.to_datetime(pivot_df.index).strftime('%m/%d/%Y')
    
    # 9. Reset index to make 'date' a column
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'index': 'date'})
    
    # 10. Select and order columns verbatim
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    return pivot_df[target_columns]