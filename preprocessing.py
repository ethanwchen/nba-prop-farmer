#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:

import os
from dotenv import load_dotenv
from nba_api.stats.endpoints import commonplayerinfo, playergamelog
from nba_api.stats.static import players

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def get_player_id(player_name):
    player_dict = players.find_players_by_full_name(player_name)
    return player_dict[0]['id'] if player_dict else None

def get_last_n_games(player_id, n):
    game_log = playergamelog.PlayerGameLog(player_id, season='2022')
    df = game_log.get_data_frames()[0]
    return df.head(n)
