from oologic.event import Event
from oologic.create_test_match import createMatch


class Test:
    match = createMatch()
    event1 = Event("00:15:36", "Red_Card", match.guest_team.coach)
    match.guest_team.coach.expulsion()
    event2 = Event("00:18:34", "Bella parata", match.home_team.roster[0])
    event3 = Event("00:35:22", "Goal su punizione", match.home_team.roster[6])
    match.home_team.score_goal()
    match.event_list.append(event1)
    match.event_list.append(event2)
    match.event_list.append(event3)

    match.json_and_txt_create()
