# # Lấy dữ liệu từ learnlog -> dữ liệu thực tế
# # Lấy dữ liệu từ lịch sử predict -> dữ liệu dự đoán

# import pandas as pd

# data = [
#     {"student": "SV1", "semester": "2023-1", "y_true": {"CS101", "MA101", "PHY101"}, 
#      "y_pred": ["CS101", "MA101", "CS102", "PHY102"]},
    
#     {"student": "SV1", "semester": "2023-2", "y_true": {"CS201", "MA202", "PHY102"}, 
#      "y_pred": ["CS201", "CS101", "MA202", "PHY103"]},

#     {"student": "SV2", "semester": "2023-1", "y_true": {"CS101", "CS102"}, 
#      "y_pred": ["CS101", "CS103", "CS102", "MA101"]},

#     {"student": "SV2", "semester": "2023-2", "y_true": {"CS202", "MA203"}, 
#      "y_pred": ["CS201", "CS202", "MA203", "PHY201"]},
# ]

# # Hàm tính Precision@K, Recall@K, F1-score@K
# def precision_at_k(y_true, y_pred, k):
#     relevant = set(y_true)
#     recommended = set(y_pred[:k])
#     return len(relevant & recommended) / k

# def recall_at_k(y_true, y_pred, k):
#     relevant = set(y_true)
#     recommended = set(y_pred[:k])
#     return len(relevant & recommended) / len(relevant) if relevant else 0

# def f1_at_k(y_true, y_pred, k):
#     p = precision_at_k(y_true, y_pred, k)
#     r = recall_at_k(y_true, y_pred, k)
#     return 2 * (p * r) / (p + r) if (p + r) > 0 else 0

# k = 3  # Đánh giá top-K

# # Chuyển dữ liệu thành DataFrame
# df = pd.DataFrame(data)

# # Tính Precision, Recall, F1-score cho từng hàng
# df["precision"] = df.apply(lambda row: precision_at_k(row["y_true"], row["y_pred"], k), axis=1)
# df["recall"] = df.apply(lambda row: recall_at_k(row["y_true"], row["y_pred"], k), axis=1)
# df["f1_score"] = df.apply(lambda row: f1_at_k(row["y_true"], row["y_pred"], k), axis=1)

# # Tính trung bình theo học kỳ
# semester_avg = df.groupby("semester")[["precision", "recall", "f1_score"]].mean()

# # Tính trung bình theo sinh viên
# student_avg = df.groupby("student")[["precision", "recall", "f1_score"]].mean()

# # Tính trung bình toàn hệ thống
# overall_avg = df[["precision", "recall", "f1_score"]].mean()

# # Kết quả
# print("Trung bình theo học kỳ:\n", semester_avg)
# print("\nTrung bình theo sinh viên:\n", student_avg)
# print("\nTrung bình toàn hệ thống:\n", overall_avg)

# Sinh viên K21, học từ học kỳ 211
# 211 không có lựa chọn
# Đề xuất từ học kỳ 212
# Lấy đề xuất từ học kỳ 212 các môn học = predict, Lấy đề xuất tới học kỳ trong learnlog hiện tại
# Đánh giá precision, recall, f1_score từng học kỳ của 1 sinh viên
# Lấy trung bình của sinh viên này
# Mỗi sinh viên lặp lại như vậy
# => Trung bình toàn bộ hệ thống
# Problem ở đây sẽ là việc input đầu vào cho hệ thống dự đoán

# Lấy danh sách mssv trong logs folder
from pathlib import Path
import pandas as pd
import json

def get_student_folders(logs_path):
    return [f.name for f in Path(logs_path).iterdir() if f.is_dir()]

# Ví dụ sử dụng
logs_path = Path("logs")
sid = get_student_folders(logs_path)
print(sid[0])

df = pd.read_csv("student_course_data.csv")

fs = df[df["student"] == int(sid[0])]
with open(Path("logs/" + sid[0] + "/" + "2110162_20250308_154228.txt"), "r", encoding="utf-8") as file:
    data = json.load(file)

y_predict = []
for sem_data in data["learning_path"]:
    sem_inf = {
        "sem": sem_data["semester"],
        "course": [course["course_code"] for course in sem_data["courses"]]
    }
    y_predict.append(sem_inf)

learning_log = fs.groupby("semester")["course"].apply(list).reset_index()

r = [{"sem": row["semester"], "course": row["course"]} for _, row in learning_log.iterrows()]

y_true = list(filter(lambda x: x["sem"] >= y_predict[0]["sem"], r))

# Chuyển thành DataFrame và gom nhóm theo học kỳ
# Chuyển danh sách 'course' thành set trước khi groupby
df_true = pd.DataFrame(y_true)
df_true['course'] = df_true['course'].apply(set)  # Chuyển từng list thành set
df_true = df_true.groupby('sem', as_index=False).agg({'course': 'first'}).rename(columns={'course': 'actual_course'})

df_pred = pd.DataFrame(y_predict)
df_pred['course'] = df_pred['course'].apply(set)
df_pred = df_pred.groupby('sem', as_index=False).agg({'course': 'first'}).rename(columns={'course': 'pred_course'})

# Gộp hai bảng theo học kỳ
df_merge = df_true.merge(df_pred, on='sem', how='outer')

# Thay NaN bằng set rỗng để tránh lỗi khi tính toán
df_merge['actual_course'] = df_merge['actual_course'].apply(lambda x: x if isinstance(x, set) else set())
df_merge['pred_course'] = df_merge['pred_course'].apply(lambda x: x if isinstance(x, set) else set())

# Tính số lượng môn học dự đoán đúng
df_merge['correct'] = df_merge.apply(lambda x: len(x['actual_course'] & x['pred_course']), axis=1)

print(df_merge)

# Tính Precision & Recall
df_merge['Precision'] = df_merge.apply(lambda x: x['correct'] / len(x['pred_course']) if len(x['pred_course']) > 0 else 0, axis=1)
df_merge['Recall'] = df_merge.apply(lambda x: x['correct'] / len(x['actual_course']) if len(x['actual_course']) > 0 else 0, axis=1)

# Hiển thị kết quả
print(df_merge[['sem', 'Precision', 'Recall']])