from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib

X = np.array([
    [5,0],
    [12,1],
    [20,1],
    [4,0],
    [18,1]
])

y = [0,1,1,0,1]

model = RandomForestClassifier()

model.fit(X,y)

joblib.dump(model,"password_ai_model.pkl")

print("AI Model Trained")