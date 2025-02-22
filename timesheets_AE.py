import os
import pandas as pd
import numpy as np
from datetime import datetime

def process_timesheet(
    main_path,
    file
    ):
    """
    Imports a .csv timesheet file, which must have the following columns:
    - 'Duration': working time, format '%H:%M:%S'.
    - 'Activity': working efficiency, format 'X%'.
    The function processes the timesheet, converting 'Duration' into hours
    and 'Activity' into percentages. The modified timesheet is exported.
    
    --- Inputs --- 
    {main_path} [String]: Path to locate the timesheet file. Do not include
    a final '/'.
    {file} [String]: File's name, including the .csv extension.

    --- Returns ---
    Exports the modified timesheet into the {main_path}. The name of the file is:
    '{old_name}_hours{total_working_hours}_activity{average_activity}.csv',
    where {old_name} is the original {file} input without the .csv extension,
    {total_working_hours} is the total amount of worked hours, with one decimal
    digit, and {average_activity} is the average activity, weighted by the
    corresponding working hours, in [%] units, rounded to the nearest integer.
    """
    # Prepare data and identify time and activity columns:
    df = pd.read_csv(main_path+'/'+file)
    work_activity = df['Activity']
    # Convert work_time into hours:
    df['work_hours'] = df['Duration'].apply(
        lambda x: (datetime.strptime(x, '%H:%M:%S').hour+
                   datetime.strptime(x, '%H:%M:%S').minute/60+
                   datetime.strptime(x, '%H:%M:%S').second/3660
                  ))
    # Convert efficienty into numbers [%]:
    df['activity_%'] = df['Activity'].apply(
        lambda x: float(x[:-1]))
    # Calculate total working time:
    total_time_hours = df['work_hours'].sum()
    # Calculate average activity:
    avg_act = sum(df['activity_%']*df['work_hours']/total_time_hours)
    # Create new filename:
    new_name = f'_{file[:-4]}_hours{total_time_hours:.1f}_activity{avg_act:.0f}.csv'
    df.to_csv(main_path+'/'+new_name, index=False)  

    # Load .csv file:
keyword = '_timesheet_'
main_path = '/home/meneses/Downloads'
files = [file for file in os.listdir(main_path) if
        keyword in file and '.csv' in file]
for file in files:
    process_timesheet(main_path,file)