from bs4 import BeautifulSoup
import requests

def fetch_anime_sama_schedule():
    url = "https://anime-sama.fr/planning/"
    response = requests.get(url)
    if response.status_code != 200:
        return "Erreur : Impossible d'accéder au planning."

    soup = BeautifulSoup(response.content, 'html.parser')
    schedule = {}

    days = soup.find_all('div', class_='day-container')  # Ajustez ce sélecteur si nécessaire
    for day in days:
        day_name = day.find('h2').text.strip()
        shows = []
        anime_cards = day.find_all('div', class_='anime-card')
        for card in anime_cards:
            title = card.find('h3').text.strip()
            time = card.find('div', class_='time').text.strip()
            shows.append(f"{title} ({time})")
        schedule[day_name] = shows

    return schedule

def setup_planning(bot):
    @bot.command()
    async def asc(ctx):
        schedule = fetch_anime_sama_schedule()
        if isinstance(schedule, str):  # Si une erreur est survenue
            await ctx.send(schedule)
            return

        for day, shows in schedule.items():
            shows_list = "\n".join(shows)
            await ctx.send(f"**{day}**\n{shows_list}")