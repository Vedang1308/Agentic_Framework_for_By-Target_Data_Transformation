import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse date
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract dt_strata (MM/DD/YY)
    df['dt_strata'] = df['date'].dt.strftime('%m/%d/%y')
    
    # 3. Extract dow (1=Monday, ..., 7=Sunday)
    # pandas dayofweek: Monday=0, Sunday=6
    df['dow'] = df['date'].dt.dayofweek + 1
    
    # 4. Extract hour and map to target column names
    # Hour 0 -> pct_hourly_0100
    # Hour 23 -> pct_hourly_2400
    df['hour'] = df['date'].dt.hour
    df['hour_col'] = 'pct_hourly_' + df['hour'].apply(lambda h: f"{h+1:02d}00")
    
    # 5. Aggregate by dt_strata, dow, and hour_col
    # The values in target are sums of the source values (approx 6 values per hour * 24.5 ~ 147)
    agg_df = df.groupby(['dt_strata', 'dow', 'hour_col'])['cerc_logger_1'].sum().reset_index()
    
    # 6. Pivot to wide format
    pivot_df = agg_df.pivot_table(
        index=['dt_strata', 'dow'], 
        columns='hour_col', 
        values='cerc_logger_1', 
        fill_value=0
    ).reset_index()
    
    # 7. Define all target columns
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
    
    # 8. Ensure all columns exist (especially pct_hourly_2500 which has no source data)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 9. Select and order columns
    result = pivot_df[target_columns]
    
    # 10. Cast types
    result['dow'] = result['dow'].astype('int64')
    # The target schema says pct_hourly_2500 is int64, others float64.
    # However, pandas usually handles floats. Let's cast 2500 to int if possible, 
    # but since it's 0, it's fine.
    # To be safe with mixed types in a single df, we can leave as float except for specific ones if needed.
    # The prompt asks for exact schema.
    result['pct_hourly_2500'] = result['pct_hourly_2500'].astype('int64')
    
    return result