import os
import discord
import typing
from discord.ext import commands
from dotenv import load_dotenv 
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import commonplayerinfo, playergamelog
from nba_api.stats.static import players
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from typing import Optional
import numpy as np
from numpy.random import randn


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

def get_player_id(player_name):
    player_dict = players.find_players_by_full_name(player_name)
    return player_dict[0]['id'] if player_dict else None

def get_last_n_games(player_id, n):
    game_log = playergamelog.PlayerGameLog(player_id, season='2022')
    df = game_log.get_data_frames()[0]
    return df.head(n)

def monte_carlo_simulation(model, X, y, games, simulations=1000):
    over_count = 0
    under_count = 0
    exact_count = 0
    mse = mean_squared_error(y, model.predict(X))
    std_dev = np.std(y)
    predictions = []

    for _ in range(simulations):
        noise = randn() * std_dev
        prediction = model.predict([[games + 1]])[0][0] + noise
        prediction = round(prediction)
        predictions.append(prediction)
        if prediction > games:
            over_count += 1
        elif prediction < games:
            under_count += 1
        else:
            exact_count += 1

    over_percentage = over_count / simulations
    under_percentage = under_count / simulations
    exact_percentage = exact_count / simulations

    return over_percentage, under_percentage, exact_percentage, predictions

def linear_regression(df, stat, games):
    X = np.array(range(1, games + 1)).reshape(-1, 1)
    y = df[stat].values.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    projected_stat = model.predict([[games + 1]])
    return projected_stat[0][0], model, X, y

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='project_stat')
async def project_stat(ctx, player_name: str, stat: str, games: Optional[int] = 5):
    player_id = get_player_id(player_name)
    if player_id is None:
        await ctx.send(f"Player '{player_name}' not found.")
        return

    df = get_last_n_games(player_id, games)
    if df.empty:
        await ctx.send("No game data found.")
        return

    stat_map = {
        "P": "PTS",
        "R": "REB",
        "A": "AST",
        "PA": "PTS_AST",
        "PR": "PTS_REB",
        "3P": "FG3M"
    }

    if stat not in stat_map:
        await ctx.send(f"Stat '{stat}' not supported.")
        return

    if stat == "PA":
        df["PTS_AST"] = df["PTS"] + df["AST"]
    elif stat == "PR":
        df["PTS_REB"] = df["PTS"] + df["REB"]

    projected_stat, model, X, y = linear_regression(df, stat_map[stat], games)
    fig, ax = plt.subplots()
    ax.plot(range(1, games + 1), df[stat_map[stat]], 'o-', label='Actual')
    ax.plot(games + 1, projected_stat, 'rx', label='Projected', markersize=12)
    ax.set_xlabel('Games')
    ax.set_ylabel(stat_map[stat])
    ax.set_title(f'{player_name} {stat_map[stat]} Projection')
    ax.legend()
    plt.savefig('projection.png')
    over_percentage, under_percentage, exact_percentage, predictions = monte_carlo_simulation(model, X, y, games)
    await ctx.send(f"Over {games} {stat_map[stat]}: {over_percentage * 100:.1f}%, Under {games} {stat_map[stat]}: {under_percentage * 100:.1f}%, Exactly {games} {stat_map[stat]}: {exact_percentage * 100:.1f}%")
    fig, ax = plt.subplots()
    min_value = max(min(predictions), 0)
    max_value = max(predictions)
    bins = np.linspace(min_value, max_value, 50)
    ax.hist(predictions, bins=bins, edgecolor='black', alpha=0.75)
    ax.set_xlabel(stat_map[stat])
    ax.set_ylabel('Frequency')
    ax.set_title(f'{player_name} {stat_map[stat]} Distribution (1000 simulations)')
    plt.savefig('simulation_histogram.png')
    await ctx.send(file=discord.File('simulation_histogram.png'))
    await ctx.send(file=discord.File('projection.png'))

    
bot.run(TOKEN)
