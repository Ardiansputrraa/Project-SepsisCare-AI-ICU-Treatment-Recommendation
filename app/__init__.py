from flask import Flask, current_app
from config import Config
from pymongo import MongoClient



def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # MONGODB
    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client[app.config['DBNAME']]
    
    from .routes.auth import auth_
    app.register_blueprint(auth_)
    
    from .routes.profile import profile_
    app.register_blueprint(profile_)
    
    from .routes.bed_selection import dashboard_
    app.register_blueprint(dashboard_)
    
    from .routes.summary import summary_
    app.register_blueprint(summary_)
    
    from .routes.sofa import sofa_
    app.register_blueprint(sofa_)
    
    from .routes.similarity import similarity_
    app.register_blueprint(similarity_)
    
    from .routes.forecasting import forecasting_
    app.register_blueprint(forecasting_)
    
    from .routes.treatment_history import treatment_history_
    app.register_blueprint(treatment_history_)
    
    from .routes.vital_patient import vital_patient_
    app.register_blueprint(vital_patient_)
    
    from .routes.recommendation import recommendation_
    app.register_blueprint(recommendation_)
    
    from .routes.treatment_recommendation import treatment_recommendation_
    app.register_blueprint(treatment_recommendation_)
    
    from .routes.predict import predict_
    app.register_blueprint(predict_)
    
    return app