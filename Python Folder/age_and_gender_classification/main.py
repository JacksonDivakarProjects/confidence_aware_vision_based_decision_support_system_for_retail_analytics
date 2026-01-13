from python_file.age_classifier import AgeClassifier
from python_file.gender_classifier import GenderClassifier
from services.video_processor import VideoProcessor

import os





def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    age_model_path = os.path.join(
        BASE_DIR, "trained_models", "age_detection_model_.h5"
    )

    gender_model_path = os.path.join(
        BASE_DIR, "trained_models", "gender_classification_model.pth"
    )

    age_clf = AgeClassifier()
    age_clf.load_model(age_model_path)

    gender_clf = GenderClassifier()
    gender_clf.load_model(gender_model_path)

    app = VideoProcessor(age_clf, gender_clf)
    app.run()

if __name__ == "__main__":
    main()
