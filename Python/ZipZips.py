import sys
import os
from zipfile import ZipFile
import shutil
import time

def main():
    #string manipulation of the selected values of the dropdown menus to grab variables needed to calculate attributes.
    # the parameters sent in are long strings containing meta data of each selected field (project, orthomosaic, boundary, etc.) each attribute of selected field split with "::".

    selected_project = sys.argv[1].split("::")
    selected_project_name = selected_project[0]                                              # name of the selected project

    selected_boundary = sys.argv[4].split("::")
    selected_boundary_FileName = selected_boundary[0]                                           # File name of the selected boundary file with file extension
    selected_boundary_FilePath = selected_boundary[1]                                            # file path of the selected boundary file
    selected_boundary_FileName_noExt = selected_boundary_FileName.split(".")
    selected_boundary_FileName_noExt = selected_boundary_FileName_noExt[0]                          # file name of selected boundary file withoout file extension

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

    #attributes array containing attribute boundary string extentions
#    attributes = ["cc_boundary", "exg_boundary", "ch_boundary", "cv_boundary"]

    attributes = []
    if(cc_checked):
        attributes.append("cc_boundary")
    if(exg_checked):
        attributes.append("exg_boundary")
    if(ch_checked):
        attributes.append("ch_boundary")
    if(cv_checked):
        attributes.append("cv_boundary")

    #
    temp_zip = "/var/www/html/uas_data/download/product/" + selected_project_name
    #

    #selected_orthomosaic_list = selected_orthomosaic.split(",")                                 ## split the multiple selections of orthomosaic
    all_orthos = ""
    orthoCount = 1
    #selected_orthomosaic_list = sys.argv[2].split(",")
    selected_orthomosaic_list = sys.argv[2]
    selected_orthomosaic_list_length = len(selected_orthomosaic_list)
    for x in selected_orthomosaic_list:
        #selected_orthomosaic_individual = sys.argv[2].split("::")
        selected_orthomosaic = x.split("::")
        selected_orthomosaic_FileName = selected_orthomosaic[0]                                      # File name of the selected orthomosaic with file extension
        selected_orthomosaic_FilePath = selected_orthomosaic[1]                                     # file path of the selected orthomosaic
        selected_orthomosaic_EPSG = selected_orthomosaic[2]                                          # EPSG value of the selected orthomosaic
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName.split(".")
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName_noExt[0]                #  file name of selected orthomosaic withoout file extension
        all_orthos += selected_orthomosaic_FileName_noExt
        if (orthoCount < selected_orthomosaic_list_length):
            all_orthos += "_"
            orthoCount += 1

        all_chm = ""
        chmCount = 1
        #selected_CanopyHeightModel_list = sys.argv[3].split(",")
        selected_CanopyHeightModel_list = sys.argv[3]
        selected_chm_list_length = len(selected_CanopyHeightModel_list)
        for y in selected_CanopyHeightModel_list:
            if(sys.argv[3] == "0"):
                selected_CanopyHeightModel = sys.argv[3]
                print("There was no CHM selected!")
            else:
                #selected_CanopyHeightModel = sys.argv[3].split("::")
                selected_CanopyHeightModel = y.split("::")
                selected_CanopyHeightModel_FileName = selected_CanopyHeightModel[0]                              # File name of the selected Canopy Height Model (CHM) with file extension
                selected_CanopyHeightModel_FilePath = selected_CanopyHeightModel[1]                                 # file path of the selected CHM
                selected_CanopyHeightModel_FileName_noExt = selected_CanopyHeightModel_FileName.split(".")
                selected_CanopyHeightModel_FileName_noExt = selected_CanopyHeightModel_FileName_noExt[0]        # file name of selected CHM withoout file extension
                all_chm += selected_CanopyHeightModel_FileName_noExt
                if (chmCount < selected_chm_list_length):
                    all_chm += "_"
                    chmCount += 1

                #base path to where attribute generation results are stored in regards to what project, Orthomosaic and boundary are selected.
            path_to_project_folder = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_orthomosaic_FileName_noExt + "_" + selected_boundary_FileName_noExt + "/"
            if not (os.path.exists(path_to_project_folder)):
                print("The specified project/orthomosaic results do not exist!")
                return 0

        #attributes array containing attribute boundary string extentions
        #    attributes = ["cc_boundary", "exg_boundary", "ch_boundary", "cv_boundary"]

            attributes = []
            if(cc_checked):
                attributes.append("cc_boundary")
            if(exg_checked):
                attributes.append("exg_boundary")
            if(ch_checked):
                attributes.append("ch_boundary")
            if(cv_checked):
                attributes.append("cv_boundary")


        #path to temporary directory that will hold the results
            path_to_temp_folder = path_to_project_folder + selected_project_name + "_" + selected_orthomosaic_FileName_noExt + "_" + selected_boundary_FileName_noExt + "_results"
            temp_folder_exists = os.path.isdir(path_to_temp_folder)
            print("temp_folder_exists: " + str(temp_folder_exists))

            if not (temp_folder_exists):                        #if the temp direcory doesn't exist create one
                os.makedirs(path_to_temp_folder)
                print("temp folder did not exist yet, creating one.")
            else:
                shutil.rmtree(path_to_temp_folder)              # if the temp directory exists, delete it then create the temporary directory.
                os.makedirs(path_to_temp_folder)
                print("temp folder already existed. removing and creating a new one.")

            index = 0
            while index < len(attributes):              # index through the number of attribute boundary string extensions
                if(csv_checked):
                    file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_boundary_FileName_noExt + ".csv"          #if the csv checkbox was checked. Copy the file to the temporary results directory.
                    if os.path.exists(file_path):
                        shutil.copy(file_path, path_to_temp_folder)
                    else:
                        print(file_path)
                        print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                        shutil.rmtree(path_to_temp_folder)
                        return 0

                if(xls_checked):
                    file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_boundary_FileName_noExt + ".xlsx"           #if the xls checkbox was checked. Copy the file to the temporary results directory.
                    if os.path.exists(file_path):
                        shutil.copy(file_path, path_to_temp_folder)
                    else:
                        print(file_path)
                        print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                        shutil.rmtree(path_to_temp_folder)
                        return 0

                if(geojson_checked):
                    file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_boundary_FileName_noExt + ".geojson"       #if the geojson checkbox was checked. Copy the file to the temporary results directory.
                    if os.path.exists(file_path):
                        shutil.copy(file_path, path_to_temp_folder)
                    else:
                        print(file_path)
                        print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                        shutil.rmtree(path_to_temp_folder)
                        return 0

                if(shape_checked):
                    file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_boundary_FileName_noExt + ".shp"           #if the shape checkbox was checked. Copy the file to the temporary results directory.
                    if os.path.exists(file_path):
                        shutil.copy(file_path, path_to_temp_folder)
                    else:
                        print(file_path)
                        print("The specified canopy attribute results do not exist!")                  #if not, state that the file does not exist.
                        shutil.rmtree(path_to_temp_folder)
                        return 0

                    file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_boundary_FileName_noExt + ".shx"           #if the shape checkbox was checked. Copy the file to the temporary results directory.
                    if os.path.exists(file_path):
                        shutil.copy(file_path, path_to_temp_folder)
                    else:
                        print("File does not exist: " + file_path)                  #if not, state that the file does not exist.

                    file_path = path_to_project_folder + attributes[index] + "/" + attributes[index] + "_" + selected_boundary_FileName_noExt + ".dbf"           #if the shape checkbox was checked. Copy the file to the temporary results directory.
                    if os.path.exists(file_path):
                        shutil.copy(file_path, path_to_temp_folder)
                    else:
                        print("File does not exist: " + file_path)                  #if not, state that the file does not exist.
                index += 1
                count = 0
            shutil.copytree(path_to_temp_folder, temp_zip)



    path_to_zip = temp_zip + "/" + selected_project_name + "_" + all_orthos + "_" + all_chm + "_" + selected_boundary_FileName_noExt + "_results"
    shutil.copytree(temp_zip, path_to_zip)
    # use shutil.copytree() if there are issues with the src being a directory rather than a file
    path_to_zip_ext = path_to_zip + ".zip"
    #path_to_zip = path_to_temp_folder + ".zip"                                      # set name of Zip file
    if(os.path.exists(path_to_zip_ext)):                                                # if the Zip file already exists, delete it before creating it.
        os.remove(path_to_zip_ext)
        shutil.make_archive(path_to_zip, 'zip', path_to_zip)
    else:
        shutil.make_archive(path_to_zip, 'zip', path_to_zip)
    #os.remove(path_to_temp_folder)



#---------------------------------------------------------------------------------------------------------------------Run Main
if __name__ == "__main__":
    main()
