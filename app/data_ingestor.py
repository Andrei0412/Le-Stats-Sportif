import os
import json
import csv
from collections import defaultdict
import pandas as pd


class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        self.csv_path = csv_path

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def check_directory(directory_name):
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        pass

    def average_each_state(self, question):
        df = pd.read_csv(self.csv_path)

        # Filter rows where the question is "Percent of adults aged 18 years and older who have an overweight classification"
        df_filtered = df[df['Question'] == question]

        # Group by state and calculate the mean of 'Data_Value'
        state_averages = df_filtered.groupby('LocationDesc')['Data_Value'].mean().reset_index()

        # Sort by the mean values
        sorted_states = state_averages.sort_values(by='Data_Value')

        # Convert DataFrame to a dictionary
        sorted_states_dict = dict(zip(sorted_states['LocationDesc'], sorted_states['Data_Value']))

        return sorted_states_dict
    

    def states_mean(self, job_id, question):
        sorted_states_dict = self.average_each_state(question)

        # Write the result to a JSON file
        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(sorted_states_dict, json_file, separators=(', ', ': '))

    
    def state_mean(self, job_id, question, state):
        df = pd.read_csv(self.csv_path)

        # Filter rows where the question is "Percent of adults aged 18 years and older who have an overweight classification"
        df_filtered = df[(df['Question'] == question) & (df['LocationDesc'] == state)]

        # Calculate the mean of 'Data_Value'
        state_average = df_filtered['Data_Value'].mean()

        # Create a dictionary with the state and its average value
        state_dict = {state: state_average}

        # Write the result to a JSON file
        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(state_dict, json_file, separators=(', ', ': '))


    def best_five(self, job_id, question):
        sorted_states_dict = self.average_each_state(question)
        five = {}

        if question in self.questions_best_is_min:
            five = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[:5]}
        else:
            temp = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[-5:]}
            five = {k: temp[k] for k in reversed(list(temp.keys()))}

        # Write the result to a JSON file
        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(five, json_file, separators=(', ', ': '))


    def worst_five(self, job_id, question):
        sorted_states_dict = self.average_each_state(question)
        five = {}

        if question in self.questions_best_is_max:
            five = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[:5]}
        else:
            temp = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[-5:]}
            five = {k: temp[k] for k in reversed(list(temp.keys()))}

        # Write the result to a JSON file
        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(five, json_file, separators=(', ', ': '))

    
    def overal_average(self, question):
        df = pd.read_csv(self.csv_path)

        # Filter rows where the question is specified
        df_filtered = df[df['Question'] == question]

        # Calculate the overall mean of 'Data_Value'
        overall_mean = df_filtered['Data_Value'].mean()

        result = overall_mean

        return result

    
    def global_mean(self, job_id, question):
        result = self.overal_average(question)

        result_dict = {"global_mean": result}

        # Write the result to a JSON file
        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(result_dict, json_file, separators=(', ', ': '))


    def state_diff_from_mean(self, job_id, question, state):
        global_mean = self.overal_average(question)

        df = pd.read_csv(self.csv_path)

        # Filter rows where the question is "Percent of adults aged 18 years and older who have an overweight classification"
        df_filtered = df[(df['Question'] == question) & (df['LocationDesc'] == state)]

        # Calculate the mean of 'Data_Value'
        state_average = df_filtered['Data_Value'].mean()

        new_value = float(global_mean - state_average)
        state_dict = {state: new_value}

        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(state_dict, json_file, separators=(', ', ': '))

        
    def diff_from_mean(self, job_id, question):
        global_mean = self.overal_average(question)

        df = pd.read_csv(self.csv_path)

        state_diff_dict = {}

        for state in df['LocationDesc'].unique():
            # Filter rows for the current state and question
            df_filtered = df[(df['Question'] == question) & (df['LocationDesc'] == state)]

            # Calculate the mean of 'Data_Value' for the current state
            state_average = df_filtered['Data_Value'].mean()

            # Compute the difference from the global mean
            state_diff = float(global_mean - state_average)

            # Store the difference in a dictionary with the state as the key
            state_diff_dict[state] = state_diff

        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(state_diff_dict, json_file, separators=(', ', ': '))

    def compute_state_averages(self, state, question):
        # Read CSV file into a DataFrame
        df = pd.read_csv(self.csv_path)
    
        # Filter rows for the given state and question
        df_state_question = df[(df['LocationDesc'] == state) & (df['Question'] == question)]
    
        # Group by 'StratificationCategory1' and calculate the mean for each category and its variations
        state_averages = {}
        for category, group in df_state_question.groupby('StratificationCategory1'):
            subcategory_averages = group.groupby('Stratification1')['Data_Value'].mean().to_dict()
            formatted_subcategory_averages = {f"('{category}', '{subcategory}')": value for subcategory, value in subcategory_averages.items()}
            state_averages.update(formatted_subcategory_averages)
        
        return state_averages

    def state_mean_by_category(self, job_id, question, state):
        # Compute state averages for the specified state and question
        state_averages = self.compute_state_averages(state, question)
    
        # Write the result to a JSON file
        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump({state: state_averages}, json_file, separators=(', ', ': '))

    def mean_by_category(self, job_id, question):
        # Define a dictionary to store state averages for all states
        all_state_averages = {}
        
        # Get a list of all states
        all_states = pd.read_csv(self.csv_path)['LocationDesc'].unique()
        
        # Iterate over each state
        for state in all_states:
            # Compute state averages for the specified state and question
            state_averages = self.compute_state_averages(state, question)
            all_state_averages[state] = state_averages
        
        # Write the result to a JSON file
        with open(f"results/{job_id}.json", 'w') as json_file:
            json.dump(all_state_averages, json_file, separators=(', ', ': '))









        


