"""Module providing computations methods for desired tasks."""

import os
import json
import pandas as pd


class DataIngestor:
    """Class representing the data processor."""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.required_columns = ['LocationDesc', 'Question',
                                 'StratificationCategory1', 
                                 'Stratification1', 'Data_Value']
        self.df = pd.read_csv(self.csv_path, usecols=self.required_columns)

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

    def check_directory(self, directory_name):
        """Function responsible for checking if the folder exists."""
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

    def average_each_state(self, question):
        """Function responsible for computing the average for each state."""
        df = self.df
        df_filtered = df[df['Question'] == question]
        state_averages = df_filtered.groupby('LocationDesc')['Data_Value'].mean().reset_index()

        sorted_states = state_averages.sort_values(by='Data_Value')

        sorted_states_dict = dict(zip(sorted_states['LocationDesc'], sorted_states['Data_Value']))

        return sorted_states_dict

    def states_mean(self, job_id, question):
        """Function responsible for computing the mean for all states."""
        sorted_states_dict = self.average_each_state(question)

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(sorted_states_dict, json_file, separators=(', ', ': '))

    def state_mean(self, job_id, question, state):
        """Function responsible for computing the mean for specific state."""
        df = self.df
        df_filtered = df[(df['Question'] == question) & (df['LocationDesc'] == state)]
        state_average = df_filtered['Data_Value'].mean()

        state_dict = {state: state_average}

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(state_dict, json_file, separators=(', ', ': '))

    def best_five(self, job_id, question):
        """Function responsible for computing the best fives for a specific question."""
        sorted_states_dict = self.average_each_state(question)
        five = {}

        if question in self.questions_best_is_min:
            five = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[:5]}
        else:
            temp = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[-5:]}
            five = {k: temp[k] for k in reversed(list(temp.keys()))}

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(five, json_file, separators=(', ', ': '))

    def worst_five(self, job_id, question):
        """Function responsible for computing the worst fives for a specific question."""
        sorted_states_dict = self.average_each_state(question)
        five = {}

        if question in self.questions_best_is_max:
            five = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[:5]}
        else:
            temp = {k: sorted_states_dict[k] for k in list(sorted_states_dict.keys())[-5:]}
            five = {k: temp[k] for k in reversed(list(temp.keys()))}

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(five, json_file, separators=(', ', ': '))

    def overall_average(self, question):
        """Function responsible for computing the overall average."""
        df = self.df
        df_filtered = df[df['Question'] == question]

        overall_mean = df_filtered['Data_Value'].mean()

        return overall_mean

    def global_mean(self, job_id, question):
        """Function responsible for computing the global mean."""
        result = self.overall_average(question)
        result_dict = {"global_mean": result}

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(result_dict, json_file, separators=(', ', ': '))

    def state_diff_from_mean(self, job_id, question, state):
        """Function responsible for the difference from global mean with state's."""
        global_mean = self.overall_average(question)
        df = self.df
        df_filtered = df[(df['Question'] == question) & (df['LocationDesc'] == state)]

        state_average = df_filtered['Data_Value'].mean()

        new_value = float(global_mean - state_average)
        state_dict = {state: new_value}

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(state_dict, json_file, separators=(', ', ': '))

    def diff_from_mean(self, job_id, question):
        """Function responsible for the difference from global mean with all states."""
        global_mean = self.overall_average(question)
        df = self.df
        state_diff_dict = {}

        for state in df['LocationDesc'].unique():
            df_filtered = df[(df['Question'] == question) & (df['LocationDesc'] == state)]
            df_filtered = df_filtered.dropna(subset=['Data_Value'])

            if not df_filtered.empty:
                state_average = df_filtered['Data_Value'].mean()

                state_diff = float(global_mean - state_average)

                state_diff_dict[state] = state_diff

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(state_diff_dict, json_file, separators=(', ', ': '))

    def compute_state_averages(self, state, question, all_states):
        """Function responsible for computing the state average for all states."""
        df = self.df
        df_state_question = df[(df['LocationDesc'] == state) & (df['Question'] == question)]

        # Group by 'StratificationCategory1' and calculate the mean for each category, subcategory
        state_averages = {}
        for category, group in df_state_question.groupby('StratificationCategory1'):
            subcategory_averages = group.groupby('Stratification1')['Data_Value'].mean().to_dict()
            if not all_states:
                formatted_subcategory_averages = {f"('{category}', '{subcategory}')":
                                        value for subcategory,
                                        value in subcategory_averages.items()}
            else:
                formatted_subcategory_averages = {f"('{state}', '{category}', '{subcategory}')":
                                        value for subcategory,
                                        value in subcategory_averages.items()}

            state_averages.update(formatted_subcategory_averages)

        return state_averages

    def state_mean_by_category(self, job_id, question, state):
        """Function responsible for computing the mean by category for a specific state."""
        state_averages = self.compute_state_averages(state, question, False)

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump({state: state_averages}, json_file, separators=(', ', ': '))

    def mean_by_category(self, job_id, question):
        """Function responsible for computing the mean by category for all states."""
        all_state_averages = {}
        all_states = self.df['LocationDesc'].unique()

        # Iterate over each state
        for state in all_states:
            state_averages = self.compute_state_averages(state, question, True)
            all_state_averages.update(state_averages)

        with open(f"results/{job_id}.json", mode = "w", encoding = "utf-8") as json_file:
            json.dump(all_state_averages, json_file, separators=(', ', ': '))
