import sys
import os
import shutil
import time

def main():
    zip_file_path = sys.argv[1] #grabs system arguments containing the path to the temp results dirtectory and zipfile downloaded by the client
    #print("Selected File Path noExt: ", zip_file_path) #code here is similar to setup of deleteTempResults.py
    cc_ckd = sys.argv[2]
    exg_ckd = sys.argv[3]
    ch_ckd = sys.argv[4]
    cv_ckd = sys.argv[5]
    attributes = []
    if (cc_ckd == 'true'):
        attributes.append("cc_boundary")
    if (exg_ckd == 'true'):
        attributes.append("exg_boundary")
    if (ch_ckd == 'true'):
        attributes.append("ch_boundary")
    if (cv_ckd == 'true'):
        attributes.append("cv_boundary")
    ortho_temp = sys.argv[6].split(',')
    ortho_temp = sorted(ortho_temp)
    project = sys.argv[7].split("::")
    project_name = project[0]
    chm_date = sys.argv[8].split(",")
    index = 0
    print("zip: ", zip_file_path)
    print("cc: ", cc_ckd)
    print("exg: ", exg_ckd)
    print("ch: ", ch_ckd)
    print("cv: ", cv_ckd)
    print("ortho: ", ortho_temp)
    print("project: ", project)
    chm_counter = []
    print("attributes: ", attributes)

    # checks to see if the attribute results folder exists
    for i in ortho_temp:
        for j in attributes:
            file_path = "/var/www/html/uas_data/download/product/" + project_name + '/' + i + '/' + j
            print("file name: ", file_path)
            if (os.path.exists(file_path)):
                print(j,' exists')

                # if CH/CV is selected then check to see if any file types exist for those results
                # orthos with results will be appended to a CHM counter list
                if (j == 'ch_boundary' or j == 'cv_boundary'):
                    print("A1")
                    temp_file_path_csv = file_path + '/' + j + '_' + i + '.csv'
                    temp_file_path_xlsx = file_path + '/' + j + '_' + i + '.xlsx'
                    temp_file_path_geoJSON = file_path + '/' + j + '_' + i + '.geoJSON'
                    temp_file_path_shp = file_path + '/' + j + '_' + i + '.shp'
                    print("A2")
                    if (os.path.exists(temp_file_path_csv)):
                        print("A3")
                        chm_counter.append(i.split("_")[0] + "_" + "CHM")
                        print("A3b")
                    elif (os.path.exists(temp_file_path_xlsx)):
                        print("A4")
                        chm_counter.append(i.split("_")[0] + "_" + "CHM")
                    elif (os.path.exists(temp_file_path_geoJSON)):
                        print("A5")
                        chm_counter.append(i.split("_")[0] + "_" + "CHM")
                    elif (os.path.exists(temp_file_path_shp)):
                        print("A6")
                        chm_counter.append(i.split("_")[0] + "_" + "CHM")
                    print("B")
            elif(j == 'ch_boundary' or j == 'cv_boundary'):

                try:
                    print("chm_date: ", chm_date)
                    print("ortho_date: ", i.split("_")[0])
                    chm_date.index(i.split("_")[0])
                    return
                except ValueError:
                    print("value error")
                    pass

                continue
            else:
                print("else")
                return
            # this is to print the existing file types to let the user know which file types exist
            if (index == 0):
                temp_file_path = file_path + '/' + j + '_' + i + '.csv'
                if (os.path.exists(temp_file_path)):
                    print("csv")
                temp_file_path = file_path + '/' + j + '_' + i + '.xlsx'
                if (os.path.exists(temp_file_path)):
                    print("xls")
                temp_file_path = file_path + '/' + j + '_' + i + '.geojson'
                if (os.path.exists(temp_file_path)):
                    print("geoJSON")
                temp_file_path = file_path + '/' + j + '_' + i + '.shp'
                if (os.path.exists(temp_file_path)):
                    print("shp")
            index += 1
    print("C")
    print(chm_counter)

    # if either the ortho and CHM list are equal or there are no CHMs selected, then all is printed so that the JS knows it isnt a mismatch case
    if ((len(chm_counter) == len(ortho_temp)) or (len(chm_counter) == 0)):
        print("all")
    bool_check = 0 #case is to interpret the result so that it can be grabbed for other code

    # checks to see if there is a results folder created for the results the user is trying to generate
    if (os.path.exists(zip_file_path)): #difference lies here where the file is not deleted
        bool_check = 1
        print("The temp results directory and zip file have already been generated, you can download the generated results.")
    else:
        bool_check = 0
        print("The temp results directory and zip file do not exist!")

if __name__ == "__main__":
    main()
