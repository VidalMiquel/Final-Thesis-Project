import sys
import os
import pandas as pd


# Function to get command-line parameters
def getParameters():
    if len(sys.argv) == 3:
        return sys.argv[1], sys.argv[2]
    else:
        print("Exactly two values must be provided as arguments.")
        sys.exit(1)
        

# Function to generate dynamic paths for data and target folders
def generateDynamicPaths(experimentName, clubName):

    fileName = f"metadata{clubName}.csv"
    
    currentDir = os.path.abspath(
        os.path.dirname(__file__)
    )  # Get the current directory of the script

    targetFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "03Stage"
    )
    
    metaDataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "02Stage", fileName
    )
    dataFolder = os.path.join(
        currentDir, "..", "..", "Data", experimentName, "03Stage", "TargetFiles"
    )
    if not os.path.exists(metaDataFolder):
        print(
            f"The folder {metaDataFolder} does not exist for experiment {metaDataFolder}."
        )
        sys.exit(1)

    return metaDataFolder, dataFolder, targetFolder



def readMetadataFile(path):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    


# Function to change file names to a new format
def getIdFile(fileName):
    # Check if the file name follows the pattern "Football_day_{jornada_value}_{i+1}.json"   
    if fileName.endswith(".csv"):
        parts = fileName.split("_")
        if len(parts) >= 3 and parts[-1] == "footballDayPasses.csv":
            idValue = f"{parts[0]}_{parts[1]}"
            return idValue
        else:
            print("The file name does not follow the expected pattern.")
            return None
    else:
        print("The file name does not have a CSV extension.")
        return None
    
def getPasses(data, fileName):
    try:
        idFile = getIdFile(fileName)
        # Assuming "type_name" contains the types of passes and "pass_outcome_name" contains the outcomes
        totalPasses = data.shape[0]  # Counting the total number of passes (rows)
        incompletePasses = (data["pass_outcome_name"] == "Incomplete").sum()  # Counting incomplete passes
        completedPasses = totalPasses - incompletePasses
        # Get the first and last values of 'minute' and 'second' columns
        data['minute'] = data['minute'].astype(int)
        # Get the first and last values of 'minute' and 'second' columns
        minuteDifference = data['minute'].iloc[-1] - data['minute'].iloc[0]
        minuteDifference += 1

        # Returning the counts as a list
        return [idFile, totalPasses, completedPasses, incompletePasses, minuteDifference]
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return [None, None, None, None, None, None]  # Return None values in case of an error

    
def getPassesForFile(dataFolder):
    finalVersion = []
    # Iterate through all the files in the folder
    for fileName in os.listdir(dataFolder):
        try:
            # Join the folder path with the file name
            filePath = os.path.join(dataFolder, fileName)
            df = pd.read_csv(filePath, dtype=str)
            finalVersion.append(getPasses(df, fileName))
        except Exception as e:
            print(f"Error processing file '{fileName}': {e}")
    return finalVersion


# Function to save filtered data to a file
def saveFilteredFile(data, targetFolder):
    # Check if the segment is not empty before saving
    if not data.empty:
        try:
            data.to_csv(targetFolder, index=False, encoding="utf-8-sig")
            # print(f"File '{newFileName}' generated successfully.")
        except Exception as e:
            print(f"Error while saving the file: {e}")
    else:
        print(f"The data is empty, no file will be generated")
     
def generateFinalMetaDataFile(passesList,firstMetadataFile, targetFolder, clubName):
    
    # Convert passesList to a DataFrame for easier manipulation   
    passes_df = pd.DataFrame(passesList, columns=["IdFiles", "passes", "completePasses", "incompletePasses", "minutes"])
    
    # Merge passes_df with firstMetadataFile based on 'IdFiles'
    firstMetadataFile = pd.merge(firstMetadataFile, passes_df, on='IdFiles', how='left')
    
            
    try:
        filePath = os.path.join(targetFolder, f"finalMetadata{clubName}.csv")
        firstMetadataFile.to_csv(filePath, index=False, encoding="utf-8-sig")

    except Exception as e:
        print(f"Error while saving the file: {e}")
        
        
# Main function to execute the program
def main():
    experimentName, clubName = getParameters()
    metaDataFolder, dataFolder, targetFolder = generateDynamicPaths(experimentName, clubName)
    firstMetadataFile = readMetadataFile(metaDataFolder)
    passesList = getPassesForFile(dataFolder)
    generateFinalMetaDataFile(passesList, firstMetadataFile, targetFolder, clubName) 
    

if __name__ == "__main__":
    main()