import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with daily hourly percentages into a target DataFrame
    with hourly averages for each month.
    """
    # 1. Parse the date column to extract month information
    # The format is inferred as '%m/%d/%Y' from the sample '7/2/2016'
    source['DT_STRATA'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # 2. Identify hourly columns
    # Columns are PCT_HOURLY_0100 to PCT_HOURLY_2400 (and 2500 which we ignore)
    hourly_cols = [col for col in source.columns if col.startswith('PCT_HOURLY_')]
    
    # Filter out 2500 if present, as target only has hours 1-24
    hourly_cols = [col for col in hourly_cols if not col.endswith('2500')]
    
    # 3. Melt the dataframe to long format
    # Keep DT_STRATA, melt the hourly columns
    df_long = source[['DT_STRATA'] + hourly_cols].melt(
        id_vars=['DT_STRATA'],
        value_vars=hourly_cols,
        var_name='hour_column',
        value_name='value'
    )
    
    # Drop rows with NaN values if any (though source seems dense)
    df_long = df_long.dropna(subset=['value'])
    
    # 4. Extract hour number from column name
    # e.g., 'PCT_HOURLY_0100' -> 1, 'PCT_HOURLY_2400' -> 24
    # The last 4 chars are the time, e.g., '0100'. Dividing by 100 gives the hour.
    df_long['hour'] = df_long['hour_column'].apply(lambda x: int(x.split('_')[-1]) // 100)
    
    # 5. Extract month number from DT_STRATA
    df_long['month'] = df_long['DT_STRATA'].dt.month
    
    # 6. Aggregate: Calculate mean value for each hour and month
    # Group by hour and month, then take the mean of the 'value' column
    grouped = df_long.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot the data
    # Index: hour, Columns: month, Values: mean value
    df_pivot = grouped.pivot(index='hour', columns='month', values='value')
    
    # 8. Rename month columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot.rename(columns=month_names, inplace=True)
    
    # 9. Reset index to make 'hour' a column
    df_pivot.reset_index(inplace=True)
    
    # 10. Ensure hour is integer type
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 11. Define target columns in the correct order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 12. Sort by hour to ensure correct order
    df_pivot = df_pivot.sort_values('hour')
    
    # 13. Select only the required columns to match target schema exactly
    # Fill NaNs if any month/hour combination is missing (though unlikely with full data)
    df_pivot = df_pivot[target_columns]
    
    return df_pivot