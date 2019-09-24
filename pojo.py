"""
24/09/2019 : 10:21PM
Program to demonstrate working of Elastic search without using any library to filter data
"""
from elasticsearch5 import Elasticsearch
from googlesearch import search
es = Elasticsearch()


# Google search library
def get_urls(company_name):
    print('get_urls')
    """
    :param company_name: Name of the company
    :return: URLs of LinkedIn, Angel.co, crunch_base and the company mentioned.
    """
    sites = ['linked_in', 'angel_co', 'crunch_base', 'website']
    urls = {}
    for site in sites:
        query = company_name + site
        url_generator = search(query, tld="com", num=1, stop=1, pause=2)
        for url in url_generator:
            urls[site] = url.replace('/jobs', "")
    return urls


def store_data(data, table_name):
    es.index(index="fundoo_contact", body=data, doc_type=table_name)


def search_data(database_name, table_name, operation, query):
    response = es.search(index=database_name, doc_type=table_name, body={"query": {operation: query}})
    return response


company_name = ["Niyo Solutions", "Hashtag Loyalty", "Think Analytics"]
for c_name in company_name:
    urls = get_urls(c_name)
    store_data(urls, 'company_data')

query = {"linked_in": "*niyo*"}
res = search_data('fundoo_contact', 'company_data', 'match', query)
print(res['hits']['hits'])