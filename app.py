from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler , MessageHandler, Filters, CallbackContext
import requests
from bs4 import BeautifulSoup
import json
#########################################################################################################################
class Bot :
    token = '6463578757:AAF0asPmgajFPpt43mNnN8elM6FP253NstU'

    start_text = """ 
🎬 Welcome to *MovieMash*! 🌟

Embark on a cinematic journey like never before with MovieMash, your ultimate destination for a seamless anime-watching experience! 🍿✨ Immerse yourself in a world of captivating stories, breathtaking animation, and endless entertainment.

🚀 Why *MovieMash*?

- **All-in-One Hub:** Explore a vast collection of anime from various genres, conveniently housed under one roof.

- **User-Friendly Interface:** Navigate effortlessly through our sleek and intuitive interface designed for your viewing pleasure.

- **High-Quality Streaming:** Enjoy crystal-clear streaming and indulge in the magic of your favorite anime with stunning visuals and crisp audio.

- **Discover New Gems:** Uncover hidden treasures and discover new anime titles that will keep you hooked from the first episode.

Join our community of anime enthusiasts and let *MovieMash* be your go-to destination for an unforgettable anime-watching experience! 🌈✨ Start streaming now and let the adventure unfold! 🎉🍿
"""
    instruction = """
🍿 **Introduction** 🌟

To embark on your anime adventure, use the following commands:

1. **Search for an Anime:** `search@ anime_name` - Discover new anime gems.

2. **Get Anime Content:** `content@ anime_name` - Dive into the details of your favorite anime.

3. **List Episodes:** `episode@ anime_name` - Explore the number of episodes.

4. **Episode Details:** `episode@ number` - Get info on a specific episode.

5. **Press Watch:** `press watch` - Start streaming your selected anime.

6. **Press Download:** `press download` - Download content for offline enjoyment.

Join the *MovieMash* community and let the anime magic unfold! 🌈✨🎉


    """
    nothing_found = """
🍿 **Oops! Nothing Found** 🌟

It seems that we couldn't find any information matching your search. 🤔

Please try another search term or explore the wide variety of anime available on *MovieMash*! 🌈✨

Feel free to use the following commands:
- To search for an anime: `search@ anime_name`
- To explore the collection: `content@ anime_name`

Happy anime hunting! 🍿🕵️‍♂️

"""
    

def get_webpage_data(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the data you need from the HTML
            # Here, we're just printing the entire HTML content for demonstration purposes
            data = str(soup.prettify())

            data = json.loads(data)

            return data

        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        pass

def data_text_search(data,update):
    for index, anime_info in data.items():
        msg = f"""
🍿 **Anime Info** 🌟

------------------------------
*Title:* {anime_info['Title']}
*Episode:* {anime_info['Episode']}
*Image Source:* [View Image]({anime_info['Img_Src']})
*Anime URL:* content@ {anime_info['Anime_Url']}
*Release Date:* {anime_info['Released_date']}
------------------------------
"""
        url = f"content@ {anime_info['Anime_Url']}"
        update.message.reply_text(msg, parse_mode='Markdown', disable_web_page_preview=True)

        keyboard = [[InlineKeyboardButton(url, callback_data=url)],]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Hello! Click the button below:', reply_markup=reply_markup)


def data_text_content(data):
    msg = f"""
🍿 **Anime Details** 🌟

*Title:* {data['Title']}
*Genre:* {data['Genre']}
*Type:* {data['Type']}
*Status:* {data['Status']}
*Total No. Of Episodes:* {data['Total No. Of Episode']}
*Other Name:* {data['Other Name']}
*Released:* {data['Released']}
*Plot Summary:* {data['Plot Summary']}
*Anime Image:* [Click to View Image]({data['Img_Src']})


"""
    return msg
########################################################################################################################################

TOKEN =  '6463578757:AAF0asPmgajFPpt43mNnN8elM6FP253NstU'

Watch_url = ""
Download_url = ""

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(Bot.start_text)
    update.message.reply_text(Bot.instruction)

def echo(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    update.message.reply_text(str(update.message.text))

    if "search@" in url or "Search@" in url or "SEARCH@" in url:
        update.message.reply_text(str("Searching..."))
        try:
            url = str(url[7:])
            data = get_webpage_data(f"https://animeweeb.onrender.com/get-user/Search/{url}/Data")
            data_text_search(data,update)
        except:
            update.message.reply_text(Bot.nothing_found)

    else:
        try:
            update.message.reply_text(str("Searching..."))
            data = get_webpage_data(f"https://animeweeb.onrender.com/get-user/Search/{url}/Data")
            data_text_search(data,update)
        except:
            update.message.reply_text(Bot.nothing_found)




def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    print("Returned query from button press:",query.data)
    if "content@ " in query.data:
        url = query.data.replace("content@ ", "")
        
        # Fetch data from the webpage
        data = get_webpage_data(f"https://animeweeb.onrender.com/get-user/Content/{url}/Data")
        
        # Process and format the data
        formatted_data = data_text_content(data)
        
        # Edit the callback_query message with the fetched and formatted data
        query.message.reply_text(text=formatted_data)
        
        # Check if the original message is present before replying
        episode = data['Total No. Of Episode']
        episode = episode.replace("Episode:","")
        episode = url + "Episode@ "   + episode
        if query.message:
            # Add a new button with the original URL
            keyboard = [[InlineKeyboardButton("Episode@", callback_data = episode )],]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send a new message with the button
            query.message.reply_text('Hello! Click the button below:', reply_markup=reply_markup)
        
    elif "Episode@ " in query.data:
        word = query.data
        index = word.find("Episode@ ")
        url = word[ :index]
        episode = word[index:]
        episode = episode.replace("Episode@ ", "")

    
               
        if query.message:
            # Add a new button with the original URL

            for index_ in range(1 , int(episode) + 1 ):
                keyboard = [[InlineKeyboardButton(f"Episode@  {index_}", callback_data = "get-user/Player/" + url + "-episode-" + str(index_) + "/Data" )],]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                # Send a new message with the button
                query.message.reply_text('Hello! Click the button below:', reply_markup=reply_markup)
           
        

    elif "-episode-" in query.data:
        anime_info = get_webpage_data("https://animeweeb.onrender.com/" + query.data)

        if anime_info:
            Watch_url = anime_info.get("Video Player Link", "")
            Download_url = anime_info.get("Download URL", "")
            
            
            

            if query.message and Watch_url and Download_url:
                keyboard = [[InlineKeyboardButton("Watch", url = Watch_url)],[InlineKeyboardButton("Download", url = Download_url)]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.message.reply_text('Choose an option:', reply_markup=reply_markup)
            else:
                print("Error: Invalid URLs or message missing.")
        else:
            print("Error: Failed to fetch anime information.")

           
    elif "Watch:Player" in query.data or "Download:Player" in query.data:
        if "Watch:Player" in query.data:
            query.message.reply_text(Watch_url)
        else: 
            query.message.reply_text(Download_url)
   
########################################################################################################################################

def main() -> None:
    updater = Updater(Bot.token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()

    updater.idle()

########################################################################################################################################


#if __name__ == '__main__':
#    main()

while True:
    try:
        print("% Restarting Telegram Bot % Animeweeb")
        main()
    except:
        print("Error Occured ! ")
        continue