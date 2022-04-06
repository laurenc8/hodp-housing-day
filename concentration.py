import pandas as pd

df = pd.read_csv('./data/responses.csv')

# Extract data for freshman and relevant columns
freshman_df = df[df['Are you a freshman?'] == 'Yes'].dropna(subset=['Concentration? (Please select both if joint)'])
concentration_col = freshman_df['Concentration? (Please select both if joint)']
happiness_col = freshman_df['How happy are you with your house placement?']

concentration_dict = {} # dictionary of form {id: [id's concentrations]}
happiness_by_conc = {} # dictionary of form {concentration: [sum of happiness, number of people, average happiness]}
all_conc_list = [] # list of all concentrations

for i in freshman_df.index:
  concentration_dict[i] = concentration_col[i].split(', ')
  for conc in concentration_dict[i]:
    if conc not in happiness_by_conc.keys():
      happiness_by_conc[conc] = [0, 0, 0]
      all_conc_list.append(conc)

for i in freshman_df.index:
  for conc in concentration_dict[i]:
    happiness_by_conc[conc][0] += happiness_col[i]
    happiness_by_conc[conc][1] += 1

for conc in all_conc_list:
  if happiness_by_conc[conc][1] > 4: # only include if at least 5 people in that concentration; otherwise not representative
    happiness_by_conc[conc][2] = happiness_by_conc[conc][0] / happiness_by_conc[conc][1]
  else:
    del happiness_by_conc[conc]

happiness_df = pd.DataFrame.from_dict(happiness_by_conc, orient='index',
                       columns=['Sum of Happiness', 'Number of People', 'Average Happiness'])
sorted_happiness_df = happiness_df.sort_values(by='Average Happiness', ascending=False)
print(sorted_happiness_df)