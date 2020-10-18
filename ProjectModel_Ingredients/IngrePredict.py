from tensorflow.keras.models import load_model
import numpy as np

class IngrePredict:
    def __init__(self, model_path=None, inputs=None):
        if model_path is not None:
            self.model_path = model_path
        else:
            self.model_path = None

        if inputs is not None:
            self.inputs = self._correct_inputs_dim(inputs)
            self.num_classes = self.inputs.shape[1]
        else:
            self.inputs = None
            self.num_classes = None

    def _correct_inputs_dim(self, inputs):
        # make sure inputs array is 2-dimensional:
        if inputs.ndim == 1:
            inputs = np.reshape(inputs, (1, -1))
        elif (inputs.ndim < 1) or (inputs.ndim > 2):
            raise Exception('Inputs array must be either one or two-dimensional array.')
        return inputs

    def _set_modelpath(self, model_path):
        self.model_path = model_path

    def _set_inputs(self, inputs):
        self.inputs = self._correct_inputs_dim(inputs)
        self.num_classes = self.inputs.shape[1]

    def _check_num_classes(self, model, inputs):
        if model.input.shape.as_list()[1] == inputs.shape[1]:
            return True
        else:
            return False

    def _one_hot_encode(self, predicted_class):
        row = len(predicted_class)
        one_hot_prediction = np.zeros((row, self.num_classes), dtype=np.int8)
        for i in range(len(predicted_class)):
            one_hot_prediction[i, predicted_class[i]] = 1
        return one_hot_prediction


    def _predict_inputs(self, model_path=None, inputs=None):
        if model_path is not None:
            print('I am here 1')
            self._set_modelpath(self, model_path)

        if inputs is not None:
            print('I am here 2')
            self._set_inputs(inputs)

        if self.inputs is None:
            raise Exception("Inputs array is missing for prediction.")

        if self.model_path is None:
            raise Exception("Model is missing for prediction.")

        model = load_model(self.model_path)
        if not (self._check_num_classes(model, self.inputs)):
            raise Exception("Total classes of inputs array does not tally with model input dimension.")

        predict_probability = model.predict(self.inputs)
        predict_class = np.argmax(predict_probability, axis=1)
        return self._one_hot_encode(predict_class)


if __name__ == "__main__":
    import pandas as pd
    import time

    # specify path to model
    MODEL_PATH = r"C:\Users\KC Cheng\Documents\ISS-PRSPM-Grp-18\ISS-PRSPM-GRP-18\ISS-PRSPM-GRP-18\ProjectModel_Ingredients\codefull.hdf5"

    # getting a test row from recipes_input.csv
    FTR_PATH = r"C:\Users\KC Cheng\Documents\ISS-PRSPM-Grp-18\ISS-PRSPM-GRP-18\ISS-PRSPM-GRP-18\Recipe_Requests\recipes_input.csv"
    ftr_df = pd.read_csv(FTR_PATH, skipinitialspace=True)
    ftr_df.drop(columns=['Unnamed: 0'], inplace=True)
    test_row = np.asarray(ftr_df.iloc[0:1000])
    print("Consisting of {} data rows and {} classes".format(test_row.shape[0], test_row.shape[1]))

    # initialize predictor instance, and apply the predict_inputs method to get the one-hot-encoded predictions
    # for multiple inputs
    t0 = time.perf_counter()
    print("Starting prediction....")
    predictor = IngrePredict(model_path=MODEL_PATH, inputs=test_row)
    predicted_class = predictor._predict_inputs()
    t1 = time.perf_counter() - t0
    print("Prediction completed.")
    print("Took {} to predict {} instances.".format(t1, test_row.shape[0]))
    print("One-hot-encoded output:")
    print(predicted_class)
    print("Output shape: ", predicted_class.shape)










