import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a wide daily hourly format to a pivoted 
    monthly hourly average format.
    """
    # Define target columns for final verification
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 1. Parse the Date column to extract the month
    # The format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    source['Date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month_num'] = source['Date'].dt.month
    
    # 2. Melt the DataFrame to long format
    # Identify hour columns. They are all columns except 'Segment' and 'Date' and 'month_num'
    id_vars = ['month_num']
    # Get all numeric/hour columns
    hour_cols = [col for col in source.columns if col not in id_vars and col != 'Segment']
    
    df_long = source.melt(id_vars=id_vars, value_vars=hour_cols, 
                          var_name='hour_str', value_name='value')
    
    # 3. Extract integer hour from the hour string
    # Columns are like '1:00', '2:00', ..., '24:00:00'
    # We can split by ':' and take the first part, then convert to int
    df_long['hour'] = df_long['hour_str'].apply(lambda x: int(str(x).split(':')[0]))
    
    # 4. Map month numbers to month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_long['month_name'] = df_long['month_num'].map(month_map)
    
    # 5. Aggregate by hour and month_name
    # The target values appear to be averages of the daily values for that hour in that month.
    df_agg = df_long.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot the table
    # Index: hour, Columns: month_name, Values: value
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value')
    
    # 7. Clean up the pivot table
    # Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # Sort by hour to ensure correct order (1, 2, ..., 24)
    df_pivot = df_pivot.sort_values('hour')
    
    # Ensure column order matches target exactly
    # The pivot columns might be sorted alphabetically or by insertion order, we need specific order
    # Rename columns if necessary (pivot usually keeps the column names from the 'columns' level)
    
    # Fill NaNs if any (though unlikely with full data)
    df_pivot = df_pivot.fillna(0)
    
    # Select and order columns as required
    # Note: df_pivot.columns might include 'hour' and then the month names.
    # We explicitly construct the final dataframe to ensure column order and names.
    
    final_df = pd.DataFrame()
    final_df['hour'] = df_pivot['hour']
    
    for month in ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']:
        if month in df_pivot.columns:
            final_df[month] = df_pivot[month]
        else:
            final_df[month] = np.nan # Should not happen
            
    # Ensure float type for month columns
    for month in ['january', 'february', 'march', 'april', 'may', 'june', 
                  'july', 'august', 'september', 'october', 'november', 'december']:
        final_df[month] = final_df[month].astype(float)
        
    # Ensure hour is int
    final_df['hour'] = final_df['hour'].astype(int)
    
    return final_df[target_columns]