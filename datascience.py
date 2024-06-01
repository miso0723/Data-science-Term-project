# -*- coding: utf-8 -*-
"""databaseTerm.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1v-LjEaX5ejcnEQRuF8e_SIRnxx4jWYqf
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'drug_deaths.csv'
df = pd.read_csv(file_path)
# Dropping columns not listed in the provided features list
features_to_keep = [
    'Date', 'Age', 'Sex', 'Race', 'ResidenceCity', 'DeathCity',
    'Heroin', 'Cocaine', 'Fentanyl', 'Fentanyl_Analogue', 'Oxycodone',
    'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone',
    'Amphet', 'Tramad', 'Morphine_NotHeroin'
]

# 사용할 열만 선택
df = df[features_to_keep]
df.info()
# Date, Age, Deathcity 같은 경우에는 없을 때 다른 정보도 없는 경우가 너무 많으므로 모두 drop
df.dropna(subset=['Date', 'Age', 'DeathCity'], inplace=True)

# 'Date' 열을 datetime 형식으로 변환
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# 'Date' 열을 연도와 월까지만 표시되도록 변환
df['Date'] = df['Date'].dt.to_period('Y')

# 'Age' 열을 정수형으로 반올림
df['Age'] = df['Age'].round().astype(int)

# 연령을 범주형으로 변환
# age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
# age_labels = ['Child', 'Young Adult', 'Adult', 'Middle Adult', 'Older Adult', 'Senior', 'Elder']
# df['Age'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

# 'Sex' 열의 null 값을 'Unknown'값으로 바꾼 후 'Unknown' 값을 최빈값으로 대체
df.loc[:,'Sex'].fillna('Unknown', inplace=True)
sex_mode = df['Sex'][df['Sex'] != 'Unknown'].mode()[0]
df['Sex'] = df['Sex'].replace('Unknown', sex_mode)

# 'Race' 열의 null 값들을 'Unknown'값으로 바꾼 후 'Unknown' 값을 최빈값으로 대체
# 인종은 'Black', 'White', 'Asian', 'Other' 이렇게 4가지로만 구분한다
df.loc[:,'Race'].fillna('Unknown', inplace=True)
race_replacements = {
    'Hispanic, White': 'White',
    'Hispanic, Black': 'Black',
    'Asian, Other': 'Asian',
    'Asian Indian': 'Asian',
    'Chinese': 'Asian',
    'Native American, Other': 'Other',
    'Hawaiian': 'Other'
}
df['Race'] = df['Race'].replace(race_replacements)
race_mode = df['Race'][df['Race'] != 'Unknown'].mode()[0]
df['Race'] = df['Race'].replace('Unknown', race_mode)

# 거주지는 알려지지 않을 수도 있기 때문에 빈칸의 경우 'Unknown'으로 판단한다
df.loc[:,'ResidenceCity'].fillna('Unknown', inplace=True)
# 'Fentanyl' 열의 특수한 값을 1로 변환
df['Fentanyl'] = df['Fentanyl'].replace(['1-A', '1 POPS', '1 (PTCH)'], 1).astype(int)

# Change dtype of 'Fentanyl_Analogue' to int64
df['Fentanyl_Analogue'] = df['Fentanyl_Analogue'].astype('int64')

# Morphine_NotHeroin 열의 특후나 값을 1로 변환
df['Morphine_NotHeroin'] = df['Morphine_NotHeroin'].replace(['1ES','STOLE MEDS','NO RX BUT STRAWS','PCP NEG'],1).astype(int)

# Drop rows where all specified columns have a value of 0
columns_to_check = ['Heroin', 'Cocaine', 'Fentanyl', 'Fentanyl_Analogue', 'Oxycodone',
                    'Oxymorphone', 'Ethanol', 'Hydrocodone', 'Benzodiazepine', 'Methadone',
                    'Amphet', 'Tramad', 'Morphine_NotHeroin']

filtered_data = df[(df[columns_to_check] != 0).any(axis=1)]
filtered_data.to_csv("null_drug_deaths.csv", index=False)
# null control 이후 EDA 및 multi-drug 추가하기
file_path = 'null_drug_deaths.csv'
data = pd.read_csv(file_path)
data.info()
# file_path = 'null_drug_deaths.csv'
# drug_deaths_df = pd.read_csv(file_path)

# Summary statistics
summary_stats = data.describe()

# Distribution plots for age
plt.figure(figsize=(10, 6))
plt.hist(data['Age'].dropna(), bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

# Count plot for Sex
plt.figure(figsize=(10, 6))
data['Sex'].value_counts().plot(kind='bar', color=['blue', 'orange'])
plt.title('Count of Deaths by Sex')
plt.xlabel('Sex')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

# Count plot for Race
plt.figure(figsize=(10, 6))
data['Race'].value_counts().plot(kind='bar', color=['green', 'red', 'blue', 'purple', 'orange'])
plt.title('Count of Deaths by Race')
plt.xlabel('Race')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Plotting presence of different drugs
drug_columns = ['Heroin', 'Cocaine', 'Fentanyl', 'Fentanyl_Analogue', 'Oxycodone', 'Oxymorphone', 'Ethanol',
                'Hydrocodone', 'Benzodiazepine', 'Methadone', 'Amphet', 'Tramad', 'Morphine_NotHeroin']

drug_presence = data[drug_columns].sum()

plt.figure(figsize=(14, 8))
drug_presence.plot(kind='bar', color='skyblue')
plt.title('Presence of Different Drugs in Death Cases')
plt.xlabel('Drug')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Count plots for ResidenceCity and DeathCity

# ResidenceCity analysis
residence_city_counts = data['ResidenceCity'].value_counts().head(10)  # Top 10 cities
plt.figure(figsize=(14, 8))
residence_city_counts.plot(kind='bar', color='coral')
plt.title('Top 20 Residence Cities for Drug-Related Deaths')
plt.xlabel('Residence City')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# DeathCity analysis
death_city_counts = data['DeathCity'].value_counts().head(10)  # Top 10 cities

plt.figure(figsize=(14, 8))
death_city_counts.plot(kind='bar', color='lightblue')
plt.title('Top 20 Death Cities for Drug-Related Deaths')
plt.xlabel('Death City')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()

# Show the value counts for all cities in a table
residence_city_counts_all = data['ResidenceCity'].value_counts()
death_city_counts_all = data['DeathCity'].value_counts()

residence_city_counts_all = residence_city_counts_all.reset_index().rename(columns={'index': 'ResidenceCity', 'ResidenceCity': 'Count'})
death_city_counts_all = death_city_counts_all.reset_index().rename(columns={'index': 'DeathCity', 'DeathCity': 'Count'})
# Plot trends for specific drugs
yearly_drug_trends = data.groupby('Date')[drug_columns].sum()
yearly_drug_trends.plot(title='Yearly Trends for Specific Drugs', colormap='tab20')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()
# 지역이 너무 많아 top 5 지역만을 선택

residence_top_5 = ['HARTFORD', 'WATERBURY', 'BRIDGEPORT', 'NEW HAVEN', 'NEW BRITAIN']
death_top_5 = ['HARTFORD', 'NEW HAVEN', 'WATERBURY', 'BRIDGEPORT', 'NEW BRITAIN']
# file_path = 'null_drug_deaths.csv'
# drug_deaths_df = pd.read_csv(file_path)

filtered_df = data[(data['ResidenceCity'].isin(residence_top_5))]
new_filtered_df = filtered_df[(filtered_df['DeathCity'].isin(death_top_5))]
new_filtered_df.to_csv("filtered_drug_deaths.csv", index=False)
# 다중 약물 복용 행 추가 (True, False)
file_path = 'filtered_drug_deaths.csv'
data = pd.read_csv(file_path)

# Create the 'Multi-Drug' column based on the given conditions
data['Multi-Drug'] = data[drug_columns].sum(axis=1).apply(lambda x: True if x > 1 else False)

data.to_csv("multi_drug_deaths.csv", index=False)
file_path = 'multi_drug_deaths.csv'
data = pd.read_csv(file_path)

# 성별에 따른 다중 약물 복용 여부 그래프 생성
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Sex', hue='Multi-Drug')
plt.title('Count of Multi-Drug Usage by Sex')
plt.xlabel('Sex')
plt.ylabel('Count')
plt.show()

# 인종별 다중 약물 복용 여부 그래프 생성
plt.figure(figsize=(12, 6))
sns.countplot(data=data, x='Race', hue='Multi-Drug')
plt.title('Count of Multi-Drug Usage by Race')
plt.xlabel('Race')
plt.ylabel('Count')
plt.show()

# 연도별 다중 약물 복용 여부 그래프 생성
data['Year'] = data['Date']
plt.figure(figsize=(12, 6))
sns.countplot(data=data, x='Year', hue='Multi-Drug')
plt.title('Count of Multi-Drug Usage by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.show()
from sklearn.preprocessing import OneHotEncoder

# 데이터 로드
df = pd.read_csv('multi_drug_deaths.csv')

# 인코딩할 열 정의
columns_to_encode = ['Date', 'Sex', 'Race', 'ResidenceCity', 'DeathCity']

# 각 열의 카테고리 정의
categories = {
    'Date': [2012, 2013, 2014, 2015, 2016, 2017, 2018],
    'Sex': ['Male', 'Female'],
    'Race': ['Asian', 'Black', 'White', 'Other'],
    'ResidenceCity': ['HARTFORD', 'WATERBURY', 'BRIDGEPORT', 'NEW HAVEN', 'NEW BRITAIN'],
    'DeathCity': ['HARTFORD', 'NEW HAVEN', 'WATERBURY', 'BRIDGEPORT', 'NEW BRITAIN']
}

# OneHotEncoder 초기화 및 인코딩 수행
encoder = OneHotEncoder(categories=[categories[col] for col in columns_to_encode], drop='first', sparse_output=False)
encoded_data = encoder.fit_transform(df[columns_to_encode])

# 인코딩된 데이터를 데이터프레임으로 변환
encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns_to_encode))

# 원본 데이터프레임에서 인코딩된 열 제거하고 병합
df_encoded = pd.concat([df.drop(columns=columns_to_encode), encoded_df], axis=1)
df_encoded.to_csv("encoded_multi_drug_deaths.csv", index=False)
file_path = 'encoded_multi_drug_deaths.csv'
data = pd.read_csv(file_path)

# Compute the correlation matrix
correlation_matrix = data.corr()

# Plot the heatmap
plt.figure(figsize=(16, 12))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix Heatmap')
plt.show()
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# 특성과 목표 변수 정의

# 특성과 목표 변수 준비
X = data.loc[:,(data.columns != 'Multi-Drug')]
y = data['Multi-Drug']

# 데이터를 학습용과 테스트용으로 분리

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=data['Multi-Drug'])

# 결정 트리 분류기 초기화
clf = DecisionTreeClassifier(max_depth=4,random_state=42)

# 모델 학습
clf.fit(X_train, y_train)

# 예측 수행
y_pred = clf.predict(X_test)

# 모델 평가
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", report)
from sklearn import tree

# Plot the decision tree
plt.figure(figsize=(20,10))
tree.plot_tree(clf, feature_names=X.columns.tolist(), class_names=['False', 'True'], filled=True, rounded=True)
plt.title('Decision Tree for Multi-Drug Prediction')
plt.show()
from sklearn.metrics import confusion_matrix
y_pred = clf.predict(X_test)

# Compute the confusion matrix
cm = confusion_matrix(y_test, y_pred)
# Plot the confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
from sklearn.model_selection import cross_val_score, KFold

# Initialize k-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Perform k-fold cross-validation
cv_scores = cross_val_score(clf, X, y, cv=kf, scoring='accuracy')

# Display the cross-validation scores and mean score
cv_scores, cv_scores.mean()