# import modules
import os


#
def run_progress_bar(self, current_idx, idx_list):
    """
    This function run the progressbar while importing/exporting data
    current_idx: the index of the file to export/import
    idx_list   : list of indexes
    """
    self.gm_progressBar.setGeometry(20, 240, 161, 16)
    bar_max = self.gm_progressBar.maximum()
    self.current_value = int(bar_max * (current_idx / len(idx_list)))
    #
    self.gm_progressBar.setValue(self.current_value)
    if len(idx_list) != len(idx_list) + 1:
        self.gm_progressBar.setValue(bar_max)
        pass
    return


def fill_in_modelcheckbox(self, call_func):
    """
    This function fill in the combobox once the QcheckBox is selected to True
    call_func:  the function that move model to your directory
    """
    self.mcomboBox.clear()
    self.mcomboBox.addItems(self.modelsaved)
    self.modelcheckBox.stateChanged.connect(call_func)
    return


def find_model_in_plugin_dir(self, datapath, extension):
    """
    This function return the .model3
    # datapath :  the model source path
    # extension:  model extension to search for
    """
    # extension = ".model3"
    self.modelsaved = [
        each for each in os.listdir(datapath) if each.endswith(str(extension))
    ]
    return self.modelsaved


# def import_export(self):
#     """
#     This function enabled the export and import feature
#     """
#     try:
#         self.Export_pushButton.setEnabled(False)
#         self.Import_pushButton.setEnabled(False)
#     except:
#         print("Not reading radio button")

#     return


# def user_connection_parameters(self):
#     """
#     This function enabled the server connection parameters
#     """
#     try:
#         for i in range(5):
#             self.user_label_ + str(i).setEnabled(False)
#             self.server_param_ + str(i).setReadonly(True)
#     except:
#         print("Not reading server connection parameter")
#     return

# from qgis.PyQt import uic
# from qgis.PyQt import QtWidgets
# from processing.modeler.ModelerDialog import ModelerDialog
# from qgis.core import (
#     QgsVectorLayer,
#     QgsRasterLayer,
#     QgsDataSourceUri,
#     QgsProject,
#     QgsProviderRegistry,
# )
# from PyQt5.QtWidgets import QFileDialog, QMessageBox
