import requests
import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Profile:
    id: str
    name: str


@dataclass
class Match:
    match_id: str
    name: str
    bio: str


@dataclass
class Message:
    id: str
    match_id: str
    message: str
    from_id: str
    to_id: str
    sent_date: datetime.datetime


class Chatroom:
    def __init__(self, match_id: str, messages: List[Message], api):
        self.match_id = match_id
        self.messages = messages
        self.api = api

    def get_lastest_message(self) -> Optional[Message]:
        if not self.messages:
            return None
        return self.messages[0]

    def send(self, message: str, from_id: str, to_id: str):
        return self.api.send_message(self.match_id, message)


class TinderAPI:
    BASE_URL = "https://api.gotinder.com"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.token
        }

    def profile(self) -> Profile:
        response = requests.get(f"{self.BASE_URL}/v2/profile?include=user", headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch profile. Status code: {response.status_code}")
        try:
            data = response.json()
            return Profile(
                id=data['data']['user']['_id'],
                name=data['data']['user']['name']
            )
        except (ValueError, KeyError) as e:
            raise Exception(f"Invalid response from Tinder API: {str(e)}")

    def matches(self, limit: int = 10) -> List[Match]:
        response = requests.get(
            f"{self.BASE_URL}/v2/matches?count={limit}",
            headers=self.headers
        )
        data = response.json()
        matches = []
        for match in data['data']['matches']:
            matches.append(Match(
                match_id=match['id'],
                name=match['person']['name'],
                bio=match['person'].get('bio', '')
            ))
        return matches

    def get_messages(self, match_id: str) -> Chatroom:
        response = requests.get(
            f"{self.BASE_URL}/v2/matches/{match_id}/messages?count=100",
            headers=self.headers
        )
        data = response.json()
        messages = []
        for msg in data['data']['messages']:
            messages.append(Message(
                id=msg['_id'],
                match_id=match_id,
                message=msg['message'],
                from_id=msg['from'],
                to_id=msg['to'],
                sent_date=datetime.datetime.strptime(
                    msg['sent_date'], '%Y-%m-%dT%H:%M:%S.%fZ'
                )
            ))
        return Chatroom(match_id, messages, self)

    def send_message(self, match_id: str, message: str):
        response = requests.post(
            f"{self.BASE_URL}/user/matches/{match_id}",
            headers=self.headers,
            json={"message": message}
        )
        return response.status_code == 200