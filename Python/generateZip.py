import sys
import os
from zipfile import ZipFile
import shutil
import time
import csv
import pandas as pd
import geopandas as gpd
import rs2
import glob


def main():
    #string manipulation of the selected values of the dropdown menus to grab variables needed to calculate attributes.
    # the parameters sent in are long strings containing meta data of each selected field (project, orthomosaic, boundary, etc.) each attribute of selected field split with "::".
    selected_project = sys.argv[1].split("::")
    selected_project_name = selected_project[0]                                              # name of the selected project

    selected_orthomosaic_list = sys.argv[2].split(",")
    selected_orthomosaic_list = sorted(selected_orthomosaic_list)
    selected_CanopyHeightModel_list = sys.argv[3].split(",")
    selected_CanopyHeightModel_list = sorted(selected_CanopyHeightModel_list)
    selected_ortho_temp = ''
    selected_orthomosaic_name_array = []
    count = 1
    chm_list_count = 0
    loopCount = 0;

    # iterate through ortho list to create a string containing all of them seperated by underscores
    # used for file naming purposes
    for a in selected_orthomosaic_list:
        selected_orthomosaic = a.split("::")
        selected_orthomosaic_FileName = selected_orthomosaic[0]                                      # File name of the selected orthomosaic with file extension
        selected_orthomosaic_FilePath = selected_orthomosaic[1]                                     # file path of the selected orthomosaic
        selected_orthomosaic_EPSG = selected_orthomosaic[2]                                          # EPSG value of the selected orthomosaic
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName.split(".")
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName_noExt[0]
        selected_ortho_temp += selected_orthomosaic_FileName_noExt
        selected_orthomosaic_name_array.append(selected_orthomosaic_FileName_noExt)
        if (count < len(selected_orthomosaic_list)):
            selected_ortho_temp += "_"
        count += 1
    print("Long Ortho File Name: ", selected_ortho_temp)

    # for loop to iterate through the results retrieving process for each of the selected Orthomosaics
    selected_chm_name_array = []
    chm_counter = 0
    path_count = 0
    first_chm = False
    no_chm = False
    for x in selected_orthomosaic_list:
        chm_count = 1                                                                               # for counting the numbers of CHMs selected
        selected_orthomosaic = x.split("::")
        selected_orthomosaic_FileName = selected_orthomosaic[0]                                      # File name of the selected orthomosaic with file extension
        selected_orthomosaic_FilePath = selected_orthomosaic[1]                                     # file path of the selected orthomosaic
        selected_orthomosaic_EPSG = selected_orthomosaic[2]                                          # EPSG value of the selected orthomosaic
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName.split(".")
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName_noExt[0]                #  file name of selected orthomosaic withoout file extension

        # if there are no CHMs selected then string manipulation isnt necessary
        if (no_chm == True):
            pass
        elif(selected_CanopyHeightModel_list[path_count] == "0"):               # if CHM list is zero then this selected orthomosaic has no accompanying CHM
            if (path_count == 0):                                               # if CHM list value is zero and this is the first one than there were nno CHM selected
                no_chm = True
            pass
            print("There was no CHM selected!")
        else:
            selected_CanopyHeightModel = selected_CanopyHeightModel_list[path_count].split("::")
            print(selected_CanopyHeightModel)
            selected_CanopyHeightModel_FileName = selected_CanopyHeightModel[0]                              # File name of the selected Canopy Height Model (CHM) with file extension
            selected_CanopyHeightModel_FilePath = selected_CanopyHeightModel[1]                                 # file path of the selected CHM
            selected_CanopyHeightModel_FileName_noExt = selected_CanopyHeightModel_FileName.split(".")
            selected_CanopyHeightModel_FileName_noExt = selected_CanopyHeightModel_FileName_noExt[0]        # file name of selected CHM withoout file extension
            selected_chm_name_array.append(selected_CanopyHeightModel_FileName_noExt)

            # this is for creating a CHM list that is equal in length to the orthoosaic list
            # this is to add "0" to orthos with no CHM input, used for file merging purposes
            if (path_count == 0):
                chm_list_count = len(selected_CanopyHeightModel_list)
            count = 0
            while(len(selected_CanopyHeightModel_list) < len(selected_orthomosaic_list)):
                date = selected_orthomosaic_list[count].split('_')
                date = date[0]
                if (count == len(selected_CanopyHeightModel_list)):
                    selected_CanopyHeightModel_list.append("0")
                elif (selected_CanopyHeightModel_list[count].find(date) == -1):
                    selected_CanopyHeightModel_list.insert(count, '0')
                count +=1

        # this is used for determining if a results folder needs to be created for CH/CV attributes
        # this method avoids making multiple and creating one when unnecessary
        if (no_chm == True):
            pass
        elif (selected_CanopyHeightModel_list[path_count] != '0'):
            if (chm_counter == 0):
                first_chm = True
            else:
                first_chm = False
            chm_counter += 1
        else:
            first_chm = False
        selected_boundary = sys.argv[4].split("::")
        selected_boundary_FileName = selected_boundary[0]                                           # File name of the selected boundary file with file extension
        selected_boundary_FilePath = selected_boundary[1]                                            # file path of the selected boundary file
        selected_boundary_FileName_noExt = selected_boundary_FileName.split(".")
        selected_boundary_FileName_noExt = selected_boundary_FileName_noExt[0]                          # file name of selected boundary file withoout file extension
        print("arg4:", sys.argv[4])
        if(sys.argv[5] == "true"):              # grab checkbox parameters and set them to boolean.
            csv_checked = True
        else:
            csv_checked = False

        if(sys.argv[6] == "true"):
            xls_checked = True
        else:
            xls_checked = False

        if(sys.argv[7] == "true"):
            geojson_checked = True
        else:
            geojson_checked = False

        if(sys.argv[8] == "true"):
            shape_checked = True
        else:
            shape_checked = False

        if(sys.argv[9] == "true"):
            cc_checked = True
        else:
            cc_checked = False

        if(sys.argv[10] == "true"):
            exg_checked = True
        else:
            exg_checked = False

        if(sys.argv[11] == "true"):
            ch_checked = True
        else:
            ch_checked = False

        if(sys.argv[12] == "true"):
            cv_checked = True
        else:
            cv_checked = False

        check_zip_val = sys.argv[13]

    #base path to where attribute generation results are stored in regards to what project, Orthomosaic and boundary are selected.
        path_to_project_folder = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_orthomosaic_FileName_noExt + "/"
        chm_count += 1
        if not (os.path.exists(path_to_project_folder)):
            print("path: ", path_to_project_folder)
            print("The specified project/orthomosaic results do not exist!")
            return 0

    #attributes array containing attribute boundary string extentions if selected
        attributes = []
        if(cc_checked):
            attributes.append("cc_boundary")
        if(exg_checked):
            attributes.append("exg_boundary")
        if(ch_checked and (selected_CanopyHeightModel_list[path_count] != '0')):
            attributes.append("ch_boundary")
        if(cv_checked and (selected_CanopyHeightModel_list[path_count] != '0')):
            attributes.append("cv_boundary")
        dat_dirs = []
        att = []
        if (cc_checked):
            dat_dirs.append("cc_rgb")
            att.append("cc_boundary")
        if (exg_checked):
            dat_dirs.append("exg")
            att.append("exg_boundary")
        if (ch_checked):
            dat_dirs.append("ch")
            att.append("ch_boundary")
        if (cv_checked):
            dat_dirs.append("cv")
            att.append("cv_boundary")

    #path to temporary directory that will hold the results
        if (path_count == 0):
            path_to_temp_folder = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_ortho_temp + "_" + selected_boundary_FileName_noExt + "/"
            temp_folder_exists = os.path.isdir(path_to_temp_folder)
            print("temp_folder_exists: " + str(temp_folder_exists))

            if not (temp_folder_exists):                        #if the temp direcory doesn't exist create one
                os.makedirs(path_to_temp_folder)
                print("temp folder did not exist yet, creating one.")
            else:
                if (check_zip_val == 1):
                    index = 0
                    inner_index = 0
                    for a in att:
                        temp_dat_folder = "/var/www/html/uas_data/download/product/" + selected_project_name + "temp_dat_folder_" + dat_dirs[index]
                        if (os.path.exists(temp_dat_folder)):
                            shutil.rmtree(temp_dat_folder)
                            os.makedirs(temp_dat_folder)
                        else:
                            os.makedirs(temp_dat_folder)
                        index += 1
                        for o in selected_orthomosaic_name_array:
                            existing_merged_shp = path_to_temp_folder + a + '/' + "merged_shp_" + dat_dirs[index] + ".shp"
                            existing_merged_shx = path_to_temp_folder + a + '/' + "merged_shp_" + dat_dirs[index] + ".shx"
                            existing_merged_dbf = path_to_temp_folder + a + '/' + "merged_shp_" + dat_dirs[index] + ".dbf"
                            existing_merged_prj = path_to_temp_folder + a + '/' + "merged_shp_" + dat_dirs[index] + ".prj"
                            if (os.path.exists(existing_merged_shp)):
                                shutil.copy(existing_merged_shp, temp_dat_folder)
                                shutil.copy(existing_merged_shx, temp_dat_folder)
                                shutil.copy(existing_merged_dbf, temp_dat_folder)
                                shutil.copy(existing_merged_prj, temp_dat_folder)
                            inner_index += 1
                shutil.rmtree(path_to_temp_folder)              # if the temp directory exists, delete it then create the temporary directory.
                os.makedirs(path_to_temp_folder)
                print("temp folder already existed. removing and creating a new one.")
        path_count += 1

        # while loop to grab the generated files of each attribute and place them in their respective results folder
        index = 0
        while index < len(attributes):              # index through the number of attribute boundary string extensions
            attribute_path = path_to_temp_folder + "/" + attributes[index]              # path to attribute result folder
            # creating attribute result folders
            if ((first_chm == True) and ((attributes[index] == 'ch_boundary') or (attributes[index] == 'cv_boundary'))):
                print("made path1: ", attributes[index])
                os.makedirs(attribute_path)
            elif(path_count == 1):
                print("made path2: ", attributes[index])
                os.makedirs(attribute_path)
            if(csv_checked):
                file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_orthomosaic_FileName_noExt + ".csv"
                print("FILE PATH: ", file_path)
                if os.path.exists(file_path):
                    print("AAAAAAAA")
                    shutil.copy(file_path, attribute_path)
                else:
                    print(file_path)
                    print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                    shutil.rmtree(path_to_temp_folder)
                    return 0

            if(xls_checked):
                file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_orthomosaic_FileName_noExt + ".xlsx"
                if os.path.exists(file_path):
                    shutil.copy(file_path, attribute_path)
                else:
                    print(file_path)
                    print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                    shutil.rmtree(path_to_temp_folder)
                    return 0

            if(geojson_checked):
                file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_orthomosaic_FileName_noExt + ".geojson"
                if os.path.exists(file_path):
                    shutil.copy(file_path, attribute_path)
                else:
                    print(file_path)
                    print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                    shutil.rmtree(path_to_temp_folder)
                    return 0

            if(shape_checked):
                file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_orthomosaic_FileName_noExt + ".shp"
                if os.path.exists(file_path):
                    shutil.copy(file_path, attribute_path)
                else:
                    print(file_path)
                    print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                    shutil.rmtree(path_to_temp_folder)
                    return 0

                file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_orthomosaic_FileName_noExt + ".shx"
                if os.path.exists(file_path):
                    shutil.copy(file_path, attribute_path)
                else:
                    print("File does not exist: " + file_path)                  #if not, state that the file does not exist.

                file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_orthomosaic_FileName_noExt + ".dbf"
                if os.path.exists(file_path):
                    shutil.copy(file_path, attribute_path)
                else:
                    print("File does not exist: " + file_path)                  #if not, state that the file does not exist.

                file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_orthomosaic_FileName_noExt + ".prj"
                if os.path.exists(file_path):
                    shutil.copy(file_path, attribute_path)
                else:
                    print("File does not exist: " + file_path)
            index += 1
            print("index: " + str(index))

    # merging CSV files and moving merged SHP files over

    # arrays for the naming conventions of selected attributes for folders and shp files
    dat_array = []
    attributes = []
    if (cc_checked):
        dat_array.append("cc_rgb")
        attributes.append("cc_boundary")
    if (exg_checked):
        dat_array.append("exg")
        attributes.append("exg_boundary")
    if (ch_checked):
        dat_array.append("ch")
        attributes.append("ch_boundary")
    if (cv_checked):
        dat_array.append("cv")
        attributes.append("cv_boundary")
    # if only one ortho is selected than merging isnt necessary
    if (len(selected_orthomosaic_name_array) > 1):
        dat_count = 0
        # merged files and zip files are created for each attribute
        for a in attributes:
            merge_name_csv = "merged_" + a + ".csv"                             #name of merged CSV file
            merge_name_shp = "merged_" + a + ".shp"                             # name of merged SHP file
            print("A")
            # paths to the created merged SHP file and the extensions and projection
            path_to_merged_shp_folder =  "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + "temp_dat_folder_" + dat_array[dat_count]
            path_to_shp =  "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + "temp_dat_folder_" + dat_array[dat_count] + '/' + 'merged_shp_' + dat_array[dat_count] + '.shp'
            path_to_dbf =  "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + "temp_dat_folder_" + dat_array[dat_count] + '/' + 'merged_shp_' + dat_array[dat_count] + '.dbf'
            path_to_shx =  "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + "temp_dat_folder_" + dat_array[dat_count] + '/' + 'merged_shp_' + dat_array[dat_count] + '.shx'
            path_to_prj =  "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + "temp_dat_folder_" + dat_array[dat_count] + '/' + 'merged_shp_' + dat_array[dat_count] + '.prj'
            out_dir = path_to_temp_folder + '/' + a
            # moving the merged SHP file package to the results attribute folder
            if os.path.exists(path_to_shp):
                shutil.move(path_to_shp, out_dir)
                shutil.move(path_to_dbf, out_dir)
                shutil.move(path_to_shx, out_dir)
                shutil.move(path_to_prj, out_dir)
                if (os.path.exists(path_to_merged_shp_folder)):
                    shutil.rmtree(path_to_merged_shp_folder)
            dat_count += 1
            mergeCount = 0
            chm_merge_count = 0

            #iterating through each orthomosaic in order to create the merged CSV file
            for i in selected_orthomosaic_name_array:
                print("chm_list_count: ", chm_list_count)
                if ((a == 'ch_boundary' or a == 'cv_boundary') and (chm_list_count == 1)):
                    break                             # if there is only one CHM, then merged CSV files are necessary for CH/CV attributes
                elif ((a == 'ch_boundary' or a == 'cv_boundary') and (selected_CanopyHeightModel_list[mergeCount] == '0')):
                    mergeCount += 1
                    continue                             # if there is a "0" for this index then no data needs to be merged
                else:
                    pass
                print("C")
                csv1 = path_to_temp_folder + "/" + a + "/" + merge_name_csv                             # path to new merged CSV file
                csv2 = path_to_temp_folder + "/" + a + "/" + a + "_" + i + ".csv"                             # path to existing CSV file that needs to be read
                # if this is the first CHM file to merge then the base file needs to be created
                if (chm_merge_count == 0):
                    shutil.copy(csv2,csv1)                             # base file is the first set of data copied to a new file
                    csv_file1 = pd.read_csv(csv1)
                    chm_merge_count += 1
                    mergeCount += 1
                    continue
                if (mergeCount == 0):                             # for both if statements, no merging on the first set of data, or else there is duplicate data
                    shutil.copy(csv2,csv1)
                    csv_file1 = pd.read_csv(csv1)
                    mergeCount += 1
                    continue

                # this is for the second+ data sets to be read and merged
                csv_file2 = pd.read_csv(csv2)
                print("C2")
                #csv_file1 = pd.concat([csv_file1, csv_file2], join = 'outer')
                csv_file1 = pd.merge(csv_file1,csv_file2, how = 'outer')
                print("C3")
                mergeCount += 1
            csv_file1.to_csv(csv1)                             # export the merged CSV dataFrame into a CSV file

    print("zip")
    #  creating the results directories
    results_dir = path_to_temp_folder + "/results"
    ccZip = results_dir + "/" + "ccZip"
    exgZip = results_dir + "/" + "exgZip"
    chZip = results_dir + "/" + "chZip"
    cvZip = results_dir + "/" + "cvZip"
    os.makedirs(results_dir)
    index = 0

    # creating the attribute zip files
    for i in attributes:
        attribute_path = path_to_temp_folder + "/" + i
        if(os.path.exists(attribute_path)):
            if(i == "cc_boundary"):
                shutil.make_archive(ccZip, 'zip', attribute_path)
            if(i == "exg_boundary"):
                shutil.make_archive(exgZip, 'zip', attribute_path)
            if(i == "ch_boundary"):
                shutil.make_archive(chZip, 'zip', attribute_path)
            if(i == "cv_boundary"):
                shutil.make_archive(cvZip, 'zip', attribute_path)
        index += 1

    # creating the Results zip file
    resultsZip = path_to_temp_folder + "/" + "resultsZip"
    path_to_zip = resultsZip + ".zip"                                      # set name of Zip file
    print("path_to_zip:" , resultsZip)
    if(os.path.exists(resultsZip)):                                                # if the Zip file already exists, delete it before creating it.
        os.remove(resultsZip)
        shutil.make_archive(resultsZip, 'zip', results_dir)
        #shutil.make_archive(results_dir, 'zip', resultsZip)
    else:
        shutil.make_archive(resultsZip, 'zip', results_dir)
        #shutil.make_archive(results_dir, 'zip', resultsZip)


#---------------------------------------------------------------------------------------------------------------------Run Main
if __name__ == "__main__":
    main()
    # reading csv files
#data2 = pd.read_csv('datasets/borrower.csv')

# using merge function by setting how='right'
#output3 = pd.merge(data1, data2,
                   #on='LOAN_NO',
                   #how='right')

#combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
