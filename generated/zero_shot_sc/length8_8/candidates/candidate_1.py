import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to extract month information
    source = source.copy()
    source['date_parsed'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_num'] = source['date_parsed'].dt.month
    
    # Mapping for month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['month_num'].map(month_names)
    
    # 2. Identify Hour columns
    hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # 3. Melt the dataframe from wide to long format
    # We keep 'month_name' as an identifier. We don't strictly need 'date' for aggregation 
    # if we group by month, but it's good practice to keep identifiers if needed.
    df_long = source.melt(
        id_vars=['month_name'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 4. Extract hour integer from the string 'Hour 1' -> 1
    df_long['hour'] = df_long['hour_str'].str.extract(r'(\d+)', expand=False).astype(int)
    
    # 5. Group by hour and month_name, and calculate the mean
    # Using mean because the sample values suggest averaging (sum would be much larger)
    df_agg = df_long.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot the table so months are columns and hours are rows
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value').reset_index()
    
    # 7. Rename columns to match target verbatim
    # The pivot might have added a name to the columns axis, but reset_index handles index.
    # We need to ensure the column names are exactly the month names.
    # Sometimes pandas adds a tuple or name to the column axis after pivot.
    # Let's flatten the column names if necessary, though reset_index usually handles simple pivots.
    
    # Check if columns are a MultiIndex (unlikely with simple pivot + reset_index, but good to be safe)
    if isinstance(df_pivot.columns, pd.MultiIndex):
        df_pivot.columns = df_pivot.columns.get_level_values(1)
        
    # Ensure 'hour' is an integer type
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 8. Define the target columns in the correct order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 9. Select and order columns. Missing months will be NaN, which is expected.
    df_result = df_pivot[target_columns]
    
    # 10. Sort by hour to ensure deterministic output (1, 2, 3...)
    df_result = df_result.sort_values(by='hour').reset_index(drop=True)
    
    return df_result