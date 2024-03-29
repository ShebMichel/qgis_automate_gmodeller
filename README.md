# qgis_automate_gmodeller
This processing plugin assess the environmental impact of linear projects (pipeline, roads, railway, etc.) on living species such as Raptor, Bald Eagle (BAEA), Heron Roockeries (GBH) Nests and Burrowing Owl (BUOWL) habitats.
# How to install this plugin?
# 1. Quick install
   
## 1.1. Windows (using zip file)

For installion execute the below steps:
- run the command:
  ```bash
  git clone https://github.com/ShebMichel/qgis_automate_gmodeller.git
  ```
  Then zip the qgis_automate_gmodeller folder.
- Go in the Settings tab of the QGIS Plugins Manager window (see official documentation)
- Choose install zip, then after successfull message
- Go to Plugins -> Manage and Install Plugins -> All
- Search for “your_plugin name” check its associated box
  
## 1.2. Windows (other method)
  will be upgraded soon'''


# 2. Environment Installation
## 2.1. Required
This plugin will requires the below dependencies: 
- QGIS version: 3.28.4-Firenze
- Qt version  : 5.15.3
- Python 3.9.5

# 3. Running the plugin using local data
A usage example of running the graph modeller is shown below:
<p align="center">
<img src="https://github.com/ShebMichel/qgis-animated_gif/blob/main/impact_asssessment_via_local_data.gif">
</p>
In this example, it is a straight forward exercise, where the user will deal with data locally and conduct a routine assessment.

# 4. Running the plugin using db data
A usage example of running the graph modeller is shown below:
<p align="center">
<img src="https://github.com/ShebMichel/qgis-animated_gif/blob/main/impact_asssessment_via_db_data.gif">
</p>
## The data are exported from a local directory to a database, 
## The db data are published into QGIS for further calculations.
Unlike using the local data, here, the user have the possiblity to export data as shown in the below example, 
but also to import data directly (this feature is not released, can be done on demand).

# 5. Feature releases:
  - Run Interpreter:  This is an extra feature in which the user can plot the general trend of the impact assessment (on demand).
  - Run GModeller  : While the data are imported from db, the next process is available on demand (for now).
# 6. Remarks:
- This demo is very useful for monitoring projects. Here we present the impact assessment of linear features, such as roads and railways on a few birds habitats.
- It is a project which has the potential to be adapted in different ecosystem. Feel free to touch base or contact me for a chat. 
