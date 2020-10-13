from bs4 import BeautifulSoup as bs
import requests


from PIL import Image, ImageOps, ImageDraw, ImageFont\

#decides if you want to write the context ON the image for easy reading and exporting
Context_write = True

def main(Context_write):
    url = 'https://xkcd.com/archive/'

    src = requests.get(url).text
    soup = bs(src, 'lxml')

    download_img(archive_list(soup), Context_write)


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

#this splits the context into writtable lines for the write image function
def makeMulti_lines(context):
    lines = (len(context)//60)+1
    print(lines)
    contextlist = ""
    #t is used to make sure that a \n isnt added at the start or end
    t = 0
    set1 = 0
    char = 60
    
    nextSpace = context.find(" ",char)
    if t == 0:
        contextlist = context[set1:nextSpace]+'_insert_'
        t=t+1
        set1 = set1+60
        char = char+60


    for i in range(lines):
        #splits the sentence into 60 char segments

        #t = len(contextlist)

        if char<len(context):

            nextSpace = context.find(" ",char)
            contextlist = contextlist+context[set1:nextSpace]+"_insert_"
            set1 = set1+60
            char = char+60
            #print(contextlist)
            
          
        else:
            #print((nextSpace-char))
            contextlist = contextlist +"  "+ context[char+(nextSpace-char):]
            
            #print(lines)
            
            return contextlist, lines
        

def download_img(post_list: list, Context_write):
    """
    Takes in a list of posts and then downloads the images from each of them
    using the xkcd API
    """
    
    for i in range(15): #can use this if want
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

        if Context_write == True:

            #takes the image and expands it to have some extra pixels to write text with
            pil_img = Image.open(f'ImageDownloads\\{img_num}.png')
            print(pil_img.size)
        
            img_s = pil_img.size
            img_w = img_s[0]
            img_h = img_s[1]
            

            contextSections, lines = makeMulti_lines(context) 
            print(context+'\n'+"********************************")
            #print(contextSections)
            
            contextSections = contextSections.replace("_insert_","\n")


             


            #tells how much to expand the image based on how many lines there are in the context string
            expand = lines*20
            #example of box widths
            box_height_expand = (0,0,100,expand)
            box_width_expand = (0,0,400,0)

            pil_img = ImageOps.expand(pil_img,box_height_expand)
            
            fnt = ImageFont.truetype("Piazzolla-BlackItalic-opsz=8.ttf", 10)
            write = ImageDraw.Draw(pil_img)
            write.multiline_text((10,img_h),contextSections, fill=(100,100,200), font=fnt)

            pil_img.save(f'ImageDownloads\\{img_num}.png')

        
            
   

     
    


if __name__ == '__main__':
    main(Context_write)



