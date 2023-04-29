# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 17:37:59 2022

@author: motte
"""

#--------------------------------------------------------------------------------------------------------------Imported Libraries
import os
import numpy as np
import sys
import rs2
import glob
from osgeo import gdal, gdalnumeric, ogr, osr
#from threading import *
from gen_ch_boundry import get_ch
from gen_cc_boundary import get_cc
from gen_cv_boundary import get_cv
from gen_exg_boundary import get_exg
from zipfile import ZipFile
import geopandas
import shutil
#-----------------------------------------------------------------------------------------------------------------Initialzie Golbal Variables

espg_var               = ""

img_file               = ""
shp_file               = ""
out_dir                = ""
chm_file               = ""

cc_out_dir             = ""
grvi_out_dir           = ""
mgrvi_out_dir          = ""
rgbvi_out_dir          = ""
exg_out_dir            = ""
exgr_out_dir           = ""

exg_attributes_out_dir = ""

files                  = []
chm_files              = []
ortho_name_array       = []
project_folder         = ''

globalCount = 0
no_chm = False
#------------------------------------------------------------------------------------------------------------------------Main Function
# testing and additions:
    # unmatching number of orthos and chms
def main():
    global globalCount, project_folder, ortho_name_array, chm_files, no_chm
    print("Global Count: ", globalCount)
    # string manipulation of the selected values of the dropdown menus to grab variables needed to calculate attributes.
    # the parameters sent in are long strings containing meta data of each selected field (project, orthomosaic, boundary, etc.) each attribute of selected field split with "::".
    selected_project = sys.argv[1].split("::")
    selected_project_name = selected_project[0]                                          # name of the selected project

    selected_orthomosaic_list = sys.argv[2].split(",")                             # grab ortho list
    selected_orthomosaic_list = sorted(selected_orthomosaic_list)
    print("OrthoList: ", selected_orthomosaic_list)

    # for loop to iterate through the results generation process for each of the selected Orthomosaics
    loopCount = 0
    for x in selected_orthomosaic_list:
        selected_orthomosaic = x.split("::")
        selected_orthomosaic_FileName = selected_orthomosaic[0]                                 # File name of the selected orthomosaic with file extension
        selected_orthomosaic_FilePath = selected_orthomosaic[1]                                 # file path of the selected orthomosaic
        selected_orthomosaic_EPSG = selected_orthomosaic[2]                                     # EPSG value of the selected orthomosaic
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName.split(".")
        selected_orthomosaic_FileName_noExt = selected_orthomosaic_FileName_noExt[0]            #  file name of selected orthomosaic withoout file extension
        #print("!!!!!!!!!!!!!!!!Ortho: ", selected_orthomosaic_FileName)
        ortho_name_array.append(selected_orthomosaic_FileName_noExt)

        # creating the sorted CHM list
        if (loopCount == 0):
            selected_CanopyHeightModel_list = sys.argv[3].split(",")
            selected_CanopyHeightModel_list = sorted(selected_CanopyHeightModel_list)
        print("CHMList: ", selected_CanopyHeightModel_list)

        # no CHM means string manipulation is unnecessary
        if (no_chm == True):
            print("pass1")
            pass
        elif (selected_CanopyHeightModel_list[loopCount] == "0"):
            if (loopCount == 0):
                no_chm = True
            print("pass")
            pass
        else:
            selected_CanopyHeightModel = selected_CanopyHeightModel_list[loopCount].split("::")
            selected_CanopyHeightModel_FileName = selected_CanopyHeightModel[0]                             # File name of the selected Canopy Height Model (CHM) with file extension
            selected_CanopyHeightModel_FilePath = selected_CanopyHeightModel[1]
            selected_CanopyHeightModel_FileName_noExt = selected_CanopyHeightModel_FileName.split(".")
            selected_CanopyHeightModel_FileName_noExt = selected_CanopyHeightModel_FileName_noExt[0]        # file name of selected CHM withoout file extension

            count = 0
            # this is for making the CHM list equal to the ortho list by placing "0" for the CHM that werent input by the user
            # this is used to omit CH/CV calculations for certain orthos
            while(len(selected_CanopyHeightModel_list) < len(selected_orthomosaic_list)):
                date = selected_orthomosaic_list[count].split('_')
                date = date[0]
                print("date: ", date)
                if (count == len(selected_CanopyHeightModel_list)):
                    selected_CanopyHeightModel_list.append("0")
                    #chm_files.append("0")
                elif (selected_CanopyHeightModel_list[count].find(date) == -1):
                    selected_CanopyHeightModel_list.insert(count, '0')
                    #chm_files.insert(count, '0')
                count +=1
        # this is to create a CHM file path array that is used for CH/CV SHP file merging
        if (len(chm_files) == 0):
            print("inside chm_files loop")
            for chm in selected_CanopyHeightModel_list:
                if (chm == '0'):
                    chm_files.append("0")
                else:
                    temp_selected_CanopyHeightModel = chm.split("::")
                    temp_selected_CanopyHeightModel_FileName = temp_selected_CanopyHeightModel[0]
                    temp_selected_CanopyHeightModel_FilePath = temp_selected_CanopyHeightModel[1]
                    chm_files.append(temp_selected_CanopyHeightModel_FilePath)

        print("post-pass")
        print("list: ", selected_CanopyHeightModel_list)
        print("files: ", chm_files)
        selected_boundary = sys.argv[4].split("::")
        print('boundary: ', selected_boundary)
        selected_boundary_FileName = selected_boundary[0]                               # File name of the selected boundary file with file extension
        selected_boundary_FilePath = selected_boundary[1]                                   # file path of the selected boundary file
        selected_boundary_FileName_noExt = selected_boundary_FileName.split(".")
        selected_boundary_FileName_noExt = selected_boundary_FileName_noExt[0]              # file name of selected boundary file withoout file extension

        if(sys.argv[5] == "true"):                  # bools for checkboxes that are passed in as string so we need to set checkboxes to reset them to boolean vars.
            cc_checked = True
        else:
            cc_checked = False

        if(sys.argv[6] == "true"):
            exg_checked = True
        else:
            exg_checked = False

        if(sys.argv[7] == "true"):
            ch_checked = True
        else:
            ch_checked = False

        if(sys.argv[8] == "true"):
            cv_checked = True
        else:
            cv_checked = False

        object_name = "variable_debug.txt"      #DEBUG FILE FOR VARIABLES
        object_handle = open(object_name, "w")

    # path to the results directory in regard to what project is selected
        path_to_project_folder = ("/home/ubuntu/web/uas_data/download/product/" + selected_project_name)
        project_folder = path_to_project_folder
        project_exists = os.path.exists(path_to_project_folder)
        if not(project_exists):
            os.makedirs(path_to_project_folder)
    # path to results directory in regard to what orthomosiac is selected. Nested in project results directory
        chm_name = "chm" + str(globalCount)
        path_to_results_folder = path_to_project_folder + "/" + selected_orthomosaic_FileName_noExt
        results_exists = os.path.exists(path_to_results_folder)

        if not(results_exists):
            print("making ortho dir: ", path_to_results_folder)
            os.makedirs(path_to_results_folder)
        else:
            #pass
            print("deleting and making ortho dir: ", path_to_results_folder)
            shutil.rmtree(path_to_results_folder)              # if the temp directory exists, delete it then create the temporary directory.
            os.makedirs(path_to_results_folder)

    #    #object_handle.write("selected_project_name: " + selected_project_name + "\n")          # TO WRITE VARIABLES.
    # Call main functions to set global variables, generate attributes and remove files that are no longer needed.
        print("before img")
        upload_img(object_handle, selected_orthomosaic_FilePath)
        print("after img")
        select_out_folder(object_handle, path_to_results_folder)
        print("after select folder")

        generate_cc(selected_orthomosaic_FileName_noExt, object_handle)
        print("exitted generate")

        generate_vis(object_handle, selected_orthomosaic_FileName_noExt)
        print("left vis")

        upload_shp(object_handle, selected_boundary_FilePath)
        if (no_chm == True):
            pass
        elif (selected_CanopyHeightModel_list[loopCount] == "0"):
            pass
        else:
            upload_chm(object_handle, selected_CanopyHeightModel_FilePath)
        print("before attributes")
        generate_attributes(object_handle, selected_orthomosaic_FileName_noExt, selected_orthomosaic_EPSG, selected_boundary_FileName_noExt, cc_checked, exg_checked, ch_checked, cv_checked)
        print("after attributes")
        print("finish")
        loopCount += 1
        globalCount += 1
    # only call merge SHP function if more than one ortho was selected
    if (len(selected_orthomosaic_list) > 1):
        merge_shp(selected_boundary_FilePath, selected_orthomosaic_EPSG, cc_checked, exg_checked, ch_checked, cv_checked)
    rm_files(object_handle, selected_project_name, selected_orthomosaic_FileName_noExt, selected_boundary_FileName_noExt)
    print("out")
    object_handle.close()           # CLOSE DEBUG FILE



"""                                 Threading... might use this to generate attributes for multiple orthomosaics at the same time.
def upload_img_threading():
    # Call work function
    t1 = Thread(target = upload_img)
    t1.start()

def generate_cc_threading():
    # Call work function
    t1 = Thread(target = generate_cc)
    t1.start()

def generate_vis_threading():
    # Call work function
    t1 = Thread(target = generate_vis)
    t1.start()

def upload_shp_threading():
    # Call work function
    t1 = Thread(target = upload_shp)
    t1.start()

def upload_chm_threading():
    # Call work function
    t1 = Thread(target = upload_chm)
    t1.start()

def generate_attributes_threading():
    # Call work function
    t1 = Thread(target = generate_attributes(shp_file))
    t1.start()
"""
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------upload_img Function
"""
 Name: upload_img
 Function: loads path into global array called "files" which will be used later to generate files.
 Parameters: object_handle - writing to debug file, selected_orthomosaic_FilePath - selected orthomosaic file path
"""

def upload_img(object_handle, selected_orthomosaic_FilePath):
    global files
    object_handle.write("Will upload the image! " + "\n")
    #print("Will upload the image! ")

    img_file = selected_orthomosaic_FilePath                #Set the img_file variable to the orthomosaic file path.            # Is this var not what it's suppose to be???
    #print(f"selected_orthomosaic_FilePath= {selected_orthomosaic_FilePath}")
    object_handle.write("selected_orthomosaic_FilePath= " + selected_orthomosaic_FilePath + "\n")
    object_handle.write("img_file= " + img_file + "\n")

    if not img_file:
        object_handle.write("ERROR: Error reading the image file!" + "\n")
        #print("not image")
        return

    # load the image
    files.append(img_file)
    for f in files:
        object_handle.write("Uploaded the image: "+ f + "\n")
        #print("uploaded image")
    print("files in upload: ", files)
#------------------------------------------------------------------------------------------------------------------------------------select_out_folder Function
"""
 Name: select_out_folder
 Function: Checks existance and creates directories for dat files needed to calculate the canopy attributes.
 Parameters: object_handle - writing to debug file
             path_to_results_folder (String)- path to orthomosiac direcory located in the project results directory.
"""

def select_out_folder(object_handle, path_to_results_folder):
    #print("selected out folder")
    global out_dir
    out_dir = path_to_results_folder        # set output directory to orthomosiacs directory nested in project directory.

    cc_out_dir = os.path.join(out_dir, "cc_rgb")    # Create paths for directories to hold data files
    grvi_out_dir = os.path.join(out_dir, "grvi")
    mgrvi_out_dir = os.path.join(out_dir, "mgrvi")
    rgbvi_out_dir = os.path.join(out_dir, "rgbvi")
    exg_out_dir = os.path.join(out_dir, "exg")
    exgr_out_dir = os.path.join(out_dir, "exgr")

    results_folders = [cc_out_dir,                  # put paths of directories into an array
                       grvi_out_dir,
                       mgrvi_out_dir,
                       rgbvi_out_dir,
                       exg_out_dir,
                       exgr_out_dir]

    for folder in results_folders:                                          # for every directory path
        if not os.path.exists(folder):                                          # if the directory path doesn't exist, create it.
            print("path didnt exist")
            object_handle.write(folder + " folder does not exist. \n")
            os.makedirs(folder)
            object_handle.write(folder + " folder was created. \n")
            object_handle.write("Will be saving cc the results to: " + folder + " \n")
        else:
            print("path did exist")
            shutil.rmtree(folder)
            os.makedirs(folder)

#------------------------------------------------------------------------------------------------------------------------------------generate_cc Function

def generate_cc(selected_orthomosaic_FileName_noExt, object_handle):
    global out_dir
    global files
    print("generate1")
    print("files in generate: ", files)
    if(len(files) == 0):
        object_handle.write("ERROR: There are no files uploaded in the array. " + " \n")
        return

    field_count = 10
    th1 = 0.95
    th2 = 0.95
    th3 = 20
    for f in files:
        print("1")
        filename_temp = f.split("/")
        filename = filename_temp[-1]
        object_handle.write("Generating CC for the image: " + filename + "\n")
        print("2")
        # Open image without loading to memory
        object_handle.write("f = " + f + " \n")
        in_img = rs2.RSImage(f)
        print("3")

        # Read bands
        red = in_img.img[0,:,:].astype(np.float32)
        green = in_img.img[1,:,:].astype(np.float32)
        blue = in_img.img[2,:,:].astype(np.float32)

        # Calculate index
        try:
            print("red: ", red)
            print("green: ", green)
            i1 = red / green
            print("$1")
        except ZeroDivisionError:
            print("excepted")
            object_handle.write("Warning: i1 - Divide by Zero " + "\n")
            print("@1")
            pass
        except ValueError:
            object_handle.write("Warning: i1 - Value Error" + "\n")
            pass

        try:
            i2 = blue / green
            print("$2")
        except ZeroDivisionError:
            object_handle.write("Warning: i1 - Divide by Zero " + "\n")
            print("@2")
            pass
        except ValueError:
            object_handle.write("Warning: i1 - Value Error" + "\n")
            pass

        try:
            i3 = 2*green - blue - red
            #i3 = a
            print("$3")
        except ZeroDivisionError:
            object_handle.write("Warning: i1 - Divide by Zero " + "\n")
            print("@3")
            pass
        except ValueError:
            object_handle.write("Warning: i1 - Value Error" + "\n")
            pass

        print("past try")
        red = None
        green = None
        blue = None

        cond1 = i1 < th1
        cond2 = i2 < th2
        cond3 = i3 > th3

        i1 = None
        i2 = None
        i3 = None

        cond = (cond1 * cond2 * cond3)

        cond1 = None
        cond2 = None
        cond3 = None

        # Save image
        object_handle.write("out_dir=  " + out_dir + "\n")
        out_fn = os.path.join(out_dir, "cc_rgb", selected_orthomosaic_FileName_noExt + '_cc_rgb.dat') # splittext: split the path name into a pair root and ext
        object_handle.write("out_fn = " + out_fn + " \n")
        driver = gdal.GetDriverByName("ENVI")

        outds = driver.Create(out_fn, in_img.ds.RasterXSize, in_img.ds.RasterYSize, 1, gdal.GDT_Byte)
        outds.SetGeoTransform(in_img.ds.GetGeoTransform())
        outds.SetProjection(in_img.ds.GetProjection())
        outds.GetRasterBand(1).WriteArray(cond)
        print("after")
        outds = None
        in_img = None
        cond = None

        object_handle.write("Done with cc... " + " \n")

#------------------------------------------------------------------------------------------------------------------------------------------------------------generate_vis Function

def generate_vis(object_handle, selected_orthomosaic_FileName_noExt):
    global out_dir
    global files
    if(len(files) == 0):
        object_handle.write("ERROR: There are no files uploaded in the array. " + " \n")
        return
    print("vis_files: ", files)
    index = 0
    for f in files:
        print("index: ", index)
        print("file at index: ", files[index])
        index += 1
        object_handle.write("Generating VIs for the image: " + f + " \n")

        # Open image without loading to memory
        in_img = rs2.RSImage(f)
        x_size = in_img.ds.RasterXSize
        y_size = in_img.ds.RasterYSize
        geo_transform = in_img.ds.GetGeoTransform()
        geo_proj = in_img.ds.GetProjection()

        # Read bands
        red = in_img.img[0,:,:].astype(np.uint8)
        green = in_img.img[1,:,:].astype(np.uint8)
        blue = in_img.img[2,:,:].astype(np.uint8)
        alpha = in_img.img[2,:,:].astype(np.uint8) # TODO: put this back to 3

        in_img = None

        # grvi processing
        grvi = (green - red) / (green + red)
        object_handle.write("Saving GRVI... " + " \n")
        out_fn_grvi = os.path.join(out_dir, 'grvi', selected_orthomosaic_FileName_noExt + '_grvi.dat')
        driver_grvi = gdal.GetDriverByName("ENVI")
        outds_grvi = driver_grvi.Create(out_fn_grvi, x_size, y_size, 2, gdal.GDT_Float32)
        outds_grvi.SetGeoTransform(geo_transform)
        outds_grvi.SetProjection(geo_proj)
        outds_grvi.GetRasterBand(1).WriteArray(grvi)
        outds_grvi.GetRasterBand(2).WriteArray(alpha)
        outds_grvi = None
        grvi = None

        # mgrvi processing
        mgrvi = np.float32(green**2 - red**2) / np.float32(green**2+red**2)
        object_handle.write("Saving MGRVI... " + " \n")
        out_fn_mgrvi = os.path.join(out_dir, 'mgrvi', selected_orthomosaic_FileName_noExt + '_mgrvi.dat')
        driver_mgrvi = gdal.GetDriverByName("ENVI")
        outds_mgrvi = driver_mgrvi.Create(out_fn_mgrvi, x_size, y_size, 2, gdal.GDT_Float32)
        outds_mgrvi.SetGeoTransform(geo_transform)
        outds_mgrvi.SetProjection(geo_proj)
        outds_mgrvi.GetRasterBand(1).WriteArray(mgrvi)
        outds_mgrvi.GetRasterBand(2).WriteArray(alpha)
        outds_mgrvi = None
        mgrvi = None

        # rgbvi processing
        rgbvi = (green**2 - red * blue) / (green**2 + red * blue)
        object_handle.write("Saving RGBVI... " + " \n")
        out_fn_rgbvi = os.path.join(out_dir, 'rgbvi', selected_orthomosaic_FileName_noExt + '_rgbvi.dat')
        driver_rgbvi = gdal.GetDriverByName("ENVI")
        outds_rgbvi = driver_rgbvi.Create(out_fn_rgbvi, x_size, y_size, 2, gdal.GDT_Float32)
        outds_rgbvi.SetGeoTransform(geo_transform)
        outds_rgbvi.SetProjection(geo_proj)
        outds_rgbvi.GetRasterBand(1).WriteArray(rgbvi)
        outds_rgbvi.GetRasterBand(2).WriteArray(alpha)
        outds_rgbvi = None
        rgbvi = None

        # exg processing
        red_s = np.float32(red)/np.float32(red+green+blue)
        green_s = np.float32(green)/np.float32(red+green+blue)
        blue_s = np.float32(blue)/np.float32(red+green+blue)
        red = None
        green = None
        blue = None
        exg = 2*green_s - red_s - blue_s
        object_handle.write("Saving ExG... " + " \n")
        out_fn_exg = os.path.join(out_dir, 'exg', selected_orthomosaic_FileName_noExt + '_exg.dat')
        driver_exg = gdal.GetDriverByName("ENVI")
        outds_exg = driver_exg.Create(out_fn_exg, x_size, y_size, 2, gdal.GDT_Float32)
        outds_exg.SetGeoTransform(geo_transform)
        outds_exg.SetProjection(geo_proj)
        outds_exg.GetRasterBand(1).WriteArray(exg)
        outds_exg.GetRasterBand(2).WriteArray(alpha)
        outds_exg = None
        exg = None

        # exgr processing
        exgr = 2*green_s - red_s - blue_s - 1.4*red_s - green_s
        object_handle.write("Saving ExGR... " + " \n")
        out_fn_exgr = os.path.join(out_dir, 'exgr', selected_orthomosaic_FileName_noExt + '_exgr.dat')
        driver_exgr = gdal.GetDriverByName("ENVI")
        outds_exgr = driver_exgr.Create(out_fn_exgr, x_size, y_size, 2, gdal.GDT_Float32)
        outds_exgr.SetGeoTransform(geo_transform)
        outds_exgr.SetProjection(geo_proj)
        outds_exgr.GetRasterBand(1).WriteArray(exgr)
        outds_exgr.GetRasterBand(2).WriteArray(alpha)
        outds_exgr = None
        exgr = None
        alpha = None

    object_handle.write("Done with VIs... " + " \n")

#------------------------------------------------------------------------------------------------------------------------------------upload_shp Function
"""
 Name: upload_shp
 Function: Sets the selected boundary file to the global shape file variable that contains the file path to what shape file to use in attribute generation.
 Parameters: object_handle - writing to debug file
             selected_boundary_FilePath (String) - path to selected boundary file
"""

def upload_shp(object_handle, selected_boundary_FilePath):
    global shp_file
    object_handle.write("Will upload the shp file... " + " \n")

    shp_file = selected_boundary_FilePath                           # set shape file path to the one specified in the boundary field of the website by the user.
    #shp_file.set(askopenfilename(filetypes=[("Files", "*.shp"), ("All Files", "*.*")]))

    if not shp_file:                                                            # error handling if shape file is not properly read
        object_handle.write("ERROR: unable to read the SHP file " + " \n")
        return

    object_handle.write("Uploading the SHP file (path): " + shp_file + " \n")
    object_handle.write("Done uploading the boundary file ..." + " \n")

#------------------------------------------------------------------------------------------------------------------------------------upload_chm Function
"""
 Name: upload_chm
 Function: Sets the selected Canopy Height Model(CHM) file to the global chm_file variable that contains the file path to what CHM to use in attribute generation.
 Parameters: object_handle - writing to debug file
             selected_CanopyHeightModel (String) - path to selected CHM file
"""

def upload_chm(object_handle, selected_CanopyHeightModel_FilePath):
    global chm_file

    chm_file = selected_CanopyHeightModel_FilePath                          # set Canopy Height Model file path to the one specified in the respectful field located on the webpage by the user.
    object_handle.write("Selected the CHM file as " + chm_file + " \n")

    #chm_files = glob.glob(os.path.join(chm_dir.get(), '*.tif'))
    # chm_files = os.listdir(chm_dir.get())
    #print(f'The files read are: {chm_files}')
    #return

#------------------------------------------------------------------------------------------------------------------------------------generate_attributes Function
"""
 Name: generate_attributes
 Function: generate the different attributes using the get_cc, get_exg, get_ch and get_cv functions located in their respectful Python files.
 Parameters: object_handle - writing to debug file
             selected_orthomosaic_EPSG (Integer) - EPSG value of selected Othomosaic files
             selected_boundary_FileName_noExt (String) - the selected boundary filename with no file extension.
             cc_checked (Boolean) - is cc checkbox checked
             exg_checked (Boolean) - is exg checkbox checked
             ch_checked (Boolean) - is ch checkbox checked
             cv_checked (Boolean) - is cv checkbox checked
"""

def generate_attributes(object_handle, selected_orthomosaic_FileName_noExt, selected_orthomosaic_EPSG, selected_boundary_FileName_noExt, cc_checked, exg_checked, ch_checked, cv_checked):

    global shp_file, chm_file, out_dir, globalCount, chm_files, no_chm       # grab global vars
    chm_name = "chm" + str(globalCount)
    object_handle.write("Using EPSG: " + selected_orthomosaic_EPSG + " \n")                             # write to check what vars are holding
    object_handle.write("GENERATE - shp_file: " + shp_file + " \n")
    object_handle.write("GENERATE - out_dir: " + out_dir + " \n")
    object_handle.write("GENERATE -  chm_file " + chm_file + " \n")

    if(cc_checked):
        cc_shp_path = os.path.join(out_dir, 'cc_boundary', ('cc_boundary_' + selected_orthomosaic_FileName_noExt + ".shp"))
        if(os.path.exists(cc_shp_path)):
            print("The Cc shape file already exists! Skipping Cc attribute generation!")
            pass
        else:
            print('EPSG: ', selected_orthomosaic_EPSG)
            get_cc(selected_orthomosaic_EPSG, shp_file, out_dir, selected_orthomosaic_FileName_noExt, object_handle)                     # call to python function to calculate canopy cover(cc)
            cc_geojson_path = os.path.join(out_dir, 'cc_boundary', ('cc_boundary_' + selected_orthomosaic_FileName_noExt + '.geojson'))
            command = f"ogr2ogr -f geojson {cc_geojson_path} {cc_shp_path}"                           #command to convert shape file to geojson file
            if(os.system(command) == 0):                                                                #if the command was success, print success message. else, print error message
                print("The shape file was successfully converted to a geojson file!")

                cc_geojson_file = geopandas.read_file(cc_geojson_path)                                                                              # read exg geojson file to variable
                cc_geojson_file_ESPG = cc_geojson_file.crs                                                                                 # check the CRS of the geojson file.

                print(f"cc_geojson_file_ESPG: {cc_geojson_file_ESPG}")

                if (cc_geojson_file_ESPG != 4326):                             #If GeoJSON file EPSG not equal to 4326, convert the file.
                    cc_geojson_converted_path = os.path.join(out_dir, 'cc_boundary', ('cc_boundary_' + selected_boundary_FileName_noExt + "_converted"+ '.geojson'))     # path for converted cc geoJSON file
                    command = f"ogr2ogr -s_srs {cc_geojson_file_ESPG} -t_srs epsg:4326 -f GEOJSON {cc_geojson_converted_path} {cc_geojson_path}"
                    if(os.system(command) == 0):                                                            #if the command was success, print success message. else, print error message
                        print("The GeoJSON file was successfully converted to the EPSG value 3426!")
                        os.remove(cc_geojson_path)
                        shutil.move(cc_geojson_converted_path, cc_geojson_path)
                    else:
                        print("ERROR: There was an error trying to convert the cc GeoJSON file to the correct EPSG!")
                else:
                    print("The GeoJSON file already has the correct EPSG value (4326).")
            else:
                print("ERROR: there was an error trying to create the GeoJSON file!")

            cc_csv_path = os.path.join(out_dir, 'cc_boundary', ('cc_boundary_' + selected_orthomosaic_FileName_noExt + '.csv'))
            command = f"ogr2ogr -f CSV {cc_csv_path} {cc_shp_path}"                                                                    # command to convert shape file to CSV file format.
            if(os.system(command) == 0):                                                                                                 # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a CSV file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the CSV file format.")

            cc_xlsx_path = os.path.join(out_dir, 'cc_boundary', ('cc_boundary_' + selected_orthomosaic_FileName_noExt + '.xlsx'))
            command = f"ogr2ogr -f xlsx {cc_xlsx_path} {cc_shp_path}"                                                                          # command to convert shape file to xlsx file format.
            if(os.system(command) == 0):                                                                                                    # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a xlsx file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the xlsx file format.")

            object_handle.write("Done with CC attributes " + " \n")
            print("something")
    else:
        object_handle.write("cc_checked was false!" + " \n")
    print ("pre-exg")
    if(exg_checked):
        exg_shp_path = os.path.join(out_dir, 'exg_boundary', ('exg_boundary_' + selected_orthomosaic_FileName_noExt + ".shp"))
        if(os.path.exists(exg_shp_path)):
            print("The Exg shape file already exists! Skipping Exg attribute generation!")
            pass
        else:
            get_exg(selected_orthomosaic_EPSG, shp_file, out_dir, selected_orthomosaic_FileName_noExt, object_handle)                        # call to python function to calculate Excess Greeness (exg)

            exg_geojson_path = os.path.join(out_dir, 'exg_boundary', ('exg_boundary_' + selected_orthomosaic_FileName_noExt + '.geojson'))
            command = f"ogr2ogr -f geojson {exg_geojson_path} {exg_shp_path}"                           #command to convert shape file to geojson file
            if(os.system(command) == 0):                                                                #if the command was success, print success message. else, print error message
                print("The shape file was successfully converted to a geojson file!")

                exg_geojson_file = geopandas.read_file(exg_geojson_path)                                                                              # read exg geojson file to variable
                exg_geojson_file_ESPG = exg_geojson_file.crs                                                                                 # check the CRS of the geojson file.

                print(f"exg_geojson_file_ESPG: {exg_geojson_file_ESPG}")

                if (exg_geojson_file_ESPG != 4326):                             #If GeoJSON file EPSG not equal to 4326, convert the file.
                    exg_geojson_converted_path = os.path.join(out_dir, 'exg_boundary', ('exg_boundary_' + selected_boundary_FileName_noExt + "_converted"+ '.geojson'))     # path for converted exg geoJSON file
                    command = f"ogr2ogr -s_srs {exg_geojson_file_ESPG} -t_srs epsg:4326 -f GEOJSON {exg_geojson_converted_path} {exg_geojson_path}"
                    if(os.system(command) == 0):                                                            #if the command was success, print success message. else, print error message
                        print("The GeoJSON file was successfully converted to the EPSG value 3426!")
                        os.remove(exg_geojson_path)
                        shutil.move(exg_geojson_converted_path, exg_geojson_path)
                    else:
                        print("ERROR: There was an error trying to convert the EXG GeoJSON file to the correct EPSG!")
                else:
                    print("The GeoJSON file already has the correct EPSG value (4326).")
            else:
                print("ERROR: there was an error trying to create the GeoJSON file!")

            exg_csv_path = os.path.join(out_dir, 'exg_boundary', ('exg_boundary_' + selected_orthomosaic_FileName_noExt + '.csv'))
            command = f"ogr2ogr -f CSV {exg_csv_path} {exg_shp_path}"                                                                    # command to convert shape file to CSV file format.
            if(os.system(command) == 0):                                                                                                 # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a CSV file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the CSV file format.")

            exg_xlsx_path = os.path.join(out_dir, 'exg_boundary', ('exg_boundary_' + selected_orthomosaic_FileName_noExt + '.xlsx'))
            command = f"ogr2ogr -f xlsx {exg_xlsx_path} {exg_shp_path}"                                                                          # command to convert shape file to xlsx file format.
            if(os.system(command) == 0):                                                                                                    # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a xlsx file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the xlsx file format.")

        object_handle.write("Done with ExG attributes " + " \n")

    # if there is no CHM then skip
    if (no_chm == True):
        print('pass-ch')
        pass
    elif((ch_checked) and (chm_files[globalCount] != '0')):                     # if CH is checked but the CHM = "0" then skip CH generation for this ortho
        print("in ch")
        ch_shp_path = os.path.join(out_dir, 'ch_boundary', ('ch_boundary_' + selected_orthomosaic_FileName_noExt + ".shp"))
        if(os.path.exists(ch_shp_path)):
            print("The CH shape file already exists! Skipping CH attribute generation!")
            pass
        else:
            get_ch(selected_orthomosaic_EPSG, shp_file, chm_file, out_dir, selected_orthomosaic_FileName_noExt, object_handle)           # call to python function to calculate canopy height(ch)

            ch_geojson_path = os.path.join(out_dir, 'ch_boundary', ('ch_boundary_' + selected_orthomosaic_FileName_noExt + '.geojson'))
            command = f"ogr2ogr -f geojson {ch_geojson_path} {ch_shp_path}"                           #command to convert shape file to geojson file
            if(os.system(command) == 0):                                                                #if the command was success, print success message. else, print error message
                print("The shape file was successfully converted to a geojson file!")

                ch_geojson_file = geopandas.read_file(ch_geojson_path)                                                                              # read ch geojson file to variable
                ch_geojson_file_ESPG = ch_geojson_file.crs                                                                                 # check the CRS of the geojson file.

                print(f"ch_geojson_file_ESPG: {ch_geojson_file_ESPG}")

                if (ch_geojson_file_ESPG != 4326):                             #If GeoJSON file EPSG not equal to 4326, convert the file.
                    ch_geojson_converted_path = os.path.join(out_dir, 'ch_boundary', ('ch_boundary_' + selected_boundary_FileName_noExt + "_converted"+ '.geojson'))     # path for converted ch geoJSON file
                    command = f"ogr2ogr -s_srs {ch_geojson_file_ESPG} -t_srs epsg:4326 -f GEOJSON {ch_geojson_converted_path} {ch_geojson_path}"
                    if(os.system(command) == 0):                                                            #if the command was success, print success message. else, print error message
                        print("The GeoJSON file was successfully converted to the EPSG value 3426!")
                        os.remove(ch_geojson_path)
                        shutil.move(ch_geojson_converted_path, ch_geojson_path)
                    else:
                        print("ERROR: There was an error trying to convert the ch GeoJSON file to the correct EPSG!")
                else:
                    print("The GeoJSON file already has the correct EPSG value (4326).")
            else:
                print("ERROR: there was an error trying to create the GeoJSON file!")

            ch_csv_path = os.path.join(out_dir, 'ch_boundary', ('ch_boundary_' + selected_orthomosaic_FileName_noExt + '.csv'))
            command = f"ogr2ogr -f CSV {ch_csv_path} {ch_shp_path}"                                                                    # command to convert shape file to CSV file format.
            if(os.system(command) == 0):                                                                                                 # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a CSV file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the CSV file format.")

            ch_xlsx_path = os.path.join(out_dir, 'ch_boundary', ('ch_boundary_' + selected_orthomosaic_FileName_noExt + '.xlsx'))
            command = f"ogr2ogr -f xlsx {ch_xlsx_path} {ch_shp_path}"                                                                          # command to convert shape file to xlsx file format.
            if(os.system(command) == 0):                                                                                                    # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a xlsx file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the xlsx file format.")

            object_handle.write("Done with CH attributes " + " \n")

    # if no CHM then skip CV
    print("pre-cv")
    if (no_chm == True):
        pass
    elif((cv_checked) and (chm_files[globalCount] != '0')):                     # if CV is checked but CHM = "0" then skip CV for this ortho
        print("in cv")
        cv_shp_path = os.path.join(out_dir, 'cv_boundary', ('cv_boundary_' + selected_orthomosaic_FileName_noExt + ".shp"))
        if(os.path.exists(cv_shp_path)):
            print("The CV shape file already exists! Skipping CV attribute generation!")
            pass
        else:
            get_cv(selected_orthomosaic_EPSG, shp_file, chm_file, out_dir, selected_orthomosaic_FileName_noExt, object_handle)       # call to python function to calculate canaopy volume(cv)
            print("out of cv")
            cv_geojson_path = os.path.join(out_dir, 'cv_boundary', ('cv_boundary_' + selected_orthomosaic_FileName_noExt + '.geojson'))
            command = f"ogr2ogr -f geojson {cv_geojson_path} {cv_shp_path}"                           #command to convert shape file to geojson file
            if(os.system(command) == 0):                                                                #if the command was success, print success message. else, print error message
                print("The shape file was successfully converted to a geojson file!")

                cv_geojson_file = geopandas.read_file(cv_geojson_path)                                                                              # read cv geojson file to variable
                cv_geojson_file_ESPG = cv_geojson_file.crs                                                                                 # check the CRS of the geojson file.

                print(f"cv_geojson_file_ESPG: {cv_geojson_file_ESPG}")

                if (cv_geojson_file_ESPG != 4326):                             #If GeoJSON file EPSG not equal to 4326, convert the file.
                    cv_geojson_converted_path = os.path.join(out_dir, 'cv_boundary', ('cv_boundary_' + selected_boundary_FileName_noExt + "_converted"+ '.geojson'))     # path for converted ch geoJSON file
                    command = f"ogr2ogr -s_srs {cv_geojson_file_ESPG} -t_srs epsg:4326 -f GEOJSON {cv_geojson_converted_path} {cv_geojson_path}"
                    if(os.system(command) == 0):                                                            #if the command was success, print success message. else, print error message
                        print("The GeoJSON file was successfully converted to the EPSG value 3426!")
                        os.remove(cv_geojson_path)
                        shutil.move(cv_geojson_converted_path, cv_geojson_path)
                    else:
                        print("ERROR: There was an error trying to convert the cv GeoJSON file to the correct EPSG!")
                else:
                    print("The GeoJSON file already has the correct EPSG value (4326).")
            else:
                print("ERROR: there was an error trying to create the GeoJSON file!")

            cv_csv_path = os.path.join(out_dir, 'cv_boundary', ('cv_boundary_' + selected_orthomosaic_FileName_noExt + '.csv'))
            command = f"ogr2ogr -f CSV {cv_csv_path} {cv_shp_path}"                                                                    # command to convert shape file to CSV file format.
            if(os.system(command) == 0):                                                                                                 # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a CSV file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the CSV file format.")

            cv_xlsx_path = os.path.join(out_dir, 'cv_boundary', ('cv_boundary_' + selected_orthomosaic_FileName_noExt + '.xlsx'))
            command = f"ogr2ogr -f xlsx {cv_xlsx_path} {cv_shp_path}"                                                                          # command to convert shape file to xlsx file format.
            if(os.system(command) == 0):                                                                                                    # if the command was success, print success message. else, print error message
                print("The file was successfully converted to a xlsx file!!!!!!!!")
            else:
                print("ERROR: There was an error trying to convert the shape file to the xlsx file format.")

        object_handle.write("Done with CV attributes " + " \n")

#------------------------------------------------------------------------------------------------------------------------------------merge_shp function

def merge_shp(selected_boundary_FilePath, selected_orthomosaic_EPSG, cc_checked, exg_checked, ch_checked, cv_checked):
    #### ADD CH AND CV TO THE SHP FILE MERGING
    print("start")
    global ortho_name_array, project_folder, chm_files

    # create an array containing the selected names for dat files
    dat_dirs = []
    if (cc_checked):
        dat_dirs.append("cc_rgb")
    if (exg_checked):
        dat_dirs.append("exg")
    if (ch_checked):
        dat_dirs.append("ch")
    if (cv_checked):
        dat_dirs.append("cv")

    # nested loop to grab all of the ortho files and CHM files for each specific attribtue
    # this is to create a merged SHP file
    for d in dat_dirs:
        count = 0
        chm_counter = 0
        for o in ortho_name_array:            # Iterate through the length of string extensions for the directories
            path_to_dat_file = project_folder + '/' + o + '/' + d + '/' + o + '_' + d + ".dat"
            path_to_hdr_file = project_folder + '/' + o + '/' + d + '/' + o + '_' + d + ".hdr"
            temp_dat_folder = project_folder + '/' + 'temp_dat_folder' + '_' + d
            if ((d == 'ch' or d == 'cv')):                                      # only CH/CV use CHM files for SHP results
                if (chm_files[count] != '0'):
                    chm_path = chm_files[count]
                    chm_counter += 1
                else:
                    count += 1
                    continue
            if (count == 0 or chm_counter == 1):                                     # create temp folders for merged SHP results
                if os.path.exists(temp_dat_folder):
                    shutil.rmtree(temp_dat_folder)
                    os.makedirs(temp_dat_folder)
                else:
                    os.makedirs(temp_dat_folder)
            if (d == 'cc_rgb' or d == "exg"):                                     # Move dat files for CC/EXG results
                if (os.path.exists(path_to_dat_file)):
                    shutil.move(path_to_dat_file, temp_dat_folder)
                    shutil.move(path_to_hdr_file, temp_dat_folder)
                    print("path to dat file: ", path_to_dat_file)
                else:
                    print("dir doesn't exist")
            elif (d == 'ch' or d == "cv"):
                if (os.path.exists(chm_path)):                                    # Copy CHM file in order to generate attribute results into one file
                    shutil.copy(chm_path, temp_dat_folder)
                    #shutil.move(path_to_hdr_file, temp_dat_folder)
                    print("path to chm file: ", chm_path)
                else:
                    print("chm doesn't exist")
            count += 1
        #
        print("A")

        # start of the attribute generation process in order to merge all data into one file
        # conditionals throughout allow any attribute to go through this code block and only execute the commands required for that attribute 
        if (chm_counter == 1):
            break
        gdal.UseExceptions()
        sproj = osr.SpatialReference()
        #sproj.ImportFromEPSG(32614)
        sproj.ImportFromEPSG(int(selected_orthomosaic_EPSG))

        print("B")
        if (d == 'cc_rgb' or d == 'exg'):
            in_dir = temp_dat_folder
            dat_files = glob.glob(in_dir + '/' + ('*.dat'))
            #print("dat files: ", dat_files)
            dat_files.sort()
        elif (d == 'ch' or d == 'cv'):
            temp_chm_files = chm_files
            while "0" in chm_files:
                temp_chm_files.remove('0')
            dat_files = temp_chm_files
        print("C1")
        shp_fn = selected_boundary_FilePath

        out_fn = temp_dat_folder + '/' + 'merged_shp_' + d + ".shp"

        driver = ogr.GetDriverByName('ESRI Shapefile') #file type
        shapef = driver.Open(shp_fn, 1)
        lyr = shapef.GetLayer()
        spatialRef = lyr.GetSpatialRef() # Get projection

        outDriver = ogr.GetDriverByName('ESRI Shapefile')
        if os.path.exists(out_fn):
            outDriver.DeleteDataSource(out_fn)
        outDataSource = outDriver.CreateDataSource(out_fn)
        outLayer = outDataSource.CopyLayer(lyr, "agrilife")
        out_fn_prj = os.path.join(temp_dat_folder, os.path.splitext(out_fn)[0] + '.prj')
        print("C2")
        spatialRef.MorphToESRI()
        file = open(out_fn_prj, 'w')
        file.write(spatialRef.ExportToWkt())
        file.close()

        outDataSource = None
        shapef = None

        driver = ogr.GetDriverByName('ESRI Shapefile') #file type
        shapef_out = driver.Open(out_fn, 1)
        Layer = shapef_out.GetLayer()
        ###
        print("C3")
        print("Dat Files: ", dat_files)
        ratio_defn = []
        for fn in dat_files:
            basename = os.path.basename(fn)
            date_str = basename.split("20",1)[1].split("_",1)[0]
            #ratio_defn.append(ogr.FieldDefn(d+date_str, ogr.OFTReal))
            ratio_defn.append(ogr.FieldDefn('20'+date_str, ogr.OFTReal))

        for tt in ratio_defn:
            Layer.CreateField(tt)

        for i in range(len(dat_files)):
            print ("Processing (%d/%d) [%.2f]" % (i+1, len(dat_files), float(i+1) / len(dat_files) * 100.0))

            # Create an OGR layer from a boundary shapefile
            driver = ogr.GetDriverByName('ESRI Shapefile') #file type
            shapef_out = driver.Open(out_fn, 1)
            Layer = shapef_out.GetLayer()
            print("index: ", i)
            dat_fn = dat_files[i]

            basename = os.path.basename(dat_fn)
            #probably change this to fit ortho number for attribute table
            date_str = basename.split("20", 1)[1].split("_", 1)[0]


            print ("Image reading")
            dat_img = rs2.RSImage(dat_fn)

            print ("Extracting attribute")
            for crop_poly in Layer:
                geoTrans = dat_img.geotransform
                clipped_dat = dat_img.clip_by_polygon(crop_poly)
                filtered_dat = clipped_dat[0,:,:]
                if (d != "cc_rgb"):
                    filtered_dat = filtered_dat[np.nonzero(filtered_dat)]
                filtered_dat = filtered_dat[~np.isnan(filtered_dat)]
                filtered_dat = filtered_dat[~np.isinf(filtered_dat)]

                if (d == 'exg'):
                    exg_mean = np.mean((filtered_dat))
                    crop_poly.SetField('20'+date_str, float(exg_mean))
                elif (d == 'cc_rgb'):
                    total_num_pix = filtered_dat.size
                    dat_num_pix = filtered_dat.sum()
                    dat_ratio = float(dat_num_pix) / float(total_num_pix) * 100
                    #crop_poly.SetField(d+date_str, float(dat_ratio))
                    crop_poly.SetField('20'+date_str, float(dat_ratio))
                elif (d == 'ch'):
                    if (filtered_dat.size == 0):
                        ch_ratio = 0
                    else:
                        ch_ratio = np.percentile((filtered_dat), 95)
                    crop_poly.SetField('20'+date_str, float(ch_ratio))
                elif (d == 'cv'):
                    if (filtered_dat.size == 0):
                        cv_ratio = 0
                    else:
                        cv_ratio = np.sum((filtered_dat) * geoTrans[1] * geoTrans[1])
                    crop_poly.SetField('20'+date_str, float(cv_ratio))
                Layer.SetFeature(crop_poly)
            dat_img = None



        gdal.ErrorReset()
        shapef_out = None

#------------------------------------------------------------------------------------------------------------------------------------rm_files Function
"""
 Name: rm_files
 Function: generate the different attributes using the get_cc, get_exg, get_ch and get_cv functions located in their respectful Python files.
 Parameters: object_handle - writing to debug file
             selected_orthomosaic_EPSG (Integer) - EPSG value of selected Othomosaic files
"""

def rm_files(object_handle, selected_project_name, selected_orthomosaic_FileName_noExt, selected_boundary_FileName_noExt):
#path to results directory for the selected project and orthomosaic


# string extensions for the different directories constaining the different dat files used to generate the attributes that need to be deleted.
    dat_dirs = ["cc_rgb", "exg", "exgr", "grvi", "mgrvi", "rgbvi"]
    index = 0
    for o in ortho_name_array:
        path_to_project_folder = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + o + "/"
        while index < len(dat_dirs):            # Iterate through the length of string extensions for the directories
            path_to_dat_dir = path_to_project_folder + dat_dirs[index]                          #set path to directory
            if (os.path.exists(path_to_dat_dir)):                                           #if the directory exists delete it
                shutil.rmtree(path_to_dat_dir)
                #object_handle("Removed dir: " + str(path_to_dat_dir) + " \n")
                print(path_to_dat_dir)
                print("Removed!")
            else:
                #object_handle("dir: " + str(path_to_dat_dir) + " didn't exist! \n")           #else, state that the direcory does not exist
                print(path_to_dat_dir)
                print("dir doesn't exist")
                continue
            index += 1

#------------------------------------------------------------------------------------------------------------------------------------Run Main
if __name__ == "__main__":
    main()
