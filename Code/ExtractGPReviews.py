from google_play_scraper import Sort, reviews
import csv
import pandas as pd


def get_reviews(input_file):
    df = pd.read_csv(input_file)
    for row in df.iterrows():
        app_id = row[1][0]
        app_package_name = row[1][3]
        review_count = row[1][4]

        if pd.isnull(review_count):
            review_count = 20000

        status = True

        try:
            result = reviews(
                app_package_name,
                lang='en', # defaults to 'en'
                country='us', # defaults to 'us'
                sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
                count=review_count,  # defaults to 100
            )
        except:
            status = False

        if status and len(result) > 0:
            output_file = "../Output/Review/Raw/" + app_id + ".csv"

            default_text = '-'
            with open(output_file, 'w', newline='', encoding='utf_8') as w:
                writer = csv.writer(w)
                try:
                    w.write("Text" + "," + "Score" + "," + "Date" + "," + "ThumbsUpCount" + "\n")
                    for item in result:
                        if item['content'] is not None:
                            w.write(item['content'].replace(',', ' _ ').replace('\n', ' ---- '))
                        else:
                            w.write(default_text)
                        # review rating
                        if item['score'] is not None:
                            w.write(',' + str(item['score']).replace(',', ' _ '))
                        else:
                            w.write(',' + default_text)
                        # review date
                        if item['at'] is not None:
                            w.write(',' + item['at'].strftime('%m/%d/%Y'))
                        else:
                            w.write(',' + default_text)
                        # review similar thought
                        if item['thumbsUpCount'] is not None:
                            w.write(',' + str(item['thumbsUpCount']).replace(',', ' _ '))
                        else:
                            w.write(',' + default_text)

                        w.write('\n')
                    print("Total number of reviews retrieved for %s : %d" % (app_id, len(result)))
                except Exception as e:
                    print("Error accessing reviews for : ", app_id)
                    w.write('\n')
            w.close()

        else:
            print("No reviews retrieved for :", app_id)

