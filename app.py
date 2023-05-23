import requests
import openai

prewritten_info = "Trains played a crucial role in transporting refugees in Ukraine and neighboring countries during the conflict. Ukrainian Railways transported 2.5 million passengers within three weeks, with a peak of 190,000 people per day. Trains had to adapt to damaged tracks and slower speeds due to safety concerns. Some European countries provided free train travel to Ukrainian refugees. Other refugees traveled by vehicles or on foot, causing traffic jams at borders. Air travel was unavailable in Ukraine due to airspace closure. In February 2022, a refugee crisis began after Russia invaded Ukraine. Over 8.2 million refugees fled Ukraine to Europe, with 8 million internally displaced. Many Ukrainian men are banned from leaving the country. Most refugees initially sought shelter in neighboring countries and then moved to other European countries. Russia, Poland, Germany, and the Czech Republic received the most Ukrainian refugees. Forced transfers of Ukrainian civilians to Russia, including unaccompanied children, have been reported. Around 900,000 Ukrainians were forcibly relocated to Russia. Ethnic discrimination at borders affected non-European and Romani people. The EU granted Ukrainian refugees one-year rights to stay, work, and study in member states.By the end of 2019, over 13.2 million Syrians were forcibly displaced. Approximately 6.7 million Syrians left the country, with a significant number in Turkey. Three categories of concern were identified: individuals in need of international protection, individuals with a refugee background, and individuals who returned after seeking protection. The UNHCR maintains a database of estimated Syrian refugees and asylum seekers per country. The conflict caused over 580,000 deaths, 13 million displacements, and 6.7 million forced refugee outflows from Syria"

starting_country = input("Enter your country of origin: ")
starting_city = input("Enter the city from which you will begin: ")
destination_country = input("Enter your final country of destination: ")
destination_city = input("Enter your final city of destination: ")
transportation_mode = input("Preferred mode of transportation (land, air, sea, or all): ")
time_constraints = input("Any time constraints or deadlines for reaching the destination: ")
demographics = input("Demographics of the refugees (e.g., age groups, health conditions, special needs): ")
safety_concerns = input("Any safety concerns or preferences to consider: ")

openai.api_key = "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"

topics = ["refugee", "conflict", "blockade", "civil war", "Syria", "Ukraine"]

news_articles = []
for topic in topics:
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": topic,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": "2457b652ec3c4a1f9e5987ec654debad"
    }
    response = requests.get(url, params=params)
    articles = response.json()["articles"]
    for article in articles:
        news_articles.append(article)

relevant_articles = []
for article in news_articles:
    if (
        starting_country.lower() in article["title"].lower()
        and starting_city.lower() in article["title"].lower()
        and destination_country.lower() in article["title"].lower()
        and destination_city.lower() in article["title"].lower()
    ):
        relevant_articles.append(article)

if relevant_articles:
    latest_article = relevant_articles[0]
    latest_title = latest_article["title"]
    latest_content = latest_article["content"]
else:
    latest_title = ""
    latest_content = ""

explanation = f"Based on the latest news article titled '{latest_title}', it has been considered in determining the best path for refugees from {starting_city}, {starting_country} to {destination_city}, {destination_country}. Here are the details: \n\n{latest_content}"

prompt = f"{prewritten_info}\n\nGiven the latest news on refugees, please provide the best path for refugees to travel from {starting_city}, {starting_country} to {destination_city}, {destination_country}. Please take into account any current conflicts or blockades in the region. Please provide a detailed list of the cities that they must pass through to reach their destination, along with their coordinates. \n\nLatest news on the exact refugee: \n- {latest_title} \n- {latest_content}\n\nExplanation based on the latest news:\n{explanation}\n\nPlease provide a comprehensive explanation of your reasoning, including the news articles and information you used to determine the best path. Format the response well with bullet points, headings, as well as spacing in between answers."

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=3500,
    n=1,
    stop=None,
    temperature=0.5,
)

output = response.choices[0].text.strip()
output = output.replace("\n\n", "\n")
output = output.split("\n")
output = [f"- {line.strip()}" if not line.startswith("-") else line.strip() for line in output]
output = "\n".join(output)

print(output)