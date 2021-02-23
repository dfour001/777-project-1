# ------------------------------------------------------------------------------
# Main.py runs the project's GUI, allows the user to set the K value, run the
# IDW and regression analysis, and view the results.
# ------------------------------------------------------------------------------

import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox
from ProgressBar import ProgressBar
from time import sleep


root = tk.Tk()
root.title("GEOG 777 - Project 1 - Daniel Fourquet")
root.resizable(False, False)
canvas = tk.Canvas(root, height=600, width=900, bg="red")
canvas.pack()

# Background Image


# Fonts
fontTitle = tkFont.Font(family="Lucida Grande", size=20)
fontParagraph = tkFont.Font(family="Lucida Grande", size=12)
fontSmall = tkFont.Font(family="Lucida Grande", size=10)


def run_analysis(k):
    """ Runs the geoprocessing tools from RunAnalysis.py, generates
        output images via ArcGIS Pro, and displays the output in the
        results frame """
    
    # Validate K entry
    try:
        k = float(k)
        if k <= 1:
            raise ValueError
    
    except ValueError:
        messagebox.showerror("K Value Error", f"K = {k}\n\nInvalid K Value!  K must be a number greater than 1.")
        return

    # Run analysis
    btnRunAnalysis["state"] = "disabled"

    # Input data paths
    wells = "data/well_nitrate.shp"
    tracts = "data/cancer_tracts.shp"
    counties = "data/cancer_county.shp"

    # Show progress bar
    prog = ProgressBar(root)
    
    root.update()
    
    # Load arcpy
    prog.set_status("Loading arcpy...")
    prog.set_prog(0)
    import RunAnalysis as ra

    prog.set_status("Preparing folder structure...")
    ra.initialize()

    prog.set_status(f"Interpolating nitrate levels from sample wells with IDW, K={k}...")
    prog.set_prog(0.25)
    idwOutput = ra.run_idw(wells, counties, k)

    prog.set_status("Summarizing results of the nitrate interpolation at the tract level...")
    prog.set_prog(0.3)
    nitrateVals = ra.get_average_nitrate_dict(tracts, "GEOID10", idwOutput, k)

    prog.set_status("Updating nitrates field in tracts...")
    prog.set_prog(0.5)
    ra.update_nitrates_field(nitrateVals, tracts)

    prog.set_status("Running ordinary least squares linear regression...")
    prog.set_prog(0.75)
    ra.run_ols(tracts, k)

    prog.set_status("Done!")
    prog.set_prog(1)
    sleep(2)
    
    prog.close()
    btnRunAnalysis["state"] = "active"






# Setup Frame
frameSetup = tk.Frame(root, bg="black", bd=5, relief=tk.RIDGE)
frameSetup.place(relheight=0.6, relwidth=0.35, relx=0.075, rely=0.05)

lblTitle = tk.Label(frameSetup,text="Nitrates and Cancer", fg="white", bg="black", justify="center", pady = 1, font=fontTitle)
lblTitle.place(x=0, y=0, relwidth=1, relheight=0.1)

lblDesc = tk.Label(frameSetup, anchor="n", text=open('projectDescription.txt').read(), fg="white", bg="black", pady = 2, justify="center", wraplength=250, font=fontParagraph)
lblDesc.place(x=0, rely=0.11, relwidth=1, relheight=0.3)

lblEnterK = tk.Label(frameSetup, text="Enter K value greater than 1 for IDW:", bg="black", fg="white", font=fontSmall)
lblEnterK.place(x=0, rely=0.61, relwidth=1)

frameKVal = tk.Frame(frameSetup, bg="black")
frameKVal.place(relx=0.2, rely=0.67, relwidth=0.6, relheight=0.1)

lblKEquals = tk.Label(frameKVal, text="K = ", bg="black", fg="white", font=fontSmall)
lblKEquals.pack(side="left")

txtKVal = tk.Entry(frameKVal)
txtKVal.insert(0, "1.2") # Set default value to 1.2
txtKVal.pack(side="left")

btnRunAnalysis = tk.Button(frameSetup, text="Run Analysis", command=lambda: run_analysis(txtKVal.get()))
btnRunAnalysis.place(rely=0.83, relwidth=0.3, relx=0.35)



# Results Frame
frameResults = tk.Frame(root, bg="white")
frameResults.place(relheight=1, relwidth=0.5, relx=0.5)


root.mainloop()