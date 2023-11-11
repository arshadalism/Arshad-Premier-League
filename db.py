import asyncio
import random
import schema
import db
from db_client import database

players_details_col = database.get_collection("Players_details")
team_details_col = database.get_collection("Team_details")
player_pool_for_auction = database.get_collection("Available_players")
match_fixture_col = database.get_collection("Match fixture")


async def copy():
    document = await players_details_col.find({}).to_list(length=None)
    player_pool_for_auction.insert_many(document)


async def register_player(player_data: schema.Player_detail):
    players_data = {
        "_id": random.randint(100000, 999999),
        "player_name": player_data.player_name,
        "batting_skill": player_data.batting_skill,
        "bowling_skill": player_data.bowling_skill,
    }

    batting_skill = players_data["batting_skill"]
    bowling_skill = players_data["bowling_skill"]

    if -25 <= (batting_skill - bowling_skill) <= 25:
        role = "All-rounder"
    elif max(batting_skill, bowling_skill) == batting_skill:
        role = "Batter"
    else:
        role = "Bowler"
    players_data["role"] = role
    await db.players_details_col.insert_one(players_data)
    return players_data["_id"]


async def get_player_data(player_id: int):
    return await db.players_details_col.find_one({"_id": player_id})


async def get_all_players_data():
    players_data = []
    async for player in players_details_col.find({}):
        players_data.append(player)
    return players_data


async def get_team_detail(team_name: str):
    team = await team_details_col.find_one({"team_name": team_name})
    return team


async def get_players(team_name: str):
    players = await team_details_col.find_one({"team_name": team_name})
    return players['player_list']


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(copy())


