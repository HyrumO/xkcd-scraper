from bs4 import BeautifulSoup as bs
import requests

import os
directoryPath = "Files"




def main():
    url = 'https://xkcd.com/archive/'

    src = requests.get(url).text
    soup = bs(src, 'lxml')

    download_img(archive_list(soup))


def archive_list(soup_obj) -> list:
    """
    Gets a list of URLs of all of the XKCD comics

    Takes in a 'Beautiful Soup' object

    Returns all the post URLs
    """

    # Gets all the URLs from the archive table
    archive = soup_obj.find('body').find('div', id='middleContainer')
    archive = archive.find_all('a')

    base_url = 'https://www.xkcd.com'
    # Adds the main page URL to the obtained URL ending
    # eg. 'https://www.xkcd.com' + '/124/'
    archive_links = list(base_url + post['href'] for post in archive)

    return archive_links


def download_img(post_list: list):
    """
    Takes in a list of posts and then downloads the images from each of them
    using the xkcd API
    """

    for i in range(len(post_list)):
        # Adds the proper URL to get the json
        # information for each of the posts
        post_list[i] += 'info.0.json'
        post_json = requests.get(post_list[i]).json()
        img_num, img_url = post_json['num'], post_json['img']
        title = post_json['title']
        
        #confimrs that it is actually downloading it
        print(title+": "+str(img_num))
        
        # Downloads the images and saves it as the post number(img_num) to the directory "Files"
        img = requests.get(img_url)
        f  = open(f'ImageDownloads\\{img_num}.png','wb')
        f.write(img.content)
        f.close()

        

        



     
    


if __name__ == '__main__':
    main()
