import pandas as pd

df = pd.read_csv('./data/responses.csv')

# Extract data for freshman and relevant columns
freshman_df = df[df['Are you a freshman?'] == 'Yes'].dropna(subset=['Concentration? (Please select both if joint)'])
concentration_col = freshman_df['Concentration? (Please select both if joint)']
happiness_col = freshman_df['How happy are you with your house placement?']
house_col = freshman_df['What house did you get placed in through the housing lottery?']

concentration_dict = {} # dictionary of form {id: [id's concentrations]}
happiness_by_conc = {} # dictionary of form {concentration: [sum of happiness, number of people, average happiness]}
house_rank_by_conc = {} # dictionary of form {concentration: [average rank for each of the 12 houses]}
house_rank_by_conc_counts = {} # dictionary of form {concentration: [number of people who ranked each of the 12 houses]}
all_conc_list = [] # list of all concentrations
all_house_dict = {} # dictionary of form {house: index}
all_house_dict_reverse = {} # dictionary of form {index: house}

count = 0
for i in freshman_df.index:
  if house_col[i] not in all_house_dict.keys():
    all_house_dict[house_col[i]] = count
    all_house_dict_reverse[count] = house_col[i]
    count += 1

for i in freshman_df.index:
  concentration_dict[i] = concentration_col[i].split(', ')
  for conc in concentration_dict[i]:
    if conc not in happiness_by_conc.keys():
      happiness_by_conc[conc] = [0, 0, 0]


for i in freshman_df.index:
  for conc in concentration_dict[i]:
    happiness_by_conc[conc][0] += happiness_col[i]
    happiness_by_conc[conc][1] += 1
    if conc not in all_conc_list:
      all_conc_list.append(conc)

for conc in all_conc_list:
  if happiness_by_conc[conc][1] > 4: # only include if at least 5 people in that concentration; otherwise not representative
    happiness_by_conc[conc][2] = happiness_by_conc[conc][0] / happiness_by_conc[conc][1]
  else:
    del happiness_by_conc[conc]

happiness_df = pd.DataFrame.from_dict(happiness_by_conc, orient='index',
                       columns=['Sum of Happiness', 'Number of People', 'Average Happiness'])
sorted_happiness_df = happiness_df.sort_values(by='Average Happiness', ascending=False)
print(sorted_happiness_df)

# For each concentration, find average rank for each house
for conc in all_conc_list:
  house_rank_by_conc[conc] = [0] * 12
  house_rank_by_conc_counts[conc] = [0] * 12

for i in freshman_df.index:
  ranked_houses = [freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [1st]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [2nd]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [3rd]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [4th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [5th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [6th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [7th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [8th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [9th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [10th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [11th]'][i],
                    freshman_df['Now that you have been placed in a house, what is your ranking of the Harvard houses? [12th]'][i]]
  for conc in concentration_dict[i]:
    for j in range(12):
      house_rank_by_conc[conc][all_house_dict[ranked_houses[j]]] += j + 1
      house_rank_by_conc_counts[conc][all_house_dict[ranked_houses[j]]] += 1

for conc in house_rank_by_conc.keys():
  for i in range(12):
    if house_rank_by_conc_counts[conc][i] > 0:
      house_rank_by_conc[conc][i] = round(house_rank_by_conc[conc][i]/house_rank_by_conc_counts[conc][i], 2)

house_rank_df = pd.DataFrame.from_dict(house_rank_by_conc, orient='index',
                       columns=[all_house_dict_reverse[0],
                                all_house_dict_reverse[1],
                                all_house_dict_reverse[2],
                                all_house_dict_reverse[3],
                                all_house_dict_reverse[4],
                                all_house_dict_reverse[5],
                                all_house_dict_reverse[6],
                                all_house_dict_reverse[7],
                                all_house_dict_reverse[8],
                                all_house_dict_reverse[9],
                                all_house_dict_reverse[10],
                                all_house_dict_reverse[11],])
house_rank_df = house_rank_df.drop_duplicates().rename(index={'Theater': 'Theater, Dance, & Media', 'Art': 'Art, Film, and Visual Studies', 'Study of Women': 'Study of Women, Gender, and Sexuality'})
house_rank_df.to_csv('Average House Rank by Concentration.csv')