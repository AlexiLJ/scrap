from bs4 import BeautifulSoup
import requests
import lxml
import json
import pandas as pd


class Scrapper():
    def __init__(self, product_detail_url) -> None:

        self.yield_ = dict()
        self.product_detail_url = product_detail_url
        self.product_page = requests.get(product_detail_url)
        self.soup = BeautifulSoup(self.product_page.content, 'lxml')
    
    
    def table_extractor(self, df_table, spec_col='spec', data_col='data', **kwargs):

        table_dict=dict()
        for key, value in kwargs.items():            
            table_dict[key]= df_table.loc[df_table[(df_table[spec_col] == value)].index[0]][data_col]
        return table_dict


    def product_detail(self):
        
        self.yield_["model"] = self.soup.find(id="detail_page").h1.text
        self.yield_["url"] = self.product_detail_url
        self.yield_["main_photo_path"] = self.soup.find(id="nahled")["src"]
        links = [link.img['src'] for link in self.soup.find_all(class_="html5lightbox")]
        if len(links) == 0: self.yield_['additional_photo_paths']=None
        else: self.yield_['additional_photo_paths']=links
        price  = self.soup.find(class_="cena").span.text.split()[0].split('.') 
        self.yield_["price"] = int(''.join(price))
        self.yield_["model_year"] = int(''.join(price))

        #Here I manage specs in the html table through pandas
        tab = self.soup.find_all('table', class_='spec')
        table_list=[]
        for t in tab:
            table_rows = t.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr.text for tr in td]
                table_list.append(row[1:])
        table=pd.DataFrame(table_list, columns=['spec', 'data'])       
        table_data={"weight" : "Hmotnost", "frame": "Rám"}
        year = table[table['spec'] == "Ročník"]
        self.yield_['model_year'] = int(year.iloc[0]['data'])        
        self.yield_["parameters"] = self.table_extractor(table, **table_data)
    
        return self.yield_

    def pandas__df(self):
        pass


def main(name, url_links):
    with open(name, 'a') as f:
        data=[Scrapper(task).product_detail() for task in url_links] #brute force
        json.dump(data, f, indent=4)
       
if __name__ == '__main__':
    tasks = [
        "https://www.lapierre-bike.cz/produkt/aircode-drs-80/5934", 
        "https://www.lapierre-bike.cz/produkt/spicy-cf-79/5993",
        "https://www.lapierre-bike.cz/produkt/lapierre-crosshill-50/6037",
        "https://www.lapierre-bike.cz/produkt/lapierre-ezesty-am-ltd-ultimate/5951",
        "https://www.lapierre-bike.cz/produkt/lapierre-ezesty-am-90-ultimate/5950"
    ]

    main("top-5-bikes.json", tasks)


    


        
   