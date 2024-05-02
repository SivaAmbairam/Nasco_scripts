import re

from module_package import *


if __name__ == '__main__':
    timestamp = datetime.now().date().strftime('%Y%m%d')
    file_name = os.path.basename(__file__).rstrip('.py')
    url = 'https://www.nascoeducation.com/'
    base_url = ''
    headers = {
        'authority': 'www.nascoeducation.com',
        'method': 'GET',
        'path': '/',
        'scheme': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        # 'Cookie': '_gcl_au=1.1.167469181.1713871569; _ga=GA1.1.98954045.1713871569; _fbp=fb.1.1713871569365.2108215192; smc_uid=1713871571623155; smc_tag=eyJpZCI6NjUzMywibmFtZSI6Im5hc2NvZWR1Y2F0aW9uLmNvbSJ9; smc_not=default; wp_ga4_customerGroup=NOT%20LOGGED%20IN; OptanonAlertBoxClosed=2024-04-23T11:26:53.243Z; _ga_RE264BGW5F=GS1.1.1713873295.1.0.1713873295.0.0.0; _ga_LBFM6FX79Q=GS1.1.1713873295.1.0.1713873295.60.0.0; _hjSessionUser_2414103=eyJpZCI6ImI1NTE0ODVmLTVmODAtNTNiOC1iNmIwLTJkNmY5MmYxYTJkOSIsImNyZWF0ZWQiOjE3MTM4NzMyOTUzNzQsImV4aXN0aW5nIjpmYWxzZX0=; form_key=j0JYLiNSWut3OEC9; private_content_version=ee78956a0586238a49c0910f10b9cb29; PHPSESSID=877161f13bf88950cc1bc65cd6b7ca0a; smc_session_id=6hfV0XIik335kW14pBWgReEYisZsB1nP; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; mage-messages=; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; smc_sesn=4; form_key=j0JYLiNSWut3OEC9; smc_tpv=26; smc_spv=4; section_data_ids={%22cart%22:1714109468}; smct_session=%7B%22s%22%3A1714109174863%2C%22l%22%3A1714109739300%2C%22lt%22%3A1714109739300%2C%22t%22%3A398%2C%22p%22%3A212%7D; klv_mage={"expire_sections":{"customerData":1714110340}}; _ga_9613NPS3Y3=GS1.1.1714109173.5.1.1714109740.60.0.0; _uetsid=4e69be30030a11ef832335dc5187520d; _uetvid=4825f220016411efb651e3531ce472ff; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Apr+26+2024+11%3A05%3A41+GMT%2B0530+(India+Standard+Time)&version=202308.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0002%3A1%2CC0004%3A1%2CBG8%3A1&AwaitingReconsent=false&geolocation=%3B',
        'Priority': 'u=0, i',
        'Referer': 'https://www.nascoeducation.com/general-kits/classroom-kits/cte.html',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    all_data = []
    soup = get_soup(url, headers)
    main_content = soup.find('nav', class_='navigation').find('ul')
    for single_content in main_content.find_all('li', class_=re.compile('level0.*?')):
        if 'Categories' in str(single_content) and 'Kits' in str(single_content):
            inner_content = single_content.find_all('li', class_=re.compile('level2.*?'))
            for main_link in inner_content:
                main_url = main_link.a['href']
                inner_request = get_soup(main_url, headers)
                '''GET PAGINATION'''
                if inner_request.find('ul', class_='items pages-items'):
                    page_nav = main_url
                    '''while loop using for page navigation'''
                    while page_nav is not None:
                        try:
                            page_link = page_nav['href']
                        except:
                            page_link = page_nav
                        print('main_page------->', page_link)
                        page_soup = get_soup(page_link, headers)
                        if page_soup is None:
                            continue
                        product_content = page_soup.find_all('div', class_='product details product-item-details')
                        for single_product in product_content:
                            '''PRODUCT URL'''
                            product_url = f"{base_url}{single_product.find('a', class_='product-item-link')['href']}"
                            print(product_url)
                            if product_url in read_log_file():
                                continue
                            product_request = get_soup(product_url, headers)
                            '''PRODUCT QUANTITY'''
                            try:
                                product_quantity = product_request.find('input', class_='input-text qty')['value']
                            except Exception as e:
                                print('product quantity:', e)
                                product_quantity = '1'
                            content = re.search('var dl4Objects.*?];', str(product_request)).group()
                            content_replace = str(content).replace('var dl4Objects = ', '').rstrip(';')
                            json_content = json.loads(content_replace)
                            for single_json_content in json_content:
                                if single_json_content['event'] == 'view_item':
                                    inside_content = single_json_content['ecommerce']['items']
                                    for inside_data in inside_content:
                                        '''PRODUCT NAME'''
                                        try:
                                            product_name = inside_data['item_name']
                                        except:
                                            product_name = ''
                                        '''PRODUCT ID'''
                                        try:
                                            product_id = inside_data['item_id']
                                        except:
                                            product_id = ''
                                        '''PRODUCT PRICE'''
                                        try:
                                            product_price = f'$ {inside_data['price']}'
                                        except:
                                            product_price = ''
                                        print('current datetime------>', datetime.now())
                                        dictionary = get_dictionary(product_ids=product_id, product_names=product_name,
                                                                    product_quantities=product_quantity,
                                                                    product_prices=product_price, product_urls=product_url)
                                        all_data.append(dictionary)
                                        write_visited_log(product_url)
                        page_nav = page_soup.find('ul', class_='items pages-items').find('a', title='Next')
                else:
                    product_content = inner_request.find_all('div', class_='product details product-item-details')
                    for single_product in product_content:
                        '''PRODUCT URL'''
                        product_url = f"{base_url}{single_product.find('a', class_='product-item-link')['href']}"
                        print(product_url)
                        if product_url in read_log_file():
                            continue
                        product_request = get_soup(product_url, headers)
                        '''PRODUCT QUANTITY'''
                        try:
                            product_quantity = product_request.find('input', class_='input-text qty')['value']
                        except Exception as e:
                            print('product quantity:', e)
                            product_quantity = '1'
                        content = re.search('var dl4Objects.*?];', str(product_request)).group()
                        content_replace = str(content).replace('var dl4Objects = ', '').rstrip(';')
                        json_content = json.loads(content_replace)
                        for single_json_content in json_content:
                            if single_json_content['event'] == 'view_item':
                                inside_content = single_json_content['ecommerce']['items']
                                for inside_data in inside_content:
                                    '''PRODUCT NAME'''
                                    try:
                                        product_name = inside_data['item_name']
                                    except:
                                        product_name = ''
                                    '''PRODUCT ID'''
                                    try:
                                        product_id = inside_data['item_id']
                                    except:
                                        product_id = ''
                                    '''PRODUCT PRICE'''
                                    try:
                                        product_price = f'$ {inside_data['price']}'
                                    except:
                                        product_price = ''
                                    print('current datetime------>', datetime.now())
                                    dictionary_1 = get_dictionary(product_ids=product_id, product_names=product_name,
                                                                product_quantities=product_quantity,
                                                                product_prices=product_price, product_urls=product_url)
                                    all_data.append(dictionary_1)
                                    write_visited_log(product_url)
    articles_df = pd.DataFrame(all_data)
    articles_df.drop_duplicates(subset=['product_id', 'product_name'], keep='first', inplace=True)
    if os.path.isfile(f'{file_name}.csv'):
        articles_df.to_csv(f'{file_name}.csv', index=False, header=False,
                           mode='a')
    else:
        articles_df.to_csv(f'{file_name}.csv', index=False)
                                    
