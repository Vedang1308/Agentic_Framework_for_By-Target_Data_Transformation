import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # 1. Parse the time column to extract month and hour
    df = source.copy()
    df['time_parsed'] = pd.to_datetime(df['time'])
    df['month'] = df['time_parsed'].dt.month
    df['hour'] = df['time_parsed'].dt.hour

    # 2. Define the aggregation columns for each target category
    
    # HVAC: Heating, Cooling, and associated fans/pumps
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    # Domestic Water Heating
    dwh_cols = [
        'electricity_water_systems_kwh'
    ]
    
    # Major Appliances
    major_appl_cols = [
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

    # 3. Create temporary columns for the sums
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    df['total'] = df[total_cols].sum(axis=1)

    # 4. Group by month and hour and sum the aggregated values
    # We sum because the source data contains multiple days for each month/hour combination
    agg_df = df.groupby(['month', 'hour']).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'total': 'sum'
    }).reset_index()

    # 5. Ensure correct column order and types
    target_columns = ['month', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    # Ensure types match target schema (int64 for month/hour, float64 for rest)
    agg_df['month'] = agg_df['month'].astype('int64')
    agg_df['hour'] = agg_df['hour'].astype('int64')
    
    for col in ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']:
        agg_df[col] = agg_df[col].astype('float64')

    return agg_df[target_columns]