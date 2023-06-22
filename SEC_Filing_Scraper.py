###############################################################################

#SEC Filling Scraper
#author: Fabian Fernandez
#Date: 06/20/23

###############################################################################

# Importing modules
import pandas as pd
import requests
import streamlit as st
import plotly.express as px 

st.title('Example of SEC Screaning for Tegus Recruitment Process')
st.write('by Fabian Fernandez')


# Creating request Header
headers = {'User-Agent': "fabian.fernandez@pucp.pe"}

# Get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json"\
                              ,headers)

# Convert dictionary to DataFrame
companyData = pd.DataFrame.from_dict(companyTickers.json(),orient='index')

# Add leadind zeros ti CIK
companyData["cik_str"] = companyData["cik_str"].astype(str).str.zfill(10)

# Use CIK as index
companyData.set_index("ticker", inplace=True)


# Look for the CIK of the stock
x_names = list(companyData.index)
x_ax = st.sidebar.selectbox("Pick the ticker of the stock to screen", options=x_names)
cticker = x_ax
CIK = companyData['cik_str'][cticker]
Name_company = companyData['title'][cticker]

###############################################################################
# Obtaining General Information of the 10-Q and 10K
###############################################################################

# Get all the financial information of the ticket
filingMetaData = requests.get(f"https://data.sec.gov/submissions/CIK{CIK}.json"\
                               ,headers=headers)

# Converting dictionary to dataframe
allForms = pd.DataFrame.from_dict(filingMetaData.json()['filings']['recent'])

#Filtering by the list of values of the company
Forms10K = allForms[allForms['form'] == '10-K']
Forms10Q = allForms[allForms['form'] == '10-Q']
len10K = len(Forms10K)
len10Q = len(Forms10Q)

###############################################################################
# Obtaining Company facts data
###############################################################################


# get company facts data
companyFacts = requests.get(
    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json',
    headers=headers
    )
Assets = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['Assets']['units']['USD'])
NetIncomeLoss = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['NetIncomeLoss']['units']['USD'])


# get assets from 10Q forms and reset index
Assets10Q = Assets[Assets.form == '10-Q']
Assets10Q = Assets10Q.reset_index(drop=True)

NetIncomeLoss10Q = NetIncomeLoss[NetIncomeLoss.form == '10-Q']
NetIncomeLoss10Q = NetIncomeLoss10Q.reset_index(drop=True)

# get assets from 10K forms and reset index
Assets10K = Assets[Assets.form == '10-K']
Assets10K = Assets10Q.reset_index(drop=True)

NetIncomeLoss10K = NetIncomeLoss[NetIncomeLoss.form == '10-K']
NetIncomeLoss10K = NetIncomeLoss10Q.reset_index(drop=True)

###############################################################################
# Using StreamLit
###############################################################################


ReportForm = ['10-Q','10-K']
ReportForm = st.sidebar.radio("Pick a reporting Form", options=ReportForm)

if x_ax != "" and ReportForm != "":
  st.write(f'\n The company choosen is {Name_company} and it has {len10K} 10-K forms and {len10Q} 10-Q forms filled registered in EDGAR')

  if ReportForm == "10-K":
    df = px.Assets10K()
    fig = px.line(df, x='end', y="val")
    fig.show()




    


