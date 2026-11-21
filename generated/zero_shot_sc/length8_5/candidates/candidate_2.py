import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a long format with hourly values as columns
    into a wide format with hours as rows and months as columns, aggregating by mean.
    """
    # 1. Parse the date column to extract month information
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_num'] = source['date_dt'].dt.month
    
    # 2. Define month names mapping
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['month_num'].map(month_names)
    
    # 3. Identify value columns (value1 to value24)
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # 4. Melt the DataFrame to convert wide hourly columns into long format
    # We keep date, month_num, and month_name as identifiers
    df_long = pd.melt(
        source,
        id_vars=['date_dt', 'month_num', 'month_name'],
        value_vars=value_cols,
        var_name='hour_col',
        value_name='load'
    )
    
    # 5. Extract the hour number from the column name (e.g., 'value1' -> 1)
    df_long['hour'] = df_long['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 6. Group by hour and month_name, and calculate the mean load
    # This aggregates all daily values for a specific hour in a specific month
    df_agg = df_long.groupby(['hour', 'month_name'])['load'].mean().reset_index()
    
    # 7. Pivot the data to get months as columns
    # Index: hour, Columns: month_name, Values: load
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='load')
    
    # 8. Reset index to make 'hour' a column again
    df_pivot = df_pivot.reset_index()
    
    # 9. Ensure column names are correct and ordered
    # The pivot columns will be the month names. We need to ensure they match the target exactly.
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Rename columns if necessary (though pivot should produce the correct names from month_name)
    # Ensure 'hour' is integer
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # Sort by hour to match typical output order (1-24)
    df_pivot = df_pivot.sort_values('hour').reset_index(drop=True)
    
    # 10. Select only the target columns, handling potential missing months (NaNs)
    # If a month is missing in the data, the pivot will not have that column, or it will be NaN.
    # We need to ensure all target month columns exist.
    for col in target_columns[1:]:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # Return the dataframe with the exact target column names
    return df_pivot[target_columns]