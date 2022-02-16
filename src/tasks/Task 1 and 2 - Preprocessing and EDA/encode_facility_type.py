
# this code will work if all facility types have Low, Med, High at the end of their names
# won't work for facility types Industrial, Public_Assembly_Recreation, Public_Assembly_Drama_theater
# I think we need to include these three into other groups

def encode_facility_type(df):

  # split market sector and site eui class (Low, Medium, High)
  df['eui_class'] = df.facility_type.apply(lambda x: x.rsplit('_')[-1])
  df['sector'] = df.facility_type.apply(lambda x: x.rsplit('_', 1)[0])

  # one-hot encode sector
  ohe_df = pd.get_dummies(df[["sector"]] )
  df = df.join(ohe_df)

  for val in df.sector.unique():
    conditions = [
                  (df['sector'] == val) & (df['eui_class'] == 'Low'),
                  (df['sector'] == val) & (df['eui_class'] == 'Med'),
                  (df['sector'] == val) & (df['eui_class'] == 'High')

    ]

    # start with 1 instead of 0 because 0 is a value indicating the absence of the ohe columns in the data
    # this is also the reason why I didn't use sklearn's LabelEncoder since it starts from 0 to n_classes-1
    values = [1, 2, 3]
    col_name = 'sector_'+val
    df[col_name] = np.select(conditions, values, default=0)
  
  df.drop(['sector', 'eui_class'], axis=1, inplace=True)

  return df
