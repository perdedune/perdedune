import requests
import json

url = "https://core-hsr.dune.com/v1/graphql"

def query_list(user,slug):
  payload = json.dumps({
    "operationName": "FindDashboard",
    "variables": {
      "session_filter": {},
      "user": user,
      "slug": slug
    },
    "query": "query FindDashboard($session_filter: Int_comparison_exp!, $user: String!, $slug: String!) {\n  dashboards(\n    where: {slug: {_eq: $slug}, _or: [{user: {name: {_eq: $user}}}, {team: {handle: {_eq: $user}}}]}\n  ) {\n    ...Dashboard\n    favorite_dashboards(where: {user_id: $session_filter}, limit: 1) {\n      created_at\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Dashboard on dashboards {\n  id\n  name\n  slug\n  is_private\n  is_archived\n  created_at\n  updated_at\n  tags\n  user {\n    ...User\n    __typename\n  }\n  team {\n    ...Team\n    __typename\n  }\n  forked_dashboard {\n    slug\n    name\n    user {\n      name\n      __typename\n    }\n    team {\n      handle\n      __typename\n    }\n    __typename\n  }\n  text_widgets {\n    id\n    created_at\n    updated_at\n    text\n    options\n    __typename\n  }\n  visualization_widgets {\n    id\n    created_at\n    updated_at\n    options\n    visualization {\n      ...Visualization\n      __typename\n    }\n    __typename\n  }\n  param_widgets {\n    id\n    key\n    visualization_widget_id\n    query_id\n    dashboard_id\n    options\n    created_at\n    updated_at\n    __typename\n  }\n  dashboard_favorite_count_all {\n    favorite_count\n    __typename\n  }\n  trending_scores {\n    score_1h\n    score_4h\n    score_24h\n    updated_at\n    __typename\n  }\n  __typename\n}\n\nfragment User on users {\n  id\n  name\n  profile_image_url\n  __typename\n}\n\nfragment Team on teams {\n  id\n  name\n  handle\n  profile_image_url\n  __typename\n}\n\nfragment Visualization on visualizations {\n  id\n  type\n  name\n  options\n  created_at\n  query_details {\n    query_id\n    name\n    description\n    show_watermark\n    parameters\n    user {\n      id\n      name\n      profile_image_url\n      __typename\n    }\n    team {\n      id\n      name\n      handle\n      profile_image_url\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
  })
  headers = {
    'content-type': 'application/json',
    'X-Hasura-Api-Key': ''
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  viz_id_list = []
  visualization_widgets = response.json()["data"]["dashboards"][0]["visualization_widgets"]
  for c in visualization_widgets:
    viz_id_list.append(c["visualization"]["query_details"]["query_id"])
  return(list(set(viz_id_list)))

def sql_from_query(id):
  payload = json.dumps({
    "operationName": "FindQuery",
    "variables": {
      "favs_last_24h": False,
      "favs_last_7d": False,
      "favs_last_30d": False,
      "favs_all_time": True,
      "session_filter": {},
      "id": id
    },
    "query": "query FindQuery($session_filter: Int_comparison_exp!, $id: Int!, $favs_last_24h: Boolean! = false, $favs_last_7d: Boolean! = false, $favs_last_30d: Boolean! = false, $favs_all_time: Boolean! = true) {\n  queries(where: {id: {_eq: $id}}) {\n    ...Query\n    favorite_queries(where: {user_id: $session_filter}, limit: 1) {\n      created_at\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Query on queries {\n  ...BaseQuery\n  ...QueryVisualizations\n  ...QueryForked\n  ...QueryUsers\n  ...QueryTeams\n  ...QueryFavorites\n  __typename\n}\n\nfragment BaseQuery on queries {\n  id\n  dataset_id\n  name\n  description\n  query\n  is_private\n  is_temp\n  is_archived\n  created_at\n  updated_at\n  schedule\n  tags\n  parameters\n  __typename\n}\n\nfragment QueryVisualizations on queries {\n  visualizations {\n    id\n    type\n    name\n    options\n    created_at\n    __typename\n  }\n  __typename\n}\n\nfragment QueryForked on queries {\n  forked_query {\n    id\n    name\n    user {\n      name\n      __typename\n    }\n    team {\n      handle\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment QueryUsers on queries {\n  user {\n    ...User\n    __typename\n  }\n  team {\n    id\n    name\n    handle\n    profile_image_url\n    __typename\n  }\n  __typename\n}\n\nfragment User on users {\n  id\n  name\n  profile_image_url\n  __typename\n}\n\nfragment QueryTeams on queries {\n  team {\n    ...Team\n    __typename\n  }\n  __typename\n}\n\nfragment Team on teams {\n  id\n  name\n  handle\n  profile_image_url\n  __typename\n}\n\nfragment QueryFavorites on queries {\n  query_favorite_count_all @include(if: $favs_all_time) {\n    favorite_count\n    __typename\n  }\n  query_favorite_count_last_24h @include(if: $favs_last_24h) {\n    favorite_count\n    __typename\n  }\n  query_favorite_count_last_7d @include(if: $favs_last_7d) {\n    favorite_count\n    __typename\n  }\n  query_favorite_count_last_30d @include(if: $favs_last_30d) {\n    favorite_count\n    __typename\n  }\n  __typename\n}\n"
  })
  headers = {
    'content-type': 'application/json',
    'X-Hasura-Api-Key': ''
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  return (response.json()["data"]["queries"][0]["query"])
  
unique_queries = query_list("DarenMatsuoka","NFT-Minting-Stats")#("perdedune","perdedune")

for c in unique_queries:
  with open("./inputs/{}_input.sql".format(c),"w") as f:
    f.write(sql_from_query(c))
