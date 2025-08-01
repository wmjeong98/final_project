import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

from sklearn.model_selection import train_test_split

def load_data():
    california = fetch_california_housing()
    X = pd.DataFrame(california.data, columns=california.feature_names)
    y = pd.Series(california.target, name='target')
    return X, y
    
import tarfile
import urllib.request

# 파일 다운로드
url = "https://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.tgz"
file_path = "cal_housing.tgz"
urllib.request.urlretrieve(url, file_path)

# tar 파일 해제
with tarfile.open(file_path) as tar:
    tar.extractall()

@st.cache_resource
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return model, mse

def main():
    # 세션 초기화
    if 'page_refresh_count' not in st.session_state:
        st.session_state.page_refresh_count = 0
    if 'predict_attempt_count' not in st.session_state:
        st.session_state.predict_attempt_count = 0
    
    st.session_state.page_refresh_count += 1

    st.title("California Housing Price")
    

    X, y = load_data()

    model, mse = train_model(X, y)
    st.write(f"Train MSE: {mse:.2f}")

    st.header("Input Features")
    MedInc = st.number_input("MedInc", float(X['MedInc'].min()), float(X['MedInc'].max()), float(X['MedInc'].mean()))
    HouseAge = st.number_input("HouseAge", float(X['HouseAge'].min()), float(X['HouseAge'].max()), float(X['HouseAge'].mean()))
    AveRooms = st.number_input("AveRooms", float(X['AveRooms'].min()), float(X['AveRooms'].max()), float(X['AveRooms'].mean()))
    AveBedrms = st.number_input("AveBedrms", float(X['AveBedrms'].min()), float(X['AveBedrms'].max()), float(X['AveBedrms'].mean()))
    Population = st.number_input("Population", float(X['Population'].min()), float(X['Population'].max()), float(X['Population'].mean()))
    AveOccup = st.number_input("AveOccup", float(X['AveOccup'].min()), float(X['AveOccup'].max()), float(X['AveOccup'].mean()))
    Latitude = st.number_input("Latitude", float(X['Latitude'].min()), float(X['Latitude'].max()), float(X['Latitude'].mean()))
    Longitude = st.number_input("Longitude", float(X['Longitude'].min()), float(X['Longitude'].max()), float(X['Longitude'].mean()))

    input_data = pd.DataFrame({
        'MedInc': [MedInc],
        'HouseAge': [HouseAge],
        'AveRooms': [AveRooms],
        'AveBedrms': [AveBedrms],
        'Population': [Population],
        'AveOccup': [AveOccup],
        'Latitude': [Latitude],
        'Longitude': [Longitude]
    })

    st.write("Input Features")
    st.write(input_data)

    if st.button("Predict"):
        st.session_state.predict_attempt_count += 1
        prediction = model.predict(input_data)
        st.write(f"Predicted House Price: ${prediction[0]*100000:.2f}")
        st.write(f"Predict Attempt Count: {st.session_state.predict_attempt_count}")
    
    st.write(f"Page Refresh Count: {st.session_state.page_refresh_count}")

if __name__ == "__main__":
    main()