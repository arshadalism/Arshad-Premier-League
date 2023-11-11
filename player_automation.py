import asyncio
from datetime import datetime, timedelta
import db
import schema
import random
from faker import Faker


async def generate_players_detail(num_players: int):
    fake = Faker()
    players_list = []

    for _ in range(num_players):
        players_data = {
            "_id": random.randint(100000, 999999),
            "player_name": fake.name(),
            "batting_skill": random.randint(20, 80),
            "bowling_skill": random.randint(20, 80),
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
        schema.Player_detail(**players_data)
        players_list.append(players_data)

    await db.players_details_col.insert_many(players_list)
    return


async def team_building(team_name: str):
    players = await db.player_pool_for_auction.find({}).to_list(length=None)
    available_players = players.copy()
    team = []
    batting_option = 0
    bowling_option = 0

    while available_players and (batting_option < 2 or bowling_option < 2):
        for player in players:
            if player in team:
                continue
            if player['role'] == "Batter":
                batting_option += 1
            elif player['role'] == "Bowler":
                bowling_option += 1
            elif player['role'] == "All-rounder":
                batting_option += 1
                bowling_option += 1
            team.append(player)
            available_players.remove(player)
            if len(team) == 5 and batting_option >= 2 and bowling_option >= 2:
                break
        else:
            continue
        break
    for player in team:
        await db.player_pool_for_auction.delete_one({"_id": player['_id']})

    team_data = {
        "_id": random.randint(100, 999),
        "team_name": team_name,
        "player_list": team
    }

    schema.Team_detail(**team_data)
    await db.team_details_col.insert_one(team_data)


async def match_fixture(team: list):
    match_number = 1
    today_date = datetime.now().date()
    for i in range(len(team)):
        for j in range(i + 1, len(team)):
            match_fixture = {
                "matchNo": match_number,
                "team1": team[i],
                "team2": team[j],
                "venue": team[i].split()[0],
                "date": str(today_date)
            }
            await db.match_fixture_col.insert_one(match_fixture)
            match_number += 1
            today_date += timedelta(days=1)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        match_fixture(["Mumbai Indians", "Chennai Super Kings", "Lucknow Super Giants"]))
