import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the time column
    df['time'] = pd.to_datetime(df['time'])
    
    # 2. Extract month and hour for grouping
    df['month'] = df['time'].dt.month
    df['hour'] = df['time'].dt.hour
    
    # 3. Define the mapping of source columns to target categories
    
    # HVAC: heating, cooling, fans, pumps
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
    major_appliance_cols = [
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
    
    # 4. Group by month and hour and sum the relevant columns
    grouped = df.groupby(['month', 'hour'])
    
    agg_dict = {
        'hvac': (hvac_cols, 'sum'),
        'domestic_water_heating': (dwh_cols, 'sum'),
        'major_appliances': (major_appliance_cols, 'sum'),
        'lighting': (lighting_cols, 'sum'),
        'miscellaneous_plug_loads': (misc_plug_cols, 'sum'),
        'total': (total_cols, 'sum')
    }
    
    # Perform aggregation
    result_df = pd.DataFrame()
    result_df['month'] = grouped.groups.keys() # This is not quite right for direct assignment, better to use agg
    
    # Correct way to aggregate multiple columns into single columns
    agg_results = pd.DataFrame({
        'month': [],
        'hour': [],
        'hvac': [],
        'domestic_water_heating': [],
        'major_appliances': [],
        'lighting': [],
        'miscellaneous_plug_loads': [],
        'total': []
    })
    
    # Using groupby().agg() with a custom dictionary is tricky for summing multiple cols into one.
    # Easier to sum each category separately and merge, or use apply.
    
    # Let's use a simpler approach: sum the columns first, then groupby
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    df['total'] = df[total_cols].sum(axis=1)
    
    # Now group by month and hour and sum the aggregated columns
    agg_cols = ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    result = df.groupby(['month', 'hour'], as_index=False)[agg_cols].sum()
    
    # 5. Ensure column order matches target
    target_columns = ['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    return result[target_columns]