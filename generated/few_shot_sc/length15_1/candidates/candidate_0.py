import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse time and derive hour and season
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    
    # Define season mapping based on meteorological seasons
    # Winter: Dec, Jan, Feb (12, 1, 2)
    # Spring: Mar, Apr, May (3, 4, 5)
    # Summer: Jun, Jul, Aug (6, 7, 8)
    # Fall: Sep, Oct, Nov (9, 10, 11)
    month = df['time_dt'].dt.month
    df['season'] = month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    })
    
    # 2. Define column mappings for target categories
    # HVAC: Heating, Cooling, Fans, Pumps related to HVAC
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    # Domestic Water Heating
    dwh_cols = [
        'electricity_water_systems_kwh'
    ]
    
    # Major Appliances
    major_appliances_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    
    # Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    
    # Miscellaneous Plug Loads
    misc_plug_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # Total
    total_cols = [
        'net_site_electricity_kwh'
    ]
    
    # 3. Aggregate by season and hour
    # We sum the values for each category within each group
    grouped = df.groupby(['season', 'hour'])
    
    agg_dict = {}
    agg_dict['hvac'] = (hvac_cols, 'sum')
    agg_dict['domestic_water_heating'] = (dwh_cols, 'sum')
    agg_dict['major_appliances'] = (major_appliances_cols, 'sum')
    agg_dict['lighting'] = (lighting_cols, 'sum')
    agg_dict['miscellaneous_plug_loads'] = (misc_plug_cols, 'sum')
    agg_dict['total'] = (total_cols, 'sum')
    
    # Perform aggregation
    # Note: pandas groupby.sum() on a subset of columns
    result = pd.DataFrame()
    result['season'] = grouped.first()['season'] # Get season from group keys
    result['hour'] = grouped.first()['hour']     # Get hour from group keys
    
    # It's cleaner to aggregate specific columns
    agg_df = df.groupby(['season', 'hour'])[[
        'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total'
    ]].sum() if False else None # Placeholder logic
    
    # Let's do it properly by summing the specific columns for each group
    # Create temporary columns for each target metric
    for col in hvac_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    for col in dwh_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    for col in major_appliances_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    for col in lighting_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    for col in misc_plug_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    for col in total_cols:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    # Sum columns for each category
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appliances_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    df['total'] = df[total_cols].sum(axis=1)
    
    # Now group by season and hour and sum these new columns
    target_cols = ['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    # Select only necessary columns for grouping
    subset = df[['season', 'hour'] + target_cols[2:]]
    
    # Group and sum
    result = subset.groupby(['season', 'hour'], as_index=False).sum()
    
    # Ensure column names match exactly
    # The sum() above should result in columns: season, hour, hvac, ...
    
    # Sort to ensure deterministic order (optional but good practice)
    # The target sample is not sorted, but let's just return the grouped result.
    # To match the exact target schema order:
    return result[target_cols]