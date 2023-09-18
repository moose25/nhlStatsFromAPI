import requests

# Replace with your NHL API endpoint
NHL_API_ENDPOINT = "https://statsapi.web.nhl.com/api/v1/"

def get_team_id(team_name):
    """Get the NHL team ID by team name."""
    teams_url = f"{NHL_API_ENDPOINT}teams"
    response = requests.get(teams_url)

    if response.status_code == 200:
        teams_data = response.json()
        for team in teams_data["teams"]:
            if team["name"] == team_name:
                return team["id"]

    return None

def list_players(team_id):
    """List players for the specified NHL team."""
    roster_url = f"{NHL_API_ENDPOINT}teams/{team_id}/roster"
    response = requests.get(roster_url)

    if response.status_code == 200:
        roster_data = response.json()
        print(f"Players for the team (Team ID: {team_id}):")
        for player in roster_data["roster"]:
            print(f"{player['person']['fullName']} ({player['position']['abbreviation']})")

def get_player_stats(player_id):
    """Get detailed statistics for an NHL player."""
    stats_url = f"{NHL_API_ENDPOINT}people/{player_id}/stats?stats=statsSingleSeason"
    response = requests.get(stats_url)

    if response.status_code == 200:
        stats_data = response.json()
        if "stats" in stats_data["people"][0]:
            return stats_data["people"][0]["stats"][0]["splits"]

    return None

if __name__ == "__main__":
    team_name = input("Enter an NHL team name: ")
    team_id = get_team_id(team_name)

    if team_id is not None:
        list_players(team_id)
        player_name = input("Enter the full name of a player to get detailed stats: ")
        player_id = None

        # Find the player ID based on the name
        roster_url = f"{NHL_API_ENDPOINT}teams/{team_id}/roster"
        response = requests.get(roster_url)
        if response.status_code == 200:
            roster_data = response.json()
            for player in roster_data["roster"]:
                if player["person"]["fullName"].lower() == player_name.lower():
                    player_id = player["person"]["id"]
                    break

        if player_id is not None:
            player_stats = get_player_stats(player_id)
            if player_stats:
                print(f"Detailed statistics for {player_name}:")
                for stat in player_stats:
                    print(stat["season"], stat["stat"])
            else:
                print("No statistics found for the player.")
        else:
            print("Player not found on the team.")
    else:
        print("Team not found.")
