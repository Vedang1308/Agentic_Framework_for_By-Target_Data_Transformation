import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse time and extract month and hour
    df['time_dt'] = pd.to_datetime(df['time'])
    df['month'] = df['time_dt'].dt.month
    df['hour'] = df['time_dt'].dt.hour
    
    # 2. Define category columns by summing relevant source columns
    
    # HVAC: Heating, Cooling, and their associated fans and pumps
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
    # Domestic Water Heating
    df['domestic_water_heating'] = df['electricity_water_systems_kwh']
    
    # Major Appliances
    major_appliance_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    df['major_appliances'] = df[major_appliance_cols].sum(axis=1)
    
    # Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    df['lighting'] = df[lighting_cols].sum(axis=1)
    
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
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    
    # Total
    df['total'] = df['net_site_electricity_kwh']
    
    # 3. Group by month and hour, and sum the values
    # Since the source data is 15-minute intervals, summing them gives the hourly total
    agg_df = df.groupby(['month', 'hour'], as_index=False).agg({
        'hvac': 'sum',
        'domestic_water_heating': 'sum',
        'major_appliances': 'sum',
        'lighting': 'sum',
        'miscellaneous_plug_loads': 'sum',
        'total': 'sum'
    })
    
    # 4. Select and order columns to match target schema verbatim
    target_columns = [
        'month', 
        'hour', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    # Sort for deterministic output (optional but good practice)
    agg_df = agg_df.sort_values(by=['month', 'hour']).reset_index(drop=True)
    
    return agg_df[target_columns]