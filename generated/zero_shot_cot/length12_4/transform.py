import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Map Time Period to Season
    season_map = {
        'January': 'Winter', 'February': 'Winter', 'March': 'Spring',
        'April': 'Spring', 'May': 'Spring', 'June': 'Summer',
        'July': 'Summer', 'August': 'Summer', 'September': 'Fall',
        'October': 'Fall', 'November': 'Fall', 'December': 'Winter'
    }
    
    # Create a copy to avoid modifying original
    df = source.copy()
    
    # Map season
    df['season'] = df['Time Period'].map(season_map)
    
    # 2. Calculate Total Demand
    # The target values are large, suggesting aggregation of (Avg Demand * Num Homes)
    # Handle NaNs in Average Demand
    df['Average Demand Per Home With This End Use [kW]'] = df['Average Demand Per Home With This End Use [kW]'].fillna(0)
    df['Number of Homes in Bin With This End Use Metered'] = pd.to_numeric(df['Number of Homes in Bin With This End Use Metered'], errors='coerce').fillna(0)
    
    df['total_demand'] = df['Average Demand Per Home With This End Use [kW]'] * df['Number of Homes in Bin With This End Use Metered']
    
    # 3. Define End Use to Target Column Mapping
    # This mapping is inferred from common energy end-use categories and target column names.
    end_use_map = {
        'Heating': 'hvac',
        'Cooling': 'hvac',
        'HVAC': 'hvac',
        'Water Heating': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Freezer': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Oven': 'cooking_range',
        'Microwave': 'cooking_range', # Often grouped with cooking
        'Pool Pumps': 'pool_spa_pumps',
        'Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting', # Generic lighting
        'Plug Loads': 'plug',
        'Miscellaneous': 'plug', # Often plug loads
        'Pool Heater': 'pool_spa_heater',
        'Spa Heater': 'pool_spa_heater',
        'Remaining Load': None # Ignore or map if necessary, but target doesn't have a 'remaining' col
    }
    
    # Map End Use to target column name
    df['target_col'] = df['End Use'].map(end_use_map)
    
    # Filter out rows that don't map to a target column
    df = df[df['target_col'].notna()]
    
    # 4. Aggregate
    # Group by season, hour, and target_col, summing total_demand
    agg_df = df.groupby(['season', 'Hour Ending', 'target_col'])['total_demand'].sum().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot_table(index=['season', 'Hour Ending'], columns='target_col', values='total_demand', fill_value=0).reset_index()
    
    # Rename Hour Ending to hour
    pivot_df = pivot_df.rename(columns={'Hour Ending': 'hour'})
    
    # 6. Ensure all target columns exist
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    # Add missing columns with 0
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    # Convert hour to int64
    result_df['hour'] = result_df['hour'].astype('int64')
    
    # Convert specific columns to int64 as per target schema
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        result_df[col] = result_df[col].astype('int64')
        
    # Float cols
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    for col in float_cols:
        result_df[col] = result_df[col].astype('float64')
        
    return result_df