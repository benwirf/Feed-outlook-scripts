
from qgis.PyQt.QtCore import QCoreApplication, QVariant, Qt
from qgis.core import (QgsProcessing, QgsProcessingAlgorithm, QgsProcessingParameterString,
                    QgsProcessingParameterVectorLayer, QgsProcessingParameterEnum,
                    QgsProcessingParameterBoolean, QgsProcessingParameterFileDestination,
                    QgsProcessingParameterFolderDestination, QgsProcessingParameterFile)
import datetime


                  
class ExAlgo(QgsProcessingAlgorithm):
    INDIR = 'INDIR'
    DISTRICTS = 'DISTRICTS'
 
    def __init__(self):
        super().__init__()
 
    def name(self):
        return "exalgo"
     
    def tr(self, text):
        return QCoreApplication.translate("exalgo", text)
         
    def displayName(self):
        return self.tr("Example script")
 
    def group(self):
        return self.tr("Examples")
 
    def groupId(self):
        return "examples"
 
    def shortHelpString(self):
        return self.tr("Example script with a custom widget")
 
    def helpUrl(self):
        return "https://qgis.org"
         
    def createInstance(self):
        return type(self)()
   
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFile(
            self.INDIR,
            'Monthly Growth Source Directory',
            behavior=QgsProcessingParameterFile.Folder))
        
        self.addParameter(QgsProcessingParameterVectorLayer(self.DISTRICTS, 'Pastoral districts', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        ###
        cdt = datetime.datetime.now()
        current_yr = cdt.year
        current_mnth = cdt.month
        if current_mnth>6:
            financial_year = f'{current_yr}-{current_yr+1} FY'
        elif current_month<=6:
            financial_year = f'{current_yr-1}-{current_yr} FY'
        financial_yrs = [financial_year,
                        f'{str(int(financial_year.split("-")[0])-1)}-{str(int(financial_year.split("-")[1][:4])-1)} FY',
                        f'{str(int(financial_year.split("-")[0])-2)}-{str(int(financial_year.split("-")[1][:4])-2)} FY',
                        f'{str(int(financial_year.split("-")[0])-3)}-{str(int(financial_year.split("-")[1][:4])-3)} FY',
                        f'{str(int(financial_year.split("-")[0])-4)}-{str(int(financial_year.split("-")[1][:4])-4)} FY']
        self.addParameter(QgsProcessingParameterEnum('FY', 'Financial Year', financial_yrs, defaultValue=financial_yrs[0]))
        ###
        self.addParameter(QgsProcessingParameterBoolean('SMOOTH', 'Interpolate monthly growth values for smooth graph lines\
 (requires scipy module)'))
        
        self.addParameter(QgsProcessingParameterFileDestination('OUTPUT_XL', 'Output District Spreadsheet', 'Microsoft Excel (*.xlsx);;Open Document Spreadsheet (*.ods)'))
        
        self.addParameter(QgsProcessingParameterFolderDestination('OUTPUT_GRAPHS', 'Output District Graphs'))
 
    def processAlgorithm(self, parameters, context, feedback):
        growth_folder_path = self.parameterAsString(parameters, self.INDIR, context)
        
        return {self.INDIR: growth_folder_path}


        