import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame (daily hourly data) into a target DataFrame 
    showing the mean value for each hour (1-24) aggregated by month.
    """
    # 1. Parse the Date column to extract the month
    # The format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    source['Date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month'] = source['Date'].dt.month
    
    # 2. Identify hourly columns
    # The columns are named '1:00', '2:00', ..., '24:00:00'
    # We can filter columns that start with a digit or contain ':00'
    # A safer approach is to list them or filter by pattern if they are consistent.
    # Given the schema, they are float64 columns excluding 'Segment', 'Date', and 'month'.
    hour_cols = [col for col in source.columns if col not in ['Segment', 'Date', 'month']]
    
    # 3. Melt the dataframe from wide to long format
    # id_vars keep 'month' (and potentially 'Segment' if we needed it, but we aggregate across all)
    # value_vars are the hour columns
    df_melted = pd.melt(
        source, 
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 4. Parse the hour string to an integer
    # '1:00' -> 1, '24:00:00' -> 24
    # We can extract the leading digits
    df_melted['hour'] = df_melted['hour_str'].str.extract(r'(\d+)').astype(int)
    
    # 5. Aggregate by hour and month
    # Calculate the mean value for each hour/month combination
    df_agg = df_melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot the table so months become columns and hours become the index
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 7. Rename month columns to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot = df_pivot.rename(columns=month_names)
    
    # 8. Reset index to make 'hour' a column
    df_final = df_pivot.reset_index()
    
    # 9. Ensure hour is integer type
    df_final['hour'] = df_final['hour'].astype(int)
    
    # 10. Sort by hour to ensure canonical order
    df_final = df_final.sort_values('hour').reset_index(drop=True)
    
    # 11. Define target columns verbatim
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 12. Select and return the final dataframe
    return df_final[target_columns]