import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("combined_singers.csv") 

df['birth_date'] = pd.to_datetime(df['birthDate'], errors='coerce') 
df['birth_year'] = df['birth_date'].dt.year 

df['decade'] = (df['birth_year'] // 10) * 10 

df = df[df['genderLabel'].isin(['male', 'female'])]

decade_gender_counts = df.groupby(['decade', 'genderLabel'])['singerLabel'].count().unstack(fill_value=0)
decade_gender_counts.plot(kind='bar', figsize=(12,6), color=['lightpink', 'skyblue'])

plt.xlabel('Decade of Birth')
plt.ylabel('Number of Singers')
plt.title('Number of Male and Female Singers by Decade')
plt.xticks(rotation=45)
plt.legend(title='Gender')
plt.tight_layout()
plt.show()
