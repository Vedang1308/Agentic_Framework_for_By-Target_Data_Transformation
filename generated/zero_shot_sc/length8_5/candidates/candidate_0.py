import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing daily hourly load data
    into a monthly hourly profile DataFrame.
    
    Steps:
    1. Parse the 'date' column.
    2. Melt the value columns (value1-value24) into a long format.
    3. Extract the hour index from the melted column names.
    4. Extract the month from the date.
    5. Group by hour and month, calculating the mean load.
    6. Pivot the data so hours are rows and months are columns.
    7. Format column names and return.
    """
    # 1. Parse dates
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Identify value columns
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # 3. Melt the dataframe to long format
    # Keep 'date' as identifier, melt value columns
    df_long = df.melt(
        id_vars=['date'], 
        value_vars=value_cols, 
        var_name='hour_col', 
        value_name='load'
    )
    
    # 4. Extract hour number from column name (e.g., 'value1' -> 1)
    df_long['hour'] = df_long['hour_col'].str.replace('value', '').astype(int)
    
    # 5. Extract month number from date
    df_long['month_num'] = df_long['date'].dt.month
    
    # 6. Group by hour and month, and calculate the mean load
    # This aggregates all days in a specific month for a specific hour
    aggregated = df_long.groupby(['hour', 'month_num'])['load'].mean().reset_index()
    
    # 7. Pivot the table: Index = hour, Columns = month_num, Values = load
    target_df = aggregated.pivot(index='hour', columns='month_num', values='load')
    
    # 8. Define month name mapping
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # 9. Rename columns to lowercase month names
    target_df.rename(columns=month_names, inplace=True)
    
    # 10. Ensure all expected month columns exist, even if empty (fill with NaN)
    expected_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                       'july', 'august', 'september', 'october', 'november', 'december']
    
    # Reindex columns to ensure correct order and presence
    target_df = target_df.reindex(columns=expected_months)
    
    # 11. Sort by hour index (1-24)
    target_df = target_df.sort_index()
    
    # 12. Reset index to make 'hour' a column
    target_df = target_df.reset_index()
    
    # 13. Ensure 'hour' is integer type
    target_df['hour'] = target_df['hour'].astype(int)
    
    # 14. Define final target columns
    target_columns = ['hour'] + expected_months
    
    return target_df[target_columns]