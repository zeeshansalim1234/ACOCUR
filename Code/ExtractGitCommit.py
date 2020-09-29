import git
import csv
from git import Repo
import os
import shutil
import stat
from os import path
import pandas as pd


def getCommits(input_file):
    df = pd.read_csv(input_file)
    for row in df.iterrows():
        try:
            app_id = row[1][0]
            git_package = row[1][1]
            commits_since = row[1][2]
            git_url = "https://github.com/" + git_package
            full_path = "../Output/" + app_id  # Make a temporary folder to clone the git repo
            os.makedirs(full_path)
            Repo.clone_from(git_url, full_path)
            g = git.Git(full_path)

            if pd.isnull(commits_since):
                loginfo = g.log('--no-merges', '--shortstat', '--pretty=format: %s :-:-: %cd',
                                '--date=short', '-100000')
            else:
                date_msg = '--since=' + commits_since
                loginfo = g.log(date_msg, '--no-merges', '--shortstat', '--pretty=format: %s :-:-: %cd',
                                '--date=short', '-100000')

            if os.path.exists(full_path):
                for root, dirs, files in os.walk(full_path):
                    for dir in dirs:
                        os.chmod(path.join(root, dir), stat.S_IRWXU)
                    for file in files:
                        os.chmod(path.join(root, file), stat.S_IRWXU)
                shutil.rmtree(full_path)

            commits = loginfo.split("\n\n")

            records = [["Text", "Date"]]
            for commit in commits:
                details = []
                commit_parts = commit.split("\n")
                commit_part1 = commit_parts[0].split(":-:-:")
                message = commit_part1[0].replace(',', ' _ ').replace("\n", "----")
                date = commit_part1[1]
                details.append(message)
                details.append(date)
                records.append(details)

            output_file = "../Output/Commit/Raw/" + app_id + ".csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for item in records:
                    writer.writerow(item)
            print("Total number of commits retrieved for %s : %d" % (app_id, len(commits)))
        except:
            print("Error with accessing commit messages for : ", app_id)

