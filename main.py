import uvicorn
import db
import schema
from fastapi import FastAPI, HTTPException
import player_automation


app = FastAPI(title="Arshad Premier League")


@app.get("/get_player_data")
async def get_player_data(player_id: int):
    response = await db.get_player_data(player_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Player not found.")
    return {"player_data": response}


@app.post("/register_player")
async def player_registration(player_data: schema.Player_detail):
    response = await db.register_player(player_data)
    return {"message": f"Player registered successfully with player_id {response}"}


@app.get("/all_players_data")
async def get_all_players_data():
    response = await db.get_all_players_data()
    return {"players": response}


@app.post("/team_building")
async def team_building(team_name: str):
    await player_automation.team_building(team_name)
    return {"success": "Team created successfully"}


@app.get("/team_details")
async def get_team_detail(team_name: str):
    response = await db.get_team_detail(team_name)
    return {"team": response}


@app.get("/players")
async def get_players(team_name: str):
    players = await db.get_players(team_name)
    return players


if __name__ == '__main__':
    uvicorn.run("main:app")
