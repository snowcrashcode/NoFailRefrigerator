import joblib
import pandas as pd
import json
import io
from sagemaker_inference import content_types, decoder, default_inference_handler, encoder

class IsolationForestInferenceHandler(default_inference_handler.DefaultInferenceHandler):

    def default_model_fn(self, model_dir):
        # Load the model from the model_dir
        model = joblib.load(f"{model_dir}/isolation_forest_model.joblib")
        return model

    def default_input_fn(self, input_data, content_type):
        if content_type == content_types.CSV:
            # Read CSV input data
            return pd.read_csv(io.StringIO(input_data))
        else:
            raise ValueError(f"Unsupported content type: {content_type}")

    def default_predict_fn(self, data, model):
        # Make predictions using the model
        return model.predict(data)

    def default_output_fn(self, prediction, accept):
        if accept == content_types.CSV:
            # Convert prediction to CSV format
            out = io.StringIO()
            pd.DataFrame(prediction).to_csv(out, header=False, index=False)
            return out.getvalue(), content_types.CSV
        elif accept == content_types.JSON:
            # Convert prediction to JSON format
            return json.dumps(prediction.tolist()), content_types.JSON
        else:
            raise ValueError(f"Unsupported accept type: {accept}")

