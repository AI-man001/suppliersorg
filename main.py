import pandas as pd, os, csv
from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests, time, itertools


class Miner:
  def __init__(self, parameters):
    self.query = parameters

  def geturl(self, page):
    self.query = str(self.query).strip().replace(" ", "+")
    params = f"pg_suppliers={page}&_format=html&BuyersOrSuppliers=suppliers"
    return f"https://www.go4worldbusiness.com/find?searchText={self.query}&pg_buyers=1&{params}"

  def getpagecontent(self, page):
    pageresults = requests.get(self.geturl(page))
    soup = BeautifulSoup(pageresults.content, 'html.parser')
    return soup.find_all('h2', class_="text-capitalize entity-row-title h2-item-title")

  @staticmethod
  def writetoexcel(suppliers, filename):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    headers = list(set(itertools.chain.from_iterable(suppliers)))
    ws.append(headers)
    for elements in suppliers:
      ws.append([elements.get(h) for h in headers])
    wb.save(f"{filename}.xlsx")

  @staticmethod
  def writetocsv(suppliers, filename):
    keys = suppliers[0].keys()
    with open(f'{filename}.csv', 'w', newline='') as output_file:
      dict_writer = csv.DictWriter(output_file, keys)
      dict_writer.writeheader()
      dict_writer.writerows(suppliers)

  @staticmethod
  def csvtoexcel(path: str):
    read_file = pd.read_csv(path)
    filename = os.path.basename(path).split(".")[0]
    read_file.to_excel(f"{filename}.xlsx", index=None, header=True)

  @property
  def suppliers(self):
    suppliers_results = []
    for page in list(range(1, 15)):
      for supplier in self.getpagecontent(page):
        company = str(supplier.get('title')).split("from", 1)
        name = company[1].split(":", 1)[1].strip()
        country = company[1].split(":", 1)[0].strip()
        product = company[0].replace("wholesale supplier", "").strip()
        supplierdata = {"Supplier": name, "Product": product, "Country": country}
        if not supplierdata in suppliers_results:
          suppliers_results.append(supplierdata)
      time.sleep(3)  # ========= add delay between page nexting ========= #
    return suppliers_results

  @staticmethod
  def getsuppliers(params, filename="output", filetype="xlsx"):
    """by default this will write results to excell filetype is set to csv"""
    if filetype in ["csv", "xlsx"]:
      if filetype.lower() == "csv":
        Miner.writetocsv(Miner(params).suppliers, filename)
      elif str(filetype).lower() == "xlsx":
        Miner.writetoexcel(Miner(params).suppliers, filename)
      print("#==: finished :==#")
    else:
      print("#==: filetype can only be either vsc or xlsx :==#")


#Miner.getsuppliers("latex male condoms")

headers = {'X-Auth-Token': '4ff45d98d6df1f9b60d6c3dd'}
results = requests.get("https://api.data-axle.com/v1/b2c_links/search?query=Masks", headers=headers)
print(results.json().get("documents"))
