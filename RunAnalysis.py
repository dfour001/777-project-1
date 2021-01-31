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

# import arcpy
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
                If it already exists, it will be overwritten.
    """

    # Set environmental variables
    # Run IDW tool
    pass


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
    # Return output as python dict
    pass


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

    # Add nitrate data via update cursor
    pass


# Run OLS linear regression
def run_ols(tracts, k):
    """ Runs the Ordinary Least Squares linear regression.  The
    output report file will be saved in the output folder.

    inputs:
        tracts (shapefile) - The census tracts shapefile
        k (number) - The input k value for the idw analysis
    """
         

if __name__ == "__main__":
    wells = ""
    tracts = ""
    counties = ""

    

