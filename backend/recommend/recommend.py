from courses.models import Course
from group_course.models import GroupCourse
from rules.service import map_group_rule
learning_path = []
current_semester = 0
learn_summer_semester = False
credit_in_semester = 18
min_credit_in_semester = 11
learned_course = []
main_semester = []
summer_semester = []
course_major = []

class LearningPathElement:
    def __init__(self, semester):
        self.semester = semester
        self.courses = []
        self.credit = 0
        
    def to_dict(self):
        return {
            "semester": self.semester,
            "courses": [
                {
                    "course_id": course.course_id,
                    "course_code": course.course_code,
                    "course_name": course.course_name,
                    "credit": course.credit,
                    **({"predict_score": course.predict_score} if course.group_course.group_course_name != "Tự chọn tự do" else {}),
                    "note": course.note,
                }
                for course in self.courses
            ],
            "total_credit": self.credit,
        }

        
def recommend(learner, learner_log, unlearned_course, course_graph, semester):
    global learning_path
    global current_semester
    global learn_summer_semester
    global credit_in_semester
    global learned_course
    global main_semester
    global summer_semester
    global min_credit_in_semester
    global course_major
    
    learning_path = []
    current_semester = 0
    learn_summer_semester = False
    credit_in_semester = 18
    main_semester = []
    summer_semester = []
    min_credit_in_semester = 11
    course_major = []
    
    # Get majors
    majors = learner["major"]
    for major in majors:
        course_major.append([major, 5])
    
    # Caculate number of course each group
    all_group_course = handle_group_course(learner, learner_log, unlearned_course, len(course_major))
   
    if learner["over_learn"] == "1":
        main_semester = learner["main_semester"]
        
    if learner["learn_summer_semester"] == "1":
        learn_summer_semester = True
        summer_semester = learner["summer_semester"]
        
    current_semester = semester
    unlearned_course = list(unlearned_course)
    add_english_course_to_learning_path(learner_log, unlearned_course)
    travel_course_graph(learner, learner_log, unlearned_course, course_graph, all_group_course)
    if learner["learn_to_improve"] == "1":
        learned_course = sorted(learned_course, key=lambda course: course.predict_score)
        for semester in learning_path:
            if int(semester.semester)%10 == 3:
                continue
            if semester.credit<min_credit_in_semester:
                for course in learned_course:
                    if int(semester.credit) + int(course.credit) <= credit_in_semester:
                        semester.courses.append(course)
                        learned_course.remove(course)
                        semester.credit = semester.credit + course.credit
                        if semester.credit >= min_credit_in_semester:
                            break
    return learning_path
    
def handle_group_course(learner, learner_log, course_list, num_of_major):
    group_course = map_group_rule()
    updated_groups = {group.group_course_code: group for group in group_course}
    for log in learner_log:
        if log.course.group_course and log.course in course_list:
            group_code = log.course.group_course.group_course_code
            if group_code in updated_groups:
                updated_groups[group_code].minimum_course -= 1
           
    for group in group_course:
        if group.group_course_code in learner:
            cur_group = updated_groups.get(group.group_course_code)
            alt_group = updated_groups.get(group.alternative_group.group_course_code)
            
            if alt_group:
                alt_group.minimum_course += cur_group.minimum_course - int(learner[group.group_course_code])
                cur_group.minimum_course = int(learner[group.group_course_code])
        
        if group.group_course_code == "group_c":
            modified_group = updated_groups.get(group.group_course_code)
            modified_group.minimum_course += 5 * (num_of_major-1)
        
    return group_course
            
def add_english_course_to_learning_path(learner_log, unlearned_course):
    global learning_path
    english_course_name = ["Anh văn 1", "Anh văn 2", "Anh văn 3", "Anh văn 4"]
    english_unlearned = []
    for course in unlearned_course:
        if course.course_name in english_course_name:
            english_unlearned.append(course)
            unlearned_course.remove(course)
   
    for log in learner_log:
        if log.course.course_name in english_course_name:
            english_unlearned.remove(log.course)
       
    for course in english_unlearned:
        global current_semester
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = 2
        learning_path.append(learning_path_element)
        current_semester = next_semester(current_semester)      
 
### Add english 
### Travel course and add new course to learning_path
### Step 1: if it is not course not ---> recursive
### Step 2: if it is course node ---> check is_subject_learned
### Step 3: Check prerequisite
def travel_course_graph(learner, learner_log, unlearned_course, course_graph, all_group_course):
    global learned_course
    global course_major
    
    if course_graph.is_course == False:
        for child_node in course_graph.children:
            travel_course_graph(learner, learner_log, unlearned_course, child_node, all_group_course)
    else:
        # print(course_graph.course_node.course_name)
        if is_subject_learned(course_graph.course_node, learner_log, unlearned_course):
            # print("Môn đã học --- ", course_graph.course_node.course_name)
            learned_course.append(course_graph.course_node)
        
            if course_graph.course_node.group_course.group_course_code == "group_c":
                major_of_course = course_graph.course_node.majors.all()
                for major in major_of_course:
                    for major_course in course_major:
                        if major_course[0] == major.major_code:
                            major_course[1] = major_course[1] - 1
                
        else:
            # print("Môn chưa học --- ", course_graph.course_node.course_name)
            if course_graph.course_node.group_course.group_course_code == "group_c":
                major_of_course = course_graph.course_node.majors.all()
                for major in major_of_course:
                    for major_course in course_major:
                        if str(major_course[0]) == str(major.major_code):
                            if major_course[1] <= 0:
                                return
                            major_course[1] = major_course[1] - 1
            # Kiem tra so mon con lai cua tung nhom mon
            if course_graph.course_node.group_course:
                for group in all_group_course:
                    if group.group_course_code == course_graph.course_node.group_course.group_course_code:
                        if int(group.minimum_course) <= 0:
                            return
                        else:
                            group.minimum_course = group.minimum_course - 1
                            
                        # Kiem tra cac mon hoc chung dai dien cho nhom
                        if not group.specifically:
                            course_graph.course_node.course_name = course_graph.course_node.group_course.group_course_name
                    
            check_prerequisite_and_add_learning_path(int(learner["english_level"]), course_graph.course_node, learner_log, unlearned_course)
            
                
### If course was learned, remove it unlearned_course
def is_subject_learned(course, learner_log, unlearned_course):
    if course.course_code in ["LA1003", "LA1005", "LA1007", "LA1009"]:
        return True
    for log in learner_log:
        if log.course.course_code == course.course_code:
            unlearned_course.remove(course)
            return True
    return False
    
def check_prerequisite_and_add_learning_path(english_level, course, leaner_log, unlearned_course):
    ### Chech subject prerequisite
    ### If this course has subject prerequisite: 2 cases
    ### Case 1: Subject prerequisite was learned (In leaner_log) -> add learning_path this semester
    ### Case 2: Subject prerequisite was recommend (Not in unlearned_course) -> add learning_path next semester
    english_course = get_english_course_level(course.course_code)

    if course.prerequisites and english_level >= english_course:
        check_log_in_learner_log = False
        for log in leaner_log:
            if log.course == course.prerequisites:
                # add_course_to_learning_path_with_english(course, english_course, unlearned_course)
                add_course_to_learning_path(course, unlearned_course)
                check_log_in_learner_log = True
                break
        if not check_log_in_learner_log:
            # add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_course) 
            add_course_to_learning_path_in_case_prerequisite_unlearned(course, unlearned_course)
    
    ### Check English
    if not course.prerequisites and english_level < english_course:
        add_course_to_learning_path_with_english(course, english_course, unlearned_course)
    
    ### Check subject prerequisite and English
    if course.prerequisites and english_level < english_course:
        check_log_in_learner_log = False
        for log in leaner_log:
            if log.course == course.prerequisites:
                add_course_to_learning_path_with_english(course, english_course, unlearned_course)
                check_log_in_learner_log = True
                break
        if not check_log_in_learner_log:
            add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_course) 
        # if course.prerequisites in leaner_log:
        #     add_course_to_learning_path_with_english(course, english_course, unlearned_course)
        # else:
        #     add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_course)
    
    if not course.prerequisites and english_level >= english_course:
        add_course_to_learning_path(course, unlearned_course)
            
def next_semester(semester):
    if semester%10 == 1:
        return semester + 1
    if semester%10 == 2:
        global learn_summer_semester
        if learn_summer_semester:
            if semester + 1 in [int(semester["semester"]) for semester in summer_semester]:
                return semester + 1
        return semester + 10 - 1
    if semester%10 == 3:
        return semester + 10 - 2
     
def get_english_course_level(course_code):
    if  course_code == "DATH":
        return 3
    if course_code == "DADN":
        return 3
    if course_code in ["TCTD1", "TCTD2", "TCTD3"]:
        return 1
    return int(course_code[2])
            
def add_course_to_learning_path_in_case_prerequisite_learned(course, unlearned_course):
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_course
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    global credit_in_semester
    global main_semester
    global summer_semester
    added_course = False
    for element in learning_path:
        credit = credit_in_semester
        if int(element.semester) % 10 != 3:
            for semester in main_semester:
                if element.semester == int(semester["semester"]):
                   credit = int(semester["credit"])
        else:
            for semester in summer_semester:
                if element.semester == int(semester["semester"]):
                    credit = int(semester["credit"])
        if element.credit + course.credit <= credit:
            element.courses.append(course)
            added_course = True
            element.credit = element.credit + course.credit
            for course_element in unlearned_course:
                if course_element == course:
                    unlearned_course.remove(course)
                    break
            break
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        unlearned_course.remove(course)
        
def add_course_to_learning_path_in_case_prerequisite_unlearned(course, unlearned_course):
    ### Find semester has prerequisite
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_course
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    global credit_in_semester
    global main_semester
    global summer_semester
    added_course = False
    num_prerequisite = 1
    
    for element in learning_path:
        if num_prerequisite != 0:
            for element_course in element.courses:
                if element_course == course.prerequisites:
                    num_prerequisite = num_prerequisite - 1
        else:
            credit = credit_in_semester
            if int(element.semester) % 10 != 3:
                for semester in main_semester:
                    if element.semester == int(semester["semester"]):
                        credit = int(semester["credit"])
            else:
                for semester in summer_semester:
                    if element.semester == int(semester["semester"]):
                        credit = int(semester["credit"])
            if element.credit + course.credit <= credit:
                element.courses.append(course)
                added_course = True
                element.credit = element.credit + course.credit
                for course_element in unlearned_course:
                    if course_element == course:
                        unlearned_course.remove(course)
                        break
                break
            
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        unlearned_course.remove(course)
        
def add_course_to_learning_path_with_english(course, english_course, unlearned_course):
    ### Find semester has english_course
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_course
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    global credit_in_semester
    global main_semester
    global summer_semester
    find_english_course = False
    added_course = False
    if english_course == 1:
        english_course = "Anh văn 1"
    if english_course == 2:
        english_course = "Anh văn 2"
    if english_course == 3:
        english_course = "Anh văn 3"
    if english_course == 4:
        english_course = "Anh văn 4"
    for element in learning_path:
        if not find_english_course:
            for element_course in element.courses:
                if element_course.course_name == english_course:
                    find_english_course = True
                    break
        else:
            credit = credit_in_semester
            if int(element.semester) % 10 != 3:
                for semester in main_semester:
                    if element.semester == int(semester["semester"]):
                        credit = int(semester["credit"])
            else:
                for semester in summer_semester:
                    if element.semester == int(semester["semester"]):
                        credit = int(semester["credit"])
            if element.credit + course.credit <= credit:
                element.courses.append(course)
                added_course = True
                element.credit = element.credit + course.credit
                for course_element in unlearned_course:
                    if course_element == course:
                        unlearned_course.remove(course)
                        break
                break
            
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        unlearned_course.remove(course)
        
def add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_course):
    ### Find semester has prerequisite and english
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_course
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    global credit_in_semester
    global main_semester
    global summer_semester
    num_prerequisite = 1
    find_english_course = False
    added_course = False
    if english_course == 1:
        english_course = "Anh văn 1"
    if english_course == 2:
        english_course = "Anh văn 2"
    if english_course == 3:
        english_course = "Anh văn 3"
    if english_course == 4:
        english_course = "Anh văn 4"
    for element in learning_path:
        if num_prerequisite != 0 or not find_english_course:
            for element_course in element.courses:
                if element_course == course.prerequisites:
                    num_prerequisite = num_prerequisite - 1
                if element_course.course_name == english_course:
                    find_english_course = True
                if find_english_course and num_prerequisite == 0:
                    break    
        else:
            credit = credit_in_semester
            if int(element.semester) % 10 != 3:
                for semester in main_semester:
                    if element.semester == int(semester["semester"]):
                        credit = int(semester["credit"])
            else:
                for semester in summer_semester:
                    if element.semester == int(semester["semester"]):
                        credit = int(semester["credit"])
            if element.credit + course.credit <= credit:
                element.courses.append(course)
                added_course = True
                element.credit = element.credit + course.credit
                for course_element in unlearned_course:
                    if course_element == course:
                        unlearned_course.remove(course)
                        break
                break
            
    if not added_course:
        global current_semester
        current_semester = next_semester(learning_path[-1].semester)
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = course.credit
        learning_path.append(learning_path_element)
        unlearned_course.remove(course)
        
def add_course_to_learning_path(course, unlearned_course):
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_course
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    global credit_in_semester
    global main_semester
    global summer_semester
    added_course = False
    for element in learning_path:
        credit = credit_in_semester
        if int(element.semester) % 10 != 3:
            for semester in main_semester:
                if int(element.semester) == int(semester["semester"]):
                    credit = int(semester["credit"])
        else:
            for semester in summer_semester:
                if element.semester == int(semester["semester"]):
                    credit = int(semester["credit"])
        
        if element.credit + course.credit <= credit:
            element.courses.append(course)
            added_course = True
            element.credit = element.credit + course.credit
            for course_element in unlearned_course:
                if course_element == course:
                    unlearned_course.remove(course)
                    break
            break
            
    if not added_course:
        global current_semester
        if len(learning_path) == 0:
            learning_path_element = LearningPathElement(current_semester)
            learning_path_element.courses.append(course)
            learning_path_element.credit = course.credit
            learning_path.append(learning_path_element)
        else:
            current_semester = next_semester(current_semester)
            learning_path_element = LearningPathElement(current_semester)
            learning_path_element.courses.append(course)
            learning_path_element.credit = course.credit
            learning_path.append(learning_path_element)
        unlearned_course.remove(course)

# learning_path = []
# current_semester = 0
# course_group_c = []
# num_course_group_c = 0
# num_course_group_d = 0
# learn_summer_semester = False
# total_course_group_c = 0
# credit_in_semester = 18
# min_credit_in_semester = 11
# learned_course = []
# main_semester = []
# summer_semester = []

# class LearningPathElement:
#     def __init__(self, semester):
#         self.semester = semester
#         self.courses = []
#         self.credit = 0
        
#     def to_dict(self):
#         return {
#             "semester": self.semester,
#             "courses": [
#                 {
#                     "course_id": course.course_id,
#                     "course_code": course.course_code,
#                     "course_name": course.course_name,
#                     "credit": course.credit,
#                     **({"predict_score": course.predict_score} if course.course_name != "Tự chọn tự do" else {}),
#                     "note": course.note,
#                 }
#                 for course in self.courses
#             ],
#             "total_credit": self.credit,
#         }

        
# def recommend(learner, learner_log, unlearned_course, course_graph, semester):
#     global learning_path
#     global current_semester
#     global course_group_c
#     global num_course_group_c
#     global num_course_group_d
#     global learn_summer_semester
#     global total_course_group_c
#     global credit_in_semester
#     global learned_course
#     global main_semester
#     global summer_semester
#     global min_credit_in_semester
    
#     learning_path = []
#     current_semester = 0
#     course_group_c = []
#     num_course_group_c = 0
#     num_course_group_d = 0
#     learn_summer_semester = False
#     total_course_group_c = 0
#     credit_in_semester = 18
#     main_semester = []
#     summer_semester = []
#     min_credit_in_semester = 11
    
#     ### Caculate number of course group c
#     for course in unlearned_course:
#         if course.is_group_c == True:
#             total_course_group_c = total_course_group_c + 1
      
#     if learner["over_learn"] == "1":
#         main_semester = learner["main_semester"]
        
#     if learner["learn_summer_semester"] == "1":
#         learn_summer_semester = True
#         summer_semester = learner["summer_semester"]
        
#     num_course_group_c = 5 + 3 - int(learner["course_free_elective"])
#     if num_course_group_c > total_course_group_c:
#         return "Môn nhóm C không đủ"
#     current_semester = semester
#     add_english_course_to_learning_path(learner_log, unlearned_course)
#     travel_course_graph(learner, learner_log, unlearned_course, course_graph)
#     if learner["learn_to_improve"] == "1":
#         learned_course = sorted(learned_course, key=lambda course: course.predict_score)
#         for semester in learning_path:
#             if int(semester.semester)%10 == 3:
#                 continue
#             if semester.credit<min_credit_in_semester:
#                 for course in learned_course:
#                     if int(semester.credit) + int(course.credit) <= credit_in_semester:
#                         semester.courses.append(course)
#                         learned_course.remove(course)
#                         semester.credit = semester.credit + course.credit
#                         if semester.credit >= min_credit_in_semester:
#                             break
#     return learning_path
    
# ### Add english 
# ### Travel course and add new course to learning_path
# ### Step 1: if it is not course not ---> recursive
# ### Step 2: if it is course node ---> check is_subject_learned
# ### Step 3: Check prerequisite
# def travel_course_graph(learner, learner_log, unlearned_course, course_graph):
#     global course_group_c
#     global num_course_group_c
#     global num_course_group_d
#     global learned_course
    
#     if course_graph.is_course == False:
#         for child_node in course_graph.children:
#             travel_course_graph(learner, learner_log, unlearned_course, child_node)
#     else:
#         # print(course_graph.course_node.course_name)
#         if is_subject_learned(course_graph.course_node, learner_log, unlearned_course):
#             learned_course.append(course_graph.course_node)
#             if course_graph.course_node.is_group_c == True:
#                 course_group_c.append(course_graph.course_node)
#         else:
#             # Check group c
#             if course_graph.course_node.is_group_c == True and len(course_group_c) == num_course_group_c:
#                 return
            
#             # Check group d
#             if course_graph.course_node.is_group_d == True and num_course_group_d < 4:
#                 num_course_group_d = num_course_group_d + 1
#                 return
#             elif course_graph.course_node.is_group_d == True and num_course_group_d == 4:
#                 course_graph.course_node.course_name = "Tín chỉ tự chọn nhóm D"
#                 check_prerequisite_and_add_learning_path(int(learner["english_level"]), course_graph.course_node, learner_log, unlearned_course)
#                 return
            
#             # Check free elective course
#             if course_graph.course_node.course_code in ["TCTD1", "TCTD2", "TCTD3"]:
#                 if int(learner["course_free_elective"]) > 0:
#                     learner["course_free_elective"] = int(learner["course_free_elective"]) - 1
#                     check_prerequisite_and_add_learning_path(int(learner["english_level"]), course_graph.course_node, learner_log, unlearned_course)
#                 return
            
#             check_prerequisite_and_add_learning_path(int(learner["english_level"]), course_graph.course_node, learner_log, unlearned_course)
#             if course_graph.course_node.is_group_c == True and course_graph.course_node not in course_group_c:
#                 course_group_c.append(course_graph.course_node)
                
# def add_english_course_to_learning_path(learner_log, unlearned_course):
#     global learning_path
#     english_course_name = ["Anh văn 1", "Anh văn 2", "Anh văn 3", "Anh văn 4"]
#     english_uncourse = []
#     for course in unlearned_course:
#         if course.course_name in english_course_name:
#             english_uncourse.append(course)
#             unlearned_course.remove(course)
   
#     for log in learner_log:
#         if log.course.course_name in english_course_name:
#             english_uncourse.remove(log.course)
       
#     for course in english_uncourse:
#         global current_semester
#         learning_path_element = LearningPathElement(current_semester)
#         learning_path_element.courses.append(course)
#         learning_path_element.credit = 2
#         learning_path.append(learning_path_element)
#         current_semester = next_semester(current_semester)
        
# ### If course was learned, remove it unlearned_course
# def is_subject_learned(course, learner_log, unlearned_course):
#     if course.course_code in ["LA1003", "LA1005", "LA1007", "LA1009"]:
#         return True
#     for log in learner_log:
#         if log.course.course_code == course.course_code:
#             unlearned_course.remove(course)
#             return True
#     return False
    
# def check_prerequisite_and_add_learning_path(english_level, course, leaner_log, unlearned_course):
#     ### Chech subject prerequisite
#     ### If this course has subject prerequisite: 2 cases
#     ### Case 1: Subject prerequisite was learned (In leaner_log) -> add learning_path this semester
#     ### Case 2: Subject prerequisite was recommend (Not in unlearned_course) -> add learning_path next semester
#     english_course = get_english_course_level(course.course_code)
#     if course.prerequisites and english_level >= english_course:
#         if course.prerequisites in leaner_log:
#             add_course_to_learning_path_in_case_prerequisite_learned(course, unlearned_course)
#         else:
#             add_course_to_learning_path_in_case_prerequisite_unlearned(course, unlearned_course)
    
#     ### Check English
#     if not course.prerequisites and english_level < english_course:
#         add_course_to_learning_path_with_english(course, english_course, unlearned_course)
    
#     ### Check subject prerequisite and English
#     if course.prerequisites and english_level < english_course:
#         if course.prerequisites in leaner_log:
#             add_course_to_learning_path_with_english(course, english_course, unlearned_course)
#         else:
#             add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_course)
    
#     if not course.prerequisites and english_level >= english_course:
#         add_course_to_learning_path(course, unlearned_course)
            
# def next_semester(semester):
#     if semester%10 == 1:
#         return semester + 1
#     if semester%10 == 2:
#         global learn_summer_semester
#         if learn_summer_semester:
#             if semester + 1 in [int(semester["semester"]) for semester in summer_semester]:
#                 return semester + 1
#         return semester + 10 - 1
#     if semester%10 == 3:
#         return semester + 10 - 2
     
# def get_english_course_level(course_code):
#     if  course_code == "DATH":
#         return 3
#     if course_code == "DADN":
#         return 3
#     if course_code in ["TCTD1", "TCTD2", "TCTD3"]:
#         return 1
#     return int(course_code[2])
            
# def add_course_to_learning_path_in_case_prerequisite_learned(course, unlearned_course):
#     ### Add any semester has total credit <= 18
#     ### After add successfull, remove this course from unlearned_course
#     ### If not any semester can add, create new node and add course to this new node
#     global learning_path
#     global credit_in_semester
#     global main_semester
#     global summer_semester
#     added_course = False
#     for element in learning_path:
#         credit = credit_in_semester
#         if int(element.semester) % 10 != 3:
#             for semester in main_semester:
#                 if element.semester == int(semester["semester"]):
#                    credit = int(semester["credit"])
#         else:
#             for semester in summer_semester:
#                 if element.semester == int(semester["semester"]):
#                     credit = int(semester["credit"])
#         if element.credit + course.credit <= credit:
#             element.courses.append(course)
#             added_course = True
#             element.credit = element.credit + course.credit
#             for course_element in unlearned_course:
#                 if course_element == course:
#                     unlearned_course.remove(course)
#                     break
#             break
#     if not added_course:
#         global current_semester
#         current_semester = next_semester(learning_path[-1].semester)
#         learning_path_element = LearningPathElement(current_semester)
#         learning_path_element.courses.append(course)
#         learning_path_element.credit = course.credit
#         learning_path.append(learning_path_element)
#         unlearned_course.remove(course)
        
# def add_course_to_learning_path_in_case_prerequisite_unlearned(course, unlearned_course):
#     ### Find semester has prerequisite
#     ### Add any semester has total credit <= 18
#     ### After add successfull, remove this course from unlearned_course
#     ### If not any semester can add, create new node and add course to this new node
#     global learning_path
#     global credit_in_semester
#     global main_semester
#     global summer_semester
#     added_course = False
#     num_prerequisite = 1
    
#     for element in learning_path:
#         if num_prerequisite != 0:
#             for element_course in element.courses:
#                 if element_course == course.prerequisites:
#                     num_prerequisite = num_prerequisite - 1
#         else:
#             credit = credit_in_semester
#             if int(element.semester) % 10 != 3:
#                 for semester in main_semester:
#                     if element.semester == int(semester["semester"]):
#                         credit = int(semester["credit"])
#             else:
#                 for semester in summer_semester:
#                     if element.semester == int(semester["semester"]):
#                         credit = int(semester["credit"])
#             if element.credit + course.credit <= credit:
#                 element.courses.append(course)
#                 added_course = True
#                 element.credit = element.credit + course.credit
#                 for course_element in unlearned_course:
#                     if course_element == course:
#                         unlearned_course.remove(course)
#                         break
#                 break
            
#     if not added_course:
#         global current_semester
#         current_semester = next_semester(learning_path[-1].semester)
#         learning_path_element = LearningPathElement(current_semester)
#         learning_path_element.courses.append(course)
#         learning_path_element.credit = course.credit
#         learning_path.append(learning_path_element)
#         unlearned_course.remove(course)
        
# def add_course_to_learning_path_with_english(course, english_course, unlearned_course):
#     ### Find semester has english_course
#     ### Add any semester has total credit <= 18
#     ### After add successfull, remove this course from unlearned_course
#     ### If not any semester can add, create new node and add course to this new node
#     global learning_path
#     global credit_in_semester
#     global main_semester
#     global summer_semester
#     find_english_course = False
#     added_course = False
#     if english_course == 1:
#         english_course = "Anh văn 1"
#     if english_course == 2:
#         english_course = "Anh văn 2"
#     if english_course == 3:
#         english_course = "Anh văn 3"
#     if english_course == 4:
#         english_course = "Anh văn 4"
#     for element in learning_path:
#         if not find_english_course:
#             for element_course in element.courses:
#                 if element_course.course_name == english_course:
#                     find_english_course = True
#                     break
#         else:
#             credit = credit_in_semester
#             if int(element.semester) % 10 != 3:
#                 for semester in main_semester:
#                     if element.semester == int(semester["semester"]):
#                         credit = int(semester["credit"])
#             else:
#                 for semester in summer_semester:
#                     if element.semester == int(semester["semester"]):
#                         credit = int(semester["credit"])
#             if element.credit + course.credit <= credit:
#                 element.courses.append(course)
#                 added_course = True
#                 element.credit = element.credit + course.credit
#                 for course_element in unlearned_course:
#                     if course_element == course:
#                         unlearned_course.remove(course)
#                         break
#                 break
            
#     if not added_course:
#         global current_semester
#         current_semester = next_semester(learning_path[-1].semester)
#         learning_path_element = LearningPathElement(current_semester)
#         learning_path_element.courses.append(course)
#         learning_path_element.credit = course.credit
#         learning_path.append(learning_path_element)
#         unlearned_course.remove(course)
        
# def add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_course):
#     ### Find semester has prerequisite and english
#     ### Add any semester has total credit <= 18
#     ### After add successfull, remove this course from unlearned_course
#     ### If not any semester can add, create new node and add course to this new node
#     global learning_path
#     global credit_in_semester
#     global main_semester
#     global summer_semester
#     num_prerequisite = 1
#     find_english_course = False
#     added_course = False
#     if english_course == 1:
#         english_course = "Anh văn 1"
#     if english_course == 2:
#         english_course = "Anh văn 2"
#     if english_course == 3:
#         english_course = "Anh văn 3"
#     if english_course == 4:
#         english_course = "Anh văn 4"
#     for element in learning_path:
#         if num_prerequisite != 0 or not find_english_course:
#             for element_course in element.courses:
#                 if element_course == course.prerequisites:
#                     num_prerequisite = num_prerequisite - 1
#                 if element_course.course_name == english_course:
#                     find_english_course = True
#                 if find_english_course and num_prerequisite == 0:
#                     break    
#         else:
#             credit = credit_in_semester
#             if int(element.semester) % 10 != 3:
#                 for semester in main_semester:
#                     if element.semester == int(semester["semester"]):
#                         credit = int(semester["credit"])
#             else:
#                 for semester in summer_semester:
#                     if element.semester == int(semester["semester"]):
#                         credit = int(semester["credit"])
#             if element.credit + course.credit <= credit:
#                 element.courses.append(course)
#                 added_course = True
#                 element.credit = element.credit + course.credit
#                 for course_element in unlearned_course:
#                     if course_element == course:
#                         unlearned_course.remove(course)
#                         break
#                 break
            
#     if not added_course:
#         global current_semester
#         current_semester = next_semester(learning_path[-1].semester)
#         learning_path_element = LearningPathElement(current_semester)
#         learning_path_element.courses.append(course)
#         learning_path_element.credit = course.credit
#         learning_path.append(learning_path_element)
#         unlearned_course.remove(course)
        
# def add_course_to_learning_path(course, unlearned_course):
#     ### Add any semester has total credit <= 18
#     ### After add successfull, remove this course from unlearned_course
#     ### If not any semester can add, create new node and add course to this new node
#     global learning_path
#     global credit_in_semester
#     global main_semester
#     global summer_semester
#     added_course = False
#     for element in learning_path:
#         credit = credit_in_semester
#         if int(element.semester) % 10 != 3:
#             for semester in main_semester:
#                 if element.semester == int(semester["semester"]):
#                     credit = int(semester["credit"])
#         else:
#             for semester in summer_semester:
#                 if element.semester == int(semester["semester"]):
#                     credit = int(semester["credit"])
#         if element.credit + course.credit <= credit:
#             element.courses.append(course)
#             added_course = True
#             element.credit = element.credit + course.credit
#             for course_element in unlearned_course:
#                 if course_element == course:
#                     unlearned_course.remove(course)
#                     break
#             break
            
#     if not added_course:
#         global current_semester
#         if len(learning_path) == 0:
#             learning_path_element = LearningPathElement(current_semester)
#             learning_path_element.courses.append(course)
#             learning_path_element.credit = course.credit
#             learning_path.append(learning_path_element)
#         else:
#             current_semester = next_semester(current_semester)
#             learning_path_element = LearningPathElement(current_semester)
#             learning_path_element.courses.append(course)
#             learning_path_element.credit = course.credit
#             learning_path.append(learning_path_element)
#         unlearned_course.remove(course)