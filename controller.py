import pandas as pd
from bs4 import BeautifulSoup
import requests


def load_data (file) :
    df = pd.read_json(file) # extract and load the data
    # transform 
    df['time'] = df['time'].apply(pd.to_datetime) # change the type of time to datetime
    df = __add_time_indicator(df, 'time', ['year', 'weekday', 'hour']) # add columns year / weekday / hour
    df = __clean_prefix(df, 'title', 'Vous avez regardé ') # del prefix 
    df = df.drop(['header', 'subtitles', 'products', 'details'], axis = 1) # del useless columns
    
    df['date'] = df['time'].map(lambda x : x.date()) # get date
    return df  


def __add_time_indicator(df, colref, indicators, suffix = ''):   # @vaihauWILIAMU
    type_indicator = {
        'year'    : lambda dt: dt.year,
        'month'   : lambda dt: dt.month,
        'weekday' : lambda dt: dt.weekday(),
        'day'     : lambda dt: dt.day,
        'hour'    : lambda dt: dt.hour
    }
    for indicator in indicators:
        if indicator in type_indicator: # If it is a valid indicator
            
            # The colname will be the indicator
            col_name = indicator
            
            # Add the suffix if there is one
            if suffix != '':
                col_name += '_' + suffix
            
            # Add the column
            df[col_name] = df[colref].map(type_indicator[indicator])
    return df


def __clean_prefix(df, col, taboo_word):   # @vaihauWILIAMU
    """
        Delete the prefix to_del in the column col in all dataframe in df
    """
    df = __drop_redundancy(df, col, taboo_word) 
    return df



def __drop_redundancy(df,col,txt):    # @vaihauWILIAMU
    """
        Get rid off txt repetition in a column of a dataframe
        Parameters :
            df : dataframe which have the column to handle [DataFrame]
            col : the column name [string]
            txt : the text to get rid off [string]
    """
    df[col] = pd.Series([ ''.join(elt.split(txt)) for elt in df[col].tolist() ])
    return df



def get_freq_mult(df, grpby):     # @vaihauWILIAMU
    """
    Get the frequence when grouped by grpby in df

    Parameters
    ----------
    df : Dataframe
        Dataframe to get freq
        
    grpby : 
        columns to group by.

    Returns
    -------
    DataFrame
        Dataframe in long format

    """
    k = df.groupby(grpby).size().unstack().reset_index()
    long = pd.melt(k, id_vars=grpby[0], value_vars=k.columns[1:])    
    return long.rename(columns={'value':'count'})


def filter_df(f,year=None, col='type', nbr=7):
    
    if year != None:
        f = f[f['year'] == year]
    
    filtered_df = f.groupby(col).size().to_frame().sort_values([0],ascending=False).head(nbr).reset_index()
    filtered_df.rename(columns={0:'count'}, inplace=True)
    
    return filtered_df

    