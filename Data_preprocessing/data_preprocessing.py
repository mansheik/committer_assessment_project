
class Preprocessing:

    def __init__(self,file_object,logger_object):
        self.logger_object = logger_object
        self.file_object = file_object

    def droping_unnecessary_cols(self,data):
        try:

            self.data = data.drop(columns=['Dev_ID','Geographic_Regions','Gender','Age','Project_Age','Dev_Status','Education','Expt_Het'],axis=1)

            self.logger_object.log(self.file_object,
                               'column(s) has been removed')
            return self.data
        except Exception as e:


            self.logger_object.log(self.file_object,
                               'Error in droping_unnecessary_cols :  ' + str(
                                   e))

    