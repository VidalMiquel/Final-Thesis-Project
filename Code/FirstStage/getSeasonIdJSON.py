import json
import urllib.request
import os
import sys


def getExperimentName():
    # Check if the proper arguments were provided
    if len(sys.argv) != 2:
        print(
            "Please provide values for CompetitionName, CompetitionYear, CompetitionGender, and Club."
        )
        return None

    # Get the argument values
    experimentName = sys.argv[1]

    return experimentName


def getChosenSeasonDataJson(fileName):
    with open(fileName, "r") as file:
        data = json.load(file)
    return data


def getParameters(data):
    results = data["results"]
    return results["competitionId"], results["seasonId"]


def buildUrl(competitionId, seasonId):
    return f"https://github.com/VidalMiquel/Statsbomb/raw/master/data/matches/{competitionId}/{seasonId}.json"


def downloadFile(url, fileName):
    try:
        urllib.request.urlretrieve(url, fileName)
        print(
            f"The file season_id.json has been downloaded successfully."
        )
    except Exception as e:
        print(
            f"Failed to download the file. Error: {e}"
        )


currentPath = os.path.abspath(os.path.dirname(__file__))
experimentName = getExperimentName()

inputPath = os.path.abspath(
    os.path.join(
        currentPath,
        "..",
        "..",
        "Data",
        experimentName,
        "FirstStage",
        "MiddleFiles",
    )
)
outputPath = os.path.abspath(
    os.path.join(
        currentPath,
        "..",
        "..",
        "Data",
        experimentName,
        "FirstStage",
        "MiddleFiles",
    )
)

chosenSeasonFileName = "chosenSeasonData.json"
chosenSeasonFilePath = os.path.join(
    inputPath, chosenSeasonFileName
)

dataFrame = getChosenSeasonDataJson(chosenSeasonFilePath)

competitionId, seasonId = getParameters(dataFrame)

url = buildUrl(competitionId, seasonId)

downloadFileName = "seasonId.json"
downloadFilePath = os.path.join(outputPath, downloadFileName)

downloadFile(url, downloadFilePath)
