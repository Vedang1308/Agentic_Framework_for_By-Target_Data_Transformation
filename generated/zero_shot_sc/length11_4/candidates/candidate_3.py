import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define target columns verbatim
    target_columns = [
        'month', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Map Time Period (Month Name) to Numeric Month
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    df['month'] = df['Time Period'].map(month_map)
    
    # 2. Map Hour Ending to hour
    df['hour'] = df['Hour Ending'].astype(int)
    
    # 3. Define mapping from End Use to Target Column
    # Note: "Freezer" and "Refrigerator" both map to "refrigerator"
    end_use_to_col = {
        'HVAC': 'hvac',
        'Water Heating': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Freezer': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Pool Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting', # Generic lighting
        'Plug': 'plug',
        'Pool Spa Heater': 'pool_spa_heater'
    }
    
    # 4. Initialize target appliance columns with 0
    for col in target_columns:
        if col not in ['month', 'hour']:
            df[col] = 0.0
            
    # 5. Assign values based on End Use
    # We iterate through the unique End Uses present in the source
    # to avoid creating unnecessary intermediate series
    
    # Get the demand column
    demand_col = 'Average Demand Per Home With This End Use [kW]'
    
    # Create a mask for valid end uses
    valid_end_uses = df['End Use'].isin(end_use_to_col.keys())
    
    # For each target column, find rows where End Use maps to it
    for end_use, target_col in end_use_to_col.items():
        # Mask for this specific end use
        mask = df['End Use'] == end_use
        # Assign the demand value to the target column for these rows
        # Use where to keep existing 0s for other rows
        df[target_col] = df[target_col].where(~mask, df.loc[mask, demand_col])
        
    # 6. Select and return the target columns
    # Ensure types match if necessary, though pandas usually handles float/int inference
    # The target schema specifies int64 for some appliance columns, but they contain floats in source.
    # However, the sample target shows integers (0) and floats (1.07).
    # The schema says 'hvac' is float64, 'refrigerator' is int64.
    # This is contradictory if 'refrigerator' has non-integer values.
    # Looking at the sample target: 'refrigerator' is 0 (int). 'hvac' is 1.07 (float).
    # It's likely the schema types in the prompt are hints but the data is float.
    # We will return the data as is, letting pandas determine types, or cast if strictly required.
    # Given "Strict Requirements", we just return the dataframe.
    
    return df[target_columns]