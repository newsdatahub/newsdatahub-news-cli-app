#!/usr/bin/env python3
import requests
import datetime
import random
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from emoji import emojize

# ====== CONFIGURATION ======
PER_PAGE = 100  # change this once — used everywhere
API_KEY = "YOUR_API_KEY"
URL = "https://api.newsdatahub.com/v1/news"
PARAMS = {
    "per_page": PER_PAGE,
    "topic": "technology",
    "language": "en",
    "country": "US",
    "source_type": "mainstream_news"
}
# ============================

console = Console()

FUN_EMOJIS = [
    "🚀", "🤖", "📰", "⚡", "🧠", "💡", "🔋", "🪄", "🌎", "📈",
    "🎯", "📱", "🛰️", "🎉", "🦾", "💬", "💻", "🔧", "🔮", "🪙",
    "🧪", "🏙️", "🎥", "🧭", "🧩", "🌠", "🏎️", "🌍", "🔥", "📊"
]

KEYWORD_EMOJIS = {
    "tesla": "🚘",
    "spacex": "🚀",
    "ai": "🤖",
    "robot": "🦾",
    "technology": "💻",
    "innovation": "💡",
    "finance": "💰",
    "stock": "📈",
    "crypto": "🪙",
    "climate": "🌍",
    "energy": "⚡",
    "launch": "🛫",
    "startup": "🚀",
    "science": "🔬",
    "research": "🧠",
    "market": "📊",
    "policy": "🏛️",
    "security": "🔒",
    "china": "🐉",
    "usa": "🦅",
}

def emoji_for_headline(title: str) -> str:
    title_lower = title.lower()
    for word, icon in KEYWORD_EMOJIS.items():
        if word in title_lower:
            return icon
    return random.choice(FUN_EMOJIS)

def fetch_news():
    headers = {"X-API-Key": API_KEY}

    console.print(
        "\n[bold #003366]📰 Presented by [bold orange3]NewsDataHub[/bold orange3] — "
        "Your Gateway to Global News Intelligence[/bold #003366]\n"
    )

    with Progress(SpinnerColumn(), TextColumn("[green]Connecting to NewsDataHub API...")) as progress:
        task = progress.add_task("", total=None)
        try:
            response = requests.get(URL, headers=headers, params=PARAMS, timeout=10)
        except Exception as e:
            progress.remove_task(task)
            console.print(f"[bold red]❌ Connection failed:[/bold red] {e}")
            return
        progress.remove_task(task)

    # Handle HTTP errors gracefully
    if response.status_code == 429:
        console.print("[bold red]⚠️ Rate limit reached (HTTP 429)[/bold red]. Try again later.")
        return
    elif 500 <= response.status_code < 600:
        console.print(f"[bold red]⚠️ Server error (HTTP {response.status_code}).[/bold red] Please try again later.")
        return
    elif 400 <= response.status_code < 500:
        console.print(f"[bold red]⚠️ Request error (HTTP {response.status_code}).[/bold red] Check your parameters or API key.")
        return

    data = response.json()
    articles = data.get("data", [])
    if not articles:
        console.print("[yellow]No articles found. Try adjusting your filters.[/yellow]")
        return

    console.print(
        f"\n[bold magenta]🚀 Latest US Tech Headlines ({PER_PAGE} results)[/bold magenta]\n"
    )

    for i, a in enumerate(articles[:PER_PAGE], start=1):
        icon = emoji_for_headline(a["title"])
        link = f"[link={a['article_link']}][blue underline]{a['article_link']}[/blue underline][/link]"

        console.print(f"[cyan]{i}.[/cyan] {icon} [bold]{a['title']}[/bold]")
        console.print(f"[red]{a['source_title']}[/red] • [black]{a['pub_date']}[/black]")
        console.print(f"{link}\n")
        time.sleep(0.35)  # pacing between headlines

    console.print("[dim]------------------------------------------------------------[/dim]")
    console.print(f"[black]Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/black]")
    console.print("\n[bold #003366]✨ Delivered by [bold orange3]NewsDataHub[/bold orange3] ✨[/bold #003366]\n")

if __name__ == "__main__":
    fetch_news()
