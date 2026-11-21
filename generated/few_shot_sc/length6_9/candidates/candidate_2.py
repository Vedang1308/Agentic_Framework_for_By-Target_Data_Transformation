import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour  # 0-23
    
    # 3. Aggregate by date and hour
    # We use mean to aggregate the minute-level data into hourly values
    # dropna=False in groupby is not directly applicable to the agg result, 
    # but mean handles NaNs naturally (ignoring them).
    agg_df = df.groupby(['date_only', 'hour'])['zone_016'].mean().reset_index()
    
    # 4. Pivot the data
    # Index: date_only, Columns: hour, Values: zone_016
    pivot_df = agg_df.pivot(index='date_only', columns='hour', values='zone_016')
    
    # 5. Rename columns from 0-23 to 'Hr 1'-'Hr 24'
    # Hour 0 -> Hr 1, Hour 1 -> Hr 2, ..., Hour 23 -> Hr 24
    pivot_df.columns = [f'Hr {h + 1}' for h in pivot_df.columns]
    
    # 6. Reset index to make date_only a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Format the date column as '%m/%d/%Y'
    pivot_df['Date'] = pd.to_datetime(pivot_df['date_only']).dt.strftime('%m/%d/%Y')
    
    # 8. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 9. Select and return
    # Ensure all Hr columns exist (fill missing hours with NaN if any date lacks certain hours)
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    return pivot_df[target_columns]