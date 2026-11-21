import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source table into the target table by pivoting hourly data
    across months.
    """
    df = source.copy()
    
    # 1. Melt the dataframe to convert hour columns into rows
    # Identify hour columns (all columns except 'Segment' and 'Date')
    id_cols = ['Segment', 'Date']
    value_cols = [c for c in df.columns if c not in id_cols]
    
    melted = df.melt(id_vars=id_cols, value_vars=value_cols, 
                     var_name='hour_str', value_name='value')
    
    # 2. Parse Date to extract Month
    # Format: '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    melted['date_dt'] = pd.to_datetime(melted['Date'], format='%a %m/%d/%Y')
    melted['month_num'] = melted['date_dt'].dt.month
    
    # Map month numbers to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    melted['month_name'] = melted['month_num'].map(month_map)
    
    # 3. Extract Hour integer from hour_str
    # Columns are like '1:00', '24:00:00'
    melted['hour'] = melted['hour_str'].apply(lambda x: int(x.split(':')[0]))
    
    # 4. Aggregate
    # Group by hour and month, calculate mean of values
    # Using mean as it's standard for profile aggregation
    agg_df = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # 6. Clean up
    pivot_df = pivot_df.reset_index()
    
    # Ensure column order matches target
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Rename columns if necessary (pivot creates column names from month_name)
    # The columns in pivot_df should already be the month names
    # Ensure 'hour' is int64
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Select and return
    return pivot_df[target_columns]