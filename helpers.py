import requests
from config import endPointsKey as statsapi
import logging
import json
from datetime import datetime

INTERNAL_ERR_RESPONSE = {"results":{"error":"Sorry, internal error occured."}}
VALUE_ERR_RESPONSE = {"results":{"error":"Please enter Valid league name and dates."}}

#get response for scoreboard api
def get_metrics_between_dates(league_name, date_from, date_to):
    #raise exception if the league name is empty
    if not league_name:
        raise ValueError("League Name should not be null or empty.")
    #to raise date invalid format Exception
    datetime.strptime(date_from, '%Y-%m-%d')
    datetime.strptime(date_to, '%Y-%m-%d')

    url=statsapi.SCOREBOARD_ENDPOINT.format(league=league_name,start_date=date_from,end_date=date_to)
    result = requests.get(url)
    return result

#get response from team rankings api
def get_team_rankings(league_name):
    if not league_name:
        raise ValueError("League Name should not be null or empty")
    url=statsapi.TEAM_RANKING_ENDPOINT.format(league=league_name)
    result = requests.get(url)
    return result

#get events list from parsing the scoreboard endpoint json
def get_events_list_from_json(metrics_json):
    events = []
    dates_dict = metrics_json['results']
    for date in dates_dict:
        #if the day has the dictionary for data
        if "data" in dates_dict[date]:
            for event in dates_dict[date]["data"]:
                events.append(dates_dict[date]["data"][event])
    return events

#get team by id from the list of dictionaries
def get_team_by_id(team_id,teams):
    for team in teams:
        if team['team_id'] == team_id:
            return team

#function to create the response required
def get_masked_json_response(events, teams):
    result_events = []
    #iterate the events and append to the new list
    for event in events:
        temp_event={}
        home_team = get_team_by_id(event["home_team_id"],teams)
        away_team = get_team_by_id(event["away_team_id"],teams)
        temp_event["event_id"]=event["event_id"]
        #format date and time of the event
        temp_event["event_date"]=datetime.fromisoformat(event["event_date"]).strftime("%d-%m-%Y")
        temp_event["event_time"]=datetime.fromisoformat(event["event_date"]).strftime("%H:%M")
        temp_event["away_team_id"]=event["away_team_id"]
        temp_event["away_nick_name"]=event["away_nick_name"]  
        temp_event["away_city"]=event["away_city"]
        temp_event["away_rank"]=away_team["rank"]
        #format the team points to the decimal of two digits
        temp_event["away_rank_points"]=round(float(away_team["adjusted_points"]), 2)
        temp_event["home_team_id"]=event["home_team_id"]
        temp_event["home_nick_name"]=event["home_nick_name"]
        temp_event["home_city"]=event["home_city"]
        temp_event["home_rank"]=home_team["rank"]
        temp_event["home_rank_points"]=round(float(home_team["adjusted_points"]), 2)
        result_events.append(temp_event)
    return json.dumps(result_events)

#function to get the results from two end points and merge the responses
def get_combined_result(league_name, date_from, date_to):
    try:
        #get response from ranking endpoint
        rankings_result = get_team_rankings(league_name)
        #on successful response get the events and parse the result
        if rankings_result.status_code == 200:
            metrics_result = get_metrics_between_dates(league_name,date_from,date_to)
            if metrics_result.status_code == 200:
                #create list of events by parsing the result
                events = get_events_list_from_json(json.loads(metrics_result.text))
                #if no events on the given days 
                if len(events) > 0:
                    #get team rankings list
                    teams=json.loads(rankings_result.text)['results']['data']
                    return get_masked_json_response(events, teams)
                else:
                    return json.dumps(events)
            else:
                return metrics_result.text
        else:
            return rankings_result.text
    #handling the value err raised from invalid inputs
    except ValueError as value_err:
        logging.exception("Invalid Value for API")
        return json.dumps(VALUE_ERR_RESPONSE)
    except Exception as err:
        logging.exception("Error occured in the request")
        return json.dumps(INTERNAL_ERR_RESPONSE)