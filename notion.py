import yuag
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def changeURL_prarameter_value(url: str, parameter: str, value: str):
    # قم بتحليل الرابط
    parsed_url = urlparse(url)

    # استخراج المعلومات
    query_params = parse_qs(parsed_url.query)

    # قم بتحديث قيمة width إلى 250
    query_params[parameter] = [value]

    # قم بتجميع معلومات الاستعلام
    updated_query = urlencode(query_params, doseq=True)

    # قم بإعادة تجميع الرابط مع التحديثات
    updated_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query, parsed_url.fragment))

    return updated_url

# soup.find_all(recursive=False) # important

# text ==> .notranslate
# is_check ==> [style="position: relative; flex-shrink: 0; flex-grow: 0; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; transition: background 200ms ease-out 0s; --pseudoHover--background: rgba(55,53,47,.08); --pseudoActive--background: rgba(55,53,47,.16); background: rgb(35, 131, 226);"]
def get_pages_elements(): return ".layout .notion-page-block"
def get_h_elements(): return ".layout h2, .layout h3, .layout h4"
def get_text_elements(): return ".layout .notion-text-block"
def get_bulletted_elements(): return ".layout .notion-bulleted_list-block[style][data-block-id]"
def get_numbered_elements(): return ".layout .notion-numbered_list-block[style][data-block-id]"
def get_todo_elements(): return ".layout .notion-to_do-block[style][data-block-id]"
def get_image_elements(): return ".layout .notion-image-block[style][data-block-id]"
def get_code_elements(): return ".layout .notion-code-block[style][data-block-id]"
def get_quote_elements(): return ".layout .notion-quote-block[style][data-block-id]"
def get_database_elements(): return ".layout .notion-collection_view-block[style][data-block-id]"

def get_elements(elements, is_res_arr = 0, res_arr = []):
    print("########")
    res = []
    if is_res_arr == 1:
        res = res_arr
    
    for i, item in enumerate(elements):
        # set item_tag ==> h1, text, ...
        item_tag = ""
        if "notion-page-block" in item.get("class", []): # page element
            item_tag = "page"
        elif "notion-header-block" in item.get("class", []) or item.name in ["h2", "h3", "h4"]: # h element
            if "notion-header-block" in item.get("class", []):
                item = item.select("h2, h3, h4")[0]

            item_tag = f"h{yuag.decodeNum(item.name)[1] - 1}"
        elif "notion-text-block" in item.get("class", []): # text element
            item_tag = "text"
        elif "notion-bulleted_list-block" in item.get("class", []): # bulleted element
            item_tag = "bulleted"
        elif "notion-numbered_list-block" in item.get("class", []): # numbered element
            item_tag = "numbered"
        elif "notion-to_do-block" in item.get("class", []): # todo element
            item_tag = "todo"
        elif "notion-image-block" in item.get("class", []): # image element
            item_tag = "image"
        elif "notion-code-block" in item.get("class", []): # code element
            item_tag = "code"
        elif "notion-quote-block" in item.get("class", []): # quote element
            item_tag = "quote"
        elif "notion-collection_view-block" in item.get("class", []): # quote element
            item_tag = "database"
        elif "notion-column_list-block" in item.get("class", []): # column element
            item_tag = "column"

        # add item to page's data
        if item_tag != "":
            print(item_tag)
            print("###")
            # add item data
            if (item_tag == "page" and len(item.select("a")) == 0) == False:
                if item_tag not in ["page", "code", "column"]: res.append({"item": item_tag})                
                
                if item_tag in ["h1", "h2", "h3"]:
                    res[-1]["value"] = yuag.innerHTML(item)
                elif item_tag in ["text", "bulleted", "numbered"]:
                    if item_tag == "numbered":
                        res[-1]["number"] = yuag.re.search(r'--pseudoBefore--content:\s*["\']([^"\']*)["\']', item.get("style", "")).group(1)

                    try:
                        res[-1]["value"] = yuag.innerHTML(item.select(".notranslate")[0])
                    except:
                        res[-1]["value"] = yuag.innerText(item)
                        # print("fix:")
                        # print(yuag.innerHTML(item))
                        # print(str(item))
                elif item_tag == "todo":
                    res[-1]["value"] = yuag.innerHTML(item.select(".notranslate")[0])
                    if len(item.select('[style="position: relative; flex-shrink: 0; flex-grow: 0; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; transition: background 200ms ease-out 0s; --pseudoHover--background: rgba(55,53,47,.08); --pseudoActive--background: rgba(55,53,47,.16); background: rgb(35, 131, 226);"]')) == 0:
                        res[-1]["checked"] = True
                    else:
                        res[-1]["checked"] = False
                elif item_tag == "image":
                    res[-1]["url"] = "https://www.notion.so" + item.select("img")[0].get("src")
                elif item_tag == "code":
                    try:
                        res.append({"item": item_tag})
                        res[-1]["language"] = item.select("[role=button]")[0].text
                        res[-1]["code"] = item.select(".notranslate")[0].text
                    except:
                        print(yuag.innerHTML(item))
                        print(str(item))
                elif item_tag == "quote":
                    res[-1]["value"] = yuag.innerHTML(item.select(".notranslate")[0])
                elif item_tag == "database":
                    for table in soup.select(get_database_elements()):
                        # headers
                        res[-1]["headers"] = []
                        header_items = table.select('.notion-table-view-header-row div[style="display: inline-flex; margin: 0px;"] div[style="display: flex; flex-direction: row;"]')
                        for header_item in header_items:
                            header_item_type = header_item.select("svg")[0].get("class", [])[0]
                            header_item_value = header_item.select('div[style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"]')[0].text
                            
                            res[-1]["headers"].append({})
                            res[-1]["headers"][-1]["type"] = header_item_type
                            res[-1]["headers"][-1]["value"] = header_item_value
                    
                        # values
                        res[-1]["values"] = []
                        rows = table.select(".notion-table-view-row")
                        for row in rows:
                            row_data = []
                            cells = row.select(".notion-table-view-cell")
                            for cell in cells:
                                row_data.append(yuag.innerHTML(cell.select("div div")))
                            
                            res[-1]["values"].append(row_data)
                elif item_tag == "column":
                    res.append({"item": item_tag, "columns": []})

                    tmp_columns = []
                    columns = item.select("[style=\"padding-top: 12px; padding-bottom: 12px; flex-grow: 0; flex-shrink: 0; width: calc(50% - 23px);\"]")
                    for column in columns:
                        column_items = column.select("div")[0].find_all(recursive=False)
                        tmp_append = get_elements(column_items)
                        tmp_columns.append(tmp_append)
                        
                        res[-1]["columns"] = tmp_columns
                    
                    res[-1]["columns"] = tmp_columns
                elif item_tag == "page":
                    tmp_page_link = "https://www.notion.so" + item.select("a")[0].get("href")
                    
                    res.append({"item": item_tag, "value": item.text})
                    res[-1]["link"] = tmp_page_link
                    res[-1]["items"] = []

            yuag.saveJson(output_data, "result.json")
            yuag.wait(1)
            print(999999999)

    # sub pages
    for i, item in enumerate(res):
        if item["item"] == "page":
            yuag.wait(2)
            driver.get(item["link"])
            # item.pop("link") # delete link key ==> { "item": "page", "value": "page 1", "link": "the link" }
            yuag.wait(1)
            item = get_page_data(driver, item)

            yuag.saveJson(output_data, "result.json")

    return res

def get_page_data(driver, page, manual = 0):
    page = yuag.equalObject(page, 1000)
    soup = yuag.driverToSoup(driver)
    
    # get elements
    pages_elements = get_pages_elements()
    h_elements = get_h_elements()
    text_elements = get_text_elements()
    bulletted_elements = get_bulletted_elements()
    numbered_elements = get_numbered_elements()
    todo_elements = get_todo_elements()
    image_elements = get_image_elements()
    code_elements = get_code_elements()
    quote_elements = get_quote_elements()
    database_elements = get_database_elements()

    if manual != 0:
        yuag.clear()
        input("when page fully load press any key: ")
    
    while len(soup.select(pages_elements)) == 0: # wait until page load
        yuag.wait(1)
        soup = yuag.driverToSoup(driver)
    
    if len(soup.select(database_elements)) > 0: # wait until database load
        yuag.clear()
        input("if database fully load press any key: ")

    # all = soup.select(all_elements)
    all = soup.select(".notion-page-content")[0].find_all(recursive=False)
    page["items"] = get_elements(all, 1, page["items"])
    # for i, item in enumerate(all):
    #     # set item_tag ==> h1, text, ...
    #     item_tag = ""
    #     if ("notion-page-block" in item.get("class", [])) and (i > 0): # page element
    #         item_tag = "page"
    #     elif item.name in ["h2", "h3", "h4"]: # h element
    #         item_tag = f"h{yuag.decodeNum(item.name)[1] - 1}"
    #     elif "notion-text-block" in item.get("class", []): # text element
    #         item_tag = "text"
    #     elif "notion-bulleted_list-block" in item.get("class", []): # bulleted element
    #         item_tag = "bulleted"
    #     elif "notion-numbered_list-block" in item.get("class", []): # numbered element
    #         item_tag = "numbered"
    #     elif "notion-to_do-block" in item.get("class", []): # todo element
    #         item_tag = "todo"
    #     elif "notion-image-block" in item.get("class", []): # image element
    #         item_tag = "image"
    #     elif "notion-code-block" in item.get("class", []): # code element
    #         item_tag = "code"
    #     elif "notion-quote-block" in item.get("class", []): # quote element
    #         item_tag = "quote"
    #     elif "notion-collection_view-block" in item.get("class", []): # quote element
    #         item_tag = "database"
    #     elif "notion-column_list-block" in item.get("class", []): # column element
    #         item_tag = "column"


    #     # add item to page's data
    #     if item_tag != "":
    #         # add item data
    #         if (item_tag == "page" and len(item.select("a")) == 0) == False:
    #             if item_tag not in ["page", "code", "column"]: page["items"].append({"item": item_tag})                
                
    #             if item_tag in ["h1", "h2", "h3"]:
    #                 page["items"][-1]["value"] = yuag.innerHTML(item)
    #             elif item_tag in ["text", "bulleted", "numbered"]:
    #                 if item_tag == "numbered":
    #                     page["items"][-1]["number"] = yuag.re.search(r'--pseudoBefore--content:\s*["\']([^"\']*)["\']', item.get("style", "")).group(1)

    #                 try:
    #                     page["items"][-1]["value"] = yuag.innerHTML(item.select(".notranslate")[0])
    #                 except:
    #                     print(yuag.innerHTML(item))
    #                     print(str(item))
    #             elif item_tag == "todo":
    #                 page["items"][-1]["value"] = yuag.innerHTML(item.select(".notranslate")[0])
    #                 if len(item.select('[style="position: relative; flex-shrink: 0; flex-grow: 0; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; transition: background 200ms ease-out 0s; --pseudoHover--background: rgba(55,53,47,.08); --pseudoActive--background: rgba(55,53,47,.16); background: rgb(35, 131, 226);"]')) == 0:
    #                     page["items"][-1]["checked"] = True
    #                 else:
    #                     page["items"][-1]["checked"] = False
    #             elif item_tag == "image":
    #                 page["items"][-1]["url"] = "https://www.notion.so" + item.select("img")[0].get("src")
    #             elif item_tag == "code":
    #                 try:
    #                     page["items"].append({"item": item_tag})
    #                     page["items"][-1]["language"] = item.select("[role=button]")[0].text
    #                     page["items"][-1]["code"] = item.select(".notranslate")[0].text
    #                 except:
    #                     print(yuag.innerHTML(item))
    #                     print(str(item))
    #             elif item_tag == "quote":
    #                 page["items"][-1]["value"] = yuag.innerHTML(item.select(".notranslate")[0])
    #             elif item_tag == "database":
    #                 for table in soup.select(database_elements):
    #                     # headers
    #                     page["items"][-1]["headers"] = []
    #                     header_items = table.select('.notion-table-view-header-row div[style="display: inline-flex; margin: 0px;"] div[style="display: flex; flex-direction: row;"]')
    #                     for header_item in header_items:
    #                         header_item_type = header_item.select("svg")[0].get("class", [])[0]
    #                         header_item_value = header_item.select('div[style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"]')[0].text
                            
    #                         page["items"][-1]["headers"].append({})
    #                         page["items"][-1]["headers"][-1]["type"] = header_item_type
    #                         page["items"][-1]["headers"][-1]["value"] = header_item_value
                    
    #                     # values
    #                     page["items"][-1]["values"] = []
    #                     rows = table.select(".notion-table-view-row")
    #                     for row in rows:
    #                         row_data = []
    #                         cells = row.select(".notion-table-view-cell")
    #                         for cell in cells:
    #                             row_data.append(yuag.innerHTML(cell.select("div div")))
                            
    #                         page["items"][-1]["values"].append(row_data)
    #             elif item_tag == "column":
    #                 page["items"].append({"item": item_tag, "columns": []})

    #                 tmp_columns = []
    #                 columns = item.select("div div [style=\"padding-top: 12px; padding-bottom: 12px; flex-grow: 0; flex-shrink: 0; width: calc(50% - 23px);\"]")
    #                 for column in columns:
    #                     column_items = column.select("div")[0].find_all(recursive=False)
    #                     tmp_columns.append(get_elements(column_items))
                    
    #                 page["items"][-1]["columns"] = tmp_columns
    #                 print(9999)
    #                 yuag.wait(2)
    #             elif item_tag == "page":
    #                 tmp_page_link = "https://www.notion.so" + item.select("a")[0].get("href")
                    
    #                 page["items"].append({"item": item_tag, "value": item.text})
    #                 page["items"][-1]["link"] = tmp_page_link
    #                 page["items"][-1]["items"] = []

    #     yuag.saveJson(output_data, "result.json")
    
    # sub pages
    # for i, item in enumerate(page["items"]):
    #     if item["item"] == "page":
    #         yuag.wait(2)
    #         driver.get(item["link"])
    #         # item.pop("link") # delete link key ==> { "item": "page", "value": "page 1", "link": "the link" }
    #         yuag.wait(1)
    #         item = get_page_data(driver, item)

    #         yuag.saveJson(output_data, "result.json")

    return page



output_data = {}
output_data["pages"] = []

driver = yuag.makeFirefoxDriver()
# driver.get("https://www.notion.so/login")
# driver.get("https://yusufasagiba.notion.site/yusufasagiba/038b53549b894ac99b461247b07fa244")
driver.get("https://yusufasagiba.notion.site/yusufasagiba/asdf-29f4baf795ee4722b693f36858b181b8")

yuag.clear()
waiting = input("when logged in press any key: ")
soup = yuag.driverToSoup(driver)

page_name = soup.select(get_pages_elements())[0].text
output_data["pages"].append({"item": "page", "value": page_name, "items": []})
output_data["pages"][-1] = get_page_data(driver, output_data["pages"][-1]) # driver.current_url)

yuag.saveJson(output_data, "result.json")