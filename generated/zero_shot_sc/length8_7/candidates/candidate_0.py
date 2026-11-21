import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse Date and extract month
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['month_num'] = df['Date'].dt.month
    
    # 2. Define month name mapping
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['month_num'].map(month_map)
    
    # 3. Identify hour columns (1-24)
    hour_cols = [str(i) for i in range(1, 25)]
    
    # 4. Melt the dataframe to long format
    # We keep 'month_name' and melt the hour columns
    df_long = df.melt(
        id_vars=['month_name'],
        value_vars=hour_cols,
        var_name='hour',
        value_name='value'
    )
    
    # 5. Convert hour to integer
    df_long['hour'] = df_long['hour'].astype(int)
    
    # 6. Aggregate: Calculate mean value for each hour and month
    # Group by hour and month_name, then mean the values
    aggregated = df_long.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 7. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    df_pivot = aggregated.pivot(index='hour', columns='month_name', values='value')
    
    # 8. Reset index to make hour a column
    df_pivot = df_pivot.reset_index()
    
    # 9. Ensure column order and names match target
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Sort by hour to match typical output expectations (though not strictly required if index is unique)
    df_pivot = df_pivot.sort_values('hour').reset_index(drop=True)
    
    # 10. Select and return only the target columns
    # Note: If any month is missing in the data, it will be NaN, which is expected behavior.
    return df_pivot[target_columns]