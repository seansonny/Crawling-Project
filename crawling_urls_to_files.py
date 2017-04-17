from bs4 import BeautifulSoup
import requests
import math


### Search
def kr_search_encoding(keyword_kr, url):
    encoded = str(keyword_kr.encode('utf-8')).replace("\\x", '%').split('%', 1)[1].split("'")[0].upper()
    encoded = url + '&query=%' + encoded
    return encoded


def page_generator(url, page_num):
    url = url + "&page=" + str(page_num)
    return url


def dom_generator(url):
    response = requests.get(url)
    dom = BeautifulSoup(response.text, "html.parser")
    return dom


def generate_post_links(dom):
    post_links = dom.findAll("a", {"class": "posting_name"})
    links = []
    for link in post_links:
        url = "https://www.jobplanet.co.kr" + link.get('href')
        links.append(url)
    return links


def total_postings(dom):
    num = dom.findAll("span", {"class": "num"})
    num_postings = []
    for n in num:
        num_postings.append(n.text)
    return int(num_postings[0])


def file_writing(list1):
    url_file = open("urls.txt", "w")
    url_file.write('\n'.join(list1))
    url_file.close()

def main():
    default_url = 'https://www.jobplanet.co.kr/job_postings/search?_rs_act=index&_rs_con=search&_rs_element=see_more_job_postings_bottom'
    # blankurl = 'https://www.jobplanet.co.kr/job_postings/search?utf8=%E2%9C%93&jp_show_search_result=true&jp_show_search_result_chk=true&order_by=score'
    data_url = kr_search_encoding("데이터", default_url)
    data_dom = dom_generator(data_url)

    ### calculate the number of pages
    links = generate_post_links(data_dom)
    postings = total_postings(data_dom)
    num_pages = math.ceil(postings / len(links))
    print("The number of pages: " + str(num_pages))

    ### generating the url of pages
    total_page_links = []
    for i in range(num_pages):
        total_page_links.append(page_generator(data_url, i + 1))

    ### total links of postings
    total_posting_links = []
    for page in total_page_links:
        total_posting_links = total_posting_links + generate_post_links(dom_generator(page))
    print("The number of postings: " + str(len(total_posting_links)))

    ### file writing to urls.txt
    file_writing(total_posting_links)

if __name__ == "__main__":
    main()