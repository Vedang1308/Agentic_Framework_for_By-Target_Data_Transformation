import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse Month
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    df = source.copy()
    df['month'] = df['Time Period'].map(month_map)
    df['hour'] = df['Hour Ending']
    
    # 2. Map End Use to Target Columns
    # Define a mapping from Source 'End Use' to Target Column Name
    end_use_to_target = {
        'HVAC': 'hvac',
        'Heating': 'hvac',
        'Cooling': 'hvac',
        'Water Heater': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Freezer': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Range': 'cooking_range',
        'Oven': 'cooking_range',
        'Stove': 'cooking_range',
        'Pool Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting',
        'Plug Loads': 'plug',
        'Plug': 'plug',
        'Miscellaneous Plug': 'plug',
        'Pool Spa Heater': 'pool_spa_heater'
    }
    
    # Apply mapping. Use normalize() to handle potential case/whitespace issues if necessary,
    # but assuming exact match first. If not found, it will be NaN.
    df['target_col'] = df['End Use'].map(end_use_to_target)
    
    # Filter out rows that don't map to a target column (e.g., 'Remaining Load')
    df_valid = df.dropna(subset=['target_col'])
    
    # 3. Pivot the data
    # We need to aggregate by month and hour, spreading the demand into the target columns.
    # Using sum to handle cases where multiple source end-uses map to the same target column 
    # (e.g., Refrigerator and Freezer -> refrigerator) for the same month/hour.
    pivot_df = df_valid.pivot_table(
        index=['month', 'hour'],
        columns='target_col',
        values='Average Demand Per Home With This End Use [kW]',
        aggfunc='sum'
    ).reset_index()
    
    # 4. Ensure all target columns exist and fill missing with 0
    target_columns = [
        'month', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # Get the appliance columns specifically for filling
    appliance_cols = [c for c in target_columns if c not in ['month', 'hour']]
    
    # Fill NaN in appliance columns with 0
    for col in appliance_cols:
        if col in pivot_df.columns:
            pivot_df[col] = pivot_df[col].fillna(0)
        else:
            pivot_df[col] = 0
            
    # Select and order columns
    result_df = pivot_df[target_columns]
    
    # 5. Cast types to match target schema
    # month: float64, hour: int64
    # hvac, water_heating: float64
    # others: int64 (as per schema description, though physically odd for kW, we follow spec)
    
    result_df['month'] = result_df['month'].astype('float64')
    result_df['hour'] = result_df['hour'].astype('int64')
    
    result_df['hvac'] = result_df['hvac'].astype('float64')
    result_df['water_heating'] = result_df['water_heating'].astype('float64')
    
    int_cols = [
        'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 
        'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    for col in int_cols:
        # Convert to float first to handle any residual NaNs, then to int
        # Note: If values are small floats like 0.031, casting to int will truncate to 0.
        # Given the target sample shows 0s, and schema says int64, this is likely intended 
        # or the data is already integer-like (e.g. counts or scaled). 
        # However, if the data is kW, truncation is lossy. But we must follow schema.
        result_df[col] = result_df[col].fillna(0).astype('float64').astype('int64')
        
    return result_df