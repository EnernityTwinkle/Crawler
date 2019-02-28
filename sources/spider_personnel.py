import sys

from imp import reload
reload(sys)

# sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import urllib
import requests, re, time


def get_html(url):                      #得到网址为url的网页内容，格式为bytes
    html = requests.get(url).content
    return html


def get_links(soup):                                                #得到需要的所有网址
    # tag1 = soup.find('h1')
    # print(type(tag1))
    # if (tag1.get_text() == '404 Not Found'):
    #     print('网页出错')
    #     return
    href_dic = {}
    count = 0
    fin_tab_1 = soup.find('div', class_=re.compile('clearfix w1000 p2j_con01'))   #得到title mtl5标签内容
    fin_tab_1 = fin_tab_1.find('div', class_=re.compile('fl'))
    # print(fin_tab_1)
    # print(type(fin_tab_1))
    # print(fin_tab_1)
    if fin_tab_1:
        for link in fin_tab_1.find_all('a'):
            # print(link)
            pure_link = link.get('href')                    #得到href的值
            # print(pure_link)
            if pure_link is not None:
                if 'http' in pure_link:
                    href_dic[pure_link] = count
                    count += 1
                elif(pure_link[0] == '/'):
                    href_dic['http://renshi.people.com.cn' + pure_link] = count
                    count += 1

    # fin_tab_2 = soup.find('div', class_=re.compile('p1_content w1000'))
    # if fin_tab_2:
    #     for link in fin_tab_2.find_all('a'):
    #         pure_link = link.get('href')            # 得到所有href的值
    #         # print(pure_link)
    #         if pure_link is not None:
    #             if 'http' in pure_link:
    #                 # print("http:")
    #                 # print(pure_link)
    #                 href.append(pure_link)
    #             else:
    #                 # print(pure_link)
    #                 href.append('http://finance.people.com.cn' + pure_link)
    # fin_tab_3 = soup.find('div', class_=re.compile('w1000 tbtj_box clearfix'))
    # if fin_tab_3:
    #     for link in fin_tab_3.find_all('a'):
    #         # print(link)
    #         pure_link = link.get('href')
    #         # print(pure_link)
    #         if pure_link is not None:
    #             # print(type(pure_link))
    #             # print(pure_link)
    #             if 'http' in pure_link:
    #                 pass
    #             else:
    #                 pure_link = 'http://finance.people.com.cn' + pure_link
    #         if pure_link:
    #             pure_link = pure_link.replace('\t', '').replace('\n', '')
    #         if pure_link not in href:
    #             href.append(pure_link)
    # fin_tab_4 = soup.find('div', class_=re.compile('img_list1 clearfix'))
    # if fin_tab_4:
    #     for link in fin_tab_4.find_all('a'):
    #         pure_link = link.get('href')
    #         # print(pure_link)
    #         if pure_link is not None:
    #             if 'http' in pure_link:
    #                 pass
    #             else:
    #                 pure_link = 'http://finance.people.com.cn' + pure_link
    #         if pure_link:
    #             pure_link = pure_link.replace('\t', '').replace('\n', '')
    #         if pure_link not in href:
    #             href.append(pure_link)
    # fin_tab_5 = soup.find('div', class_=re.compile('w1000 mt20 column_2 p9_con'))
    # if fin_tab_5:
    #     for link in fin_tab_5.find_all('a'):
    #         pure_link = link.get('href')
    #         # print(pure_link)
    #         if pure_link is not None:
    #             if 'http' in pure_link:
    #                 pass
    #             else:
    #                 pure_link = 'http://finance.people.com.cn' + pure_link
    #         if pure_link:
    #             pure_link = pure_link.replace('\t', '').replace('\n', '')
    #         if pure_link not in href:
    #             href.append(pure_link)
    #
    #             # print(pure_link)
    # href_list = sorted(href_dic.items(), key=lambda x:x[1], reverse=False)
    href_list = []
    for key in href_dic:
        href_list.append(key)
    return href_list


def get_text(soup, out):
    tag = soup.find('h1')
    tag_time = soup.select('body > div.p2j_con03.clearfix.w1000 > div.text_con.text_con01 > div > p.sou')
    # print(type(soup))
    # print(tag_time)

    tag_1 = soup.find('div', class_=re.compile('show_text'))
    # print(type(tag_1))
    # print('tag1', tag_1)
    tag_2 = soup.find('div', class_=re.compile('edit'))
    if tag.get_text() == '404 Not Found':
        print('网页出错')
        return 0
    if tag and (tag_1):
        out.write('<title>' + tag.get_text() + '\n')
        # print('<title>' + tag.get_text())
    for i in tag_time:
        # print(type(i))
        out.write(i.getText() + '\n')
        # print('tag_time', i.getText())
    if tag_1:
        for t in tag_1.find_all('p'):
            # fout.write(t.get_text())
            text = t.get_text()
            if(text.strip('\n') == u"相关新闻"):
                break
            if text is not '\n' and len(text) > 1:
                out.write(text.strip('\n') + '\n')
                # print(text.strip('\n'))

    if tag_2:
        text = tag_2.get_text()
        if text is not '\n':
            out.write(text.strip('\n') + '\n')
            # print(text.strip('\n'))
    return 1

def get_all_text(link_list, fout):

    for url in link_list:
        try:
            fout.write('url:')
            fout.write(url + '\n')
            print('url:', url)
            html_doc = get_html(url)
            import chardet
            # content = urllib2.urlopen(req).read()
            typeEncode = sys.getfilesystemencoding()  ##系统默认编码
            infoencode = chardet.detect(html_doc).get('encoding', 'utf-8')  ##通过第3方模块来自动提取网页的编码
            html_doc = html_doc.decode(infoencode, 'ignore').encode(typeEncode)  ##先转换成unicode编码，然后转换系统编码输出
            soup = BeautifulSoup(html_doc, 'html.parser')
            err = get_text(soup, fout)
            if err == 0:
                return 0
            # print('\n')
        except:
            pass

    return 1

i = 1
start = time.time()
sum = 0
out_file = './text_data'
fout = open(out_file, 'w', encoding='utf-8')
while(i):
    url = 'http://renshi.people.com.cn/index' + str(i) + '.html'
    i += 1
    print('source:', url)
    html_doc = get_html(url)                                 #得到网页内容，格式为bytes
    # print(type(html_doc))
    # print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')           #得到网页内容，格式为bs4.BeautifulSoup
    # print(type(soup))
    # print(soup)
    # tag1 = soup.find('h1')
    # print(type(tag1))
    # if(tag1.get_text() == '404 Not Found'):
    #     print('网页出错')
    #     break
    link_list = get_links(soup)
    print(type(link_list))
    print(link_list)
    print('link_list:', len(link_list))
    sum += len(link_list)
    print('sum:',sum)

    # out_file = './text_data'
    # fout = open(out_file, 'w+')

    get_all_text(link_list, fout)
fout.close()
end = time.time()
print('the code took %s (s)' % int(end - start))
print('sum:', sum)

# print(len(link_list))
