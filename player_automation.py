import asyncio
from datetime import datetime, timedelta
import db
import schema
import random
from faker import Faker
from typing import List


async def generate_players_detail(num_players: int):
    fake = Faker()
    players_list = []

    for _ in range(num_players):
        players_data = {
            "_id": random.randint(100000, 999999),
            "player_name": fake.name(),
            "batting_skill": random.randint(30, 80),
            "bowling_skill": random.randint(30, 80),
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


async def generate_fixtures(teams):
    fixtures = []
    teams_copy = list(teams)

    if len(teams_copy) % 2 != 0:
        teams_copy.append("BYE")

    for i in range(len(teams_copy) - 1):
        round_fixtures = []
        for j in range(len(teams_copy) // 2):
            match = (teams_copy[j], teams_copy[len(teams_copy) - 1 - j])
            round_fixtures.append(match)
        fixtures.extend(round_fixtures)

        teams_copy = [teams_copy[0]] + [teams_copy[-1]] + teams_copy[1: -1]
    return fixtures


async def match_fixture(team: List[str]):
    match_number = 1
    match_fixtures = []
    today_date = datetime.now().date()

    fixtures = await generate_fixtures(team)

    for match in fixtures:
        team1, team2 = match
        match_fixture_data = {
            "_id": random.randint(100, 99999),
            "matchNo": match_number,
            "team1": team1,
            "team2": team2,
            "venue": random.choice([team1.split()[0], team2.split()[0]]),
            "date": str(today_date)
        }
        schema.Fixture_details(**match_fixture_data)
        match_fixtures.append(match_fixture_data)
        match_number += 1
        today_date += timedelta(days=1)
    await db.match_fixture_col.insert_many(match_fixtures)
    return {"Successfully done"}


async def match_winner_result():
    async for document in db.matches_result_col.find():
        winner = random.choice([document["team1"], document["team2"]])
        db.matches_result_col.update_one({'_id': document['_id']}, {"$set": {"winner": winner}})

    return {"message": 'Done successfully'}


async def point_table():
    team_wins = {"Mumbai Indians": 0, "Chennai Super Kings": 0, "Delhi Capitals": 0, "Gujarat titans": 0,
                 "Kolkata Knights riders": 0, "Lucknow Super Giants": 0, "Punjab Kings": 0, "Hyderabad Sunrises": 0,
                 "Bangalore challengers": 0, "Rajasthan Royals": 0}
    async for document in db.matches_result_col.find():
        winner_team = document.get('winner')
        if winner_team in team_wins:
            team_wins[winner_team] += 1
    return team_wins


async def knockout_matches():
    teams_points = await point_table()
    teams = 10
    league_matches = (teams * (teams - 1)) // 2
    sorted_teams = sorted(teams_points.items(), key=lambda x: x[1], reverse=True)
    semifinal_teams = [team for team, _ in sorted_teams[:4]]
    winner_semifinal_1 = random.choice([semifinal_teams[0], semifinal_teams[3]])
    winner_semifinal_2 = random.choice([semifinal_teams[1], semifinal_teams[2]])
    final_winner = random.choice([winner_semifinal_1, winner_semifinal_2])
    knockout_matches_list = []
    semifinal_1 = {
        "_id": random.randint(100, 999),
        "matchNo": league_matches + 1,
        "team1": semifinal_teams[0],
        "team2": semifinal_teams[3],
        "venue": 'Mumbai',
        "date": "2023-12-27",
        "winner": winner_semifinal_1
    }
    knockout_matches_list.append(semifinal_1)
    semifinal_2 = {
        "_id": random.randint(100, 999),
        "matchNo": league_matches + 2,
        "team1": semifinal_teams[1],
        "team2": semifinal_teams[2],
        "venue": 'Kolkata',
        "date": "2023-12-28",
        "winner": winner_semifinal_2
    }
    knockout_matches_list.append(semifinal_2)

    final = {
        "_id": random.randint(100, 999),
        "matchNo": league_matches + 3,
        "team1": winner_semifinal_1,
        "team2": winner_semifinal_2,
        "venue": 'Ahmedabad',
        "date": "2023-12-31",
        "winner": final_winner
    }
    knockout_matches_list.append(final)
    await db.knockout_matches_col.insert_many(knockout_matches_list)
    return final_winner


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(knockout_matches())
