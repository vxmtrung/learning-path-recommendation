import matplotlib.pyplot as plt

# Dữ liệu mới
semesters = ['202', '211', '212', '221', '222', '231', '232', '241']
precision = [0.9583, 0.9750, 0.9931, 0.9948, 0.9972, 0.8394, 0.8729, 0.8444]
recall = [0.9583, 0.9750, 0.9931, 0.9948, 0.9972, 0.8394, 0.8571, 0.8444]
f1_score = [0.9583, 0.9750, 0.9931, 0.9948, 0.9972, 0.8394, 0.8642, 0.8444]

# Vẽ biểu đồ
plt.figure(figsize=(10, 5))
plt.plot(semesters, precision, marker='o', label='Precision')
plt.plot(semesters, recall, marker='s', label='Recall')
plt.plot(semesters, f1_score, marker='^', label='F1-score')

# Thêm nhãn và tiêu đề
plt.xlabel('Học kỳ')
plt.ylabel('Giá trị')
plt.title('Biểu đồ biến động các chỉ số Precision, Recall và F1-score theo học kỳ')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Hiển thị biểu đồ
plt.show()
