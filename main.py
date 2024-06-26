"""
title: Large Mammal Population in Elk Island National Park
author: Joanna Hao
date-created: 2022-11-25
"""
import pathlib
import sqlite3


# ----- FUNCTIONS ----- #
# --- INPUTS
def getFileContent(filename) -> list:
    """
    extracts file content into 2D array
    :param filename: str
    :return: list (2D array)
    """
    file = open(filename)
    text_list = file.readlines()
    file.close()
    # --- clean up data
    for i in range(len(text_list)):  # reading individual lines of strings from file (working w/ a string)
        if text_list[i][-1] == "\n":  # removing newline at end of lines (except last row)
            text_list[i] = text_list[i][:-1]  # to make one long string

        if '"' not in text_list[i]:  # nice data
            text_list[i] = text_list[i].split(",")
        else:
            text_list[i] = text_list[i].split('"')  # to offset a survey comment containing a comma -->
            text_list[i][0] = text_list[i][0].split(",")  # becomes 2D array (split non-survey comment items nicely by ","s)
            text_list[i][-1] = text_list[i][-1].replace(",", "")

            # turn 2D array into 1D
            text_list[i][1] = [text_list[i][1]]  # convert into list from string for concatenation of lists & remove 3rd last item (empty space from split)
            text_list[i][-1] = [text_list[i][-1]]  # convert into list from string for concatenation of lists
            text_list[i] = text_list[i][0] + text_list[i][1] + text_list[i][-1]  # concatenate lists (ends w/ 1D list)
            text_list[i].pop(-3)

        for j in range(len(text_list[i])):
            if text_list[i][j].isnumeric():
                text_list[i][j] = int(text_list[i][j])
            elif text_list[i][j] == "NA":
                text_list[i][j] = None
    return text_list


def menu() -> int:
    print("""
Please choose an option:
1. Search Population Growth
2. Add new year data
3. Population distribution by sex 
4. Exit
    """)
    return int(input("> "))


def getPopulationGrowthInputs():
    start_year = input("Start year? ")
    end_year = input("End year? ")
    species = input("Bison (1), Elk (2), Moose (3), Deer (4), or all (5)? ")
    if not (start_year.isnumeric() or end_year.isnumeric() or species.isnumeric()):
        print("Please only enter valid numbers.")
        return getPopulationGrowthInputs()
    return int(start_year), int(end_year), int(species)


def getNewYearData():
    while True:
        print("""
    NOTE:
        Some data is required while some isn't. 
        For questions without the required (R) symbol, leave the field blank if there's no data.
        """)
        park_area = input("Area of park? (R) ")
        if park_area == "" or park_area.isnumeric() or park_area.capitalize() not in ("North", "South"):
            print("Field cannot be left blank. Please only enter the appropriate text. (North/South)")
            continue
        break
    while True:
        population_year = input("Population year? (R) ")
        if population_year == "" or not population_year.isnumeric():
            print("Field cannot be left blank. Please enter a valid number for this field.")
            continue
        break
    while True:
        survey_year = input("Survey year? ")
        if survey_year == "":
            pass
        elif not survey_year.isnumeric():
            print("Please only enter numbers for this field.")
            continue
        survey_month = input("Survey month? (1-12) ")
        if survey_month == "":
            pass
        elif not survey_month.isnumeric() or not 1 <= int(survey_month) <= 12:
            print("Please enter a valid number for this field.")
            continue
        survey_day = input("Survey day? (1-31) ")
        if survey_day == "":
            pass
        elif not survey_day.isnumeric() or not 1 <= int(survey_day) <= 31:
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        species = input("Species name? (R) ")
        if species == "" or species.isnumeric():
            print("Field cannot be left blank. Please only enter the appropriate text.")
            continue
        species = species.capitalize()
        break
    while True:
        unknown_age_sex_count = input("Number of animals with unknown age and sex? ")
        if unknown_age_sex_count == "":
            pass
        elif not unknown_age_sex_count.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        adult_male = input("Number of adult males? ")
        if adult_male == "":
            pass
        elif not adult_male.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        adult_female = input("Number of adult females? ")
        if adult_female == "":
            pass
        elif not adult_female.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        unknown_adult_count = input("Number of adults of unknown sex? ")
        if unknown_adult_count == "":
            pass
        elif not unknown_adult_count.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        yearling_count = input("Number of yearlings? ")
        if yearling_count == "":
            pass
        elif not yearling_count.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        calf_count = input("Number of calves? ")
        if calf_count == "":
            pass
        elif not calf_count.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        survey_total = input("Survey total? ")
        if survey_total == "":
            pass
        elif not survey_total.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        sightability_correction_factor = input("Sightability correction factor? ")
        if sightability_correction_factor == "":
            pass
        elif not sightability_correction_factor.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        extra_captives = input("Number of additional captives? ")
        if extra_captives == "":
            pass
        elif not extra_captives.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        animals_removed = input("Number of animals removed prior to survey? ")
        if animals_removed == "":
            pass
        elif not animals_removed.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        break
    while True:
        fall_population = input("Estimate of fall population? ")
        if not fall_population.isnumeric():
            print("Please enter a valid number for this field.")
            continue
        if not fall_population.isnumeric():
            print("Please only enter numbers.")
            continue
        break
    comment = input("Survey comment: ")
    method = input("Estimate method? ")

    new_data = [park_area, population_year, survey_year, survey_month, survey_day, species, unknown_age_sex_count, adult_male, adult_female, unknown_adult_count, yearling_count, calf_count, survey_total, sightability_correction_factor, extra_captives, animals_removed, fall_population, comment, method]

    for i in range(len(new_data)):
        if new_data[i] == "":
            new_data[i] = None
        elif new_data[i].isnumeric():
            new_data[i] = int(new_data[i])
    return new_data


def getPopulationDistributionInputs():
    max_year = calcMaxYear()
    while True:
        year = input(f"What year would you like to search? (1937-{max_year}) ")
        if not (year.isnumeric() and 1937 <= int(year) <= max_year):
            print("Please enter a valid number.")
            continue
        break
    while True:
        species = input("What species would you like to search -- Bison (1), Elk (2), Moose (3), Deer (4)? ")
        if not (species.isnumeric() and 1 <= int(species) <= 4):
            print("Please select a valid option")
            continue
        break
    return int(year), int(species)


# --- Processing
def getPopulationBySex(year, species):
    """
    retrieve adult population count for each sex and total population
    :param year: int
    :return: ints or Nones
    """
    species_conversions = {1: "Bison", 2: "Elk", 3: "Moose", 4: "Deer"}
    species = species_conversions[species]

    adult_males = CURSOR.execute("""
        SELECT
            adult_male_count
        FROM
            populations
        WHERE
            population_year = ?
        AND
            species = ?
    ;""", [year, species]).fetchone()
    if not adult_males == None:
        adult_males = adult_males[0]

    adult_females = CURSOR.execute("""
        SELECT
            adult_female_count
        FROM
            populations
        WHERE
            population_year = ?
        AND
            species = ?
    ;""", [year, species]).fetchone()
    if not adult_females == None:
        adult_females = adult_females[0]

    unknown_adults = CURSOR.execute("""
        SELECT
            adult_unknown_count
        FROM
            populations
        WHERE
            population_year = ?
        AND
            species = ?
    ;""", [year, species]).fetchone()
    if not unknown_adults == None:
        unknown_adults = unknown_adults[0]
    return adult_males, adult_females, unknown_adults


def calcPopulationDistributionBySex(male, female, unknown):
    messages = []
    if male == None:
        male = 0
    if female == None:
        female = 0

    total = male + female
    if total == 0:
        messages.append("There is no population data by sex for the adult animals for this year.")
    else:
        male_proportion = male / total * 100
        if male_proportion == 0:
            messages.append("There was no male data for this year.")
        else:
            messages.append(f"The males made up {male_proportion:.2f}% of {total} adult(s), with {unknown} adult(s) of unknown sex.")

        female_proportion = female / total * 100
        if female_proportion == 0:
            messages.append("There was no female data for this year.")
        else:
            messages.append(f"The females made up {female_proportion:.2f}% of {total} adults, with {unknown} adults of unknown sex.")
    return messages


def calcMaxYear():
    global CURSOR
    all_years = CURSOR.execute("""
        SELECT
            population_year
        FROM
            populations
    ;""").fetchall()  # returns 2D array
    return all_years[-1][0]


def setupContent(data_list):
    global CURSOR, CONNECTION
    CURSOR.execute("""
        CREATE TABLE
            populations (
                park_area TEXT NOT NULL,
                population_year INTEGER NOT NULL,
                survey_year INTEGER,
                survey_month INTEGER,
                survey_day INTEGER,
                species TEXT NOT NULL,
                unknown_age_sex_count INTEGER,
                adult_male_count INTEGER,
                adult_female_count INTEGER,
                adult_unknown_count INTEGER,
                yearling_count INTEGER,
                calf_count INTEGER,
                survey_total INTEGER,
                sightability_correction_factor INTEGER,
                additional_captive_count INTEGER,
                animals_removed_before_survey INTEGER,
                fall_population_estimate INTEGER,
                survey_comment TEXT,
                estimate_method TEXT
            )
    ;""")

    for i in range(1, len(data_list)):
        CURSOR.execute("""
            INSERT INTO
                populations
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        ;""", data_list[i])

    CONNECTION.commit()


def insertNewData(list_data):
    global CURSOR, CONNECTION
    CURSOR.execute("""
        INSERT INTO
            populations
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ;""", list_data)
    CONNECTION.commit()


def getSpeciesPopulationData(year, species):
    # for specific species
    global CURSOR
    year_data = CURSOR.execute("""
        SELECT
            fall_population_estimate
        FROM
            populations
        WHERE
            population_year = ?
                AND
            species = ?
    ;""", [year, species]).fetchall()

    year_total = 0
    for i in range(len(year_data)):
        for j in range(len(year_data[i])):
            if year_data[i][j] == None:
                print(f">> Note: no data was recorded for {year}. Thus, the program is processing this year's population as 0.")
                year_data[i] = list(year_data[i])
                year_data[i][j] = 0
            year_total += year_data[i][j]
    return year_total


def getPopulationsData(year):
    # for all species
    global CURSOR, CONNECTION
    year_data = CURSOR.execute("""
        SELECT
            fall_population_estimate
        FROM
            populations
        WHERE
            population_year = ?
    ;""", [year]).fetchall()

    year_total = 0
    for i in range(len(year_data)):
        for j in range(len(year_data[i])):
            if year_data[i][j] == None:
                print(f">> Note: no data was recorded for {year}. Thus, the program is processing this year's population as 0.")
                year_data[i] = list(year_data[i])
                year_data[i][j] = 0
            year_total += year_data[i][j]
    return year_total


# --- Outputs


# --- variables
DATABASE_FILE = "large_mammals.db"
FIRST_RUN = True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False

CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()

SPECIES_OPTIONS = {1: "Bison", 2: "Elk", 3: "Moose", 4: "Deer"}

if __name__ == "__main__":
    # ----- MAIN PROGRAM CODE ----- #
    if FIRST_RUN:
        # setup everything
        CONTENT = getFileContent("Elk_Island_NP_Grassland_Forest_Ungulate_Population_1906-2017_data_reg.csv")
        setupContent(CONTENT)

    while True:
        print("--------------------------------------------------------------------------")
        print("Welcome to the Elk Island National Park Large Mammal population database! ")
        # --- inputs
        CHOICE = menu()
        if CHOICE == 1:
            START_YEAR, END_YEAR, SPECIES = getPopulationGrowthInputs()
        elif CHOICE == 2:
            NEW_DATA = getNewYearData()
        elif CHOICE == 3:
            YEAR, SPECIES = getPopulationDistributionInputs()

        # --- processing
        if CHOICE == 1:
            if SPECIES == 5:
                START_POPULATION = getPopulationsData(START_YEAR)
                END_POPULATION = getPopulationsData(END_YEAR)
                POPULATION_CHANGE = START_POPULATION - END_POPULATION
                TIME_CHANGE = START_YEAR - END_YEAR
                GROWTH = POPULATION_CHANGE/TIME_CHANGE
                if int(GROWTH) == GROWTH:
                    GROWTH = int(GROWTH)
            else:
                SPECIES = SPECIES_OPTIONS[SPECIES]
                START_POPULATION = getSpeciesPopulationData(START_YEAR, SPECIES)
                END_POPULATION = getSpeciesPopulationData(END_YEAR, SPECIES)
                POPULATION_CHANGE = START_POPULATION - END_POPULATION
                TIME_CHANGE = START_YEAR - END_YEAR
                GROWTH = POPULATION_CHANGE / TIME_CHANGE
                if int(GROWTH) == GROWTH:
                    GROWTH = int(GROWTH)
        elif CHOICE == 2:
            insertNewData(NEW_DATA)
        elif CHOICE == 3:
            ADULT_MALES, ADULT_FEMALES, UNKNOWN_ADULTS = getPopulationBySex(YEAR, SPECIES)
            ALERTS = calcPopulationDistributionBySex(ADULT_MALES, ADULT_FEMALES, UNKNOWN_ADULTS)

        # --- outputs
        if CHOICE == 1:
            print(f"The growth rate of {SPECIES} between {START_YEAR} and {END_YEAR} is {GROWTH} {SPECIES}/year.")
        elif CHOICE == 2:
            print(f"Successfully added {NEW_DATA[1]} data.")
        elif CHOICE == 3:
            for MESSAGE in ALERTS:
                print(MESSAGE)
        elif CHOICE == 4:
            print("Goodbye!")
            exit()
        else:
            print("Please enter a valid option number")
