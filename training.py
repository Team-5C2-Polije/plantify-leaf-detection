import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load data dari file Excel
data = pd.read_excel("extractions\extr_ftr_new_dataset_train.xlsx")

X = data.drop(columns=["Label"])
y = data["Label"]

# Split data menjadi training dan testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Inisialisasi dan latih model Decision Tree
model = DecisionTreeClassifier(max_depth=10, criterion='entropy', random_state=42)
model.fit(X_train, y_train)
print("Model Decision Tree berhasil dilatih!")

# Evaluasi model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Akurasi model: {accuracy:.2f}")
print("\nLaporan Klasifikasi:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Cross-validation
scores = cross_val_score(model, X, y, cv=5)
print(f"Cross-validated accuracy: {scores.mean():.2f}")

# Simpan model ke 
model_file = r"models\test\decision_data_new_dataset.pkl"
joblib.dump(model, model_file)
print(f"Model disimpan ke {model_file}")
