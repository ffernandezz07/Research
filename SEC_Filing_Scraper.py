###############################################################################

#SEC Filling Scraper
#author: Fabian Fernandez
#Date: 06/20/23

###############################################################################

# Importing modules
import pandas as pd
import requests
import streamlit as st

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
cticker = 'AAPL'
CIK = companyData['cik_str'][cticker]

###############################################################################
# Obtaining General Information of the 10-Q and 10K
###############################################################################

# Get all the financial information of the ticket
filingMetaData = requests.get(f"https://data.sec.gov/submissions/CIK{CIK}.json"\
                               ,headers=headers)

# Converting dictionary to dataframe
allForms = pd.DataFrame.from_dict(filingMetaData.json()['filings']['recent'])

#Filtering by the list of values of the company
listForms = ['10-K','10-Q']
allForms = allForms.loc[allForms['form'].isin(listForms)]


###############################################################################
# Obtaining Company facts data
###############################################################################


# get company facts data
companyFacts = requests.get(
    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json',
    headers=headers
    )
Assets = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['Assets']['units']['USD'])
Revenues = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['Revenues']['units']['USD'])
NetIncomeLoss = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['NetIncomeLoss']['units']['USD'])


# get assets from 10Q forms and reset index
Assets10Q = Assets[Assets.form == '10-Q']
Assets10Q = Assets10Q.reset_index(drop=True)

Revenues10Q = Revenues[Revenues.form == '10-Q']
Revenues10Q = Revenues10Q.reset_index(drop=True)

NetIncomeLoss10Q = NetIncomeLoss[NetIncomeLoss.form == '10-Q']
NetIncomeLoss10Q = NetIncomeLoss10Q.reset_index(drop=True)

###############################################################################
# Using StreamLit
###############################################################################

x_names = list(companyData.index)
ReportForm = ['10-Q','10-K']

x_ax = st.sidebar.selectbox("Pick the ticker of the stock to screen", options=x_names)
ReportForm = st.sidebar.radio("Pick a reporting Form", options=ReportForm)

