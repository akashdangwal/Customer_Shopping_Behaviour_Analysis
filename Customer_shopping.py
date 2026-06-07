import pandas as pd

df = pd.read_csv(r"C:\Users\hp\Downloads\customer_shopping.csv")
print(df.head())
print(df.describe(include='all'))

print(df.isnull().sum())
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))
print(df.isnull().sum())

df.columns = df.columns.str.lower()    
df.columns = df.columns.str.replace(' ',"_")
print(df.columns)    # now all columns are sneak casing
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)

# feature engineering--> create a column age_group
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels= labels)
print(df[['age', 'age_group']].head(5))

# create another column purchase_frequency_days
frequency_mapping = {
    'Fortnightly':14,
    'Weekly' : 7,
    'Monthly' : 30,
    'Quarterly' : 90,
    'Bi-Weekly' : 14,
    'Annually' : 365,
    'Every 3 Months' : 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days','frequency_of_purchases']].head(10))

print(df[['discount_applied','promo_code_used']].head(5))

print((df['discount_applied'] == df['promo_code_used']).all())  # checks, in these columns values are same or not:if same then display--) True

df = df.drop('promo_code_used', axis = 1)
print(df.columns)


# step 1--) connect to mysql
# replace placeholder with actual details
from sqlalchemy import create_engine  

Username = 'root'
Password = 'Akash%402006'
Host=  'localhost'
Port = '3306'
database = 'customer_shopping'

engine = create_engine(f'mysql+mysqlconnector://{Username}:{Password}@{Host}:{Port}/{database}')

# step 2--> load dataframe into mysql
table_name = 'customer'  # choose any table name
df.to_sql(table_name, engine, if_exists='replace', index= False)

print(f"Data Successfully loaded into Table '{table_name}' in Database '{database}'.")
# pd.read_sql("select * from customer limit 20", engine)   # you can also use this , another shortcuts

 