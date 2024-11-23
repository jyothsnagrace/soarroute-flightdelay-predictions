import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load dataset
file_path = 'data/T_ONTIME_REPORTING.csv'
flight_data = pd.read_csv(file_path)

# Select relevant columns for analysis
relevant_columns = [
    "DEP_DELAY", "ARR_DELAY", "CARRIER_DELAY", "WEATHER_DELAY", "NAS_DELAY",
    "SECURITY_DELAY", "LATE_AIRCRAFT_DELAY", "ORIGIN", "DEST", "CRS_DEP_TIME", "CRS_ARR_TIME"
]
delay_data = flight_data[relevant_columns]

# Filter rows where at least one delay reason is present
delay_reasons = ["CARRIER_DELAY", "WEATHER_DELAY", "NAS_DELAY", "SECURITY_DELAY", "LATE_AIRCRAFT_DELAY"]
delay_data = delay_data.dropna(subset=delay_reasons, how='all')

# Create a new column to label the primary delay reason
def classify_delay(row):
    for reason in delay_reasons:
        if row[reason] > 0:
            return reason.replace("_DELAY", "")
    return "NO_DELAY"

delay_data["PRIMARY_DELAY_REASON"] = delay_data.apply(classify_delay, axis=1)

# Drop columns no longer needed
delay_data = delay_data.drop(columns=delay_reasons)

# Encode categorical variables
encoder = LabelEncoder()
delay_data["ORIGIN"] = encoder.fit_transform(delay_data["ORIGIN"])
delay_data["DEST"] = encoder.fit_transform(delay_data["DEST"])
delay_data["PRIMARY_DELAY_REASON"] = encoder.fit_transform(delay_data["PRIMARY_DELAY_REASON"])

# Define features and target
X = delay_data.drop(columns=["PRIMARY_DELAY_REASON"])
y = delay_data["PRIMARY_DELAY_REASON"]

# Standardize numerical features
scaler = StandardScaler()
X[["DEP_DELAY", "ARR_DELAY", "CRS_DEP_TIME", "CRS_ARR_TIME"]] = scaler.fit_transform(
    X[["DEP_DELAY", "ARR_DELAY", "CRS_DEP_TIME", "CRS_ARR_TIME"]]
)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Decision Tree Classifier
dt_classifier = DecisionTreeClassifier(random_state=42)
dt_classifier.fit(X_train, y_train)
dt_predictions = dt_classifier.predict(X_test)

# Evaluate Decision Tree
print("Decision Tree Classifier Results:")
print(classification_report(y_test, dt_predictions))
print("Accuracy:", accuracy_score(y_test, dt_predictions))

# K-Nearest Neighbors Classifier
knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)
knn_predictions = knn_classifier.predict(X_test)

# Evaluate KNN
print("K-Nearest Neighbors Classifier Results:")
print(classification_report(y_test, knn_predictions))
print("Accuracy:", accuracy_score(y_test, knn_predictions))
