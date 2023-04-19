import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd

def moneyline(team1, team2, odds1, odds2):
      model = keras.models.load_model("classification2")

  # Define the team names
  team1 = input("What is your first team? (3 letter code) ")
  team2 = input("What is your second team? (3 letter code) ")
  odds1 = float(input(f"What are the odds for {team1}? "))
  odds2 = float(input(f"What are the odds for {team2}? "))

  # Load the statistics for both teams
  raw_stats = pd.read_csv("2023_model_1_stats.csv")
  stats = raw_stats[['team', 'off_rtg', 'def_rtg', 'efg', 'reb_diff']]

  team_raptor_dict = []
  unique_teams = raw_raptor['Tm'].unique()
  for team_name in raw_raptor['Tm'].unique():
    team_raptor_data = raw_raptor[raw_raptor['Tm'] == team_name]
    for index, row in team_raptor_data.iterrows():
      team_raptor_data.at[index, 'RAPTOR'] = team_raptor_data.at[index, 'RAPTOR']*float(team_raptor_data.at[index, 'MP'])
    adj_raptor = team_raptor_data['RAPTOR'].sum()/48
    team_w_raptor = {"team": team_name, "raptor": adj_raptor}
    team_raptor_dict.append(team_w_raptor)

  team_raptors = pd.DataFrame(team_raptor_dict)
      
  for index3, row3 in stats.iterrows():
    for index4, row4, in team_raptors.iterrows():
      if stats.at[index3, 'team'] in team_raptors.loc[index4, 'team']:
          stats.at[index3, 'raptor'] = team_raptors.loc[index4, 'raptor']

  test_row = pd.DataFrame(columns = ["off_rtg", 'def_rtg', 'efg', 'reb_diff', 'raptor', 'off_rtg2', 'def_rtg2', 'efg2', 'reb_diff2','raptor2'])
  for i in range(1):
      for x, row2 in stats.iterrows():
          if team1 in stats.loc[x, 'team']:
              test_row.at[i, "off_rtg"] = stats.loc[x, 'off_rtg']
              test_row.at[i, "def_rtg"] = stats.loc[x, 'def_rtg']
              test_row.at[i, "efg"] = stats.loc[x, 'efg']
              test_row.at[i, "reb_diff"] = stats.loc[x, 'reb_diff']
              test_row.at[i,'raptor'] = stats.loc[x,'raptor']
          if team2 in stats.loc[x, 'team']:
              test_row.at[i, "off_rtg2"] = stats.loc[x, 'off_rtg']
              test_row.at[i, "def_rtg2"] = stats.loc[x, 'def_rtg']
              test_row.at[i, "efg2"] = stats.loc[x, 'efg']
              test_row.at[i, "reb_diff2"] = stats.loc[x, 'reb_diff']
              test_row.at[i,'raptor2'] = stats.loc[x,'raptor']

  test_row = np.asarray(test_row).astype('float32')

  # Predict the outcome and probability for team 1
  predictions = model.predict(test_row)
  team1_prob = predictions[0][0]
  team2_prob = 1-team1_prob
  print(f"The probability of {team1} winning is {team1_prob:.2f}")
  print(f"The probability of {team2} winning is {team2_prob:.2f}")

  #evaluate which side to bet
  if odds1 < 0:
      prob1 = abs(odds1)/(abs(odds1) +100)
  elif odds1 > 0:
      prob1 = 100/(odds1+100)
  if odds2 < 0:
      prob2 = abs(odds2)/(abs(odds2) +100)
  elif odds2 > 0:
      prob2 = 100/(odds2+100)
  my_dict = {
  'ATL': 'Atlanta Hawks',
  'BOS': 'Boston Celtics',
  'BRK': 'Brooklyn Nets',
  'CHO': 'Charlotte Hornets',
  'CHI': 'Chicago Bulls',
  'CLE': 'Cleveland Cavaliers',
  'DAL': 'Dallas Mavericks',
  'DEN': 'Denver Nuggets',
  'DET': 'Detroit Pistons',
  'GSW': 'Golden State Warriors',
  'HOU': 'Houston Rockets',
  'IND': 'Indiana Pacers',
  'LAC': 'LA Clippers',
  'LAL': 'LA Lakers',
  'MEM': 'Memphis Grizzlies',
  'MIA': 'Miami Heat',
  'MIL': 'Milwaukee Bucks',
  'MIN': 'Minnesota Timberwolves',
  'NOP': 'New Orleans Pelicans',
  'NYK': 'New York Knicks',
  'OKC': 'Oklahoma City Thunder',
  'ORL': 'Orlando Magic',
  'PHI': 'Philadelphia 76ers',
  'PHO': 'Phoenix Suns',
  'POR': 'Portland Trailblazers',
  'SAC': 'Sacramento Kings',
  'SAS': 'San Antonio Spurs',
  'TOR': 'Toronto Raptors',
  'UTA': 'Utah Jazz',
  'wAS': 'Washington Wizards'
  }
  if team1 in my_dict:
      team1 = my_dict.get(team1)
  if team2 in my_dict:
      team2 = my_dict.get(team2)
  if team1_prob > prob1 and team2_prob < prob2:
      print(f"Betting on the {team1} is the more favorable bet.")
      return team1
  elif team1_prob < prob1 and team2_prob > prob2:
      print(f"Betting on the {team2} is the more favorable bet. ")
      return team2
  elif team1_prob < prob1 and team2_prob < prob2:
      if prob1 - team1_prob < prob2 - team2_prob:
          print(f"Betting on the {team1} is the more favorable bet.")
          return team1
      elif prob1 - team1_prob > prob2 - team2_prob:
          print(f"Betting on the {team2} is the more favorable bet.")
          return team2
  elif team1_prob > prob1 and team2_prob > prob2: 
      if prob1 - team1_prob < prob2 - team2_prob:
          print(f"Betting on the {team2} is the more favorable bet.")
          return team2
      elif prob1 - team1_prob > prob2 - team2_prob:
          print(f"Betting on the {team1} is the more favorable bet.")
          return team1
          