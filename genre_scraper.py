from selenium import webdriver
import pymongo

client = None
try:
    client = pymongo.MongoClient()
    print('Connection successful')
except:
    print('Could not connect to database')
if client:
    db = client.porchfest_radio
    collection = db.genre


    def scrape_genres(url):
        browser = webdriver.Chrome()
        browser.get(url)
        genres = []
        genres_divs = browser.find_elements_by_class_name('hFvVJe')
        for column in genres_divs:
            genre_links = column.find_elements_by_tag_name('a')
            for genre_link in genre_links:
                genres.append(genre_link.text)
        print(len(genres))
        return genres


    def main():
        genres = scrape_genres('https://www.google.com/search?q=music+genres&rlz=1C5CHFA_enUS738US738&oq=music+genres&aqs=chrome..69i57j69i60j0l4.1688j0j7&sourceid=chrome&ie=UTF-8')
        for genre in genres:
            genre_doc = {
                'name': genre
            }
            collection.insert_one(genre_doc)

    main()
