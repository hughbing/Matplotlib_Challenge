#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Dependencies and Setup
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Hide warning messages in notebook
import warnings
warnings.filterwarnings('ignore')

# File to Load (Remember to Change These)
mouse_drug_data_to_load = "data/mouse_drug_data.csv"
clinical_trial_data_to_load = "data/clinicaltrial_data.csv"

# Read the Mouse and Drug Data and the Clinical Trial Data

tumor_data = pd.read_csv("data/clinicaltrial_data.csv")
tumor_data.head()

drug_data = pd.read_csv("data/mouse_drug_data.csv")
drug_data.head()

# Combine the data into a single dataset
trial_df= pd.merge(tumor_data, drug_data, how='outer', on='Mouse ID')
trial_df.head()


# ## Tumor Response to Treatment

# In[3]:


# Store the Mean Tumor Volume Data Grouped by Drug and Timepoint 
fourdrug_trial_df = trial_df.loc [(trial_df["Drug"] == "Capomulin") | (trial_df["Drug"] == "Infubinol") | (trial_df["Drug"] == "Ketapril") | (trial_df["Drug"] == "Placebo"), :]
fourdrug_trial_df.head()
# Convert to DataFrame
Tumor_group_df = fourdrug_trial_df.groupby(['Drug','Timepoint'])
Tumor_sem_df = pd.DataFrame(Tumor_group_df ["Tumor Volume (mm3)"].sem())
Tumor_sem_df.head()


# In[2]:





# In[4]:


# Store the Standard Error of Tumor Volumes Grouped by Drug and Timepoint
Capomulin_yerr_df=Tumor_sem_df.loc['Capomulin',["Tumor Volume (mm3)"]]
Capomulin_yerr=Capomulin_yerr_df.iloc[:, 0].values
Capomulin_yerr

Infubinol_yerr_df=Tumor_sem_df.loc['Infubinol',["Tumor Volume (mm3)"]]
Infubinol_yerr= Infubinol_yerr_df.iloc[:, 0].values
Infubinol_yerr

Ketapril_yerr_df=Tumor_sem_df.loc['Ketapril',["Tumor Volume (mm3)"]]
Ketapril_yerr= Ketapril_yerr_df.iloc[:, 0].values
Ketapril_yerr

Placebo_yerr_df=Tumor_sem_df.loc['Placebo',["Tumor Volume (mm3)"]]
Placebo_yerr= Placebo_yerr_df.iloc[:, 0].values
Placebo_yerr

# Convert to DataFrame
Tumor_mean_df = pd.DataFrame(Tumor_group_df ["Tumor Volume (mm3)"].mean())
Tumor_mean_df.reset_index(inplace=True)
Tumor_mean_df.head()



# In[3]:





# In[5]:


# Minor Data Munging to Re-Format the Data Frames
Capomulin_df=Tumor_mean_df.loc[Tumor_mean_df["Drug"]=="Capomulin",:]
Capomulin_df
rename_Capomulin_df = Capomulin_df.rename(columns={"Tumor Volume (mm3)":"Capomulin"})
rename_Capomulin_df.head()

Infubinol_df=Tumor_mean_df.loc[Tumor_mean_df["Drug"]=="Infubinol",:]
Infubinol_df
rename_Infubinol_df = Infubinol_df.rename(columns={"Tumor Volume (mm3)":"Infubinol"})
rename_Infubinol_df.head()

Ketapril_df=Tumor_mean_df.loc[Tumor_mean_df["Drug"]=="Ketapril",:]
Ketapril_df
rename_Ketapril_df = Ketapril_df.rename(columns={"Tumor Volume (mm3)":"Ketapril"})
rename_Ketapril_df.head()

Placebo_df=Tumor_mean_df.loc[Tumor_mean_df["Drug"]=="Placebo",:]
Placebo_df
rename_Placebo_df = Placebo_df.rename(columns={"Tumor Volume (mm3)":"Placebo"})
rename_Placebo_df.head()


# In[6]:


meger1_df=pd.merge(rename_Capomulin_df, rename_Infubinol_df, on="Timepoint")
meger1_df.head()

meger2_df=pd.merge(rename_Ketapril_df, rename_Placebo_df, on="Timepoint")
meger2_df.head()

merge3_df = pd.merge(meger1_df, meger2_df, on="Timepoint")
merge3_df.head()

tumor_response_df=merge3_df[["Timepoint", "Capomulin", "Infubinol", "Ketapril", "Placebo"]]
tumor_response_df

tumor_response_df['Timepoint'] = tumor_response_df['Timepoint'].astype(float)
tumor_response_df.dtypes


# In[7]:


# Generate the Plot (with Error Bars)
ax=tumor_response_df.plot(kind='scatter', x='Timepoint',y='Capomulin', linestyle='--', color='red', marker='o', yerr=Capomulin_yerr);
ax.errorbar(x=tumor_response_df['Timepoint'],y=tumor_response_df['Capomulin'], yerr=Capomulin_yerr, fmt='o', mfc='r', mec='k', ms=6, mew=1, linestyle='--',alpha=0.5, label="Capomulin" )
tumor_response_df.plot(kind='scatter', x='Timepoint', y='Infubinol', linestyle='--', color='DarkGreen', marker='d', yerr = Infubinol_yerr, ax=ax);
ax.errorbar(x=tumor_response_df['Timepoint'],y=tumor_response_df['Infubinol'], yerr=Infubinol_yerr, fmt='x', mfc='b', mec='k', ms=6, mew=1, linestyle='--', alpha=0.5, label="Infubinol")
tumor_response_df.plot(kind='scatter', x='Timepoint', y='Ketapril', linestyle='--', color='blue', marker='x',  yerr = Ketapril_yerr,  ax=ax);
ax.errorbar(x=tumor_response_df['Timepoint'],y=tumor_response_df['Ketapril'], yerr=Ketapril_yerr, fmt='+', mfc='g', mec='k', ms=6, mew=1, linestyle='--', alpha=0.5, label="Ketapril")
tumor_response_df.plot(kind='scatter', x='Timepoint', y='Placebo', linestyle='--', color='black', marker='s',  yerr = Placebo_yerr,  ax=ax);
ax.errorbar(x=tumor_response_df['Timepoint'],y=tumor_response_df['Placebo'], yerr=Placebo_yerr, fmt='s', mfc='y', mec='k', ms=6, mew=1, linestyle='--', alpha=0.5, label="Placebo")
xlim = ax.get_xlim()
factor = 0.1 
new_xlim = (xlim[0] + xlim[1])/2 + np.array((-0.5, 0.5)) * (xlim[1] - xlim[0]) * (1 + factor) 
ax.set_xlim(new_xlim)
ax.grid()
ax.set_xlabel("Time(days)")
ax.set_ylabel("Tumor Volume (mm3)")
ax.set_title("Tumor response to treatment")
legend = ax.legend(loc='best', shadow=True)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels )
plt.savefig("tumor_response_to_treatment.png")
plt.show()



# In[ ]:





# ![Tumor Response to Treatment](../Images/treatment.png)

# ## Metastatic Response to Treatment

# In[8]:


# Store the Mean Met. Site Data Grouped by Drug and Timepoint 
Metastasis_mean_df = pd.DataFrame(Tumor_group_df ["Metastatic Sites"].mean())
Metastasis_mean_df.reset_index(inplace=True)
Metastasis_mean_df.head()

Capomulin_df1=Metastasis_mean_df.loc[Metastasis_mean_df["Drug"]=="Capomulin",:]
Capomulin_df1
rename_Capomulin_df1 = Capomulin_df1.rename(columns={"Metastatic Sites":"Capomulin"})
rename_Capomulin_df1.head()

Infubinol_df1=Metastasis_mean_df.loc[Metastasis_mean_df["Drug"]=="Infubinol",:]
Infubinol_df1
rename_Infubinol_df1 = Infubinol_df1.rename(columns={"Metastatic Sites":"Infubinol"})
rename_Infubinol_df1.head()

Ketapril_df1=Metastasis_mean_df.loc[Metastasis_mean_df["Drug"]=="Ketapril",:]
Ketapril_df1
rename_Ketapril_df1 = Ketapril_df1.rename(columns={"Metastatic Sites":"Ketapril"})
rename_Ketapril_df1.head()

Placebo_df1=Metastasis_mean_df.loc[Metastasis_mean_df["Drug"]=="Placebo",:]
Placebo_df1
rename_Placebo_df1 = Placebo_df1.rename(columns={"Metastatic Sites":"Placebo"})
rename_Placebo_df1.head()




# In[6]:


meger1_df1=pd.merge(rename_Capomulin_df1, rename_Infubinol_df1, on="Timepoint")
meger1_df1.head()

meger2_df1=pd.merge(rename_Ketapril_df1, rename_Placebo_df1, on="Timepoint")
meger2_df1.head()

merge3_df1 = pd.merge(meger1_df1, meger2_df1, on="Timepoint")
merge3_df1.head()


# In[ ]:


# Store the Standard Error associated with Met. Sites Grouped by Drug and Timepoint 
Metastatic_change_df=merge3_df1[["Timepoint", "Capomulin", "Infubinol", "Ketapril", "Placebo"]]
Metastatic_change_df.head()

Metastatic_change_df['Timepoint'] = Metastatic_change_df['Timepoint'].astype(float)
Metastatic_change_df.dtypes

# Convert to DataFrame
Metastasis_sem_df = pd.DataFrame(Tumor_group_df ["Metastatic Sites"].sem())
Metastasis_sem_df.head()


# In[7]:





# In[ ]:


# Minor Data Munging to Re-Format the Data Frames
Capomulin_yerr_df1=Metastasis_sem_df.loc['Capomulin',["Metastatic Sites"]]
Capomulin_yerr1=Capomulin_yerr_df1.iloc[:, 0].values
Capomulin_yerr1

Infubinol_yerr_df=Metastasis_sem_df.loc['Infubinol',["Metastatic Sites"]]
Infubinol_yerr1= Infubinol_yerr_df.iloc[:, 0].values
Infubinol_yerr1

Ketapril_yerr_df1=Metastasis_sem_df.loc['Ketapril',["Metastatic Sites"]]
Ketapril_yerr1=Ketapril_yerr_df1.iloc[:, 0].values
Ketapril_yerr1

Placebo_yerr_df1=Metastasis_sem_df.loc['Placebo',["Metastatic Sites"]]
Placebo_yerr1=Placebo_yerr_df1.iloc[:, 0].values
Placebo_yerr1


# In[8]:





# In[ ]:


# Generate the Plot (with Error Bars)
plt.figure(figsize=(20,3))
ax=Metastatic_change_df.plot(kind='scatter', x='Timepoint',y='Capomulin', linestyle='--', color='red', marker='o', yerr=Capomulin_yerr1);
ax.errorbar(x=Metastatic_change_df['Timepoint'],y=Metastatic_change_df['Capomulin'], yerr=Capomulin_yerr1, fmt='o', mfc='r', mec='k', ms=6, mew=1, linestyle='--',alpha=0.5, label="Capomulin" )
Metastatic_change_df.plot(kind='scatter', x='Timepoint', y='Infubinol', linestyle='--', color='DarkGreen', marker='d', yerr = Infubinol_yerr1, ax=ax);
ax.errorbar(x=Metastatic_change_df['Timepoint'],y=Metastatic_change_df['Infubinol'], yerr=Infubinol_yerr1, fmt='x', mfc='b', mec='k', ms=6, mew=1, linestyle='--', alpha=0.5, label="Infubinol")
Metastatic_change_df.plot(kind='scatter', x='Timepoint', y='Ketapril', linestyle='--', color='blue', marker='x',  yerr = Ketapril_yerr1,  ax=ax);
ax.errorbar(x=Metastatic_change_df['Timepoint'],y=Metastatic_change_df['Ketapril'], yerr=Ketapril_yerr1, fmt='+', mfc='g', mec='k', ms=6, mew=1, linestyle='--', alpha=0.5, label="Ketapril")
Metastatic_change_df.plot(kind='scatter', x='Timepoint', y='Placebo', linestyle='--', color='black', marker='s',  yerr = Placebo_yerr1,  ax=ax);
ax.errorbar(x=Metastatic_change_df['Timepoint'],y=Metastatic_change_df['Placebo'], yerr=Placebo_yerr1, fmt='s', mfc='y', mec='k', ms=6, mew=1, linestyle='--', alpha=0.5, label="Placebo")
xlim = ax.get_xlim()
factor = 0.1 
new_xlim = (xlim[0] + xlim[1])/2 + np.array((-0.5, 0.5)) * (xlim[1] - xlim[0]) * (1 + factor) 
ax.set_xlim(new_xlim)

ax.grid()
ax.set_xlabel("Treatment Duration(days)")
ax.set_ylabel("Metastatic sites")
ax.set_title("Metastatic spread during treatment")
legend = ax.legend(loc='best', shadow=True)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels )
plt.savefig("Metastatic_spread_during_treatment.png")
plt.show()


# ![Metastatic Spread During Treatment](../Images/spread.png)

# ## Survival Rates

# In[ ]:


# Store the Count of Mice Grouped by Drug and Timepoint (W can pass any metric)
mice_count_df=pd.DataFrame(Tumor_group_df["Mouse ID"].count())
mice_count_df.reset_index(inplace=True)
mice_count_df.head()
# Convert to DataFrame
Capomulin_df2=mice_count_df.loc[mice_count_df["Drug"]=="Capomulin",:]
Capomulin_df2
rename_Capomulin_df2 = Capomulin_df2.rename(columns={"Mouse ID":"Capomulin"})
rename_Capomulin_df2.head()

Infubinol_df2=mice_count_df.loc[mice_count_df["Drug"]=="Infubinol",:]
Infubinol_df2
rename_Infubinol_df2 = Infubinol_df2.rename(columns={"Mouse ID":"Infubinol"})
rename_Infubinol_df2.head()

Ketapril_df2=mice_count_df.loc[mice_count_df["Drug"]=="Ketapril",:]
Ketapril_df2
rename_Ketapril_df2 = Ketapril_df2.rename(columns={"Mouse ID":"Ketapril"})
rename_Ketapril_df2.head()

Placebo_df2=mice_count_df.loc[mice_count_df["Drug"]=="Placebo",:]
Placebo_df2
rename_Placebo_df2 = Placebo_df2.rename(columns={"Mouse ID":"Placebo"})
rename_Placebo_df2.head()


# In[10]:


meger1_df2=pd.merge(rename_Capomulin_df2, rename_Infubinol_df2, on="Timepoint")
meger1_df2.head()

meger2_df2=pd.merge(rename_Ketapril_df2, rename_Placebo_df2, on="Timepoint")
meger2_df2.head()

merge3_df2 = pd.merge(meger1_df2, meger2_df2, on="Timepoint")
merge3_df2.head()


# In[ ]:


# Minor Data Munging to Re-Format the Data Frames
survive_rate_df=merge3_df2[["Timepoint", "Capomulin", "Infubinol", "Ketapril", "Placebo"]]
survive_rate_df.head()

survive_rate_df = survive_rate_df.astype(float)
survive_rate_df.dtypes

survive_rate_df["Capomulin_percent"]=survive_rate_df["Capomulin"]/survive_rate_df["Capomulin"].iloc[0] * 100
survive_rate_df["Infubinol_percent"]=survive_rate_df["Infubinol"]/survive_rate_df["Infubinol"].iloc[0] * 100
survive_rate_df["Ketapril_percent"]=survive_rate_df["Ketapril"]/survive_rate_df["Ketapril"].iloc[0] * 100
survive_rate_df["Placebo_percent"]=survive_rate_df["Placebo"]/survive_rate_df["Placebo"].iloc[0] * 100
survive_rate_df



# In[11]:





# In[ ]:


# Generate the Plot (Accounting for percentages)
ax=survive_rate_df.plot(kind='line', x='Timepoint',y='Capomulin_percent', linestyle='--', color='red', marker='o', alpha=0.5, label="Capomulin");
survive_rate_df.plot(kind='line', x='Timepoint', y='Infubinol_percent', linestyle='--', color='DarkGreen', marker='d', ax=ax, alpha=0.5, label="Infubinol");
survive_rate_df.plot(kind='line', x='Timepoint', y='Ketapril_percent', linestyle='--', color='blue', marker='x',  ax=ax,  alpha=0.5, label="Ketapril");
survive_rate_df.plot(kind='line', x='Timepoint', y='Placebo_percent', linestyle='--', color='black', marker='s', ax=ax,  alpha=0.5, label="Placebo");

ax.set_xlim(0, 45, 5)
ax.set_ylim(30, 110)
ax.grid()
ax.set_xlabel("Times(days)")
ax.set_ylabel("Survival Rate Percent(%)")
ax.set_title("Survival during Treatment")
legend = ax.legend(loc='best', shadow=True)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels )
plt.savefig("Survival_during_treatment.png")
plt.show()


# ![Metastatic Spread During Treatment](../Images/survival.png)

# ## Summary Bar Graph

# In[ ]:


# Calculate the percent changes for each drug
Capomulin_tumorvolume_changepercent=(tumor_response_df["Capomulin"].iloc[9]-tumor_response_df["Capomulin"].iloc[0])/tumor_response_df["Capomulin"].iloc[0]*100
Capomulin_tumorvolume_changepercent

Infubinol_tumorvolume_changepercent=(tumor_response_df["Infubinol"].iloc[9]-tumor_response_df["Infubinol"].iloc[0])/tumor_response_df["Infubinol"].iloc[0]*100
Infubinol_tumorvolume_changepercent

Ketapril_tumorvolume_changepercent=(tumor_response_df["Ketapril"].iloc[9]-tumor_response_df["Ketapril"].iloc[0])/tumor_response_df["Ketapril"].iloc[0]*100
Ketapril_tumorvolume_changepercent

Placebo_tumorvolume_changepercent=(tumor_response_df["Placebo"].iloc[9]-tumor_response_df["Placebo"].iloc[0])/tumor_response_df["Placebo"].iloc[0]*100
Placebo_tumorvolume_changepercent


# Display the data to confirm
d = {'Capomulin': Capomulin_tumorvolume_changepercent, 'Infubinol': Infubinol_tumorvolume_changepercent, 'Ketapril': Ketapril_tumorvolume_changepercent, 'Placebo': Placebo_tumorvolume_changepercent}
totaltumor_volume_change = pd.Series(d)
totaltumor_volume_change


# In[13]:





# In[ ]:


# Store all Relevant Percent Changes into a Tuple
drug=totaltumor_volume_change.keys()
drug


# In[ ]:


ax = plt.subplot()
x_axis = np.arange(0, len(drug))
tick_locations = []
for x in x_axis:
    tick_locations.append(x + 0.4)

plt.title("Tumor Change Over 45 Days Treatment")
plt.ylabel("% Tumor Volume Change")

plt.xlim(-0.25, len(drug))
plt.ylim(-30, max(totaltumor_volume_change) + 10)
plt.grid(True, linestyle='dashed')

plt.xticks(tick_locations, drug)

width = 0.4
vals = [1,2,3,4,5]
colors = ['r','b','b','b','b']
colors = []
for value in totaltumor_volume_change:
    if value >= 0 :
        colors.append('r')
    else:
        colors.append('g')
percents=ax.bar(x_axis, totaltumor_volume_change, color=colors, alpha=0.75, align="edge")
def autolabel(percents, ax):

    (y_bottom, y_top) = ax.get_ylim()
    y_height = y_top - y_bottom
    for percent in percents:
        height = percent.get_height()
        
        ax.text(percent.get_x()+ percent.get_width()/2., 0.5*height, '%d' % int(height) +"%", ha='center', va='center')

autolabel(percents, ax)

plt.savefig("TumorChange_Over_45_Days_Treatment.png")
plt.show()


# ![Metastatic Spread During Treatment](../Images/change.png)

# In[ ]:




