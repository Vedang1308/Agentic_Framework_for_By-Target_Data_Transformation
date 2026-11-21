import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse datetime and extract month and hour
    df = source.copy()
    df['local_15min'] = pd.to_datetime(df['local_15min'], format='%m/%d/%Y %H:%M')
    df['month'] = df['local_15min'].dt.month
    df['hour'] = df['local_15min'].dt.hour
    
    # 2. Define category mappings
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'furnace1_sum', 'furnace2_sum',
        'housefan1_sum'
    ]
    
    dwh_cols = [
        'waterheater1_sum', 'waterheater2_sum',
        'circpump1_sum', 'jacuzzi1_sum',
        'pool1_sum', 'pool2_sum', 'poolpump1_sum'
    ]
    
    major_appliances_cols = [
        'refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum',
        'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'drye1_sum', 'dryg1_sum',
        'dishwasher1_sum',
        'oven1_sum', 'oven2_sum', 'range1_sum',
        'microwave1_sum', 'disposal1_sum', 'icemaker1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'poollight1_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum'
    ]
    
    # Miscellaneous: All other _sum columns except grid, solar, solar2
    # First, identify all _sum columns
    all_sum_cols = [col for col in df.columns if col.endswith('_sum')]
    
    # Exclude grid and solar generation columns from load calculations
    exclude_cols = ['grid_sum', 'solar_sum', 'solar2_sum']
    
    # Identify columns already assigned to other categories
    assigned_cols = hvac_cols + dwh_cols + major_appliances_cols + lighting_cols
    
    # Miscellaneous is everything else in all_sum_cols that is not excluded and not assigned
    misc_cols = [col for col in all_sum_cols if col not in exclude_cols and col not in assigned_cols]
    
    # 3. Sum columns for each category
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appliances_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # 4. Group by month and hour and aggregate
    target_columns = ['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads']
    
    grouped = df.groupby(['month', 'hour'])[target_columns[2:]].sum().reset_index()
    
    # 5. Calculate total
    grouped['total'] = grouped['hvac'] + grouped['domestic_water_heating'] + grouped['major_appliances'] + grouped['lighting'] + grouped['miscellaneous_plug_loads']
    
    # 6. Return with exact column order
    return grouped[['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]