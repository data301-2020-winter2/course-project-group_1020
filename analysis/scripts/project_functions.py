from pandas import *
import collections
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from collections import Counter
import seaborn as sns
import numpy as np
from IPython.display import HTML, display, Markdown
import tabulate
from pathlib import Path

import zipfile


def saveData(df):
    clean_path = Path( r"../../data/processed/terrorism_clean.csv" ) 
    df.to_csv(clean_path)


def getData():
    
    
     
    data_path = Path( r"../../data/raw/terrorism.zip" )
    terrorsimzip =  zipfile.ZipFile(data_path)
    terrorismcsv = terrorsimzip.open('terrorism.csv')
    
    df = read_csv( terrorismcsv , sep=',' , error_bad_lines=False, index_col=False, dtype='unicode', encoding="ISO-8859-1").drop(columns =[
    "eventid",
    "approxdate",
    "country",
    "vicinity",
    "region",
    "attacktype1",
    "targtype1",
    "natlty1",  
    "extended",
    "resolution",
    "location",
    "alternative",
    "alternative_txt",
    "attacktype2",
    "attacktype2_txt",
    "attacktype3",
    "attacktype3_txt",
    "crit1",
    "crit2",
    "crit3",
    "doubtterr",
    "targsubtype1",
    "targsubtype1_txt",
    "targtype2",
    "targtype2_txt",
    "targsubtype2",
    "targsubtype2_txt",
    "corp2",
    "target2",
    "natlty2",
    "natlty2_txt",
    "targtype3",
    "targtype3_txt",
    "targsubtype3",
    "targsubtype3_txt",
    "corp3",
    "target3",
    "natlty3",
    "natlty3_txt",
    "gsubname",
    "gname2",
    "gsubname2",
    "gname3",
    "gsubname3",
    "guncertain2",
    "guncertain3",
    "nperpcap",
    "claimed",
    "claimmode",
    "claimmode_txt",
    "claim2",
    "claimmode2",
    "claimmode2_txt",
    "claim3",
    "nhours",
    "ndays",
    "divert",
    "claimmode3",
    "claimmode3_txt",
    "compclaim",
    "weaptype1",
    "weapsubtype1",
    "weaptype2",
    "weaptype2_txt",
    "weapsubtype2",
    "weapsubtype2_txt",
    "weaptype3",
    "weaptype3_txt",
    "weapsubtype3",
    "weapsubtype3_txt",
    "weaptype4",
    "weaptype4_txt",
    "weapsubtype4",
    "weapsubtype4_txt",
    "weapdetail",
    "propcomment",
    "nhostkid",
    "nhostkidus",
    "addnotes",
    "scite1",
    "scite2",
    "scite3",
    "INT_LOG",
    "INT_IDEO",
    "INT_MISC",
    "INT_ANY",
    "summary",
    "motive",
    "propextent_txt",
    "related",
    "specificity",
    "multiple",
    "ransomamtus",
    "hostkidoutcome_txt"
    ]).rename(columns={
        "iyear": "year",
        "imonth": "month",
        "iday" : "day",
        "country_txt" : "country",
        "region_txt" : "region",
        "attacktype1_txt": "attacktype",
        "targtype1_txt": "targettype",
        "corp1" : "corp",
        "target1": "target",
        "natlty1_txt": "nationality",
        "kidhijcountry": "kidnaptocountry",
        "guncertain1": "guncertain",
        "weaptype1_txt": "weapontype",
        "weapsubtype1_txt": "weaponsubtype"
    }).assign(record = "international"
    )
    
    df.loc[df['country'] == df['nationality'], "record"] = "domestic"
    
    # Converting types: converting columns to floats and ints
    
    def convert_type(li, nans, types ):
        for i in li:
            df[i] = df[i].replace(nans, np.nan).astype(types)

            
    floats = "latitude longitude nperps nkill nkillus nkillter nwound nwoundus nwoundte propextent propvalue ransomamt ransompaid ransompaidus".split(" ")
    booleans = "success suicide guncertain individual property ishostkid ransom".split(" ")
    ints = "year month day".split(" ")

    convert_type(floats, ["-99", "-9", "nan", "Nan"], "float64" )
    convert_type(ints, [""], "int32" )
    
    #booleans need a special case
    for i in booleans:
        df[i] = df[i].fillna(value=0)
        df[i] = df[i].replace(["Nan"], np.nan).astype("float32").astype("bool")

        
    # Dropping unknowns: replace certain columns containing 'unknown' with NaN, then drop all Na
    
    containing_unknown = ["latitude", "longitude", "provstate", "city", "target", "nationality"]
    df[containing_unknown] = df[containing_unknown].replace('Unknown', np.nan)
    df = df.dropna(subset = containing_unknown)
    
    # Dropping zeros: filtering out certain columns with values of zero 
    
    df = df[(df['month'] != 0) & (df['day'] != 0)]
    
    # Resetting index
    
    df = df.reset_index().drop(columns='index')
    
    
    
    return df


def graph_year(df2, cnty):
    letter_counts = Counter(df2["year"])
    df3 = pandas.DataFrame.from_dict( letter_counts , orient='index', )
    df3.plot(kind='bar', width = 0.85, figsize = (16, 8), facecolor='r', edgecolor='k', title = ("Terrorist Attacks 1970 - 2017 in " + cnty), xlabel = "Year", ylabel = "Number Of Attacks")


def col_with_count( data, col):
    
    li = list()
    for i in set( data[ col]):
        li.append( [ i ,  len( data[data[col] == i]) ] )
    
    li = sorted(li, reverse=True ,key=lambda x:x[1])
    
    return li

def cont(country, df):
    
    df2 = df[df["country"] == country]
    
    
    
    #Most prolific groups
    print("There where ", len(df2) , " terrorist attackts from 1970 - 2017 in " , country, ". Killing a total number of " , df2["nkill"].sum() ," people.")
    
    print("\n\n")
    
    try:
        display(Markdown("Most prolific groups in " + country ))
        groups = DataFrame(  {"Number Of Attacks" : df2["gname"].value_counts()}  )
        display(HTML(tabulate.tabulate(groups[0:5], tablefmt='html')))
        print("\n\n")
    
    except:
        print( "Not enough data for an analysis in this country")
    
    
    #try:
    display(Markdown("Most Common Attack types"))
    groups = DataFrame(  {"Number Of Attacks" : df2["attacktype"].value_counts()}  )
    display(HTML(tabulate.tabulate(groups[0:5], tablefmt='html')))
    
    #except:
        #print( "Not enough data for an analysis in this country")
    
    print("\n\n")
    try:
        display(Markdown("Most Common Target types"))
        groups = DataFrame(  {"Number Of Attacks" : df2["target"].value_counts()}  )
        display(HTML(tabulate.tabulate(groups[0:5], tablefmt='html')))
    except:
        print( "Not enough data for an analysis in this country")
    
    #Graph
    
    sns.set_context("notebook", rc={"font.size":13,"axes.titlesize": 21 ,"axes.labelsize": 21})   
    sns.set(rc={'figure.figsize':(13,8)})
    ax = sns.countplot( x = df2["year"], palette = "rocket"  )
    ax.set(ylabel = "Number Of Attacks",xlabel='Years',  title = "Number of terrorism attacks over the years in " +  country  )
    ax.set_xticklabels( ax.get_xticklabels(), rotation=45)
    None
    
  

