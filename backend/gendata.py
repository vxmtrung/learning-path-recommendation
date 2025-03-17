import random
import faker

def generate_student_data():
    # student_code,student_name,student_email,english_level,faculty,GPA
    fake = faker.Faker("vi_VN")
    init_student_code = 2010001
    init_student_gpa = 2.1
    with open("student_data.txt", "w", encoding="utf-8") as file:
        file.write("student_code,student_name,student_email,english_level,faculty,GPA\n")
    for i in range(5):
        student_code = init_student_code + i*100000
        init_student_gpa = 2.0
        for j in range(20):
            student_name = fake.name()
            student_email = "mail." + str(student_code) + "@hcmut.edu.vn"
            english_level = None
            if str(student_code).startswith("241"):
                english_level = 1
            elif str(student_code).startswith("231"):
                english_level = 2
            elif str(student_code).startswith("221"):
                english_level = 3
            else:
                english_level = 4
            faculty = "MT"
            init_student_gpa += 0.1
            init_student_gpa = round(init_student_gpa, 1)
    
            with open("student_data.txt", "a", encoding="utf-8") as file:
                file.write(f"{student_code + j},{student_name},{student_email},{english_level},{faculty},{init_student_gpa}\n")

def generate_learn_log_student_1(index = 0):
    courses = ["LA1003", "MT1003", "PH1003", "CO1005", "CO1023",
            ]
    for i in range(20):
        for course in courses:
            semester = 241
            if course == "LA1003":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index
            elif course == "MT1003":
                score = round(random.uniform(7, 10), 1)
                semester = semester - index
            elif course == "PH1003":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index
            elif course == "CO1005":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index
            elif course == "CO1023":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index
        
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                file.write(f"{2410001 + i},{course},{score},{1},{semester}\n")
         
def generate_learn_log_student_2(index = 1):
    courses = ["LA1003", "MT1003", "PH1003", "CO1005", "CO1023",
               "LA1005", "MT1005", "MT1007", "CO1007", "CO1027", "PH1007",
               "LA1007", "SP1031", "CO2007", "CO2011", "CO2003",
            ]
    for i in range(20):
        for course in courses:
            semester = 241
            if course == "LA1003":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10
            elif course == "MT1003":
                score = round(random.uniform(7, 10), 1)
                semester = semester - index*10
            elif course == "PH1003":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "CO1005":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10
            elif course == "CO1023":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "LA1005":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10 + 1
            elif course == "MT1005":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "MT1007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "CO1007":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester - index*10 + 1
            elif course == "PH1007":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10 + 1
            elif course == "LA1007":
                score = round(random.uniform(9, 10), 1)
                semester = semester
            elif course == "SP1031":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester
            elif course == "CO2007":
                score = round(random.uniform(7, 9), 1)
                semester = semester
            elif course == "CO2011":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester
            elif course == "CO2003":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester
            elif course == "CO1027":    
                score = round(random.uniform(7, 9), 1)
                semester = semester
            
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                file.write(f"{2310001 + i},{course},{score},{1},{semester}\n")       

def generate_learn_log_student_3(index = 2):
    courses = ["LA1003", "MT1003", "PH1003", "CO1005", "CO1023",
               "LA1005", "MT1005", "MT1007", "CO1007", "CO1027", "PH1007",
               "LA1007", "SP1031", "CO2007", "CO2011", "CO2003",
               "LA1009", "SP1033", "CO2017", "CO2039", "MT2013", "TCTD1", 
               "SP1035", "CO3093", "CO2013", "CO3001", "CH1003", "DATH",
            ]
    for i in range(20):
        for course in courses:
            semester = 241
            if course == "LA1003":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10
            elif course == "CO1027":    
                score = round(random.uniform(7, 9), 1)
                semester = semester
            elif course == "MT1003":
                score = round(random.uniform(7, 10), 1)
                semester = semester - index*10
            elif course == "PH1003":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "CO1005":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10
            elif course == "CO1023":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "LA1005":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10 + 1
            elif course == "MT1005":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "MT1007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "CO1007":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester - index*10 + 1
            elif course == "PH1007":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10 + 1
            elif course == "LA1007":
                score = round(random.uniform(9, 10), 1)
                semester = semester - (index - 1)*10
            elif course == "SP1031":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2011":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2003":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 1)*10
            elif course == "LA1009":
                score = round(random.uniform(9, 10), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "SP1033":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "CO2017":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "CO2039":            
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "MT2013":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "TCTD1":
                score = round(random.uniform(7.5, 8.5), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "SP1035":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester
            elif course == "CO3093":
                score = round(random.uniform(7.5, 9), 1)
                semester = semester
            elif course == "CO2013":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester
            elif course == "CO3001":
                score = round(random.uniform(7, 9), 1)
                semester = semester
            elif course == "CH1003":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester
            elif course == "DATH":
                score = round(random.uniform(8, 10), 1)
                semester = semester
            
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                file.write(f"{2210001 + i},{course},{score},{1},{semester}\n")       

def generate_learn_log_student_4(index = 3):
    courses = ["LA1003", "MT1003", "PH1003", "CO1005", "CO1023",
               "LA1005", "MT1005", "MT1007", "CO1007", "CO1027", "PH1007",
               "LA1007", "SP1031", "CO2007", "CO2011", "CO2003",
               "LA1009", "SP1033", "CO2017", "CO2039", "MT2013", "TCTD1", 
               "SP1035", "CO3093", "CO2013", "CO3001", "CH1003", "DATH",
               "SP1039", "CO2001", "CO3005", "CO3335", "TCTD2", "DADN", 
               "SP1037", "CO4029", "TCTD3",
            ]
    
    for i in range(20):
        for course in courses:
            semester = 241
            if course == "LA1003":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10
            elif course == "CO1027":    
                score = round(random.uniform(7, 9), 1)
                semester = semester
            elif course == "MT1003":
                score = round(random.uniform(7, 10), 1)
                semester = semester - index*10
            elif course == "PH1003":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "CO1005":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10
            elif course == "CO1023":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "LA1005":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10 + 1
            elif course == "MT1005":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "MT1007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "CO1007":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester - index*10 + 1
            elif course == "PH1007":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10 + 1
            elif course == "LA1007":
                score = round(random.uniform(9, 10), 1)
                semester = semester - (index - 1)*10
            elif course == "SP1031":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2011":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2003":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 1)*10
            elif course == "LA1009":
                score = round(random.uniform(9, 10), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "SP1033":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "CO2017":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "CO2039":            
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "MT2013":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "TCTD1":
                score = round(random.uniform(7.5, 8.5), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "SP1035":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 2)*10
            elif course == "CO3093":
                score = round(random.uniform(7.5, 9), 1)
                semester = semester - (index - 2)*10
            elif course == "CO2013":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 2)*10
            elif course == "CO3001":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 2)*10
            elif course == "CH1003":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 2)*10
            elif course == "DATH":
                score = round(random.uniform(8, 10), 1)
                semester = semester - (index - 2)*10
            elif course == "SP1039":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "CO2001":
                score = round(random.uniform(8, 9), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "CO3005":
                score = round(random.uniform(6, 8), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "CO3335":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "TCTD2":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "DADN":
                score = round(random.uniform(8, 10), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "SP1037":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester
            elif course == "CO4029":
                score = round(random.uniform(7, 9), 1)
                semester = semester
            elif course == "TCTD3":
                score = round(random.uniform(7, 9), 1)
                semester = semester
            
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                file.write(f"{2110001 + i},{course},{score},{1},{semester}\n")    
        
        # Xử lý ảnh và Thị giác máy tính
        if i in [0,1,2,3]:
            speciality_courses = ["CO3043", "CO3045", "CO3049", "CO3051", "CO3057", "CO3059", "CO3089", "CO3117"]
            selected_courses = random.sample(speciality_courses, 2)  
            for course in selected_courses:
                score = round(random.uniform(7, 9), 1)
                semester = 241
                
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i},{course},{score},{1},{semester}\n")
        
        # Trí tuệ nhân tạo ứng dụng
        if i in [4,5,6,7]:
            speciality_courses = ["CO3029", "CO3035", "CO3037", "CO3041", "CO3043", "CO3045", "CO3049", "CO3051", "CO3061", "CO3085", "CO3089", "CO3117", "CO4025"]
            selected_courses = random.sample(speciality_courses, 2)  
            for course in selected_courses:
                score = round(random.uniform(7, 9), 1)
                semester = 241
                
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i},{course},{score},{1},{semester}\n")
        
        # Mật mã và An ninh mạng
        if i in [8,9,10,11]:
            speciality_courses = ["CO3047", "CO3049", "CO3051", "CO3069", "CO3083", "CO3089"]
            selected_courses = random.sample(speciality_courses, 2)  
            for course in selected_courses:
                score = round(random.uniform(7, 9), 1)
                semester = 241
                
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i},{course},{score},{1},{semester}\n")
           
        # Công nghệ Phần mềm
        if i in [12,13,14,15]:
            speciality_courses = ["CO3011", "CO3013", "CO3015", "CO3017", "CO3065", "CO3089", "CO3115"]
            selected_courses = random.sample(speciality_courses, 2)  
            for course in selected_courses:
                score = round(random.uniform(7, 9), 1)
                semester = 241
                
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i},{course},{score},{1},{semester}\n")

        # Công nghệ Dữ liệu Bảo mật và Trí tuệ Kinh doanh
        if i in [16,17,18,19]:
            speciality_courses = ["CO3021", "CO3023", "CO3027", "CO3029", "CO3033", "CO3115", "CO4031", "CO4033", "CO4035", "CO4037", "CO4039"]
            selected_courses = random.sample(speciality_courses, 2)  
            for course in selected_courses:
                score = round(random.uniform(7, 9), 1)
                semester = 241
                
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i},{course},{score},{1},{semester}\n")
                    
        # Group D
        group_d_course = ["IM1013", "IM3001", "IM1027", "IM1023", "IM1025"]
        with open("learn_log.txt", "a", encoding="utf-8") as file:
                file.write(f"{2110001 + i},{random.sample(group_d_course, 1)[0]},{round(random.uniform(7, 9), 1)},{1},{241}\n")
            
def generate_learn_log_student_5(index = 4):
    courses = ["LA1003", "MT1003", "PH1003", "CO1005", "CO1023",
               "LA1005", "MT1005", "MT1007", "CO1007", "CO1027", "PH1007",
               "LA1007", "SP1031", "CO2007", "CO2011", "CO2003",
               "LA1009", "SP1033", "CO2017", "CO2039", "MT2013", "TCTD1", 
               "SP1035", "CO3093", "CO2013", "CO3001", "CH1003", "DATH",
               "SP1039", "CO2001", "CO3005", "CO3335", "TCTD2", "DADN", 
               "SP1037", "CO4029", "TCTD3",
               "SP1007", "CO4337"
            ]
    
    for i in range(20):
        for course in courses:
            semester = 241
            if course == "LA1003":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10
            elif course == "CO1027":    
                score = round(random.uniform(7, 9), 1)
                semester = semester
            elif course == "MT1003":
                score = round(random.uniform(7, 10), 1)
                semester = semester - index*10
            elif course == "PH1003":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "CO1005":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10
            elif course == "CO1023":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10
            elif course == "LA1005":
                score = round(random.uniform(9, 10), 1)
                semester = semester - index*10 + 1
            elif course == "MT1005":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "MT1007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - index*10 + 1
            elif course == "CO1007":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester - index*10 + 1
            elif course == "PH1007":
                score = round(random.uniform(8, 10), 1)
                semester = semester - index*10 + 1
            elif course == "LA1007":
                score = round(random.uniform(9, 10), 1)
                semester = semester - (index - 1)*10
            elif course == "SP1031":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2011":
                score = round(random.uniform(6.5, 8.5), 1)
                semester = semester - (index - 1)*10
            elif course == "CO2003":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 1)*10
            elif course == "LA1009":
                score = round(random.uniform(9, 10), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "SP1033":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "CO2017":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "CO2039":            
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "MT2013":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "TCTD1":
                score = round(random.uniform(7.5, 8.5), 1)
                semester = semester - (index - 1)*10 + 1
            elif course == "SP1035":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 2)*10
            elif course == "CO3093":
                score = round(random.uniform(7.5, 9), 1)
                semester = semester - (index - 2)*10
            elif course == "CO2013":
                score = round(random.uniform(7, 8.5), 1)
                semester = semester - (index - 2)*10
            elif course == "CO3001":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 2)*10
            elif course == "CH1003":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 2)*10
            elif course == "DATH":
                score = round(random.uniform(8, 10), 1)
                semester = semester - (index - 2)*10
            elif course == "SP1039":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "CO2001":
                score = round(random.uniform(8, 9), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "CO3005":
                score = round(random.uniform(6, 8), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "CO3335":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "TCTD2":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "DADN":
                score = round(random.uniform(8, 10), 1)
                semester = semester - (index - 2)*10 + 1
            elif course == "SP1037":
                score = round(random.uniform(6.5, 8), 1)
                semester = semester - (index - 3)*10
            elif course == "CO4029":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 3)*10
            elif course == "TCTD3":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 3)*10
            elif course == "SP1007":
                score = round(random.uniform(7, 9), 1)
                semester = semester - (index - 3)*10 + 1
            elif course == "CO4337":
                score = round(random.uniform(7.5, 9), 1)
                semester = semester - (index - 3)*10 + 1
            
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")    
        
        # Xử lý ảnh và Thị giác máy tính
        if i in [0,1,2,3]:
            speciality_courses = ["CO3043", "CO3045", "CO3049", "CO3051", "CO3057", "CO3059", "CO3089", "CO3117"]
            selected_courses = random.sample(speciality_courses, 5)  
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                # 2 môn đầu: semester = 231
                for course in selected_courses[:2]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 231
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")

                # 3 môn sau: semester = 232
                for course in selected_courses[2:]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 232
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")
        
        # Trí tuệ nhân tạo ứng dụng
        if i in [4,5,6,7]:
            speciality_courses = ["CO3029", "CO3035", "CO3037", "CO3041", "CO3043", "CO3045", "CO3049", "CO3051", "CO3061", "CO3085", "CO3089", "CO3117", "CO4025"]
            selected_courses = random.sample(speciality_courses, 5)  
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                # 2 môn đầu: semester = 231
                for course in selected_courses[:2]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 231
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")

                # 3 môn sau: semester = 232
                for course in selected_courses[2:]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 232
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")
        
        # Mật mã và An ninh mạng
        if i in [8,9,10,11]:
            speciality_courses = ["CO3047", "CO3049", "CO3051", "CO3069", "CO3083", "CO3089"]
            selected_courses = random.sample(speciality_courses, 5)  
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                # 2 môn đầu: semester = 231
                for course in selected_courses[:2]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 231
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")

                # 3 môn sau: semester = 232
                for course in selected_courses[2:]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 232
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")
           
        # Công nghệ Phần mềm
        if i in [12,13,14,15]:
            speciality_courses = ["CO3011", "CO3013", "CO3015", "CO3017", "CO3065", "CO3089", "CO3115"]
            selected_courses = random.sample(speciality_courses, 5)  
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                # 2 môn đầu: semester = 231
                for course in selected_courses[:2]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 231
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")

                # 3 môn sau: semester = 232
                for course in selected_courses[2:]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 232
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")
                    
        # Công nghệ Dữ liệu Bảo mật và Trí tuệ Kinh doanh
        if i in [16,17,18,19]:
            speciality_courses = ["CO3021", "CO3023", "CO3027", "CO3029", "CO3033", "CO3115", "CO4031", "CO4033", "CO4035", "CO4037", "CO4039"]
            selected_courses = random.sample(speciality_courses, 5)  
            with open("learn_log.txt", "a", encoding="utf-8") as file:
                # 2 môn đầu: semester = 231
                for course in selected_courses[:2]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 231
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")

                # 3 môn sau: semester = 232
                for course in selected_courses[2:]:  
                    score = round(random.uniform(7, 9), 1)
                    semester = 232
                    file.write(f"{2010001 + i},{course},{score},{1},{semester}\n")
                    
        # Group D
        group_d_course = ["IM1013", "IM3001", "IM1027", "IM1023", "IM1025"]
        with open("learn_log.txt", "a", encoding="utf-8") as file:
                file.write(f"{2010001 + i},{random.sample(group_d_course, 1)[0]},{round(random.uniform(7, 9), 1)},{1},{231}\n")
                          

def generate_learn_log():
    with open("learn_log.txt", "w", encoding="utf-8") as file:
        file.write("student,course,score,count_learn,semester\n")
    generate_learn_log_student_1()
    generate_learn_log_student_2()
    generate_learn_log_student_3()
    generate_learn_log_student_4()
    generate_learn_log_student_5()
    
def geneate_learn_log_to_test():
    with open("learn_log.txt", "w", encoding="utf-8") as file:
        file.write("student,course,score,count_learn,semester\n")
    # K24
    courses = ["LA1003", "MT1003", "PH1003", "CO1005", "CO1023",
               "LA1005", "MT1005", "MT1007", "CO1007", "CO1027", "PH1007",
               "LA1007", "SP1031", "CO2007", "CO2011", "CO2003",
               "LA1009", "SP1033", "CO2017", "CO2039", "MT2013", "TCTD1", 
               "SP1035", "CO3093", "CO2013", "CO3001", "CH1003", "DATH",
               "SP1039", "CO2001", "CO3005", "CO3335", "TCTD2", "DADN", 
               "SP1037", "CO4029", "TCTD3",
            ]
    group_c_course = ["CO3043", "CO3045", "CO3049", "CO3051", "CO3057", "CO3059", "CO3089", "CO3117", "CO3029", "CO3035", "CO3037", "CO3041", "CO3043", "CO3045", "CO3049", "CO3051", "CO3061", "CO3085", "CO3089", "CO3117", "CO4025",
                      "CO3047", "CO3049", "CO3051", "CO3069", "CO3083", "CO3089", "CO3011", "CO3013", "CO3015", "CO3017", "CO3065", "CO3089", "CO3115", "CO3021", "CO3023", "CO3027", "CO3029", "CO3033", "CO3115", "CO4031", "CO4033", "CO4035", "CO4037", "CO4039"]
    group_d_course = ["IM1013", "IM3001", "IM1027", "IM1023", "IM1025"]
    for i in range(4):
        for j in range(20):
            for course in courses:
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i*100000 + j},{course},{round(random.uniform(5, 9), 1)},{1},{251}\n")
            group_c_course_random = random.sample(group_c_course, 5)
            for course in group_c_course_random:
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i*100000 + j},{course},{round(random.uniform(5, 9), 1)},{1},{251}\n")
            group_d_course_random = random.sample(group_d_course, 1)
            for course in group_d_course_random:
                with open("learn_log.txt", "a", encoding="utf-8") as file:
                    file.write(f"{2110001 + i*100000 + j},{course},{round(random.uniform(5, 9), 1)},{1},{251}\n")
            
        
        
    
generate_student_data()
# generate_learn_log()
# geneate_learn_log_to_test()
