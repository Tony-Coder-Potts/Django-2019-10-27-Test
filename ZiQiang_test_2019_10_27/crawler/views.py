from django.shortcuts import render


# Create your views here.
def get_number(request):
    from django.http import HttpResponse
    if request.method == "POST":
        try:
            required_pieces_number = request.POST.get("required_pieces_number")
            required_pieces_number = int(required_pieces_number)
            key_word = request.POST.get("key_word")
            if required_pieces_number > 0:
                import re
                import requests
                from numpy import unicode
                from django.http import HttpResponse
                # The origin URL of the news
                url = "https://news.whu.edu.cn/wdyw.htm"
                # Build the file for saving the news
                news_contents_saving = open('News.txt', 'w', encoding="UTF-8")

                # Get the news from the main page
                response = requests.get(url)
                response.encoding = "UTF-8"
                target_website = response.text
                next_page_url_list = [url]

                # Ask for the 2nd page
                second_page_url_part_tag = re.findall(r'<a href=".*?" class="Next">下页</a>', target_website)[0]
                second_page_url_part = re.findall(r'.*?.htm', second_page_url_part_tag.replace("<a href=\"", ""))[0]
                second_page_url = "https://news.whu.edu.cn/%s" % second_page_url_part
                next_page_url_list.append(second_page_url)
                target_website_second_html = requests.get(second_page_url)
                target_website_second_html.encoding = "UTF-8"
                target_website_second = target_website_second_html.text

                # Ask for the next pages of the 2nd one
                next_page = re.findall(r'上页</a><a href=".*?.htm" class="Next">下页</a>', target_website_second)[0]
                next_page_url_part = re.findall(r'.*?.htm', next_page.replace("上页</a><a href=\"", ""))[0]
                next_page_url = "https://news.whu.edu.cn/wdyw/%s" % next_page_url_part
                next_page_url_list.append(next_page_url)

                # Using a loop to get the news title lists
                news_page_number_for_loop = 3
                while news_page_number_for_loop < required_pieces_number // 20:
                    next_page_content_get = requests.get(next_page_url)
                    next_page_content_get.encoding = "UTF-8"
                    next_page_content = next_page_content_get.text
                    next_page = re.findall(r'上页</a><a href=".*?.htm" class="Next">下页</a>', next_page_content)[0]
                    next_page_url_part = re.findall(r'.*?.htm', next_page.replace("上页</a><a href=\"", ""))[0]
                    next_page_url = "https://news.whu.edu.cn/wdyw/%s" % next_page_url_part
                    next_page_url_list.append(next_page_url)
                    news_page_number_for_loop += 1

                tag = []
                for pages_url in next_page_url_list:
                    pages_url_content = requests.get(pages_url)
                    pages_url_content.encoding = "UTF-8"
                    pages_url_content = pages_url_content.text
                    tags = str(re.findall(r'<a href=".*?" title=".*?" class="gray">', pages_url_content))
                    a_hrefs1_from_tags = re.findall(r'"(../info/.*?)"', tags)
                    more_tags = str(re.findall(r'<a href=".*?" title=".*?" class="gray">', pages_url_content))
                    a_hrefs2_from_tags = re.findall(r'"(../info/.*?)"', more_tags)
                    tag.append(a_hrefs1_from_tags)
                    tag.append(a_hrefs2_from_tags)
                while [] in tag:
                    tag.remove([])
                tag_single_list = []
                for tag_list in tag:
                    for tag_single in tag_list:
                        part_of_url = tag_single_list.append(tag_single)
                tag_needed_list = tag_single_list[0:required_pieces_number]
                print(tag_needed_list)
                news_title_list = []
                news_content_list = []
                news_list = []
                for unconfirmed_url in tag_needed_list:
                    confirmed_url = "https://news.whu.edu.cn/" + unconfirmed_url
                    print(confirmed_url)
                    news_contents_saving.write(confirmed_url)
                    news_contents_saving.write('\n')
                    news_content_html = requests.get(confirmed_url)
                    news_content_html.encoding = "UTF-8"
                    news_content_html_text = news_content_html.text
                    from bs4 import BeautifulSoup

                    soup = BeautifulSoup(news_content_html_text, 'html.parser')
                    news_title_unjusted = soup.find_all('div', 'news_title')[0]
                    news_title = unicode(news_title_unjusted.string)
                    news_title_list.append(news_title)
                    news_content_unjusted = soup.find_all('div', 'v_news_content')[0]
                    news_content_tag_list = news_content_unjusted.find_all('p')
                    news_contents_saving.write(news_title)
                    news_contents_saving.write('\n')
                    print(news_title)
                    news_content_whole = []
                    for single_tag in news_content_tag_list:
                        news_content = single_tag.text
                        news_contents_saving.write(news_content)
                        news_content_whole.append(news_content)
                    news_contents_saving.write('\n')
                    news_content_whole_str = ''.join(news_content_whole)
                    print(news_content_whole_str)
                    news_content_list.append(news_content_whole_str)
                    one_piece = news_title + news_content_whole_str
                    news_list.append(one_piece)

                if key_word != "":
                    news_matched = []
                    try:
                        for i in news_list:
                            match_news = re.findall(key_word, i)
                            if match_news:
                                news_matched.append(i)
                        return render(request, "Search_Result.html", {"result": news_matched})
                    except:
                        return HttpResponse("No match")

                else:
                    return render(request, "Crawler_Result.html", {"one_piece": news_list})
            else:
                return HttpResponse("ValueError. Check if you typed an integer from 1 to 99 please.")
        except:
            return HttpResponse("ValueError. Check if you typed an integer from 1 to 99 please.")


def home(request):
    if request.method == 'GET':
        return render(request, 'Welcome.html')


def number(request):
    return render(request, "HomePage.html")
