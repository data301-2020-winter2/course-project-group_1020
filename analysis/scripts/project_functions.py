from pandas import *
import collections
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from collections import Counter
import seaborn as sns
import numpy as np
from IPython.display import HTML, display, Markdown
import tabulate




def getData(path):
    df = read_csv( path , sep=',' , error_bad_lines=False, index_col=False, dtype='unicode', encoding="ISO-8859-1").drop(columns =[
    "approxdate",
    "country",
    "vicinity",
    "region",
    "attacktype1",
    "targtype1",
    "natlty1",
    "weaptype1",   
    "extended",
    "resolution",
    "location",
    "alternative",
    "alternative_txt",
    "attacktype2",
    "attacktype2_txt",
    "attacktype3",
    "attacktype3_txt",
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
    "kidhijcountry",
    "claimmode3",
    "claimmode3_txt",
    "compclaim",
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
    "related",
    ]).rename(columns={
        "eventid": "id",
        "iyear": "year",
        "imonth": "month",
        "iday" : "day",
        "attacktype1": "attacktype", 
        "attacktype1_txt": "attacktype_txt",
        "targettype1": "targettype",
        "targettype1_txt": "target_txt",
        "target1": "target",
        "natity1": "natity",
        "guncertain1": "guncertain",
        "wepontype1": "weapontype",
        "weapontype1_txt": "weapontype_txt",
        "crit1" : "crit"
    })



    def convert_type(li, nans, types ):
        for i in li:
            df[i] = df[i].replace(nans, np.nan).astype(types)

            
    s1 = "specificity nperps nkill nkillus nkillter nwound nwoundus nwoundte propextent propvalue ransomamt ransompaid ransompaidus".split(" ")
    s2 = "success suicide multiple guncertain individual property ishostkid ransom crit".split(" ")
    s3= "month day".split(" ")
    s4= "year".split(" ")

    convert_type(s1, ["-99", "-9", "nan", "Nan"], "float64" )
    convert_type(s3, ["nan", "Nan"], "float64" )
    convert_type(s4, [ "0"], "int32" )
    
    
    #booleans need a special case
    for i in s2:
            df[i] = df[i].replace(["Nan"], np.nan).astype("float32").astype("bool")

    
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
    
    df2 = df[df["country_txt"] == country]
    
    
    
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
    
    
    try:
        display(Markdown("Most Common Attack types"))
        groups = DataFrame(  {"Number Of Attacks" : df2["attacktype_txt"].value_counts()}  )
        display(HTML(tabulate.tabulate(groups[0:5], tablefmt='html')))
    
    except:
        print( "Not enough data for an analysis in this country")
    
    print("\n\n")
    try:
        display(Markdown("Most Common Target types"))
        groups = DataFrame(  {"Number Of Attacks" : df2["target"].value_counts()}  )
        display(HTML(tabulate.tabulate(groups[0:5], tablefmt='html')))
    except:
        print( "Not enough data for an analysis in this country")
    
    #Graph
    sns.set(rc={'figure.figsize':(21,13)})
    ax = sns.countplot( x = df2["year"], palette = "YlOrBr"  )
    ax.set(ylabel = "Number Of Attacks",xlabel='Years',  title = "Number of terrorism attacks over the years in " +  country  )
    ax.set_xticklabels( ax.get_xticklabels(), rotation=45)
    None



