import pickle
from application_logging import App_Logger
from Data_preprocessing.data_preprocessing import Preprocessing
from File_operation import file_op
import numpy as np
import pandas as pd
import Data
from sklearn.preprocessing import StandardScaler
PredictorScaler=StandardScaler()

class Prediction_from_api:
    def __init__(self, int_learn, fin_gain, tech_cont_norm, sys_int, code_test_task, cont_code_dec, dec_right_del, dev_inv, proj_desertion, dev_experience):
        self.file_object = open("Prediction_logs/prediction_logs.txt", 'a+')
        self.log_writer = App_Logger()
        self.int_learn = int_learn
        self.fin_gain = fin_gain
        self.tech_cont_norm = tech_cont_norm
        self.sys_int = sys_int
        self.code_test_task = code_test_task
        self.cont_code_dec = cont_code_dec
        self.dec_right_del = dec_right_del
        self.dev_inv = dev_inv
        self.proj_desertion = proj_desertion
        self.dev_experience = dev_experience

    def prediction_api(self):
        self.log_writer.log(self.file_object, 'Start of Prediction of api....')
        InputData = pd.DataFrame(
            data=[[self.int_learn, self.fin_gain, self.tech_cont_norm, self.sys_int, self.code_test_task, self.cont_code_dec, self.dec_right_del, self.dev_inv, self.proj_desertion, self.dev_experience]],
            columns=['Int_Learn', 'Fin_Gain','Tech_Cont_Norm','Sys_Int','Cod_Test_Task', 'Cont_Code_Dec', 'Dec_Right_Del', 'Dev_Inv', 'Proj_Desertion', 'Dev_Experience'])
        Num_Inputs = InputData.shape[0]
        preprocessor = Preprocessing(self.file_object, self.log_writer)
        DataForMl = pd.read_csv('Data/train.csv')
        DataForMl=preprocessor.droping_unnecessary_cols(DataForMl)

        DataForMl = DataForMl.drop(columns='Promoted', axis=1)

        InputData = InputData.append(DataForMl)

        print(DataForMl)
        print(InputData)


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
        prediction = predictions[0]

        self.log_writer.log(self.file_object, f'Input data for model: {X}')


        # with open('Models/FinalXGBModel/FinalXGBModel.pkl', 'rb') as fileReadStream:
        #     XGB_model=pickle.load(fileReadStream)
        #     # Don't forget to close the filestream!
        #     fileReadStream.close()
            
        # # Genrating Predictions
        # Prediction=XGB_model.predict(X)
        # PredictedStatus=pd.DataFrame(Prediction, columns=['Predicted Status'])
        # print(PredictedStatus)
        # print(Prediction)
        
        # if prediction==1:
        #     return 'congratulations !! You are Promoted .'
        # else:
        #     return 'Sorry !! You are Not Promoted .'
        return prediction
