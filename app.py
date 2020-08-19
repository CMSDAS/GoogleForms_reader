import os
import pandas as pd
from unidecode import unidecode

NAME_PRE_EXERCISES = ['FirstSet', 'SecondSet', 'ThirdSet', 'FourthSet', 'FifthSet', 'SixthSet']
USER_COLUMN_REF = "Please enter your name (FirstName LastName)"
FOLDER_DATA = 'documents/'


def compare_names(name1, name2):
    """
    To match name:
    - Normalization using unidecode --> drop accents...
    - Lowercase comparison
    - Check if at lease one of the name match with the users dataset
    """
    same_name = False
    a_list = unidecode(name1.lower()).split(" ")
    b_list = unidecode(name2.lower()).split(" ")
    list_matching_names = set(a_list).intersection(b_list)
    if list_matching_names:
        same_name = True
    return same_name


def run():
    ########## READ THE CSV WITH THE USERS INFORMATION ##########
    user_data = pd.read_csv('users.csv')
    not_found = []
    ########## ITERATE OVER EACH SET OF EXERCISES ##########
    for set_name in NAME_PRE_EXERCISES:
        user_data[set_name] = ""

        for file in os.listdir(FOLDER_DATA + set_name):
            ########## ONLY STUDY THE CSV FILE WITH THE RESULTS ##########
            if ".csv" in file:
                df_result = pd.read_csv(FOLDER_DATA + set_name + "/" + file)
                ########## ITERATE OVER EACH USER FOUND ON THE PRE-EXERCISE ##########
                for index, row in df_result.iterrows():
                    ########## MATCH THE USERNAME AND EMAIL WITH THE DATASET ##########
                    locate_user_email = user_data["Email"].apply(lambda x: compare_names(x, row["Username"]))
                    locate_user_username = user_data["Name"].apply(lambda x: compare_names(x, row[USER_COLUMN_REF]))
                    ########## IF THE USER IS NOT FOUND APPEND ON A LIST TO DEBUG IT LATER ##########
                    if user_data.loc[locate_user_email].empty and user_data.loc[locate_user_username].empty:
                        user = [row["Username"], row[USER_COLUMN_REF]]
                        user_repeated = [element for element in not_found if element[1] == row[USER_COLUMN_REF]]
                        if not user_repeated:
                            not_found.append(user)
                    ########## IF USER FOUND SET TO 1 THE STATUS OF THIS PRE-EXERCISE ##########
                    else:
                        user_data.loc[locate_user_email | locate_user_username, set_name] = 1
                break

    ########## WRITE A CSV WITH THE RESULTS ##########
    user_data.to_csv('user_data.csv')

    ########## PRINT THE USERS THAT DID SOME PRE-EXERCISE BUT ARE NOT ON THE DATASET ##########
    print('{} unmatched people: \n {}'.format(len(not_found), not_found))


if __name__ == "__main__":
    run()


