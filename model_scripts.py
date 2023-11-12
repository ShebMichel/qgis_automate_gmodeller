"""
Model exported as python.
Name : impact_Assessment
Group : Qgis course
With QGIS : 32804
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsExpression
import processing


class Impact_assessment(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer('baea_nests', 'BAEA Nests', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('buowl_habitats', 'BUOWL Habitats', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('gbh_rookeries', 'GBH Rookeries', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('linear_projects', 'Linear Projects', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('raptor_nests', 'Raptor Nests', types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Impact_pcnt', 'Impact_Pcnt', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=''))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(11, model_feedback)
        results = {}
        outputs = {}

        # BAEA Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 804,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['baea_nests'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 10,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BaeaBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Linear Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': QgsExpression(" 'row_width' ").evaluate(),
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['linear_projects'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 10,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LinearBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # LB Area
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'area_ha',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': ' $area  / 10000',
            'INPUT': outputs['LinearBuffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['LbArea'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # BUOWL Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 300,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['buowl_habitats'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 10,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BuowlBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # BAEA Difference
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['LbArea']['OUTPUT'],
            'OVERLAY': outputs['BaeaBuffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BaeaDifference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # BUOWL Difference
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['BaeaDifference']['OUTPUT'],
            'OVERLAY': outputs['BuowlBuffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BuowlDifference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Raptor Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 402,
            'END_CAP_STYLE': 0,  # Round
            'INPUT': parameters['raptor_nests'],
            'JOIN_STYLE': 0,  # Round
            'MITER_LIMIT': 2,
            'SEGMENTS': 10,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RaptorBuffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Raptor Difference
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['BuowlDifference']['OUTPUT'],
            'OVERLAY': outputs['RaptorBuffer']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RaptorDifference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # GBH Difference
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['RaptorDifference']['OUTPUT'],
            'OVERLAY': parameters['gbh_rookeries'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['GbhDifference'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Impact calculator
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'impact_ha',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'area_ha-($area/10000)  ',
            'INPUT': outputs['GbhDifference']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ImpactCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Impact Percent
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'impact_pct',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'impact_ha/area_ha * 100  ',
            'INPUT': outputs['ImpactCalculator']['OUTPUT'],
            'OUTPUT': parameters['Impact_pcnt']
        }
        outputs['ImpactPercent'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Impact_pcnt'] = outputs['ImpactPercent']['OUTPUT']
        return results

    def name(self):
        return 'impact_Assessment'

    def displayName(self):
        return 'impact_Assessment'

    def group(self):
        return 'Qgis course'

    def groupId(self):
        return 'Qgis course'

    def createInstance(self):
        return Impact_assessment()
