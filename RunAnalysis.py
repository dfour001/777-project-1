# ------------------------------------------------------------------------------
# RunAnalysis.py contains functions that will be used to access the required
# geoprocessing tools.  The functions are organized in the order that they are
# run when the button to start the analysis is clicked.  The steps are:
#   - Prepare folder for first run if needed
#   - Interpolate nitrate levels from sample wells
#   - Summarize results of the nitrate interpolation at the tract level
#   - Update nitrates field in tracts shapefile
#   - Run OLS linear regression
# ------------------------------------------------------------------------------

import arcpy
import os


# Prepare folder for first run if needed
def initialize():
    """ Creates the needed folders and geodatabases that the tool
    requires if they do not exist yet. """

    # Create folders if needed
    for path in [
            'data/intermediate', # Where intermediate data will be stored 
            'data/output', # Output shapefiles
            'ols_reports' # Output pdf files
            ]:
        os.makedirs(path, exist_ok=True)
        
        


# Interpolate nitrate levels from sample wells
def run_idw(wells, counties, k):
    """ Performs IDW interpolation on nitrate values
    from input wells data.

    inputs:
        wells (point) - nitrate levels at sample wells
        counties (polygon) - used to set the extent and mask
                for the output interpolated raster
        k (number) - sets the power parameter in arcpy's IDW
                tool
    
    output:
        {k}.tif - a raster file in the data/intermediate folder.
                If it already exists, it will be overwritten.  This
                function returns a string path to the output file.
    """
    # Set tool parameters
    in_point_features = wells
    z_field = "nitr_ran"
    power = k

    outputPath = f'data/intermediate/{str(k).replace(".", "_")}.tif'


    # Set environmental variables and run IDW tool
    with arcpy.EnvManager(extent=counties, mask=counties, overwriteOutput=True):
        output = arcpy.sa.Idw(in_point_features, z_field, power=power, cell_size=0.005)
        output.save(outputPath)

    return outputPath


# Summarize results of the nitrate interpolation at the tract level
def get_average_nitrate_dict(tracts, zoneField, idw, k):
    """ Runs the Zonal Statistics as Table tool to summarize the
    average nitrate levels found in the idw analysis.

    inputs:
        tracts (polygon) - The census tracts
        zoneField (text) - The field name that identifies each tract
        idw (raster) - The output of the idw analysis
        k (number) - The input k value for idw (used to identify the
                idw tif file in the data/intermediate folder)

    output:
        A python dictionary showing {zoneField: mean nitrates} that
        can be used to calculate the nitrates field in the tracts
        shapefile.
    """
    # Run Zonal Statistics as Table tool
    outTable = "in_memory/zonalStatistics"

    arcpy.sa.ZonalStatisticsAsTable(tracts, zoneField, idw, outTable)

    # Return output as python dict
    nitrateDict = {}
    with arcpy.da.SearchCursor("in_memory/zonalStatistics", [zoneField, "MEAN"]) as cur:
        for tract, mean in cur:
            nitrateDict[tract] = mean

    outPath = r'C:\Users\danie\Desktop\GEOG777\777-project-1\data\intermediate\table.gdb'
    arcpy.env.overwriteOutput = True
    arcpy.TableToTable_conversion("in_memory/zonalStatistics", outPath, "woooork2")

    return nitrateDict


# Update nitrates field in tracts
def update_nitrates_field(nitrateVals, tracts):
    """ Updates the nitrates field in the tracts shapefile based on
    the above idw analysis.  If the field does not exist, it will be
    created.

    inputs:
        nitrateVals (dictionary) - A python dictionary containing
                mean nitrate levels for each census tract
        tracts (shapefile) - The census tracts shapefile
    """

    # Check if tracts has the mean_nitrate field.  If it does not,
    # create it.
    fields = [field.name for field in arcpy.ListFields(tracts)]
    
    if "mean_no3" not in fields:
        print("Creating mean_no3 field")
        arcpy.AddField_management(tracts, "mean_no3", "DOUBLE")

    # Add nitrate data via update cursor
    with arcpy.da.UpdateCursor(tracts, ["GEOID10", "mean_no3"]) as cur:
        for row in cur:
            try:
                id = row[0]
                val = nitrateVals[id]

                row[1] = val
                cur.updateRow(row)
            except Exception as e:
                print(f'Error updating id {id}')


# Run OLS linear regression
def run_ols(tracts, k):
    """ Runs the Ordinary Least Squares linear regression.  The
    output report file will be saved in the output folder.

    inputs:
        tracts (shapefile) - The census tracts shapefile
        k (number) - The input k value for the idw analysis
    """

    # Create UID field if it does not exist
    fields = [field.name for field in arcpy.ListFields(tracts)]
    if "UID" not in fields:
        arcpy.AddField_management(tracts, "UID", "LONG")
        with arcpy.da.UpdateCursor(tracts, ["FID", "UID"]) as cur:
            for row in cur:
                row[1] = row[0]
                cur.updateRow(row)

    arcpy.OrdinaryLeastSquares_stats(tracts, "UID", f'data/output/OLS_{str(k).replace(".","_")}.shp', 'canrate', 'mean_no3', Output_Report_File=f"ols_reports/{k}_ols.pdf")


if __name__ == "__main__":
    wells = "data/well_nitrate.shp"
    tracts = "data/cancer_tracts.shp"
    counties = "data/cancer_county.shp"
    k = 2.5

    # print('Initialize')
    # initialize()

    # print('Run IDW')
    # idwOutput = run_idw(wells, counties, k)

    # print('Get Average Nitrate Dict')
    # nitrateDict = get_average_nitrate_dict(tracts, "GEOID10", idwOutput, k)

    # print('Upating tracts with mean nitrate values')
    # update_nitrates_field(nitrateDict, tracts)    

    run_ols(tracts, k)

    print('Done!')


    

