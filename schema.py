from pydantic import BaseModel, Field
from typing import List


class Player_detail(BaseModel):
    player_name: str
    batting_skill: int = Field(ge=30, le=80)
    bowling_skill: int = Field(ge=30, le=80)


class Team_detail(BaseModel):
    _id: int
    team_name: str
    player_list: list


class Fixture_details(BaseModel):
    _id: int
    matchNo: int
    team1: str
    team2: str
    venue: str
    date: str


class MatchFixtureRequest(BaseModel):
    team_list: List[str]
