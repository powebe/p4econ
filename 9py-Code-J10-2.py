path='https://github.com/powebe/p4econ/raw/main/'
fname = 'fe-all.xlsx'
SheetName ='FE-ex1'
url = path + fname
pd.read_excel(url, sheet_name=SheetName)
