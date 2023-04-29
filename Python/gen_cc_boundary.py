import os, sys
import glob
import rs2
import numpy as np
import operator
from osgeo import gdal, gdalnumeric, ogr, osr

# main function is used to debug and test the file (running it from the server)
def main():
	#run function with dummy data if ran from server
	#get_cc(32614, "/var/www/html/uas_data/uploads/products/2021_Corpus_Christi_Cotton_and_Corn/10/28/2021/SHAPE/2021_cc_brewer_plot_boundary_map_maturity_trial/2021_cc_brewer_plot_boundary_map_maturity_trial.shp", "/home/ubuntu/web/uas_data/download/product/2021_Corpus_Christi_Cotton_and_Corn/20210408_cc_p4r_parking_mosaic", "")
	get_cc(32614, "/var/html/uas_data/uploads/products/2022_Corpus_Christi_Cotton/09/26/2022//SHAPE/2022_cc_corn_boundary/2022_cc_corn_boundary.shp", "/home/ubuntu/web/uas_data/download/product/2022_Corpus_Christi_Cotton/20220523_cc_p4r_parking_mosaic_2022_cc_corn_boundary", "20220523_cc_p4r_parking_mosaic", "")
	#get_cc(32614, "/var/html/uas_data/uploads/products/2022_Corpus_Christi_Cotton/09/26/2022//SHAPE/2022_cc_corn_boundary/2022_cc_corn_boundary.shp", "/home/ubuntu/web/uas_data/download/product/2022_Corpus_Christi_Cotton/20220523_cc_p4r_parking_mosaic_2022_cc_corn_boundary", "20220523_cc_p4r_parking_mosaic", "")
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Name: get_cc
# Function: generates Canopy Cover attribute and saves the results to its respect to what project/ orthomosiac are selected.
# Parameters: epsg - EPSG value of the selected orthomosiac
#             shp - path to the selected shape/boundary file selected
#             out_dir - path the othomosiac directory where the generated results are stored.

def get_cc(epsg, shp, out_dir, selected_orthomosaic_FileName_noExt, object_handle):

#	object_handle.write("Generating CC plot " + " \n")
#	print("Generating CC plot")
	selected_orthomosaic_FileName = selected_orthomosaic_FileName_noExt
	selected_boundary = os.path.basename(shp)
	selected_boundary_array = selected_boundary.split(".")
	selected_boundary_FileName_noExt = selected_boundary_array[0]

	gdal.UseExceptions()

	# Coordinate system
	sproj = osr.SpatialReference()
	sproj.ImportFromEPSG(int(epsg))

	in_dir_cc_ndvi = os.path.join(out_dir, 'cc_rgb')
	print(in_dir_cc_ndvi)
	files_cc_ndvi = glob.glob(os.path.join(in_dir_cc_ndvi, '*.dat'))
	files_cc_ndvi.sort()
	print('files_cc_ndvi:')
	print(files_cc_ndvi)

	out_dir = os.path.join(out_dir, 'cc_boundary')
	if not os.path.exists(out_dir):
			os.mkdir(out_dir)

	#out_cc = os.path.join(out_dir, ('cc_boundary_' + os.path.basename(shp)))
	#out_cc = os.path.join(out_dir, ('cc_boundary_' + selected_orthomosaic_FileName + "_" + selected_boundary_FileName_noExt + "_" + chm_name1 + ".shp"))
	out_cc = os.path.join(out_dir, ('cc_boundary_' + selected_orthomosaic_FileName + ".shp"))

	print ("Crop Shape")
	## shapefile open
	driver = ogr.GetDriverByName('ESRI Shapefile') #file type
	shapef = driver.Open(shp, 1)
	lyr = shapef.GetLayer()
	spatialRef = lyr.GetSpatialRef() # Get projection

	## Create the output shapefile
	outDriver = ogr.GetDriverByName('ESRI Shapefile')

	if os.path.exists(out_cc):
		outDriver.DeleteDataSource(out_cc)

	outDataSource_cc = outDriver.CreateDataSource(out_cc)
	outLayer_cc = outDataSource_cc.CopyLayer(lyr, "agrilife")
	out_fn_prj_cc = os.path.join(out_dir, os.path.splitext(out_cc)[0] + '.prj')

	spatialRef.MorphToESRI()
	file = open(out_fn_prj_cc, 'w')
	file.write(spatialRef.ExportToWkt())
	file.close()

	outDataSource_cc = None
	shapef = None

	# Create an OGR layer from a boundary shapefile
	driver = ogr.GetDriverByName('ESRI Shapefile') #file type
	shapef_out_cc = driver.Open(out_cc, 1)
	ccLayer = shapef_out_cc.GetLayer()

	cc_ratio_defn = []
	for fn in files_cc_ndvi:
		basename = os.path.basename(fn)
		print("basename: ")
		print(basename)
		date_str = basename.split("20", 1)[1].split("_",1)[0]
		cc_ratio_defn.append(ogr.FieldDefn('20' + date_str, ogr.OFTReal))
		#cc_ratio_defn.append(ogr.FieldDefn('20'+date_str, ogr.OFTReal))

	for tt in cc_ratio_defn:
		ccLayer.CreateField(tt)

	for i in range(0, len(files_cc_ndvi)):

		print ("Multi Processing (%d/%d) [%.2f]" % (i+1, len(files_cc_ndvi), float(i+1) / len(files_cc_ndvi) * 100.0))

		# Create an OGR layer from a boundary shapefile
		driver = ogr.GetDriverByName('ESRI Shapefile') #file type
		shapef_out_cc = driver.Open(out_cc, 1)
		ccLayer = shapef_out_cc.GetLayer()

		cc_fn = files_cc_ndvi[i]

		basename = os.path.basename(cc_fn)
		date_str = basename.split("20", 1)[1].split("_", 1)[0]

		print ("Image reading")
		cc_img = rs2.RSImage(cc_fn)

		print ("Extracting attribute")
		for crop_poly in ccLayer:

			geoTrans = cc_img.geotransform
			clipped_cc = cc_img.clip_by_polygon(crop_poly)

			## CC
			filtered_cc = clipped_cc[0,:,:]
			# filtered_cc = filtered_cc[np.nonzero(filtered_cc)]
			filtered_cc = filtered_cc[~np.isnan(filtered_cc)]
			filtered_cc = filtered_cc[~np.isinf(filtered_cc)]

			total_num_pix = filtered_cc.size
			cc_num_pix = filtered_cc.sum()
			cc_ratio = float(cc_num_pix) / float(total_num_pix) * 100

			crop_poly.SetField('20' + date_str, float(cc_ratio))
			#crop_poly.SetField('20'+date_str, float(cc_ratio))
			ccLayer.SetFeature(crop_poly)

		cc_img = None


	gdal.ErrorReset()
	shapef_out_cc = None

if __name__ == "__main__":
    main()
