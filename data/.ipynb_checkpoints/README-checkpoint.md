# ** Very Important **


## Loading data

Due to the massive size of our data set we cant have the csv uncompressed in git. So heres how we use the data

1. Un move and uncompress raw/terrorism.csv.zip out of the git repository.
2. Copy the path of your uncompressed csv
3. When you need to call your data import functions from the scripts folder. 
4. The getData( "path") will load the data and process it and return a pandas data frame.

Like so 

df = getData(".../terrorism.csv")


## Dont Do

Do not have the uncompressed data in your git repository. This is because when you commit the data you will exceed the file size limmit and git wont push. The only way i found a way to fix this is to delete the repository and clone it again.




## Meta Data


-All data should go in this parent directory; a final data set may reside in this directory. 
Raw data is in /raw, cleaned and processed data is in /processed.

-Data Provided By: "NATIONAL CONSORTUIM FOR THE STUDY OF TERRORISM AND RESPONSES TO TERRORISM"

-Data Contains: An array of data from Terrorist attack across the globe including but not limmited to Date, location, casualties, ect ...

-Data Collected: 2017

-Data Purpose: To better under stand where, when and how terrorism is conducted.

-Data Collection: By filtering thousands of news articals with machine learning and then catorgised by a team. 

-source1: https://www.kaggle.com/START-UMD/gtd