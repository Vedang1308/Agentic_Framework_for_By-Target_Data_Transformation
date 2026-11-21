import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing hourly load data into a wide-format
    DataFrame with hours as rows and months as columns, containing the mean load.
    """
    # 1. Select relevant columns: date and value1-value24
    value_cols = [f'value{i}' for i in range(1, 25)]
    df_subset = source[['date'] + value_cols].copy()
    
    # 2. Melt the dataframe to long format
    # id_vars=['date'], var_name='hour_str', value_name='load'
    df_long = df_subset.melt(id_vars=['date'], var_name='hour_str', value_name='load')
    
    # 3. Extract hour number from 'hour_str' (e.g., 'value1' -> 1)
    df_long['hour'] = df_long['hour_str'].str.replace('value', '').astype(int)
    
    # 4. Parse date and extract month
    df_long['date_dt'] = pd.to_datetime(df_long['date'], format='%m/%d/%Y')
    df_long['month'] = df_long['date_dt'].dt.month
    
    # 5. Group by hour and month, and calculate the mean load
    # We dropna to ensure we only average valid numeric entries
    df_agg = df_long.groupby(['hour', 'month'])['load'].mean().reset_index()
    
    # 6. Pivot the table: index=hour, columns=month, values=load
    df_pivot = df_agg.pivot(index='hour', columns='month', values='load')
    
    # 7. Rename month columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot.rename(columns=month_names, inplace=True)
    
    # 8. Ensure all month columns exist, even if empty (fill with NaN)
    for m in month_names.values():
        if m not in df_pivot.columns:
            df_pivot[m] = np.nan
            
    # 9. Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # 10. Ensure 'hour' is integer type
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 11. Define target columns in the exact order required
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 12. Select and return the final dataframe
    # Sort by hour to ensure deterministic output
    df_pivot = df_pivot.sort_values(by='hour').reset_index(drop=True)
    
    return df_pivot[target_columns]