from bs4 import BeautifulSoup as bs
import requests


from PIL import Image, ImageOps, ImageDraw, ImageFont



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
    
    for i in range(2): #can use this if want
        # Adds the proper URL to get the json
        # information for each of the posts
        #gets the title of the image, and the name of the image as well
        post_list[i] += 'info.0.json'
        post_json = requests.get(post_list[i]).json()
        img_num, img_url, title_text = post_json['num'], post_json['img'], post_json['alt']
        
        
        #confimrs that it is actually downloading it
        #print(title+": "+str(img_num))

        #what is in the photo
        context = str(title_text)
        
        

        # Downloads the images and saves it as the post number(img_num) to the directory "Files"
        
        img = requests.get(img_url)
        f  = open(f'ImageDownloads\\{img_num}.png','wb')
        f.write(img.content)
        f.close()

        
        #takes the image and expands it to have some extra pixels to write text with
        pil_img = Image.open(f'ImageDownloads\\{img_num}.png')
        print(pil_img.size)

        
        img_s = pil_img.size
        img_w = img_s[0]
        img_h = img_s[1]
        


        box_height_expand = (0,0,100,100)
        box_width_expand = (0,0,400,0)
        
        
        #if img_h<img_w:
        pil_img = ImageOps.expand(pil_img,box_height_expand,)
        
        print(len(context))
        lines = len(context)//60
        contextlist = []
        for i in range(lines):
            #splits the sentence into 60 char segments
            set1 = 0
            char = 60
            contextlist.append(context[set1:char])
            set1 = set1+60
            char = char+60
            if char>len(context):
                contextlist.append(context[char-60:])
        #print(contextlist)


            
        map(lambda contextlist: i in contextlist,contextlist)


        contextHalf1 = context[:len(context)//2]
        contextHalf2 = context[len(context)//2:]
        
        write = ImageDraw.Draw(pil_img)
        write.multiline_text((10,img_h),contextHalf1+'\n'+contextHalf2, fill=(100,100,200))

        pil_img.save(f'ImageDownloads\\{img_num}.png')

        #write = Image.open(f'ImageDownloads\\{img_num}.png')
            
   

     
    


if __name__ == '__main__':
    main()
