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

def update_dataset_source(layer, k):
    newProps = layer.connectionProperties
    newSource = f'{str(k).replace(".","_")}.tif'
    newProps['dataset'] = newSource
    layer.updateConnectionProperties(layer.connectionProperties, newProps)

def generate_reports(k):
    projectPath = r'project/Project.aprx'

    aprx = arcpy.mp.ArcGISProject(projectPath)

    # Update IDW raster in map
    IDWMap = aprx.listMaps('IDWMap')[0]
    IDWLayer = IDWMap.listLayers('Well Nitrate Levels (IDW)')[0]
    update_dataset_source(IDWLayer, k)

    # Update K label in layout
    IDWLayout = aprx.listLayouts('IDW*')[0]
    lblK = IDWLayout.listElements('TEXT_ELEMENT', 'lblK')[0]
    lblK.text = f'K = {k}'
    # Export IDW report
    IDWLayout.exportToJPEG(r'reports/IDW_{}.jpg'.format(str(k).replace(".","_")), 150)

    # Update OLS in map
    OLSMap = aprx.listMaps('OLSMap')[0]
    OLSLayer = OLSMap.listLayers('OLS')[0]
    update_dataset_source(OLSLayer, k)
    
    # Export OLS report
    OLSLayout = aprx.listLayouts('OLS*')[0]
    OLSLayout.exportToJPEG(r'reports/OLS_{}.jpg'.format(str(k).replace(".","_")), 150)
    
    aprx.save()

