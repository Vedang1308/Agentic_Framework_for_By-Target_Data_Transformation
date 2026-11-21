import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source wide-format daily time-series data into a monthly
    hourly average profile.
    """
    # 1. Parse the Date column to extract month information
    # Format: '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    source = source.copy()
    source['parsed_date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month'] = source['parsed_date'].dt.month_name().str.lower()
    
    # 2. Identify hour columns
    # Source columns are '1:00', '2:00', ..., '24:00:00'
    # We exclude 'Segment', 'Date', and the helper columns we just added
    hour_cols = [c for c in source.columns if c not in ['Segment', 'Date', 'parsed_date', 'month']]
    
    # 3. Melt the DataFrame from wide to long format
    # id_vars: columns to keep as identifiers
    # value_vars: columns to unpivot
    # var_name: name of the new column holding the original column names
    # value_name: name of the new column holding the values
    df_long = source.melt(
        id_vars=['month'],
        value_vars=hour_cols,
        var_name='hour_label',
        value_name='value'
    )
    
    # 4. Extract integer hour from the hour_label
    # Labels are like '1:00', '12:00', '24:00:00'
    # We split by ':' and take the first part, then convert to int
    df_long['hour'] = df_long['hour_label'].apply(lambda x: int(x.split(':')[0]))
    
    # 5. Aggregate: Calculate the mean value for each hour and month
    # Group by 'hour' and 'month', then mean the 'value'
    df_agg = df_long.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot the table so that months become columns
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value').reset_index()
    
    # 7. Ensure column names match exactly
    # The pivot creates multi-index or string columns for months.
    # We need to flatten and rename if necessary, but pivot usually creates string columns from the 'month' values.
    
    # 8. Define the exact target column order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 9. Fill any potential NaNs if a specific month/hour combo is missing (though unlikely with full data)
    # and ensure the 'hour' column is integer
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # 10. Reorder and select columns to match target schema verbatim
    # Check if all target columns exist in df_pivot. If some months are missing in data, they might be NaN or missing.
    # The problem implies a general transformation. We should ensure the structure is correct.
    
    # Sort by hour to match typical target presentation
    df_pivot = df_pivot.sort_values('hour')
    
    # Select only the target columns to ensure exact match and order
    # Note: If any month column is missing from the pivot (e.g. no data for December), 
    # we might need to add it as NaN or 0. However, standard pivot will only include present keys.
    # Given the "general" requirement, we assume data exists for all months or we just return what's there.
    # But to be safe and match schema verbatim, we can reindex columns.
    
    # Ensure all target month columns exist in the dataframe
    for col in target_columns[1:]: # Skip 'hour'
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    df_result = df_pivot[target_columns]
    
    return df_result