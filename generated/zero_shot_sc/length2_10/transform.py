import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components
    df['date_only'] = df['datetime'].dt.floor('D')
    df['hour'] = df['datetime'].dt.hour
    
    # Calculate dow: Sunday=0, Monday=1, ..., Saturday=6
    # pandas dayofweek: Monday=0, ..., Sunday=6
    # Formula: (dayofweek + 1) % 7
    df['dow'] = (df['datetime'].dt.dayofweek + 1) % 7
    
    # 3. Aggregate: Sum the cooling setpoint for each date and hour
    # This assumes the value 876 comes from 12 intervals * 73.0
    agg_df = df.groupby(['date_only', 'hour'])['zone_016_cooling_sp'].sum().reset_index()
    
    # 4. Pivot the data so each hour is a column
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016_cooling_sp')
    
    # 5. Handle missing hours (fill with 0)
    pivot_df = pivot_df.fillna(0)
    
    # 6. Rename columns to match target format
    # Hour 0 -> pct_hourly_0100
    # Hour 23 -> pct_hourly_2400
    new_cols = {}
    for h in range(24):
        new_cols[h] = f'pct_hourly_{h+1:04d}00'
    pivot_df.rename(columns=new_cols, inplace=True)
    
    # 7. Add the 25th column (pct_hourly_2500) which is always 0
    pivot_df['pct_hourly_2500'] = 0
    
    # 8. Reset index to bring date_only back as a column
    pivot_df = pivot_df.reset_index()
    
    # 9. Format date_only to dt_strata (MM/DD/YY)
    pivot_df['dt_strata'] = pivot_df['date_only'].dt.strftime('%m/%d/%y')
    
    # 10. Extract dow for each date. Since dow is constant for a date, we can map it or re-calculate.
    # We already calculated dow in step 2, but we grouped by date_only. 
    # Let's create a mapping from date_only to dow from the original df or re-calculate from date_only.
    # Re-calculating is safer and cleaner.
    # Create a temporary series to map date_only to dow
    dow_map = df.drop_duplicates('date_only')[['date_only', 'dow']].set_index('date_only')['dow']
    pivot_df['dow'] = pivot_df['date_only'].map(dow_map).astype(int)
    
    # 11. Define the exact target columns
    target_columns = [
        'dt_strata', 'dow', 
        'pct_hourly_0100', 'pct_hourly_0200', 'pct_hourly_0300', 'pct_hourly_0400', 
        'pct_hourly_0500', 'pct_hourly_0600', 'pct_hourly_0700', 'pct_hourly_0800', 
        'pct_hourly_0900', 'pct_hourly_1000', 'pct_hourly_1100', 'pct_hourly_1200', 
        'pct_hourly_1300', 'pct_hourly_1400', 'pct_hourly_1500', 'pct_hourly_1600', 
        'pct_hourly_1700', 'pct_hourly_1800', 'pct_hourly_1900', 'pct_hourly_2000', 
        'pct_hourly_2100', 'pct_hourly_2200', 'pct_hourly_2300', 'pct_hourly_2400', 
        'pct_hourly_2500'
    ]
    
    # Ensure all hourly columns exist and are integers
    for col in target_columns[2:]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
        pivot_df[col] = pivot_df[col].astype(int)
        
    pivot_df['dow'] = pivot_df['dow'].astype(int)
    
    # 12. Select and return the final dataframe
    return pivot_df[target_columns]