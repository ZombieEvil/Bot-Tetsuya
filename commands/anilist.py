import requests
import datetime

def fetch_anilist_anime():
    query = """
    query ($page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
            media(type: ANIME, sort: TRENDING_DESC) {
                title {
                    romaji
                }
                siteUrl
                coverImage {
                    large
                }
                nextAiringEpisode {
                    airingAt
                    episode
                }
                streamingEpisodes {
                    site
                    url
                }
            }
        }
    }
    """
    variables = {"page": 1, "perPage": 5}
    try:
        response = requests.post("https://graphql.anilist.co", json={"query": query, "variables": variables})
        if response.status_code == 200:
            return response.json()["data"]["Page"]["media"]
        else:
            return []
    except Exception:
        return []

async def post_anime_updates(bot, channel_id, published_anime_urls):
    channel = bot.get_channel(channel_id)
    if not channel:
        return

    anilist_data = fetch_anilist_anime()
    if not anilist_data:
        await channel.send("❌ Aucun anime trouvé dans AniList.")
        return

    for anime in anilist_data[:10]:
        site_url = anime.get("siteUrl", None)
        if site_url in published_anime_urls:
            continue

        published_anime_urls.add(site_url)

        title = anime["title"].get("romaji", "Titre Non Spécifié")
        episode = anime.get("nextAiringEpisode", {}).get("episode", "Non spécifié")
        airing_at = anime.get("nextAiringEpisode", {}).get("airingAt", 0)
        airing_date = datetime.datetime.fromtimestamp(airing_at).strftime("%d %B %Y, %H:%M")

        description = f"Un nouvel épisode ({episode}) est prévu en diffusion :\n\n**Date** : {airing_date}\n"
        embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
        embed.set_image(url=anime.get("coverImage", {}).get("large", "https://via.placeholder.com/300x450"))
        await channel.send(embed=embed)

def setup_anilist(bot, scheduler):
    channel_id = 1310637134318669945
    published_anime_urls = set()

    @bot.command()
    async def check_anime(ctx):
        await post_anime_updates(bot, channel_id, published_anime_urls)

    scheduler.add_job(post_anime_updates, "interval", minutes=15, args=(bot, channel_id, published_anime_urls))