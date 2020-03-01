import urllib.request
import re
import os
from pathlib import Path
import wget

def scan_url(url):
    ## Get web response ##
    t_weburl_array = []
    f_array = []
    print("Accessing URL:"+url)
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    response_string = mybytes.decode("utf8")
    response_array = response_string.split('\n')
    fp.close()

    for each_html_row in response_array:
        if "href" in each_html_row:
            file = re.findall(regex, each_html_row)[0]
            if any(symbol in ['/'] for symbol in file):
                if file not in t_weburl_array and file != '../':
                    t_weburl_array.append(url+ '/' +file)
            else:
                if file not in f_array:
                    print(file)
                    f_array.append(url+ '/' +file)
    return t_weburl_array, f_array


if __name__ == "__main__":
    ## Update Input according ##
    url = "http://xx.xxx.xxx.xxx/maximum/.git"
    remove_directory = 'http://xx.xxx.xxx.xxx'  # Split URL according for file creation

    traversable_weburl_array = []
    file_array = []
    regex = r'\"(.+?)\"'  # Start with " and end of "
    visited_url = [url]

    traversable_weburl_array, file_array = scan_url(url)
    for next_url in traversable_weburl_array:
        if next_url != url + "/../":
            if len(visited_url) != len(traversable_weburl_array) and next_url not in visited_url:
                visited_url.append(next_url)

                new_url_w_dup, new_file_w_dup = scan_url(next_url)

                if len(new_url_w_dup) > 0:
                    new_url = [item for item in new_url_w_dup if item not in traversable_weburl_array]
                    traversable_weburl_array.extend(new_url)
                if len(new_file_w_dup) > 0:
                    new_file = [item for item in new_file_w_dup if item not in file_array]
                    file_array.extend(new_file)

    path = os.getcwd()  # Current working path
    for file in visited_url:
        directory = file.split(remove_directory)[1]
        filepath = path + directory
        filepath = Path(path + directory)
        filepath.mkdir(parents=True, exist_ok=True)

    for url in file_array:
        directory = url.split(remove_directory)[1]
        filepath = path + directory
        wget.download(url, filepath)
