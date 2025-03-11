import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize seaborn
sns.set(style="whitegrid")

# Load the dataset
file_path = 'C:\\Users\\26378\\OneDrive\\Desktop\\level 4.1\\weather_data.csv'  # Update with your actual file path


@st.cache  # Cache the data loading for performance
def load_data(file_path):
    weather_data = pd.read_csv(file_path)

    # Clean Data
    weather_data.columns = weather_data.columns.str.strip()  # Strip whitespace
    date_column_name = 'Date_Time'  # Actual column name from your data

    # Convert 'Date_Time' to datetime
    if date_column_name in weather_data.columns:
        weather_data[date_column_name] = pd.to_datetime(weather_data[date_column_name], errors='coerce',
                                                        infer_datetime_format=True)
    else:
        st.error(f"'{date_column_name}' column is missing.")

    return weather_data


# Load the data
weather_data = load_data(file_path)


# Function to determine crop yield
def determine_crop_yield(row):
    temperature = row['Temperature_C']
    humidity = row['Humidity_pct']
    precipitation = row['Precipitation_mm']

    # Adjusted Yield Criteria
    if (20 <= temperature <= 30) and (50 <= humidity <= 75) and (8.91 <= precipitation <= 14.8):
        return 'Good'
    elif ((15 <= temperature < 20) or (30 < temperature <= 36)) and \
            ((40 <= humidity < 50) or (75 < humidity <= 85)) and \
            ((7 <= precipitation < 8.91) or (14.8 < precipitation <= 14.97158278)):
        return 'Moderate'
    else:
        return 'Poor'


# Apply Yield Determination Function
weather_data['crop_yield'] = weather_data.apply(determine_crop_yield, axis=1)

# Group by 'Location' and Count Crop Yields
yield_counts = weather_data.groupby('Location')['crop_yield'].value_counts().unstack(fill_value=0)


# Analyze Correlation between Weather Variables and Crop Yield
def analyze_correlations(data):
    # Convert crop_yield to numerical values for correlation calculation
    yield_numerical = data['crop_yield'].map({'Good': 2, 'Moderate': 1, 'Poor': 0})
    correlation_data = data[['Temperature_C', 'Humidity_pct', 'Precipitation_mm']].copy()
    correlation_data['crop_yield'] = yield_numerical

    correlation_matrix = correlation_data.corr()
    return correlation_matrix


correlation_matrix = analyze_correlations(weather_data)

# Layout - Header
st.markdown("<h1 style='color: blue; text-align: center;'>DISPLAY AREA</h1>", unsafe_allow_html=True)

# Sidebar Design
st.sidebar.header("Selection Bar")
st.sidebar.markdown("### Choose a Data View")
data_view_choice = st.sidebar.radio("",
                                    ("Select...",
                                     "Initial DataFrame",
                                     "Sorted DataFrame"))

st.sidebar.markdown("### Choose a Visualization")
visualization_choice = st.sidebar.radio("",
                                        ("Select...",
                                         "Crop Yield Counts by Location",
                                         "Correlation Matrix",
                                         "Crop Yield Boxplot by Temperature",
                                         "Crop Yield Boxplot by Humidity",
                                         "Crop Yield Boxplot by Precipitation"))

# Main app for selected data views and visualizations
with st.container():
    # Welcome message
    if data_view_choice == "Select..." and visualization_choice == "Select...":
        st.markdown("<h2>Welcome! All insights are revealed here for analysis.</h2>", unsafe_allow_html=True)

    # Data display logic
    if data_view_choice == "Initial DataFrame":
        st.subheader("Initial DataFrame:")
        st.dataframe(weather_data)

    elif data_view_choice == "Sorted DataFrame":
        if 'Location' in weather_data.columns and 'Date_Time' in weather_data.columns:
            sorted_weather_data = weather_data.sort_values(by=['Location', 'Date_Time']).reset_index(drop=True)
            st.subheader("Sorted DataFrame:")
            st.dataframe(sorted_weather_data)

    # Visualization selection logic
    if visualization_choice == "Crop Yield Counts by Location":
        st.subheader("Crop Yield Counts for Each Location:")
        st.bar_chart(yield_counts)

    elif visualization_choice == "Correlation Matrix":
        st.subheader("Correlation between Weather Variables and Crop Yield:")

        plt.figure(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
        plt.title('Correlation Matrix')
        st.pyplot(plt)

    elif visualization_choice == "Crop Yield Boxplot by Temperature":
        st.subheader("Temperature vs Crop Yield")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='crop_yield', y='Temperature_C', data=weather_data)
        plt.title('Temperature vs Crop Yield')
        plt.xlabel('Crop Yield')
        plt.ylabel('Temperature (C)')
        st.pyplot(plt)

    elif visualization_choice == "Crop Yield Boxplot by Humidity":
        st.subheader("Humidity vs Crop Yield")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='crop_yield', y='Humidity_pct', data=weather_data)
        plt.title('Humidity vs Crop Yield')
        plt.xlabel('Crop Yield')
        plt.ylabel('Humidity (%)')
        st.pyplot(plt)

    elif visualization_choice == "Crop Yield Boxplot by Precipitation":
        st.subheader("Precipitation vs Crop Yield")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='crop_yield', y='Precipitation_mm', data=weather_data)
        plt.title('Precipitation vs Crop Yield')
        plt.xlabel('Crop Yield')
        plt.ylabel('Precipitation (mm)')
        st.pyplot(plt)
