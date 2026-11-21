import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse the datetime column
    df = source.copy()
    df['local_15min'] = pd.to_datetime(df['local_15min'], format='%m/%d/%Y %H:%M')
    
    # Extract month and hour
    df['month'] = df['local_15min'].dt.month
    df['hour'] = df['local_15min'].dt.hour
    
    # Define column groups for each category
    hvac_cols = [
        'air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum',
        'furnace1_sum', 'furnace2_sum',
        'heater1_sum', 'heater2_sum', 'heater3_sum',
        'housefan1_sum', 'venthood1_sum'
    ]
    
    domestic_water_heating_cols = [
        'waterheater1_sum', 'waterheater2_sum', 'circpump1_sum'
    ]
    
    major_appliances_cols = [
        'dishwasher1_sum', 'clotheswasher1_sum', 'clotheswasher_dryg1_sum',
        'drye1_sum', 'dryg1_sum',
        'oven1_sum', 'oven2_sum', 'range1_sum',
        'refrigerator1_sum', 'refrigerator2_sum',
        'microwave1_sum', 'disposal1_sum', 'icemaker1_sum'
    ]
    
    lighting_cols = [
        'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum',
        'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum',
        'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum',
        'poollight1_sum'
    ]
    
    # Identify all sum columns to determine miscellaneous
    all_sum_cols = [col for col in df.columns if col.endswith('_sum')]
    
    # Exclude grid and solar sums as they are likely total meters/generation, not end-use loads
    # Also exclude the columns already assigned to other categories
    excluded_cols = set(hvac_cols + domestic_water_heating_cols + major_appliances_cols + lighting_cols + ['grid_sum', 'solar_sum', 'solar2_sum'])
    misc_cols = [col for col in all_sum_cols if col not in excluded_cols]
    
    # Create category columns by summing the respective source columns
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[domestic_water_heating_cols].sum(axis=1)
    df['major_appliances'] = df[major_appliances_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # Aggregate by month and hour
    agg_df = df.groupby(['month', 'hour']).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum'
    }).reset_index()
    
    # Calculate total
    agg_df['total'] = (
        agg_df['hvac'] + 
        agg_df['domestic_water_heating'] + 
        agg_df['major_appliances'] + 
        agg_df['lighting'] + 
        agg_df['miscellaneous_plug_loads']
    )
    
    # Ensure column order and names match target
    target_columns = ['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    return agg_df[target_columns]