import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing hourly load data into a target DataFrame
    with aggregated monthly averages per hour.
    """
    df = source.copy()
    
    # 1. Parse the date column to extract month
    df['date_dt'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['month'] = df['date_dt'].dt.month
    
    # 2. Identify value columns (value1 to value24)
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # 3. Melt the dataframe to convert wide format to long format
    # This creates columns: 'variable' (e.g., 'value1'), 'value' (the load)
    df_melted = df.melt(
        id_vars=['month'], 
        value_vars=value_cols, 
        var_name='hour_col', 
        value_name='load_value'
    )
    
    # 4. Extract the hour number from the 'hour_col' name (e.g., 'value1' -> 1)
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 5. Aggregate by hour and month
    # We calculate the mean load for each hour in each month
    grouped = df_melted.groupby(['hour', 'month'])['load_value'].mean().reset_index()
    
    # 6. Pivot the data so months are columns and hours are rows
    # This creates a DataFrame with 'hour' as index and months as columns
    df_pivot = grouped.pivot(index='hour', columns='month', values='load_value')
    
    # 7. Clean up the pivot result
    df_pivot = df_pivot.reset_index()
    
    # 8. Map month numbers to lowercase month names as required by target schema
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # Rename columns based on the map
    df_pivot.rename(columns=month_map, inplace=True)
    
    # 9. Ensure the 'hour' column is integer type
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 10. Define the target column order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 11. Sort by hour to ensure deterministic output order
    df_pivot = df_pivot.sort_values(by='hour').reset_index(drop=True)
    
    # 12. Return the DataFrame with the exact target columns
    return df_pivot[target_columns]