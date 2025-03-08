# import random
# import faker

# def generate_students(num_students=1000):
#     fake = faker.Faker("vi_VN")
#     students = []
    
#     for i in range(2410001, 2410001 + num_students):
#         student_code = str(i)
#         student_name = fake.name()
#         student_email = "a@hcmut.edu.vn"
#         english_level = random.randint(0, 4)
#         faculty = "MT"
#         gpa = round(random.uniform(0.0, 4.0), 2)
        
#         students.append(
#             f"{student_code},{student_name},{student_email},{english_level},{faculty},{gpa}"
#         )
    
#     return students

# # Gọi hàm và lưu kết quả
# students_data = generate_students()

# # Xuất ra file CSV
# with open("students_data.csv", "w", encoding="utf-8") as file:
#     file.write("student_code,student_name,student_email,english_level,faculty,GPA\n")
#     file.write("\n".join(students_data))
    
import random
import faker

def generate_data(num_records=280000):
    fake = faker.Faker("vi_VN")
    students = (
        list(range(1810001, 1811001)) +
        list(range(1910001, 1911001)) +
        list(range(2010001, 2011001)) +
        list(range(2110001, 2111001)) +
        list(range(2210001, 2211001)) +
        list(range(2310001, 2311001)) +
        list(range(2410001, 2411001))
    )
    
    courses = [
        "TCTD1", "DATH", "TCTD2", "DADN", "TCTD3", "CO3011", "CO3013", "CO3017", "CO3021", "CO3023", 
        "CO3027", "CO3029", "CO3031", "CO3033", "CO3035", "CO3037", "CO3041", "CO3043", "CO3045", "CO3047", 
        "CO3049", "CO3051", "CO3057", "CO3059", "CO3061", "CO3065", "CO3067", "CO3069", "CO3071", "CO3083", 
        "CO3085", "CO3089", "CO3115", "CO4025", "CO3117", "CO4031", "CO4033", "CO4035", "CO4037", "CO4039", 
        "IM1025", "IM3001", "IM1013", "IM1027", "IM1023", "MT1005", "MT1007", "MT2013", "CH1003", "PH1003", 
        "CO2011", "SP1031", "SP1037", "SP1035", "SP1039", "CO1005", "CO2001", "LA1005", "LA1009", "CO1023", 
        "CO1027", "CO2007", "CO2013", "CO2039", "CO2017", "CO3005", "CO3093", "CO4029", "CO3335", "CO3015", 
        "MT1003", "PH1007", "CO1007", "SP1033", "SP1007", "LA1003", "LA1007", "CO2003", "CO3001", "CO4337"
    ]
    
    semesters = [201, 202, 211, 212, 221, 222, 231, 232, 241, 242]
    
    data = []
    
    for _ in range(num_records):
        while True:
            student = random.choice(students)
            semester = random.choice(semesters)
            if int(str(student)[:3]) <= semester:
                break
        
        course = random.choice(courses)
        score = round(random.uniform(0.0, 10.0), 2)
        count_learn = 1
        
        data.append(f"{student},{course},{score},{count_learn},{semester}")
    
    return data

# Gọi hàm và lưu kết quả
data_records = generate_data()

# Xuất ra file CSV
with open("student_course_data.csv", "w", encoding="utf-8") as file:
    file.write("student,course,score,count_learn,semester\n")
    file.write("\n".join(data_records))

print("File student_course_data.csv đã được tạo thành công!")