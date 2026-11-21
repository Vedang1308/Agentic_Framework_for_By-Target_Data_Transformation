import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with 'date' and 'zone_016' into a target DataFrame
    with daily aggregated hourly data.
    """
    df = source.copy()
    
    # 1. Parse date
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Create target date string format '%m/%d/%y'
    df['dt_strata'] = df['dt'].dt.strftime('%m/%d/%y')
    
    # 3. Create day of week (Monday=1, ..., Sunday=7)
    df['dow'] = df['dt'].dt.dayofweek + 1
    
    # 4. Extract hour and map to target column names
    # Mapping: Hour 0 -> pct_hourly_2400, Hour 1 -> pct_hourly_0100, ..., Hour 23 -> pct_hourly_2300
    df['hour'] = df['dt'].dt.hour
    
    def map_hour_to_col(h):
        if h == 0:
            return 'pct_hourly_2400'
        else:
            return f'pct_hourly_{h:02d}00'
            
    df['target_col'] = df['hour'].apply(map_hour_to_col)
    
    # 5. Aggregate: Sum zone_016 for each date and target column
    # We group by dt_strata and target_col, then sum zone_016
    agg_df = df.groupby(['dt_strata', 'target_col'])['zone_016'].sum().reset_index()
    
    # 6. Pivot to wide format
    pivot_df = agg_df.pivot(index='dt_strata', columns='target_col', values='zone_016').reset_index()
    
    # 7. Fill missing hours with 0
    # Identify all possible target columns
    all_hour_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 24)] + ['pct_hourly_2400']
    
    for col in all_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
        else:
            pivot_df[col] = pivot_df[col].fillna(0)
            
    # 8. Get dow for each date
    # Since dow is constant for a date, we can get it from the original df grouped by dt_strata
    dow_df = df.groupby('dt_strata')['dow'].first().reset_index()
    
    # 9. Merge dow back
    result_df = pivot_df.merge(dow_df, on='dt_strata', how='left')
    
    # 10. Add pct_hourly_2500 column with 0
    result_df['pct_hourly_2500'] = 0
    
    # 11. Define target columns in correct order
    target_columns = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 25)] + ['pct_hourly_2500']
    
    # 12. Select and return
    return result_df[target_columns]