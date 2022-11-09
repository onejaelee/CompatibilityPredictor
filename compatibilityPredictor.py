# -*- coding: utf-8 -*-
"""
@author: One
"""
import json
import numpy as np
from numpy.linalg import norm


def extractAttributes(jsonData):
    teamAttributes = []
#Organizes metrics and gives weight to each metric into a matrix to do cosineSimilarity calculation
#Input for teamattribute averages need to be weighted the same as indvAttributes for it to properly weight values
    for member in jsonData["team"]:
        indvAttributes = []
        for attribute in member["attributes"]:
            #Weights for different attributes, intelligence given highest weight and spicyFoodTolerance the lowest
            #Set all to 1.0 coefficient for non-weighted cosine similarity score
            
            if attribute == "intelligence":
                indvAttributes.append(1.5*member["attributes"][attribute])
            elif attribute == "spicyFoodTolerance":
                indvAttributes.append(0.75*member["attributes"][attribute])
            else:
                indvAttributes.append(1*member["attributes"][attribute])
        teamAttributes.append(indvAttributes)
    return teamAttributes

#Simply takes in all the team attributes and gives a list containing corresponding averages for each metric
def averageAttributes(teamAttributes):
    return [sum(col)/len(col) for col in zip(*teamAttributes)]

def cosineSimilarity(applicantAttributes,averageAttributes):
    #A is the applicant attributes, B is team average attributes, used for basic cosine similarity calculation
    A = np.array(applicantAttributes)
    B = np.array(averageAttributes)
    return np.dot(A,B)/(norm(A)*norm(B))


def calculateSimilarity(jsonData,averageAttributes):
    
    simList = []

    #Organizes metrics and gives weight to each metric into a matrix to do cosineSimilarity calculation
    for applicant in jsonData["applicants"]:
        indvAttributes = []
        for attribute in applicant["attributes"]:
            #Weights for different attributes, intelligence given highest weight and spicyFoodTolerance the lowest
            #Set all to 1.0 coefficient for non-weighted cosine similarity score
            if attribute == "intelligence":
                indvAttributes.append(1.5*applicant["attributes"][attribute])
            elif attribute == "spicyFoodTolerance":
                indvAttributes.append(0.75*applicant["attributes"][attribute])
            else:
                indvAttributes.append(1*applicant["attributes"][attribute])
                
                
        simList.append((applicant["name"],cosineSimilarity(indvAttributes,averageAttributes)))
    return simList

#Manual way of saving JSON through string formatting
# =============================================================================
# def outputJSON(jsonData,averageAttributes):
#     indent = "   "
#     output = "{\n" + indent + '"scoredApplicants” : [\n'
#     
#     simList = calculateSimilarity(jsonData, averageAttributes)
#     
#     for candidate in simList:
#         output += indent*2 +'{\n' + indent*3 + '"name" : "' + candidate[0] + '",\n'+ indent*3 +'"score" : ' + str(candidate[1]) + '\n'+ indent*2 +'},'
#     output = output[:-1]
#     output += '\n'+ indent +']\n}'
#     
#     print(output)
# =============================================================================

#Saves scoredApplicants.json that has similarity scores for each candidate calculated by calculateSimilarity
#Takes in the JSON input and calculated average attribute score to send to calculated similarity
def outJSON(jsonData,averageAttributes):
    #Use dictionary as base to create JSON file
    scoredApplicants = {"scoredApplicants": []}
    
    #Sends in jsonData containing candidate metrics and average team metrics to caclulate cosine similarity
    simList = calculateSimilarity(jsonData, averageAttributes)
    
    for candidate in simList:
        #Rounds output to tenth like example
        candidateDict = {"name":candidate[0] ,"score": round(candidate[1],1)}
        scoredApplicants["scoredApplicants"].append(candidateDict)

    
    jsonOutput = json.dumps(scoredApplicants, indent=4)

    #change scoredApplicants to desired output JSON file name
    with open("scoredApplicants.json", "w") as outfile:
        outfile.write(jsonOutput)
            
if __name__ == '__main__':
    
    #If you want to load JSON from string instead of file
# =============================================================================
#     inp = '{"team" : [{"name" : "Eddie","attributes": {"intelligence" : 1,"strength" : 5,"endurance" : 3,"spicyFoodTolerance" : 1}}, {"name" : "Will","attributes": {"intelligence" : 9,"strength" : 4,"endurance" : 1,"spicyFoodTolerance" : 6}}, {"name" : "Mike","attributes": {"intelligence" : 3,"strength" : 2,"endurance" : 9,"spicyFoodTolerance" : 5}}],"applicants" : [{"name" : "John","attributes": {"intelligence" : 4,"strength" : 5,"endurance" : 2,"spicyFoodTolerance" : 1}}, {"name" : "Jane","attributes": {"intelligence" : 7,"strength" : 4,"endurance" : 3,"spicyFoodTolerance" : 2}}, {"name" : "Joe","attributes": {"intelligence" : 1,"strength" : 1,"endurance" : 1,"spicyFoodTolerance" : 10}}]}'
#     jsonInput = json.loads(inp)
# =============================================================================
    
    #adjust input.json to name of input JSON file
    with open('input.json', 'r') as openfile:
        jsonInput = json.load(openfile)
        
    teamAttributes = extractAttributes(jsonInput)
    averageAttributes = averageAttributes(teamAttributes)
    #print(averageAttributes)
    
    outJSON(jsonInput,averageAttributes)
    
