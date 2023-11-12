import json
import gradio
import requests
import schema


def get_player_detail(player_id: int):
    params = {
        "player_id": player_id
    }
    response = requests.get(f"http://127.0.0.1:8000/get_player_data", params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return response.status_code


player_detail_interface = gradio.Interface(
    fn=get_player_detail,
    inputs=gradio.Number(label="Enter the player id"),
    outputs=gradio.Json(),
    title="Get player detail"
)


def register_player(player_name, batting_skill, bowling_skill):
    player_data = {
        "player_name": player_name,
        "batting_skill": batting_skill,
        "bowling_skill": bowling_skill
    }
    url = "http://127.0.0.1:8000/register_player"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(player_data), headers=headers)
    if response.status_code == 200:
        data = response.json()
        player_id = data.get("message", "").split()[-1]
        return f"Player registered successfully. Player_id : {player_id}"
    else:
        return f"Player registration failed. Error :{response.json()['detail']}"


player_registration_interface = gradio.Interface(
    fn=register_player,
    inputs=[
        gradio.Textbox(label="Player name"),
        gradio.Number(minimum=30, maximum=80, label="Batting Skill"),
        gradio.Number(minimum=30, maximum=80, label="Bowling Skill"),
    ],
    outputs=gradio.Textbox()
)


def format_data_as_table(data):
    print(data)
    if not data:
        return "No data available."
    table_html = "<table><tr><th>Serial Number</th><th>Player_id</th><th>Player Name</th><th>Batting Skill</th><th>Bowling Skill</th><th>Role</th></tr>"
    for i, player in enumerate(data['players'], start=1):
        table_html += f"<tr><td>{i}</td><td>{player['_id']}</td><td>{player['player_name']}</td><td>{player['batting_skill']}</td><td>{player['bowling_skill']}</td><td>{player['role']}</td></tr>"
    table_html += "</table>"
    return table_html


def format_data_as_table_player(data):
    if not data:
        return "No data available."
    table_html = "<table><tr><th>Serial Number</th><th>Player_id</th><th>Player Name</th><th>Batting Skill</th><th>Bowling Skill</th><th>Role</th></tr>"
    for i, player in enumerate(data, start=1):
        table_html += f"<tr><td>{i}</td><td>{player['_id']}</td><td>{player['player_name']}</td><td>{player['batting_skill']}</td><td>{player['bowling_skill']}</td><td>{player['role']}</td></tr>"
    table_html += "</table>"
    return table_html


def get_all_player_data():
    url = "http://127.0.0.1:8000/all_players_data"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        table_html = format_data_as_table(data)
        return table_html
    else:
        return str(response.status_code)


all_player_data_interface = gradio.Interface(
    fn=get_all_player_data,
    inputs=None,
    outputs="html",
    title="All Players data"
)


def team_building(team_name: str):
    url = f"http://127.0.0.1:8000/team_building"
    params = {
        "team_name": team_name
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


team_building_interface = gradio.Interface(
    fn=team_building,
    inputs=gradio.Textbox(label="Enter the team name"),
    outputs=gradio.Json(),
    title="Team building"
)


def team_details(team_name: str):
    url = "http://127.0.0.1:8000/team_details"
    params = {
        "team_name": team_name
    }
    response = requests.get(url, params)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


team_details_interface = gradio.Interface(
    fn=team_details,
    inputs=gradio.Textbox(label="Enter the team name"),
    outputs=gradio.Json(),
    title="Team details"
)


def get_players(team_name: str):
    url = "http://127.0.0.1:8000/players"
    params = {
        "team_name": team_name
    }
    response = requests.get(url, params)
    if response.status_code == 200:
        data = response.json()
        player_table = format_data_as_table_player(data)
        return player_table
    else:
        return response.status_code


players_interface = gradio.Interface(
    fn=get_players,
    inputs=gradio.Textbox(label="Enter the team name"),
    outputs="html",
    title="Team details"
)


def match_fixtures(request: schema.MatchFixtureRequest):
    team_list = [team.strip() for team in request.split(',')]
    url = "http://127.0.0.1:8000/match_fixture"
    teams = {
        "team_list": team_list
    }
    response = requests.post(url, json=teams, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


match_fixture_creation_interface = gradio.Interface(
    fn=match_fixtures,
    inputs=gradio.Textbox(label="Enter the team names separated by commas:", type="text"),
    outputs=gradio.Json(),
    title="Match fixture"
)


def format_data_as_matches_list(data):
    if not data:
        return "No data available."
    table_html = "<table><tr><th>Match ID</th><th>Match No</th><th>Team 1</th><th>Versus</th><th>Team 2</th><th>Venue</th><th>Date</th></tr>"
    for i, match in enumerate(data, start=1):
        table_html += f"<tr><td>{match['_id']}</td><td>{match['matchNo']}</td><td>{match['team1']}</td><td>vs</td><td>{match['team2']}</td><td>{match['venue']}</td><td>{match['date']}</td></tr>"
    table_html += "</table>"
    return table_html


def get_all_matches_list():
    url = "http://127.0.0.1:8000/matches_list"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        matches_tabel = format_data_as_matches_list(data)
        return matches_tabel
    else:
        return response.status_code


get_all_matches_list_interface = gradio.Interface(
    fn=get_all_matches_list,
    inputs=None,
    outputs="html",
    title="All-Matches_List"
)


def format_data_as_team_matches_list(data):
    if not data:
        return "No data available."
    table_html = "<table><tr><th>Serial No</th><th>Match ID</th><th>Match No</th><th>Team 1</th><th>Versus</th><th>Team 2</th><th>Venue</th><th>Date</th></tr>"
    for i, match in enumerate(data, start=1):
        table_html += f"<tr><td>{i}</td><td>{match['_id']}</td><td>{match['matchNo']}</td><td>{match['team1']}</td><td>vs</td><td>{match['team2']}</td><td>{match['venue']}</td><td>{match['date']}</td></tr>"
    table_html += "</table>"
    return table_html


def team_matches_list(team_name: str):
    url = "http://127.0.0.1:8000/team_matches_list"
    params = {
        "team_name": team_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        match_table = format_data_as_team_matches_list(data)
        return match_table
    else:
        return response.status_code


team_matches_list_interface = gradio.Interface(
    fn=team_matches_list,
    inputs=gradio.Textbox(label="Enter the name of the team"),
    outputs="html",
    title="Team-Matches_List"
)


def format_data_as_point_table(data):
    if not data:
        return "No data available"
    point_table_html = "<table><tr><th>Serial No</th><th>Team Name</th><th>Matches Played</th><th>Wins</th><th>Losses</th><th>Points</th></tr>"
    sorted_teams = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for i, (team, wins) in enumerate(sorted_teams, start=1):
        matches_played = 9
        losses = matches_played - wins
        points = wins * 2
        team_label = "(Q)" if i <= 4 else "(E)"
        point_table_html += (
            f"<tr><td>{i}  {team_label}</td><td>{team}</td><td>{matches_played}</td><td>{wins}</td><td>{losses}</td><td>{points}</td></tr>"
        )
    point_table_html += "</table>"
    return point_table_html


def point_table():
    url = "http://127.0.0.1:8000/point_table"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        point_table = format_data_as_point_table(data)
        return point_table
    else:
        return response.status_code


point_table_interface = gradio.Interface(
    fn=point_table,
    inputs=None,
    outputs="html",
    title="Point Table"
)


def knockout_matches():
    url = "http://127.0.0.1:8000/knockout_matches"
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


knockout_matches_interface = gradio.Interface(
    fn=knockout_matches,
    inputs=None,
    outputs=gradio.Textbox(),
    title="Knockout Matches"
)


def get_match_type(match_no):
    if match_no == 46:
        return "Semifinal 1"
    elif match_no == 47:
        return "Semifinal 2"
    elif match_no == 48:
        return "Final"
    else:
        return None


def format_data_as_knockouts_matches_list(data):
    if not data:
        return "No data available."
    table_html = "<table><tr><th>Serial No</th><th>Match ID</th><th>Match No</th><th>Match Type</th><th>Team 1</th><th>Versus</th><th>Team 2</th><th>Venue</th><th>Date<th>Winner</th></th></tr>"
    for i, match in enumerate(data, start=1):
        match_type = get_match_type(match['matchNo'])
        winner_display = f"<big>{match['winner']}</big>" if match_type == "Final" else match['winner']
        table_html += f"<tr><td>{i}</td><td>{match['_id']}</td><td>{match['matchNo']}</td><td>{match_type}</td><td>{match['team1']}</td><td>vs</td><td>{match['team2']}</td><td>{match['venue']}</td><td>{match['date']}<td>{winner_display}</td></td></tr>"
    table_html += "</table>"

    table_html += "<br><br><strong>Congratulations to the team "
    if data[-1]['winner']:
        table_html += f"<big>{data[-1]['winner']}</big>"
    table_html += " - Champions!!!</strong>"
    return table_html


def knockout_matches_data():
    url = "http://127.0.0.1:8000/knockout_matches_table"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        matches_data = format_data_as_knockouts_matches_list(data)
        return matches_data
    else:
        return response.status_code


knockout_matches_interface_table = gradio.Interface(
    fn=knockout_matches_data,
    inputs=None,
    outputs="html",
    title="Knockouts Matches Data"
)


gradio.TabbedInterface(
    [player_detail_interface, player_registration_interface, all_player_data_interface, team_building_interface,
     team_details_interface, players_interface, match_fixture_creation_interface, get_all_matches_list_interface,
     team_matches_list_interface, point_table_interface, knockout_matches_interface, knockout_matches_interface_table],
    ["Player detail", "Player registration", "ALL Players Data", "Team building", "Team details", "Players",
     "Match fixtures", "Matches List", "Team Matches List", "Point Table", "Knockout Matches", "Knockout Matches Data"]
).launch()
