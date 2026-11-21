import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with 'date' and 'zone_016' into a target DataFrame
    with daily aggregated hourly load profiles.
    """
    df = source.copy()
    
    # 1. Parse date
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract components for grouping and output
    # dt_strata format: MM/DD/YY
    df['dt_strata'] = df['datetime'].dt.strftime('%m/%d/%y')
    
    # dow: Monday=1, ..., Sunday=7
    df['dow'] = df['datetime'].dt.dayofweek + 1
    
    # Extract hour for bucketing
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour to target column name
    # Mapping: Hour 0 -> pct_hourly_2400, Hour 1 -> pct_hourly_0100, ..., Hour 23 -> pct_hourly_2300
    def get_hour_col(h):
        if h == 0:
            return 'pct_hourly_2400'
        else:
            return f'pct_hourly_{h:02d}00'
            
    df['hour_col'] = df['hour'].apply(get_hour_col)
    
    # 4. Aggregate
    # Group by dt_strata and hour_col, summing the zone_016 values
    agg_df = df.groupby(['dt_strata', 'hour_col'])['zone_016'].sum().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='dt_strata', columns='hour_col', values='zone_016')
    
    # 6. Ensure all expected hourly columns exist and fill missing with 0
    expected_hour_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 24)] + ['pct_hourly_2400']
    
    # Reindex to ensure order and presence of all columns
    # Note: The order in the target is 0100, 0200, ..., 2300, 2400
    ordered_hour_cols = [f'pct_hourly_{i:02d}00' for i in range(1, 24)] + ['pct_hourly_2400']
    
    pivot_df = pivot_df.reindex(columns=ordered_hour_cols, fill_value=0)
    
    # 7. Reset index to make dt_strata a column
    result_df = pivot_df.reset_index()
    
    # 8. Merge with dow information
    # We need to get the dow for each dt_strata. Since dow is deterministic from date, 
    # we can extract it from the original df grouped by dt_strata.
    dow_df = df.groupby('dt_strata')['dow'].first().reset_index()
    result_df = result_df.merge(dow_df, on='dt_strata', how='left')
    
    # 9. Add pct_hourly_2500 column
    result_df['pct_hourly_2500'] = 0
    
    # 10. Define final column order
    target_columns = ['dt_strata', 'dow'] + ordered_hour_cols + ['pct_hourly_2500']
    
    # 11. Select and return
    return result_df[target_columns]