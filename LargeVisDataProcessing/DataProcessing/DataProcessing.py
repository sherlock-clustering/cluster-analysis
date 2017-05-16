
import fileinput #for reading large files
import json
import random
import numpy as np
import os
import shutil
import csv 
import math
from datetime import datetime
import argparse as argp

#region parse command-line args
parser = argp.ArgumentParser(
   description = 'This script creates the input data folder for the visualization tool.')

parser.add_argument(
   '-coord',
   dest = 'coordinatesFile',
   help = 'Input file containing the direct output from LargeVis')

parser.add_argument(
   '-metadata',
   dest = 'metaDataFile',
   help = 'Input file containing the text accompanying the data. Format: [id] [metadata]*.')

parser.add_argument(
   '-dir',
   dest = 'baseDir',
   help = 'Base directory to store output files')

parser.add_argument(
   '-np',
   dest = 'namesOfPropertiesFile',
   help = 'A json file containing list of properties names. Ex: ["Name", "Cluster", "Weight"]')

parser.add_argument(
   '-dim',
   dest = 'dimension',
   help = 'The dimension of data, 2 or 3')

args = parser.parse_args()
#endregion
           

#region Reading data


#to be used to read our filelists
def ReadFilelist(metaDataFile):
        """File format: Pentax_OptioA40_0_30521.JPG """
        metaDataDict = dict()
        for line in fileinput.input([metaDataFile]):
            if line != "\n":
                items = lineline = line.strip('\n').split("_")  
                camera = ""
                for i in range(0, len(items)-1):
                    camera = camera + str(items[i]) + "_"
                id = camera  + str(items[len(items) -1])                             
                metaDataDict[id] = [id, camera]
        return metaDataDict

#to be used for olympus
def ReadFilelist_olympus(metaDataFile):
        """File format: Pentax_OptioA40_0_30521.JPG coord1 coord2 """
        metaDataDict = dict()
        filelist= []
        for line in fileinput.input([metaDataFile]):
            if line != "\n":
                lines = line.split()
                if len(lines)>2:
                    #for items in csv.reader([lines[0]], delimiter='_'):   
                    items = lines[0].split("_")
                    camera = ""
                    for i in range(0, len(items)-1):
                        camera = camera + str(items[i]) + "_"
                            #camera = str(items[0]) + "_" + str(items[1]) + "_" + str(items[2]) 
                    id = camera  + str(items[len(items) -1])     
                    filelist.append(id)
                    metaDataDict[id] = [id, camera]
            f = open('filelist_olympus', 'w')
            for id in filelist:
               f.write(id + '\n')
        return metaDataDict

#to be used to read our filelist enriched with cluster labels
def ReadFilelistWithLabels(metaDataFile):
        """File format: Pentax_OptioA40_0_30521.JPG 3 """
        metaDataDict = dict()
        for line in fileinput.input([metaDataFile]):
            if line != "\n":   
                for words in csv.reader([line], delimiter=' '):   
                    fingerprint = words[0]
                    label = words[1]
                    for items in csv.reader([fingerprint], delimiter='_'):   
                        camera = str(items[0]) + "_" + str(items[1]) + "_" + str(items[2]) 
                        id = camera + "_"+ str(items[3])                             
                        metaDataDict[id] = [id, camera, label]
        return metaDataDict

#to be used to read list of photo names in real life
def ReadPhotoNames(metaDataFile):
        """File format: nameOfPhoto """
        metaDataDict = dict()
        for line in fileinput.input([metaDataFile]):
            if line != "\n":                                              
                metaDataDict[line] = [line]
        return metaDataDict


#to be used to read our filelist enriched with cluster labels
def ReadPhotoNamesWithLabels(metaDataFile):
        """File format: nameOfPhoto 3 """
        metaDataDict = dict()
        for line in fileinput.input([metaDataFile]):
            if line != "\n":   
                for words in csv.reader([line], delimiter=' '):   
                    fingerprint = words[0]
                    label = words[1]                                             
                    metaDataDict[id] = [fingerprint, label]
        return metaDataDict


def ReadCoordinates(file, dimension):#dimension = 2 or 3         
    fixed = dict()
    maxabs = 0
    for line in fileinput.input([file]):
        if line != "\n":   
            items = line.split()
            if len(items) > 2:# to skip the first line 
                if (dimension == 2):
                    maxabs = max(abs(float(items[1])), abs(float(items[2])), maxabs)
                    fixed[items[0]] = [ 0.1, float(items[1]), float(items[2])]
                else:
                    maxabs = max(abs(float(items[1])), max(abs(float(items[2])), abs(float(items[3]))), maxabs)
                    fixed[items[0]] = [float(items[1]), float(items[2]), float(items[3])]
    for key in fixed.keys():
        lis = fixed[key]
        fixed[key] = [lis[0]/maxabs, lis[1]/maxabs, lis[2]/maxabs]
    return fixed

#endregion 

          
#region Write output


def CreateSmallDataJSONFile(allPoints, startingFolder):
    string = json.dumps(allPoints)
    file = open(os.path.join(startingFolder, "data.json"), "w")
    file.write(string)
    file.close()
   

def CreatePointsDictionary(fixedCoordinates,  metaDataDict,  namesOfPropertiesFile):
    pointsDict = dict()
    if namesOfPropertiesFile != "No":
        with open(namesOfPropertiesFile) as json_data:
            list = json.load(json_data)
        pointsDict["NamesOfProperties"] = list
    else:
        pointsDict["NamesOfProperties"] = ["Name", "Camera"] #default
    for key in fixedCoordinates.keys():
        point = dict()
        point["Coordinates"] = fixedCoordinates[key]
        if (metaDataDict != "no" ):
            if key in metaDataDict:
                point["Properties"] = metaDataDict[key] 
            else:
                point["Properties"] = []
        else: 
            point["Properties"] = []        
        pointsDict[key] = point
    return pointsDict

def CreateDirIfDoesNotExist(dirname):
    if not os.path.exists(dirname):          
        os.makedirs(dirname)

def RemoveDirTreeIfExists(dirname):        
    if os.path.exists(dirname):
        shutil.rmtree(dirname)

            
#endregion 

#region Workflow

def ConvertCoordinatesToList(fixedCoordinate):
    for key in fixedCoordinate:
        fixedCoordinate[key] = list(fixedCoordinate[key])
                       
def Workflow(coordinatesFile, metaDataFile, namesOfPropertiesFile, baseDir = os.getcwd(), dimension = 2, real_life = False, clustered = False):      
    """Produces the input for DiVE. 
       coordinatesFile is the output of LargeVis
       metaDataFile contains info about the photos
       namesOfPropeties file contains a list of names of properties. Ex ["Name", "Cluster", "Weight"]
       baseDir - where to write output
       dimension - dimension of coordinates as given by LargeVis
       real_life - if true, the photo name does not contain info on camera. If false it is as in filelist
       clustered - if true, the second word in the metadata is the cluster label. The first word is the photo name.
    """
    print(str(datetime.now()) + ": Removing old data...")
    dirname1 =  os.path.join(baseDir, "data")
    RemoveDirTreeIfExists(dirname1)
    print(str(datetime.now()) + ": Reading input files...")
    if metaDataFile != "No":
        if (real_life):
            if(clustered):              
                metaDataDict = ReadPhotoNamesWithLabels(metaDataFile)
            else:
                metaDataDict = ReadPhotoNames(metaDataFile)
        else:
            if (clustered):
                metaDataDict = ReadFilelistWithLabels(metaDataFile)
            else:                
                metaDataDict = ReadFilelist(metaDataFile)
    else: 
        metaDataDict = "no"         
    fixedCoordinate = ReadCoordinates(coordinatesFile, dimension)
    ConvertCoordinatesToList(fixedCoordinate)   
    pointsDict = CreatePointsDictionary(fixedCoordinate, metaDataDict, namesOfPropertiesFile)        
    print(str(datetime.now()) + ": Start writing output...")         
    CreateDirIfDoesNotExist(dirname1)
    CreateSmallDataJSONFile(pointsDict, dirname1)
    print(str(datetime.now()) + ": Finished writing output.")
#endregion
         
#region Main

Workflow(args.coordinatesFile, args.metaDataFile, args.namesOfPropertiesFile,  args.baseDir, args.dimension) # to be used from command line
#Workflow("coordinates_praktica_2d_filtered.txt", "filelist_praktica-filtered.txt", "No",  os.getcwd(), 2, False, False)
#endregion
