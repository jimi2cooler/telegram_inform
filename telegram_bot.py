import requests
from bs4 import BeautifulSoup
import pandas as pd
import telegram as tel
import os, time

def crawling_fsc() : # 금융위원회 보도자료 Crawling
    url_fsc = 'https://www.fsc.go.kr/no010101'
    soup = BeautifulSoup(requests.get(url_fsc).text, 'html.parser')

    board_list = soup.find_all('div', {'class' : 'board-list-wrap'})[0]
    inner_list = board_list.find_all('div', {'class' : 'inner'})

    fsc_lst = []

    for tag in inner_list :
        title_tag = tag.find('div', {'class' : 'subject'})
        title = title_tag.find('a')['title']
        href_tag = 'https://www.fsc.go.kr/' + title_tag.find('a')['href']
        id = href_tag.split('/')[-1].split('?')[0]

        date_reg = tag.find('div', {'class' : 'day'}).get_text()

        info_tag = tag.find('div', {'class' : 'info'})
        incharge_dep = info_tag.find_all('span')[0].get_text().split(':')[-1].strip()

        temp_lst = ['fsc', id, title, href_tag, incharge_dep, date_reg]
        fsc_lst.append(temp_lst)

    df_fsc = pd.DataFrame(fsc_lst, columns = ['org_name', 'id', 'title', 'href', 'incharge', 'date'])
    return df_fsc


def crawling_fss() : # 금융감독원 보도자료 Crawling
    fss_board_url = r'https://www.fss.or.kr/fss/bbs/B0000188/list.do?menuNo=200218&bbsId=&cl1Cd=&pageIndex=1&sdate=&edate=&searchCnd=1&searchWrd='
    soup_fss = BeautifulSoup(requests.get(fss_board_url).text, 'html.parser')

    fss_lst = []

    board_tag = soup_fss.find('div', {"class" : "bd-list"})
    board_lst_tags = board_tag.find_all('tr')
    for tr_tag in board_lst_tags[1:] :
        td_tag_lst = tr_tag.find_all('td')

        title_fss = td_tag_lst[1].get_text()
        href_fss = td_tag_lst[1].find('a')['href']
        id_fss = href_fss.split('/')[-1].split('&')[0].split('=')[-1]
        in_charge_fss = td_tag_lst[2].get_text().strip()
        date_fss = td_tag_lst[3].get_text().strip()
        temp_lst = ['fss', id_fss, title_fss, r'https://www.fss.or.kr'+ href_fss, in_charge_fss, date_fss ]
        fss_lst.append(temp_lst)

    df_fss = pd.DataFrame(fss_lst, columns = ['org_name', 'id', 'title', 'href', 'incharge', 'date'])
    return df_fss

def crawling_bok() :
# 한국은행 보도자료

    bok_board_url = r'https://www.bok.or.kr/portal/bbs/P0000559/list.do?menuNo=200690'
    soup_bok = BeautifulSoup(requests.get(bok_board_url).text, 'html.parser')

    bok_lst = []

    bok_board_tag = soup_bok.find('div', {"class" : "bdLine type2"})
    bok_board_lst_tags = bok_board_tag.find_all('div', {"class" : "row"})
    for i, div_tag in enumerate(bok_board_lst_tags) :
        if i % 2 == 0 :
            temp_lst = []
            a_tag_lst = div_tag.find_all('a')[0] # 첫번째 a tag 가져와서

            title_bok = a_tag_lst.find('span', {'class' : 'titlesub'}).get_text()
            href_bok = a_tag_lst['href']

            id_bok = href_bok.split('/')[-1].split('&')[0].split('=')[-1]
            in_charge_bok = ""
            temp_lst = ['bok', id_bok, title_bok, r'https://www.bok.or.kr'+ href_bok, in_charge_bok]
            
        else : 
            date_bok = div_tag.find('span', {'class' : 'date'}).get_text().replace('등록일', '').replace('.', '-')
            temp_lst.append(date_bok)
            bok_lst.append(temp_lst)

    df_bok = pd.DataFrame(bok_lst, columns = ['org_name', 'id', 'title', 'href', 'incharge', 'date'])
    return df_bok


def crawling_bok_blog() : # 한국은행 Blog

    bok_blog_url = r'https://www.bok.or.kr/portal/bbs/B0000347/list.do?menuNo=201106'
    soup_bok_blog = BeautifulSoup(requests.get(bok_blog_url).text, 'html.parser')

    bok_blog_lst = []

    bok_blog_tag = soup_bok_blog.find('div', {"class" : "photoList vertical"})
    bok_blog_lst_tags = bok_blog_tag.find_all('li')

    for li_tag in bok_blog_lst_tags :
            
        href_bok_blog = li_tag.find('a')['href']
        div_tag_lst = li_tag.find('div', {"class" : "imgDesc"})

        title_bok_blog = div_tag_lst.find('span', {'class' : 'title'}).get_text()

        id_bok_blog = href_bok_blog.split('/')[-1].split('&')[0].split('=')[-1]
        in_charge_bok_blog = ""
        date_bok_blog = div_tag_lst.find('span', {'class' : 'date fl'}).get_text().split(':')[-1].replace('.', '-')

        temp_lst = ['bok_blog', id_bok_blog, title_bok_blog, r'https://www.bok.or.kr'+ href_bok_blog, in_charge_bok_blog, date_bok_blog]
        bok_blog_lst.append(temp_lst)

    df_bok_blog = pd.DataFrame(bok_blog_lst, columns = ['org_name', 'id', 'title', 'href', 'incharge', 'date'])
    return df_bok_blog


def send_message(new_df) :

    bot = tel.Bot(token="***********")
    chat_id = ***********
    new_df = new_df.reset_index()

    for k, v in new_df.iterrows() :
        if v['org_name'] == 'fsc' :
            msg = "<b>[금융위원회]</b>\n"
        elif v['org_name'] == 'fss' :
            msg = "<b>[금융감독원]</b>\n"
        elif v['org_name'] == 'bok' :
            msg = "<b>[한국은행]</b>\n"
        elif v['org_name'] == 'bok_blog' :
            msg = "<b>[한국은행 블로그]</b>\n"
        
        msg = msg + f"<a>{v['title']} / {v['date']}</a>\n" 
        msg = msg + f"{v['href']}"
        bot.sendMessage(chat_id=chat_id, text=msg, parse_mode='html') # 메세지 보내기
        time.sleep(3)


def main() :
    
    df_fsc = crawling_fsc()
    df_fss = crawling_fss()
    df_bok = crawling_bok()
    
    df_bok_blog = crawling_bok_blog()

    df_refresh = pd.concat([df_fsc, df_fss, df_bok, df_bok_blog], axis = 0).reset_index(drop=True)
    
    df_refresh = df_refresh.set_index(['org_name', 'id'])
    
    pkl_path = r'./board_list.pkl'

    if os.path.isfile(pkl_path) :
        existing_df = pd.read_pickle(pkl_path)
    else :
        df_temp = pd.DataFrame(columns = ['org_name', 'id', 'title', 'href', 'incharge', 'date'])
        df_temp = df_temp.set_index(['org_name', 'id'])
        df_temp.to_pickle(pkl_path)

    new_index = df_refresh.index.difference(existing_df.index)
    new_matching_df = df_refresh[df_refresh.index.isin(new_index)]
    
    if len(new_matching_df) > 0 :
        send_message(new_matching_df)
        update_df = pd.concat([existing_df, new_matching_df], axis=0)
        update_df.to_pickle(pkl_path)
        quit
    else : quit

if __name__ == "__main__" :
    main()






