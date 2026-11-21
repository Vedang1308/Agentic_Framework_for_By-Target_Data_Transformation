import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source electricity usage data into aggregated seasonal hourly profiles.
    """
    df = source.copy()
    
    # 1. Parse time and extract hour and month
    df['dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['dt'].dt.hour
    df['month'] = df['dt'].dt.month
    
    # 2. Map month to season
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else: # 9, 10, 11
            return 'Autumn'
            
    df['season'] = df['month'].apply(get_season)
    
    # 3. Define columns for each category
    # HVAC: Heating, Cooling, Fans (H/C), Pumps (H/C)
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
    dwhe_cols = [
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
    # Includes general plug loads, various fans, and pool/hot tub equipment
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
    
    # 4. Create aggregated columns
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwhe_cols].sum(axis=1)
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    
    # 5. Group by season and hour, then sum the categories
    # We also sum the net_site_electricity_kwh to verify total, but we'll calculate total from components
    group_cols = ['season', 'hour']
    
    agg_df = df.groupby(group_cols).agg(
        hvac=('hvac', 'sum'),
        domestic_water_heating=('domestic_water_heating', 'sum'),
        major_appliances=('major_appliances', 'sum'),
        lighting=('lighting', 'sum'),
        miscellaneous_plug_loads=('miscellaneous_plug_loads', 'sum')
    ).reset_index()
    
    # 6. Calculate total from the components
    agg_df['total'] = (agg_df['hvac'] + 
                       agg_df['domestic_water_heating'] + 
                       agg_df['major_appliances'] + 
                       agg_df['lighting'] + 
                       agg_df['miscellaneous_plug_loads'])
    
    # 7. Define target columns
    target_columns = ['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    return agg_df[target_columns]