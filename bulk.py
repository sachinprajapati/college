import pandas as pd

df = pd.read_excel('data.xlsx')

ren = {'Student Ref. No': 'reg_no', "Father's Name": 'f_name', "Mother's Name": 'm_name', "Gender": 'gender', "Date Of Birth": 'dob', "Mobile No": 'phone', 'Category': 'category', 'Email ID': 'email'}

df.rename(columns=ren, inplace=True)
df.set_index('reg_no', inplace=True)
user = df[['email']]
user['first_name'] = df['Student Name'].str.split().str[:-1].str.join(' ')
user['last_name'] = df['Student Name'].str.split().str[-1]
user['is_staff'] = False
user['is_superuser'] = False
user['date_joined'] = pd.Timestamp.utcnow()
