import pickle
from application_logging import App_Logger
from Data_preprocessing.data_preprocessing import Preprocessing
from File_operation import file_op
import numpy as np
import pandas as pd
import Data
from sklearn.preprocessing import StandardScaler
PredictorScaler=StandardScaler()

class Prediction_from_file:
    def __init__(self, file_path):
        self.file_object = open("Prediction_logs/prediction_logs.txt", 'a+')
        self.log_writer = App_Logger()
        self.file = file_path

    def prediction_file_api(self):
        self.log_writer.log(self.file_object, 'Start of Prediction of api....')
        InputData = pd.read_csv(self.file)
        preprocessor = Preprocessing(self.file_object, self.log_writer)
        InputData = preprocessor.droping_unnecessary_cols(InputData)
        Num_Inputs = InputData.shape[0]
        preprocessor = Preprocessing(self.file_object, self.log_writer)
        DataForMl = pd.read_csv('Data/train.csv')
        DataForMl=preprocessor.droping_unnecessary_cols(DataForMl)

        DataForMl = DataForMl.drop(columns='Promoted', axis=1)

        InputData = InputData.append(DataForMl)

        # print(DataForMl)
        # print(InputData)


        self.log_writer.log(self.file_object, f'datafor ML: {InputData.head()}')

        predictors = ['Int_Learn', 'Fin_Gain', 'Tech_Cont_Norm', 'Sys_Int', 'Cod_Test_Task', 'Cont_Code_Dec', 'Dec_Right_Dec', 'Dev_Inv', 'Proj_Desertion', 'Dev_Experience']
        # Generating the input values to the model


        X = InputData[predictors].values[0:Num_Inputs]


        X=InputData[predictors].values
        
        # Storing the fit object for later reference
        PredictorScalerFit=PredictorScaler.fit(X)

        X=PredictorScalerFit.transform(X)
        
        file_loader = file_op.File_operation(self.file_object)
        xgboost = file_loader.load_model('FinalXGBModel')

        predictions = xgboost.predict(X)


        self.log_writer.log(self.file_object, f'Input data for model: {X}')

        return predictions[:Num_Inputs]

