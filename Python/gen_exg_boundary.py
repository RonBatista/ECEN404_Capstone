import os, sys
import glob
import rs2
import numpy as np
import operator
from osgeo import gdal, gdalnumeric, ogr, osr

# main function is used to debug and test the file (running it from the server)
def main():

	#run function with dummy data if ran from server
	get_exg(32614, "/var/www/html/uas_data/uploads/products/2021_Corpus_Christi_Cotton_and_Corn/10/28/2021/SHAPE/2021_cc_brewer_plot_boundary_map_maturity_trial/2021_cc_brewer_plot_boundary_map_maturity_trial.shp", "/home/ubuntu/web/uas_data/download/product/2021_Corpus_Christi_Cotton_and_Corn/20210408_cc_p4r_parking_mosaic",  "20220523_cc_p4r_parking_mosaic", "")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Name: get_exg
# Function: generates EXG attribute and saves the results to its respect to what project/ orthomosiac are selected.
# Parameters: epsg - EPSG value of the selected orthomosiac
#             shp - path to the selected shape/boundary file selected
#             out_dir - path the othomosiac directory where the generated results are stored.

def get_exg(espg, shp, out_dir, selected_orthomosaic_FileName_noExt, object_handle):
	print ("Generating ExG plot")

	selected_orthomosaic_FileName = selected_orthomosaic_FileName_noExt
	selected_boundary = os.path.basename(shp)
	selected_boundary_array = selected_boundary.split(".")
	selected_boundary_FileName_noExt = selected_boundary_array[0]
	gdal.UseExceptions()

	# Coordinate system
	sproj = osr.SpatialReference()
	sproj.ImportFromEPSG(int(espg))

	# input folder including exg
	in_dir_exg = os.path.join(out_dir, 'exg')
	# files_exg = glob.glob(in_dir_exg + ('*' + 'exg.dat'))
	files_exg = glob.glob(os.path.join(in_dir_exg, '*.dat'))
	files_exg.sort()

	print(f'exg dat file directory is: {in_dir_exg}')
	print(files_exg)

	# output folder
	out_dir = os.path.join(out_dir, 'exg_boundary')
	if not os.path.exists(out_dir):
			os.mkdir(out_dir)

	# output shapefile name
	#out_exg = os.path.join(out_dir, ('exg_boundary_' + os.path.basename(shp)))
	#out_exg = os.path.join(out_dir, ('exg_boundary_' + selected_orthomosaic_FileName + "_" + selected_boundary_FileName_noExt + "_" + chm_name1 + ".shp"))
	out_exg = os.path.join(out_dir, ('exg_boundary_' + selected_orthomosaic_FileName + ".shp"))
	#print "Crop Shape"

	## shapefile open
	driver = ogr.GetDriverByName('ESRI Shapefile') #file type
	shapef = driver.Open(shp, 1)
	lyr = shapef.GetLayer()
	spatialRef = lyr.GetSpatialRef() # Get projection

	## Create the output shapefile
	outDriver = ogr.GetDriverByName('ESRI Shapefile')

	if os.path.exists(out_exg):
		outDriver.DeleteDataSource(out_exg)

	outDataSource_cc = outDriver.CreateDataSource(out_exg)
	#outLayer_cc = outDataSource_cc.CopyLayer(lyr, "Shell")
	outLayer_cc = outDataSource_cc.CopyLayer(lyr, "agrilife")
	out_fn_prj_cc = os.path.join(out_dir, os.path.splitext(out_exg)[0] + '.prj')

	#print(out_exg)
	#print(shp)
	#print(out_fn_prj_cc)

	spatialRef.MorphToESRI()
	file = open(out_fn_prj_cc, 'w')
	file.write(spatialRef.ExportToWkt())
	file.close()

	outDataSource_cc = None
	shapef = None

	# Create an OGR layer from a boundary shapefile
	driver = ogr.GetDriverByName('ESRI Shapefile') #file type
	shapef_out_cc = driver.Open(out_exg, 1)
	ccLayer = shapef_out_cc.GetLayer()

	exg_mean_defn = []
	for fn in files_exg:
		basename = os.path.basename(fn)
		print("basename: ")
		print(basename)
		date_str = basename.split("20",1)[1].split("_",1)[0]
		#exg_mean_defn.append(ogr.FieldDefn('avEG'+date_str, ogr.OFTReal))
		exg_mean_defn.append(ogr.FieldDefn( '20' + date_str, ogr.OFTReal))
		#exg_mean_defn.append(ogr.FieldDefn('20'+date_str, ogr.OFTReal))

	#exg_sd_defn = []
	#for fn in files_exg:
		#basename = os.path.basename(fn)
		#date_str = basename.split("20",1)[1].split("_",1)[0]
		#exg_sd_defn.append(ogr.FieldDefn('sdEG'+date_str, ogr.OFTReal))

	for tt in exg_mean_defn:
		ccLayer.CreateField(tt)

	#for tt in exg_sd_defn:
		#ccLayer.CreateField(tt)

	for i in range(len(files_exg)):

		print ("Processing (%d/%d) [%.2f]" % (i+1, len(files_exg), float(i+1) / len(files_exg) * 100.0))

		# Create an OGR layer from a boundary shapefile
		driver = ogr.GetDriverByName('ESRI Shapefile') #file type
		shapef_out_cc = driver.Open(out_exg, 1)
		ccLayer = shapef_out_cc.GetLayer()

		exg_fn = files_exg[i]

		basename = os.path.basename(exg_fn)
		date_str = basename.split("20", 1)[1].split("_", 1)[0]

		print ("Image reading")

		exg_img = rs2.RSImage(exg_fn)

		print ("Extracting attribute")
		for crop_poly in ccLayer:

			geoTrans = exg_img.geotransform
			clipped_exg = exg_img.clip_by_polygon(crop_poly)

			## exg mean and SD
			filtered_exg = clipped_exg[0,:,:]
			filtered_exg = filtered_exg[np.nonzero(filtered_exg)]
			filtered_exg = filtered_exg[~np.isnan(filtered_exg)]
			filtered_exg = filtered_exg[~np.isinf(filtered_exg)]

			exg_mean = np.mean((filtered_exg))
			#exg_sd = np.std((filtered_exg))

			#crop_poly.SetField('avEG'+date_str, float(exg_mean))
			crop_poly.SetField('20' + date_str, float(exg_mean))
			#crop_poly.SetField('20'+date_str, float(exg_mean))
			#crop_poly.SetField('sdEG'+date_str, float(exg_sd))

			ccLayer.SetFeature(crop_poly)

		cc_img = None
		# chm_img = None
		exg_img = None
		# ndvi_img = None

	gdal.ErrorReset()
	shapef_out_cc = None

if __name__ == "__main__":
    main()
