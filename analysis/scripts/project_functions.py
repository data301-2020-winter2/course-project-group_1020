from pandas import *
import collections
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from collections import Counter
import numpy as np


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


def cont(st):
    
    #Filter to our specific country
    df2 = df[ df["country_txt"] == st]
    
    
    #Number of terorist attacks 
    print( "Number of terrorist attacks", len(df2), "From 1970 to 2000",end = "\n" *3 ) 
    
    
    #Pie Chart of the methods
    #attack = np.array(col_with_count(df2, "attacktype_txt"))
    #plt.pie(attack[:,1], labels = attack[:,0], radius = 2, rotatelabels = True )
    #plt.show()
    
    #Terrorist orgnisations
    attacks = col_with_count(df2, "attacktype_txt")
    
    #
    print("Most common attacks", st, end = "\n" * 2)
    for i in range(0, 5):
        print( attacks[i][0], " with ", attacks[i][1], "  "  )
    
    print(end = "\n" *2)
    
    
    
    #Graph of the attacks over the years
    graph_year(df2, st)
    
    
    
    #Terrorist orgnisations
    groups = col_with_count(df2, "gname")
    
    #
    print("Most active orgnisations", st, end = "\n" * 2)
    for i in range(0, 5):
        print( groups[i][0], " with ", groups[i][1], " attacks "  )
    
    print(end = "\n" *2)
    
    
    
    
    print("Number of deaths due to terrorism :", sum(to_numeric(df2["nkill"]).dropna()),end = "\n" * 2 )
    
  

