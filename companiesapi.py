import requests
import pandas as pd

url = "https://api.opencorporates.com/v0.4/companies/search?q="
words = ("word1", "word2")

uk = "&jurisdiction_code=gb"
per_page = "&per_page=100&page="
apikey = "&api_token=yourkey"
store = []
index = 0

for w in words:
  first_get = requests.get(url + w + uk + apikey).json()['results']['total_pages'] + 1
  pages = range(1, first_get + 1)
  for p in pages:
    full_url = url + w + uk + per_page + str(p) + apikey
    response = requests.get(full_url).json()
    for i in range(0, 99):
      try:
        index = index + 1
        word = w
        name = response['results']['companies'][i]['company']['name']
        number = response['results']['companies'][i]['company']['company_number']
        company_type = response['results']['companies'][i]['company']['company_type']
        linkCH = response['results']['companies'][i]['company']['registry_url']
        status = response['results']['companies'][i]['company']['current_status']
        incorporation_date = response['results']['companies'][i]['company']['incorporation_date']
        dissolution_date = response['results']['companies'][i]['company']['dissolution_date']
        address = response['results']['companies'][i]['company']['registered_address_in_full']
        #postcode = response['results']['companies'][i]['company']['registered_address']['postal_code']
        if len(response['results']['companies'][i]['company']['industry_codes']) == 0:
          industry1 = "NULL"
          industry2 = "NULL"
        else:
          try:
            industry1 = response['results']['companies'][i]['company']['industry_codes'][0]['industry_code'][
                'description']
            industry2 = response['results']['companies'][i]['company']['industry_codes'][1]['industry_code'][
                'description']
          except IndexError:
            industry2 = "NULL"
          else:
            industry1 = response['results']['companies'][i]['company']['industry_codes'][0]['industry_code'][
                'description']

        if len(response['results']['companies'][i]['company']['previous_names']) == 0:
          previous_name = "NULL"
          effective_from = "NULL"
          ceased_on = "NULL"
        else:
          previous_name = response['results']['companies'][i]['company']['previous_names'][0]['company_name']
          try:
            effective_from = response['results']['companies'][i]['company']['previous_names'][0]['start_date']
          except KeyError:
            pass
          ceased_on = response['results']['companies'][i]['company']['previous_names'][0]['end_date']
      except IndexError:
        continue
      else:
        pass
        store.append((index, word, name, number, company_type, linkCH, status, incorporation_date, dissolution_date,
                      address, industry1, industry2, previous_name, effective_from, ceased_on))

df = pd.DataFrame(store,
                  columns=[
                      "index", "word", "name", "number", "company_type", "linkCH", "status", "incorporation_date",
                      "dissolution_date", "address", "industry1", "industry2", "previous_name", "effective_from",
                      "ceased_on"
                  ])

print(df.head(n=10))
print(len(df))
df.to_csv('companiesOpenCorporates.csv', index=False)