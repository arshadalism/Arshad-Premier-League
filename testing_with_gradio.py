import json
import gradio
import requests


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
    print(data)
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


gradio.TabbedInterface(
    [player_detail_interface, player_registration_interface, all_player_data_interface, team_building_interface, team_details_interface, players_interface], ["Player detail", "Player registration", "ALL Players Data", "Team building", "Team details", "Players"]
).launch()
