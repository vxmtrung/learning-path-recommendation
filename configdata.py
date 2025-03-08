import pandas as pd
def main():
    # đọc file learning_outcomes.csv
    df = pd.read_csv('learning_outcomes.csv')
    
    # xóa cột đầu tiên trong file và ghi đè lại file
    df = df.drop(df.columns[0], axis=1)
    # hoán đổi vị trí cột 
    df.to_csv('learning_outcomes.csv', index=False)
    
main()
    