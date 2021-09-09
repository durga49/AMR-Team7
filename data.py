import pandas as pd

def JSONtoDataframe(JSONfilename):

  total_data = pd.read_json(JSONfilename)
  index_data = total_data[['date','open','high','low','close','symbol']]
  return index_data

def AllAvailableCompanies(JSONfilename):

      total_data = pd.read_json(JSONfilename)
      return total_data['symbol'].unique().tolist()
