"""Function to detect outliers
    
    Args:
        df (dataframe): Dataframe that will be examined by the function
        
    Returns:

"""

def detect_outliers(df):
    outliers = []
    for column in df:
        cut_off = df[column].std() * 2
        lower = df[column].mean() - cut_off
        upper = df[column].mean() + cut_off
        row_count = 0
        for x in df[column]:
            if x >= upper or x <= lower:  # if below or above 2 stds from mean, add to outliers array
                outliers.append(row_count)  # adds row to outliers array
            row_count += 1
    outliers = list(set(outliers))  # removes duplicate rows
    return outliers

"""Function to remove outliers

    Args:
    
    Returns:
        dict: dict containing dataframe without outliers

"""

def remove_outliers():
    outliers = detect_outliers(df)
    df = df.drop(index=outliers)
    return df

"""Function that removes columns containing NAN

    Args:
        df (dataframe): dataframe to be checked
        col_type (str): type of data to be examined in the dataframe
        
    Returns:
        dict: dict containing dataframe without the selected column
    """

def get_col_with_no_nan(df, col_type):
    if col_type == 'num':
        predictors = df.select_dtypes(exclude=['object'])
    elif col_type == 'no_num':
        predictors = df.select_dtypes(include=['object'])
    elif col_type == 'any':
        predictors = df
    else:
        print('Please input a correct col_type value (num, no_num, any)')
        return 0

    col_with_no_nan = []
    for col in predictors.columns:
        if not df[col].isnull().any():
            col_with_no_nan.append(col)

    return col_with_no_nan