import collections

import requests.auth


def get_people(auth, *includes):
    url = f"https://api.planningcenteronline.com/people/v2/people"
    prepared_request = requests.PreparedRequest()
    prepared_request.prepare(url=url, params={
        "per_page": 100,
        "include": ",".join(includes)
    })
    print(prepared_request.url)
    response = requests.get(prepared_request.url, auth=requests.auth.HTTPBasicAuth(auth.username, auth.password))
    return response.json()


def get_team_members(plan_id: int, auth):
    url = f"https://api.planningcenteronline.com/services/v2/service_types/368342/plans/{plan_id}"
    response = requests.get(url + "/team_members?per_page=100&include=team", auth=requests.auth.HTTPBasicAuth(auth.username, auth.password))
    data = response.json()
    team_members = collections.defaultdict(lambda: collections.defaultdict(set))
    team_map = {}
    person_map = collections.defaultdict(dict)
    for inclusion in data["included"]:
        if inclusion["type"] == "Team":
            team_map[inclusion["id"]] = inclusion["attributes"]["name"]
        elif inclusion["type"] == "Person":
            person_map[inclusion["id"]]["name"] = inclusion["attributes"]["name"]

    people_data = get_people(auth, "phone_numbers")

    for person in people_data["data"]:
        for inclusion in people_data["included"]:
            print(person["id"])
            print(inclusion["relationships"]["person"]["data"]["id"])
            print()
            if inclusion["relationships"]["person"]["data"]["id"] == person["id"]:
                # Weird hack to remove unicode characters like \u202d around the string
                phone_number = inclusion["attributes"]["number"].encode("ascii", "ignore").decode("utf-8")
                phone_number = phone_number.replace(" ", "").replace("+47", "")
                person_map[person["id"]]["phone_number"] = phone_number

    for person in data["data"]:
        team = person["relationships"]["team"]["data"]["id"]
        if team not in team_map:
            raise RuntimeError(f"Team not in included teams: {team}")
        person_id = person["relationships"]["person"]["data"]["id"]
        team_members[team_map[team]][person["attributes"]["team_position_name"]].add((person["attributes"]["name"], person_map[person_id]["phone_number"] if "phone_number" in person_map[person_id] else None))

    return team_members
