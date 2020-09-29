import os
from os import path
import stat
import shutil
import Code.ExtractGitCommit as getcommits
import Code.ExtractGPReviews as getreviews
import Code.ProcessReview as pr
import Code.ProcessCommit as pc
import Code.Classifier as cls
import Code.CompatibilityTypes as cType
import Code.Finalize as cmp

INPUT_FILE = "../Data/appfile.csv"

def create_output_structure(choice):
    OUTPUT_PATH = "../Output"

    if os.path.exists(OUTPUT_PATH):
        for root, dirs, files in os.walk(OUTPUT_PATH):
            for dir in dirs:
                os.chmod(path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(path.join(root, file), stat.S_IRWXU)
        shutil.rmtree(OUTPUT_PATH)

    os.makedirs(OUTPUT_PATH)
    os.makedirs(OUTPUT_PATH + "/FINAL")

    if choice == 1:
        os.makedirs(OUTPUT_PATH + "/Review")
        os.makedirs(OUTPUT_PATH + "/Review/Raw")
        os.makedirs(OUTPUT_PATH + "/Review/Processed")
        os.makedirs(OUTPUT_PATH + "/Review/Compatible")
        os.makedirs(OUTPUT_PATH + "/Review/CTypes")

    elif choice == 2:
        os.makedirs(OUTPUT_PATH + "/Commit")
        os.makedirs(OUTPUT_PATH + "/Commit/Raw")
        os.makedirs(OUTPUT_PATH + "/Commit/Processed")
        os.makedirs(OUTPUT_PATH + "/Commit/Compatible")
        os.makedirs(OUTPUT_PATH + "/Commit/CTypes")

    else:
        os.makedirs(OUTPUT_PATH + "/Review")
        os.makedirs(OUTPUT_PATH + "/Review/Raw")
        os.makedirs(OUTPUT_PATH + "/Review/Processed")
        os.makedirs(OUTPUT_PATH + "/Review/Compatible")
        os.makedirs(OUTPUT_PATH + "/Review/CTypes")
        os.makedirs(OUTPUT_PATH + "/Commit")
        os.makedirs(OUTPUT_PATH + "/Commit/Raw")
        os.makedirs(OUTPUT_PATH + "/Commit/Processed")
        os.makedirs(OUTPUT_PATH + "/Commit/Compatible")
        os.makedirs(OUTPUT_PATH + "/Commit/CTypes")


def main():
    print("Hello, welcome to the ICCUR Tool.....")

    initial_choice = 0
    while (initial_choice != 1 and initial_choice != 2 and initial_choice != 3):
        initial_choice = int(input(
            "What do you want to analyze today?: Enter 1 for Reviews only, 2 for Commits only, and 3 for Both : "))

    create_output_structure(initial_choice)

    if initial_choice == 1:
        input_choice = ""
        while (input_choice != 'Y' and input_choice != 'N'):
            input_choice = input(
                "Is the input file updated with the Google Play package name (Y or N) : ").upper()
        if input_choice == 'N':
            print("Please update the file and try again ....")
        else:
            print("Fetching reviews from the Google Play ..... please wait ")
            getreviews.get_reviews(INPUT_FILE)
            print("Reviews extraction process is complete.")
            print("Now the reviews are being processed and cleaned. This can take some time, please wait .....")
            pr.CleanReviews()
            print("Review pre-processing and cleaning is complete.")
            print("Now, the tool is identifying the compatibility related reviews.")
            print("Would you like to use the pre-trained model or train with a new dataset? Enter you choice :")
            comp_choice = ""
            while comp_choice != 1 and comp_choice != 2:
                comp_choice = int(input("1 for pre-trained saved model, 2 to train with new data : "))

            if comp_choice == 1:
                print("Using pre-trained models to identify compatibility related reviews")
                cls.Get_Compatible_Reviews_withSavedModels()
            else:
                print("Training with new data set to identify compatibility related reviews")
                cls.Get_Compatible_Reviews_withNewTrainingSet()

            print("Compatibility classification is complete. Now it's time to identify the types")
            print("Would you like to use the pre-trained model or train with a new dataset? Enter you choice :")
            comp_choice = ""
            while comp_choice != 1 and comp_choice != 2:
                comp_choice = int(input("1 for pre-trained saved model, 2 to train with new data : "))

            if comp_choice == 1:
                print("Using pre-trained models to identify compatibility types in reviews")
                cType.Get_Reviews_Types_withSavedModels()
            else:
                print("Training with new data set to identify compatibility types in reviews")
                cls.Get_Compatible_Reviews_withNewTrainingSet()
            print("Compatibility types have been identified. It's time for the final results")

            cmp.ReviewSummary()
            print("Done.... The FINAL folder in Output has the combined result. Thank you")

    elif initial_choice == 2:
        input_choice = ""
        while (input_choice != 'Y' and input_choice != 'N'):
            input_choice = input(
                "Is the input file updated with the GitHub Repository name (Y or N) : ").upper()
        if input_choice == 'N':
            print("Please update the file and try again ....")
        else:
            print("Fetching commits from GitHub ..... please wait ")
            getcommits.getCommits(INPUT_FILE)
            print("Commit message extraction process is complete.")
            print("Now the messages are being processed and cleaned. This can take some time, please wait .....")
            pc.CleanCommitMessage()
            print("Commit message pre-processing and cleaning is complete.")

            print("Now, the tool is identifying the compatibility fixes done in commits.")
            print("Would you like to use the pre-trained model or train with a new dataset? Enter you choice :")
            comp_choice = ""
            while comp_choice != 1 and comp_choice != 2:
                comp_choice = int(input("1 for pre-trained saved model, 2 to train with new data : "))

            if comp_choice == 1:
                print("Using pre-trained models to identify compatibility related fixes")
                cls.Get_Compatible_Commits_withSavedModels()
            else:
                print("Training with new data set to identify compatibility related fixes")
                cls.Get_Compatible_Commits_withNewTrainingSet()

            print("Compatibility classification is complete. Now it's time to identify the types")
            print("Would you like to use the pre-trained model or train with a new dataset? Enter you choice :")
            comp_choice = ""
            while comp_choice != 1 and comp_choice != 2:
                comp_choice = int(input("1 for pre-trained saved model, 2 to train with new data : "))

            if comp_choice == 1:
                print("Using pre-trained models to identify compatibility types in commits")
                cType.Get_Commit_Types_withSavedModels()
            else:
                print("Training with new data set to identify compatibility types in commits")
                cType.Get_Commit_Types_withNewTrainingSet()
            print("Compatibility types have been identified. It's time for the final results")

            cmp.CommitSummary()
            print("Done.... The FINAL folder in Output has the combined result. Thank you")

    else:

        input_choice = ""
        while (input_choice != 'Y' and input_choice != 'N'):
            input_choice = input(
                "Is the input file updated with the Google Play package name and GitHub Repository name (Y or N) : ").upper()

        if input_choice == 'N':
            print("Please update the file and try again ....")
        else:
            print("Fetching reviews from the Google Play ..... please wait ")
            getreviews.get_reviews(INPUT_FILE)
            print("Reviews extraction process is complete.")

            print("Fetching commits from GitHub ..... please wait ")
            getcommits.getCommits(INPUT_FILE)
            print("Commit message extraction process is complete.")

            print("Now the reviews and commits are being processed and cleaned. This can take some time, please wait .....")
            pr.CleanReviews()
            pc.CleanCommitMessage()
            print("Review and Commit message pre-processing and cleaning is complete.")

            print("Now, the tool will identify the compatibility related records.")

            print("Would you like to use the pre-trained model or train with a new dataset? Enter you choice :")
            comp_choice = ""
            while comp_choice != 1 and comp_choice != 2:
                comp_choice = int(input("1 for pre-trained saved model, 2 to train with new data : "))

            if comp_choice == 1:
                print("Using pre-trained models to identify compatibility related reviews")
                cls.Get_Compatible_Reviews_withSavedModels()
                print("Using pre-trained models to identify compatibility related fixes")
                cls.Get_Compatible_Commits_withSavedModels()
            else:
                print("Training with new data set to identify compatibility related reviews")
                cls.Get_Compatible_Reviews_withNewTrainingSet()
                print("Training with new data set to identify compatibility related fixes")
                cls.Get_Compatible_Commits_withNewTrainingSet()

            print("Compatibility classification is complete. Now it's time to identify the types")

            print("Would you like to use the pre-trained model or train with a new dataset? Enter you choice")
            comp_choice = ""
            while comp_choice != 1 and comp_choice != 2:
                comp_choice = int(input("1 for pre-trained saved model, 2 to train with new data : "))

            if comp_choice == 1:
                print("Using pre-trained models to identify compatibility types in reviews")
                cType.Get_Reviews_Types_withSavedModels()
                print("Using pre-trained models to identify compatibility types in commit")
                cType.Get_Commit_Types_withSavedModels()
            else:
                print("Training with new data set to identify compatibility types in reviews")
                cType.Get_Reviews_Types_withNewTrainingSet()
                print("Training with new data set to identify compatibility types in commit")
                cType.Get_Commit_Types_withNewTrainingSet()

            print("Compatibility types have been identified. It's time for the final results")

            print("This tool looks for all commits done within 30 days after a review post")
            choice = input("Do you want to change the duration (Y on N) : ").upper()
            duration = 30
            if choice == 'Y':
                duration = int(input("Enter the desired duration in days: "))

            cmp.CombinedSummary(duration)
            print("Done.... The FINAL folder in Output has the combined result. Thank you")





main()