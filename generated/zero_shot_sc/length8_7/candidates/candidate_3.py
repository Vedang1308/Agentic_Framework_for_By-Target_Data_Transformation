import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame (wide format with hourly columns) into a target DataFrame
    (long format pivoted by hour and month) with aggregated mean values.
    """
    # Define target column names
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 1. Identify the hourly columns (1 to 24)
    # The source has columns '1' through '24' as strings or ints in the header.
    # Based on schema, they are float64 columns with integer names.
    hour_cols = [str(i) for i in range(1, 25)]
    
    # 2. Melt the DataFrame to convert wide hourly columns into long format
    # We keep 'Date' and 'Class' as identifiers, but we mainly need 'Date' for month extraction.
    # We melt 'hour_cols' into 'hour' (variable) and 'value' (value).
    df_melted = source.melt(
        id_vars=['Date'], 
        value_vars=hour_cols, 
        var_name='hour', 
        value_name='value'
    )
    
    # 3. Clean up the 'hour' column
    # Convert to integer
    df_melted['hour'] = df_melted['hour'].astype(int)
    
    # 4. Parse the 'Date' column and extract the month
    # Format is %m/%d/%Y
    df_melted['date_parsed'] = pd.to_datetime(df_melted['Date'], format='%m/%d/%Y')
    df_melted['month_num'] = df_melted['date_parsed'].dt.month
    
    # 5. Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_melted['month_name'] = df_melted['month_num'].map(month_map)
    
    # 6. Aggregate
    # Group by 'hour' and 'month_name' and calculate the mean of 'value'
    # This handles the reduction from multiple days per month to a single value per month per hour.
    df_agg = df_melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 7. Pivot the data
    # We want 'hour' as the row index (or column), 'month_name' as columns, and 'value' as data.
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value')
    
    # 8. Clean up the pivot result
    # Reset index to make 'hour' a column again
    df_pivot = df_pivot.reset_index()
    
    # Rename the columns axis to remove the 'value' prefix if present, though pivot usually names it based on values col
    # Ensure column names are strings
    df_pivot.columns.name = None
    
    # 9. Ensure all target month columns exist, even if empty (they will be NaN)
    for col in target_columns[1:]: # Skip 'hour'
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # 10. Sort by hour to ensure deterministic order (standard practice)
    df_pivot = df_pivot.sort_values(by='hour').reset_index(drop=True)
    
    # 11. Select and reorder columns to match target schema exactly
    df_result = df_pivot[target_columns]
    
    # 12. Cast 'hour' to int64 as per target schema
    df_result['hour'] = df_result['hour'].astype('int64')
    
    return df_result