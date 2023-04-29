# references:
# https://realpython.com/python-gui-tkinter/
# https://solarianprogrammer.com/2018/04/20/python-opencv-show-image-tkinter-window/
# run in data_processing_gui environment
import os
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
import numpy as np
from PIL import Image, ImageTk
import sys
import rs2
from osgeo import gdal, gdalnumeric, ogr, osr
import tifffile
from threading import *
import glob
from gen_ch_boundry import get_ch
from gen_cc_boundary import get_cc
from gen_cv_boundary import get_cv
from gen_exg_boundary import get_exg


window = tk.Tk()

epsg_13                = 32613
epsg_14                = 32614
epsg_var               = tk.StringVar()

img_file               = tk.StringVar()
shp_file               = tk.StringVar()
out_dir                = tk.StringVar()
chm_dir                = tk.StringVar()

cc_out_dir             = tk.StringVar()
grvi_out_dir           = tk.StringVar()
mgrvi_out_dir          = tk.StringVar()
rgbvi_out_dir          = tk.StringVar()
exg_out_dir            = tk.StringVar()
exgr_out_dir           = tk.StringVar()

exg_attributes_out_dir = tk.StringVar()

files                  = []
chm_files              = []

widgets_width  = 25
widgets_height = 3

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

def upload_img():
    print("Will upload the image")
    # # global img_file
    img_file = askopenfilename(filetypes=[("Image Files", "*.tif"), ("All Files", "*.*")]) #Possibly change this code to grab the the tif file specified in the orthomosaic field on the website.

    if not img_file:
        print("Error reading the image file")
        return
    # load the image
    files.append(img_file)
    for f in files:
        print(f'Uploaded the image: {f}')

    # UI message
    img_filename = os.path.splitext(os.path.basename(img_file))[0][:] # get filename without extension
    lbl_msg["text"] = f'Uploading the image \n {img_filename}'

    img_org = tifffile.imread(img_file)
    img_rgb = img_org[0::, 0::, 0:3]
    img_img = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image = img_img)

    # associate the image with the label
    lbl_field_img.configure (text = "")
    lbl_field_img.configure (width = img_tk.width(), height = img_tk.height(), text = " ", image = img_tk)
    lbl_field_img.image = img_tk # need to keep the reference of your image to avoid garbage collection

    # UI message
    lbl_msg["text"] = 'Done uploading the image ...'

def delete_img():
    files.pop()
    print('Loaded images:')
    for f in files:
        print(f' {f}')

def select_out_folder():
    print("Will upload the image")

    out_dir.set(askdirectory())
    print(f'Will be saving the results to: {out_dir.get()}')

    # create output folders
    cc_out_dir.set(os.path.join(out_dir.get(), "cc_rgb")),
    grvi_out_dir.set(os.path.join(out_dir.get(), "grvi")),
    mgrvi_out_dir.set(os.path.join(out_dir.get(), "mgrvi")),
    rgbvi_out_dir.set(os.path.join(out_dir.get(), "rgbvi")),
    exg_out_dir.set(os.path.join(out_dir.get(), "exg")),
    exgr_out_dir.set(os.path.join(out_dir.get(), "exgr")),

    results_folders = [cc_out_dir,
                       grvi_out_dir,
                       mgrvi_out_dir,
                       rgbvi_out_dir,
                       exg_out_dir,
                       exgr_out_dir]

    for folder in results_folders:
        if not os.path.exists(folder.get()):
            os.makedirs(folder.get())
            print(f'Will be saving cc the results to: {folder.get()}')

def generate_cc():
    if(len(files) == 0 or len(out_dir.get()) == 0):
        print(f'len(out_dir.get()) is {len(out_dir.get())}')
        lbl_msg["text"] = "Upload an image \nand select output folder ..."
        return

    field_count = 10
    th1 = 0.95
    th2 = 0.95
    th3 = 20

    for f in files:
        print(f'Generating CC for the image: {f}')

        # UI message
        img_filename = os.path.splitext(os.path.basename(f))[0][:] # get filename without extension
        lbl_msg["text"] = f'Generating CC for:\n {img_filename}'

        # Open image without loading to memory
        in_img = rs2.RSImage(f)

        # Read bands
        red = in_img.img[0,:,:].astype(np.float32)
        green = in_img.img[1,:,:].astype(np.float32)
        blue = in_img.img[2,:,:].astype(np.float32)

        # Calculate index
        i1 = red / green
        i2 = blue / green
        i3 = 2 * green - blue - red

        red = None
        green = None
        blue = None

        # print "Finding canopy only"
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
        out_fn = os.path.join(cc_out_dir.get(), img_filename[0:8] + '_cc_rgb.dat') # splittext: split the path name into a pair root and ext
        print(out_fn)
        driver = gdal.GetDriverByName("ENVI")

        outds = driver.Create(out_fn, in_img.ds.RasterXSize, in_img.ds.RasterYSize, 1, gdal.GDT_Byte)
        outds.SetGeoTransform(in_img.ds.GetGeoTransform())
        outds.SetProjection(in_img.ds.GetProjection())
        outds.GetRasterBand(1).WriteArray(cond)

        outds = None
        in_img = None
        cond = None

    # UI message
    lbl_msg["text"] = "Done with cc ..."

def generate_vis():
    if(len(files) == 0 or len(out_dir.get()) == 0):
        print(f'len(out_dir.get()) is {len(out_dir.get())}')
        lbl_msg["text"] = "Upload an image \nand select output folder ..."
        return

    for f in files:
        print(f'Generating VIs for the image: {f}')

        # UI message
        img_filename = os.path.splitext(os.path.basename(f))[0][:] # get filename without extension
        lbl_msg["text"] = f'Generating VIs for:\n {img_filename}'

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
        print ("Saving GRVI")
        lbl_msg["text"] = 'Saving GRVI'
        out_fn_grvi = os.path.join(grvi_out_dir.get(), img_filename[0:8] + '_grvi.dat')
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
        print ("Saving MGRVI")
        lbl_msg["text"] = 'Saving MGRVI'
        out_fn_mgrvi = os.path.join(mgrvi_out_dir.get(), img_filename[0:8] + '_mgrvi.dat')
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
        print ("Saving RGBVI")
        lbl_msg["text"] = 'Saving RGBVI'
        out_fn_rgbvi = os.path.join(rgbvi_out_dir.get(), img_filename[0:8] + '_rgbvi.dat')
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
        print ("Saving ExG")
        lbl_msg["text"] = 'Saving EXG'
        out_fn_exg = os.path.join(exg_out_dir.get(), img_filename[0:8] + '_exg.dat')
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
        print ("Saving ExGR")
        lbl_msg["text"] = 'Saving ExGR'
        out_fn_exgr = os.path.join(exgr_out_dir.get(), img_filename[0:8] + '_exgr.dat')
        driver_exgr = gdal.GetDriverByName("ENVI")
        outds_exgr = driver_exgr.Create(out_fn_exgr, x_size, y_size, 2, gdal.GDT_Float32)
        outds_exgr.SetGeoTransform(geo_transform)
        outds_exgr.SetProjection(geo_proj)
        outds_exgr.GetRasterBand(1).WriteArray(exgr)
        outds_exgr.GetRasterBand(2).WriteArray(alpha)
        outds_exgr = None
        exgr = None
        alpha = None

    # UI message
    lbl_msg["text"] = "Done with VIs ..."

def upload_shp():
    print("Will upload the shp file")
    shp_file.set(askopenfilename(filetypes=[("Image Files", "*.shp"), ("All Files", "*.*")]))

    # if not shp_file:
    #     print("Error reading the SHP file")
    #     return

    # load the shp file
    print(f'Uploading the SHP file: {shp_file.get()}')

    # UI message
    shp_filename = os.path.splitext(os.path.basename(shp_file.get()))[0][:] # get filename without extension
    lbl_msg["text"] = f'Uploading the SHP file \n {shp_filename}'

    # UI message
    lbl_msg["text"] = 'Done uploading the boundary file ...'

def upload_chm():
    global chm_files
    chm_dir.set(askdirectory())
    print(f'Selected the CHM folder as {chm_dir.get()}')
    chm_files = glob.glob(os.path.join(chm_dir.get(), '*.tif'))
    # chm_files = os.listdir(chm_dir.get())
    print(f'The files read are: {chm_files}')
    return

def generate_attributes(shp):
    global chm_files
    if epsg_var.get() == "13N":
        epsg_val = epsg_13
    elif epsg_var.get() == "14N":
        epsg_val = epsg_14

    print(f'Using EPSG: {epsg_val}')
    lbl_msg["text"] = "Using EPSG: " + str(epsg_val)

    get_exg(epsg_val, shp_file.get(), out_dir.get())
    print("Done with ExG attributes")
    lbl_msg["text"] = "Done with ExG Attributes"

    get_cc(epsg_val, shp_file.get(), out_dir.get())
    print("Done with CC attributes")
    lbl_msg["text"] = "Done with CC Attributes"

    get_ch(epsg_val, shp_file.get(), chm_files, out_dir.get())
    print("Done with CH attributes")
    lbl_msg["text"] = "Done with CH Attributes"

    get_cv(epsg_val, shp_file.get(), chm_files, out_dir.get())
    print("Done with CV attributes")
    lbl_msg["text"] = "Done with CV Attributes"


window.title("Data Processing GUI")
window.resizable(width = False, height = False)
window.rowconfigure(0, minsize = 800, weight = 1)
window.columnconfigure(1, minsize = 800, weight = 1)

#-------------------------------------------------------------------------------
# Widgets
#-------------------------------------------------------------------------------
header = tk.Label(text = "Data Processing GUI")

right_pannel = tk.Frame(
                    master = window,
                    bd     = 4)

left_pannel = tk.Frame(
                    master = window,
                    relief = tk.RAISED,
                    bd     = 4)

first_pannel = tk.Frame(
                    master = left_pannel,
                    bd     = 4)

vis_pannel = tk.Frame(
                    master = left_pannel,
                    bd     = 4)

attributes_pannel = tk.Frame(
                    master = left_pannel,
                    bd     = 4)

lbl_field_img = tk.Label(
                master = right_pannel,
                text   = "Your image will apppear here",
                width  = 100,
                height = widgets_height,
                bg     = "gainsboro",
                fg     = "black",
)

btn_upload_img = tk.Button(
                    master = first_pannel,
                    text   = "Upload Field Image",
                    width = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command= upload_img_threading
)

btn_delete_img = tk.Button(
                    master = first_pannel,
                    text   = "Delete Uploaded Image",
                    width = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command= delete_img
)

btn_select_out_dir = tk.Button(
                    master = first_pannel,
                    text   = "Select Output Folder",
                    width = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command = select_out_folder
)

lbl_cc_vi_processing = tk.Label(
                master = vis_pannel,
                text   = "----- CC and VIs Processing -----",
                width  = widgets_width,
                height = widgets_height,
                bg     = "gray99",
                fg     = "black"
)

btn_generate_cc = tk.Button(
                    master = vis_pannel,
                    text   = "Generate Canpy Cover",
                    width  = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command = generate_cc_threading
)

btn_generate_vis = tk.Button(
                    master = vis_pannel,
                    text   = "Generate VIs",
                    width  = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command = generate_vis_threading
)

lbl_attr_processing = tk.Label(
                master = attributes_pannel,
                text   = "----- Attributes Processing -----",
                width  = widgets_width,
                height = widgets_height,
                bg     = "gray99",
                fg     = "black"
)

btn_upload_shp = tk.Button(
                    master = attributes_pannel,
                    text   = "Upload Boundary File",
                    width = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command= upload_shp_threading
)

btn_upload_chm = tk.Button(
                    master = attributes_pannel,
                    text   = "Select CHM Folder",
                    width = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command= upload_chm_threading
)

txt_set_epsg = tk.Entry(
                master = attributes_pannel,
                width  = widgets_width,
                bg     = "dark sea green",
                fg     = "grey",
                justify = CENTER,
                textvariable = epsg_var)

btn_gen_attributes = tk.Button(
                    master = attributes_pannel,
                    text   = "Generate Attributes",
                    width = widgets_width,
                    height = widgets_height,
                    bg     = "gainsboro",
                    fg     = "black",
                    command= generate_attributes_threading
)

lbl_msg = tk.Label(
                master = first_pannel,
                text   = "Processing messages appear\n here",
                width  = widgets_width,
                height = 6,
                bg     = "gainsboro",
                fg     = "black",
)

#-------------------------------------------------------------------------------
# LAYOUT
#-------------------------------------------------------------------------------
# right pannel has the images
right_pannel.grid      (row=0, column=1, sticky="ew", padx=5, pady=5)
lbl_field_img.grid     (row=0, column=0, sticky="ew", padx=5, pady=5)

# left pannel has the processing options
left_pannel.grid       (row=0, column=0, sticky="ns")

# first in left pannel: upload image, delete image, select output directory
first_pannel.grid      (row=1, column=0, sticky="ew", pady=5)
btn_upload_img.grid    (row=0, column=0, sticky="ew")
btn_delete_img.grid    (row=1, column=0, sticky="ew")
btn_select_out_dir.grid(row=2, column=0, sticky="ew")
lbl_msg.grid           (row=3, column=0, sticky="ew")

# second in left pannel: generate cc and vis
vis_pannel.grid           (row=2, column=0, sticky="ew", pady=5)
lbl_cc_vi_processing.grid (row=0, column=0, sticky="ew")
btn_generate_cc.grid      (row=1, column=0, sticky="ew")
btn_generate_vis.grid     (row=2, column=0, sticky="ew")

# third in left pannel: generate attributes
attributes_pannel.grid   (row=3, column=0, sticky="ew", pady=5)
lbl_attr_processing.grid (row=0, column=0, sticky="ew")
txt_set_epsg.grid        (row=1, column=0, sticky="ew")
btn_upload_shp.grid      (row=2, column=0, sticky="ew")
btn_upload_chm.grid      (row=3, column=0, sticky="ew")
btn_gen_attributes.grid  (row=4, column=0, sticky="ew")

txt_set_epsg.insert(INSERT, "Set EPSG 13N for Amarillo 14N Else")

window.mainloop()
