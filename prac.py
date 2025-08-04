# 📚 Importing libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# 🔹 Load dataset
from sklearn.datasets import load_iris
iris = load_iris()

# Convert to DataFrame
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target
df['target_name'] = df['target'].apply(lambda x: iris.target_names[x])

print(df.head())

# 📊 EDA
print("\n🧼 Data Info:")
print(df.info())

print("\n📈 Class Distribution:")
print(df['target_name'].value_counts())

# Pairplot
sns.pairplot(df, hue='target_name')
plt.suptitle("Pairplot of Iris Features", y=1.02)
plt.show()

# Heatmap of correlations
plt.figure(figsize=(8, 6))
sns.heatmap(df.drop(columns='target_name').corr(), annot=True, cmap='coolwarm')
plt.title("Feature Correlation Heatmap")
plt.show()

# 📌 Feature matrix and target
X = df.drop(columns=['target', 'target_name'])
y = df['target']

# 🧪 Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🤖 Model Training
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 🎯 Predictions
y_pred = model.predict(X_test)

# 📊 Evaluation
print("\n✅ Accuracy Score:", accuracy_score(y_test, y_pred))
print("\n📋 Classification Report:\n", classification_report(y_test, y_pred))

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=iris.target_names, yticklabels=iris.target_names)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# 📌 Feature Importances
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.sort_values().plot(kind='barh', title='Feature Importances')
plt.show()