import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing hourly percentage data for different strata
    into a target DataFrame with aggregated hourly profiles per date.
    """
    
    # Define the target column names for the hours
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Define the source column names for the hours
    source_hour_cols = [f'PCT_HOURLY_{str(i).zfill(4)}00' if i < 10 else f'PCT_HOURLY_{str(i).zfill(4)}00' for i in range(1, 25)]
    # Correction for zero-padding: 1 -> 0100, 10 -> 1000
    source_hour_cols = [f'PCT_HOURLY_{str(i).zfill(4)}00' for i in range(1, 25)]
    
    # Verify source columns exist
    # The source schema lists PCT_HOURLY_0100 to PCT_HOURLY_2400
    
    # 1. Group by date and aggregate the hourly columns
    # We use mean() as the aggregation function for percentage profiles.
    # If the strata represent disjoint parts of a whole, sum() might be used, 
    # but mean() is standard for "average profile" unless weights are provided.
    # Given the ambiguity and lack of weights, mean is the robust choice for TbT.
    
    # Create a copy to avoid modifying original
    df = source.copy()
    
    # Parse dates to ensure consistent handling, then group
    # We keep DT_STRATA as the group key
    grouped = df.groupby('DT_STRATA')[source_hour_cols].mean()
    
    # 2. Rename columns to match target schema
    # Create a mapping dictionary
    col_mapping = {src_col: tgt_col for src_col, tgt_col in zip(source_hour_cols, target_hour_cols)}
    grouped.rename(columns=col_mapping, inplace=True)
    
    # 3. Reset index to make DT_STRATA a column again
    df_result = grouped.reset_index()
    
    # 4. Rename DT_STRATA to Date
    df_result.rename(columns={'DT_STRATA': 'Date'}, inplace=True)
    
    # 5. Format the Date column to match target format '%m/%d/%Y'
    # Convert to datetime object first
    df_result['Date'] = pd.to_datetime(df_result['Date'], format='%m/%d/%Y')
    # Format as string with leading zeros
    df_result['Date'] = df_result['Date'].dt.strftime('%m/%d/%Y')
    
    # 6. Define the final target columns in the correct order
    target_columns = ['Date'] + target_hour_cols
    
    # 7. Select and return the required columns
    return df_result[target_columns]