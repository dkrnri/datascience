import pandas as pd
import tabula
import numpy as np
pathr='E:/files/12res.pdf'
pathw='E:/files/12res1.csv'
# To convert pdf file into CSV file
tabula.convert_into(pathr,pathw,output_format='csv',pages='all')
# Reading data from CSV file
df=pd.read_csv(pathw)
# Dropping duplicate records in the data frame
dfndr=df.drop_duplicates(keep='first')
# Accessing the records belongs to Data Sceince students regular & LE
dfds=dfndr[dfndr['Htno'].str.contains('22KP1A61|23KP5A61')] 
replace={"A+":10,"A":9,"B":8,"C":7,"D":6,"E":5,"F":0,"ABSENT":0}
dfds['Grade']=dfds['Grade'].map(replace)
#creating pivot table 
ptable=dfds.pivot_table(index=['Htno'],columns=['Subname'],values=['Grade'])
# Creating no of backlogs column in pivot table by using sum() of column valus
ptable['backlogs']=(ptable.iloc[:,:]==0).sum(axis=1)
# Creating total column in pivot table by using sum() of column valus
ptable['total']=ptable.sum(axis=1)
#Writing pivot table into resdsfinal.xls file
ptable.to_excel('E:/files/resdsdata.xls') 
max_marks=ptable['total'].max()
topper=ptable[ptable['total']==max_marks]
# Writing toppers in a file
topper.to_excel('E:/files/resdstoppers.xls')
#print(topper)
# Analysis part
# To count total number students in each column
no_stds=np.zeros(len(ptable.columns))
for i in range(len(ptable.columns)):
    no_stds[i]=ptable.iloc[:,i].count()
# to find number of stds with zero backlogs
no_allpass=(ptable.backlogs==0).sum()
# to find the overal pass%
overall_passp=no_allpass/no_stds[0]*100
#print("overall pass% is:",overall_passp)
# overall pass%
overalldf=pd.DataFrame([[no_stds[0],no_allpass,overall_passp]])
overalldf.columns=['Total_no_stds','No_stds_pass','Pass%']
overalldf.to_excel('E:/files/overallpass.xls')
# To count total number students failed in each subject
fail=np.zeros(len(ptable.columns))
for i in range(len(ptable.columns)):
    fail[i]=sum(ptable.iloc[:,i]==0)
No_of_fails=fail
# To count total number students passed in each subject
pas=np.zeros(len(ptable.columns))
for i in range(len(ptable.columns)):
    pas[i]=sum(ptable.iloc[:,i]!=0)
No_of_pass=pas
# To calculate pass% of each subject
pasp=np.zeros(len(ptable.columns))
for i in range(len(ptable.columns)):
    pasp[i]=pas[i]/no_stds[i]*100
passp=pasp
# To calculate fail% of each subject
failp=np.zeros(len(ptable.columns))
for i in range(len(ptable.columns)):
    failp[i]=fail[i]/no_stds[i]*100
fail_p=failp

# Creating another data frame with  total no of stds, no of pass, fai, pass% 
data=[no_stds,No_of_fails,No_of_pass,passp,fail_p]
df_analysis=pd.DataFrame(data,index=['no_stds','no_of_fail','no_of_pass','pass%','fail%'])
# setting columns of ptable as columns for new data frame

df_analysis.columns=ptable.columns
# writing data frame into file
df_analysis.to_excel('E:/files/resdsanalysis.xls')