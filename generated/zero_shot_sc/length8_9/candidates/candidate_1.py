import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source hourly rate data into a monthly aggregated table by hour.
    
    Steps:
    1. Parse the 'Date' column to extract month information.
    2. Melt the dataframe from wide (Hr 1-24 columns) to long format.
    3. Extract the hour number from the melted column names.
    4. Map month numbers to lowercase month names.
    5. Group by hour and month, summing the values.
    6. Pivot to get months as columns and hours as rows.
    7. Format and return the result.
    """
    
    # 1. Parse Date
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Identify hour columns
    hour_cols = [col for col in df.columns if col.startswith('Hr ')]
    
    # 3. Melt the dataframe
    # id_vars: columns to keep as identifiers
    # value_vars: columns to unpivot
    # var_name: name for the column that will hold the original column names ('Hr 1', etc.)
    # value_name: name for the column that will hold the values
    df_melted = df.melt(
        id_vars=['Company', 'Rate', 'Rate Code', 'Date'],
        value_vars=hour_cols,
        var_name='Hour_Col',
        value_name='Value'
    )
    
    # 4. Extract Hour Number
    # 'Hour_Col' contains strings like 'Hr 1', 'Hr 2', ... 'Hr 24'
    # We extract the integer part.
    df_melted['hour'] = df_melted['Hour_Col'].str.extract('(\d+)').astype(int)
    
    # 5. Extract Month and Map to Name
    df_melted['month_num'] = df_melted['Date'].dt.month
    
    # Mapping dictionary for month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_melted['month_name'] = df_melted['month_num'].map(month_map)
    
    # 6. Aggregate: Group by hour and month_name, sum the values
    # We drop NaNs if any, though unlikely in this clean dataset
    df_agg = df_melted.groupby(['hour', 'month_name'])['Value'].sum().reset_index()
    
    # 7. Pivot to wide format
    # index: hour, columns: month_name, values: Value
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='Value')
    
    # 8. Clean up the resulting dataframe
    df_pivot.reset_index(inplace=True)
    
    # Ensure hour is integer
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # Sort by hour to ensure 1-24 order
    df_pivot = df_pivot.sort_values('hour').reset_index(drop=True)
    
    # Ensure all month columns exist and are in the correct order
    target_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                     'july', 'august', 'september', 'october', 'november', 'december']
    
    # Fill any potential NaNs with 0 if a month/hour combination is missing (though unlikely)
    for month in target_months:
        if month not in df_pivot.columns:
            df_pivot[month] = 0.0
            
    # Select and order columns as required by target
    target_columns = ['hour'] + target_months
    
    # Ensure float type for month columns
    for col in target_months:
        df_pivot[col] = df_pivot[col].astype(float)
        
    return df_pivot[target_columns]