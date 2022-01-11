import pandas as pd
from datetime import datetime
from io import StringIO

# Trim values from required fields for a file 
def trim(file, fields_to_trim):
    file_df = pd.read_csv(file)
    for field_to_trim in fields_to_trim:
        file_df[field_to_trim] = file_df[field_to_trim].apply(lambda x: x.strip())
    return file_df

def format_date(df, actual_date_format, date_format, fields_to_format):
    for field_to_format in fields_to_format:
        df[field_to_format] = df[field_to_format].apply(lambda x: datetime.strptime(x, actual_date_format).strftime(date_format))
    return df

def merge(dataset_a, dataset_b, fields):
    df_b = pd.read_csv(dataset_b)
    return dataset_a.merge(df_b, how='inner', on=fields)

def obtain_metrics(dataset):
    df = pd.read_csv(dataset)
    df_time_filter = df[df['date'] > '2017-01-01']
    # The top 10 best games for each console/company.
    top_10_best_console_company = df.sort_values(by=['console','metascore'], ascending = False).groupby(by=['console','company']).head(10)
    # The worst 10 games for each console/company.
    worst_10_console_company = df.sort_values(by=['console','metascore']).groupby(by=['console','company']).head(10)
    # The top 10 best games for all consoles.
    top_10_best_consoles = df.sort_values(by=['console','metascore'], ascending = False).groupby(by=['console']).head(10)
    # The worst 10 games for all consoles.
    worst_10_consoles = df.sort_values(by=['console','metascore']).groupby(by=['console']).head(10)
    return top_10_best_console_company,worst_10_console_company,top_10_best_consoles, worst_10_consoles

def load_to_bq(df,table_ds_name):
    try:
        df.to_gbq(table_ds_name)
        message = "data succesfully loaded to " + table_ds_name
    except:
        message = "couldn't load data"
        print(message)

def dataframe_to_buffer(dataframe):
    csv_stream = StringIO()
    dataframe.to_csv(csv_stream)
    return csv_stream