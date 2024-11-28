from courses.models import Course

learning_path = []
current_semester = 0
course_group_c = []
num_course_group_c = 0
num_course_group_d = 0
learn_summer_semester = False
credit_summer_semester = 0
total_course_group_c = 0
credit_in_semester = 0
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
                    "course_name": course.course_name,
                    "credit": course.credit,
                    **({"predict_score": course.predict_score} if course.course_name != "Tự chọn tự do" else {}),
                    "note": course.note,
                }
                for course in self.courses
            ],
            "total_credit": self.credit,
        }

        
def recommend(learner, learner_log, unlearned_course, course_graph, semester):
    global learning_path
    global current_semester
    global course_group_c
    global num_course_group_c
    global num_course_group_d
    global learn_summer_semester
    global credit_summer_semester
    global total_course_group_c
    global credit_in_semester
    
    learning_path = []
    current_semester = 0
    course_group_c = []
    num_course_group_c = 0
    num_course_group_d = 0
    learn_summer_semester = False
    credit_summer_semester = 0
    total_course_group_c = 0
    credit_in_semester = 0
    
    if learner["over_learn"] == True:
        credit_in_semester = learner["over_learn_credit"]
    else:
        credit_in_semester = 18
    ### Caculate number of course group c
    for course in unlearned_course:
        if course.is_group_c == True:
            total_course_group_c = total_course_group_c + 1
            
    if learner["learn_summer_semester"] == True:
        learn_summer_semester = True
        credit_summer_semester = int(learner["credit_summer_semester"])
    num_course_group_c = 5 + 3 - int(learner["course_free_elective"])
    if num_course_group_c > total_course_group_c:
        return "Môn nhóm C không đủ"
    current_semester = semester
    add_english_course_to_learning_path(learner_log, unlearned_course)
    travel_course_graph(learner, learner_log, unlearned_course, course_graph)
    # learner_log = sorted(learner_log, key=lambda log: log.score)
    # global learning_path
    # for semester in learning_path:
    #     if int(semester.semester)%10 == 3:
    #         continue
    #     if semester.credit<14:
    #         for log in learner_log:
    #             if int(semester.credit) + int(log.credit) <= 18:
    #                 semester.courses.append(log)
    #                 learner_log.remove(log)
    #                 semester.credit = semester.credit + log.credit
    #                 if semester.credit >= 14:
    #                     break
    return learning_path
    
### Add english 
### Travel course and add new course to learning_path
### Step 1: if it is not course not ---> recursive
### Step 2: if it is course node ---> check is_subject_learned
### Step 3: Check prerequisite
def travel_course_graph(learner, learner_log, unlearned_course, course_graph):
    global course_group_c
    global num_course_group_c
    global num_course_group_d
      
    if course_graph.is_course == False:
        for child_node in course_graph.children:
            travel_course_graph(learner, learner_log, unlearned_course, child_node)
    else:
        if is_subject_learned(course_graph.course_node, learner_log, unlearned_course):
            if course_graph.course_node.is_group_c == True:
                course_group_c.append(course_graph.course_node)
        else:
            # Check group c
            if course_graph.course_node.is_group_c == True and len(course_group_c) == num_course_group_c:
                return
            
            # Check group d
            if course_graph.course_node.is_group_d == True and num_course_group_d < 4:
                num_course_group_d = num_course_group_d + 1
                return
            elif course_graph.course_node.is_group_d == True and num_course_group_d == 4:
                course_graph.course_node.course_name = "Tín chỉ tự chọn nhóm D"
                check_prerequisite_and_add_learning_path(int(learner["english_level"]), course_graph.course_node, learner_log, unlearned_course)
                return
            
            # Check free elective course
            if course_graph.course_node.course_id in ["TCTD1", "TCTD2", "TCTD3"]:
                if int(learner["course_free_elective"]) > 0:
                    learner["course_free_elective"] = int(learner["course_free_elective"]) - 1
                    check_prerequisite_and_add_learning_path(int(learner["english_level"]), course_graph.course_node, learner_log, unlearned_course)
                return
            
            check_prerequisite_and_add_learning_path(int(learner["english_level"]), course_graph.course_node, learner_log, unlearned_course)
            if course_graph.course_node.is_group_c == True and course_graph.course_node not in course_group_c:
                course_group_c.append(course_graph.course_node)
                
def add_english_course_to_learning_path(learner_log, unlearned_course):
    global learning_path
    english_course_name = ["Anh văn 1", "Anh văn 2", "Anh văn 3", "Anh văn 4"]
    english_uncourse = []
    for course in unlearned_course:
        if course.course_name in english_course_name:
            english_uncourse.append(course)
            unlearned_course.remove(course)
   
    for log in learner_log:
        if log.course.course_name in english_course_name:
            english_uncourse.remove(log.course)
       
    for course in english_uncourse:
        global current_semester
        learning_path_element = LearningPathElement(current_semester)
        learning_path_element.courses.append(course)
        learning_path_element.credit = 2
        learning_path.append(learning_path_element)
        current_semester = next_semester(current_semester)
        
### If course was learned, remove it unlearned_course
def is_subject_learned(course, learner_log, unlearned_course):
    if course.course_id in ["LA1003", "LA1005", "LA1007", "LA1009"]:
        return True
    for log in learner_log:
        if log.course.course_id == course.course_id:
            unlearned_course.remove(course)
            return True
    return False
    
def check_prerequisite_and_add_learning_path(english_level, course, leaner_log, unlearned_course):
    ### Chech subject prerequisite
    ### If this course has subject prerequisite: 2 cases
    ### Case 1: Subject prerequisite was learned (In leaner_log) -> add learning_path this semester
    ### Case 2: Subject prerequisite was recommend (Not in unlearned_course) -> add learning_path next semester
    english_course = get_english_course_level(course.course_id)
    if course.prerequisites.exists() and english_level >= english_course:
        if course.prerequisites.first() in leaner_log:
            add_course_to_learning_path_in_case_prerequisite_learned(course, unlearned_course)
        else:
            add_course_to_learning_path_in_case_prerequisite_unlearned(course, unlearned_course)
    
    ### Check English
    if not course.prerequisites.exists() and english_level < english_course:
        add_course_to_learning_path_with_english(course, english_course, unlearned_course)
    
    ### Check subject prerequisite and English
    if course.prerequisites.exists() and english_level < english_course:
        if course.prerequisites.first() in leaner_log:
            add_course_to_learning_path_with_english(course, english_course, unlearned_course)
        else:
            add_course_to_learning_path_with_prerequisite_and_english(course, english_course, unlearned_course)
    
    if not course.prerequisites.exists() and english_level >= english_course:
        add_course_to_learning_path(course, unlearned_course)
            
def next_semester(semester):
    if semester%10 == 1:
        return semester + 1
    if semester%10 == 2:
        global learn_summer_semester
        if learn_summer_semester:
            return semester + 1
        return semester + 10 - 1
    if semester%10 == 3:
        return semester + 10 - 2
     
def get_english_course_level(course_id):
    if  course_id == "DATH":
        return 3
    if course_id == "DADN":
        return 3
    if course_id in ["TCTD1", "TCTD2", "TCTD3"]:
        return 1
    return int(course_id[2])
            
def add_course_to_learning_path_in_case_prerequisite_learned(course, unlearned_course):
    ### Add any semester has total credit <= 18
    ### After add successfull, remove this course from unlearned_course
    ### If not any semester can add, create new node and add course to this new node
    global learning_path
    global credit_in_semester
    added_course = False
    for element in learning_path:
        if element.credit + course.credit <= (int(credit_in_semester) if int(element.semester)%10 != 3 else int(credit_summer_semester)):
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
    added_course = False
    num_prerequisite = course.prerequisites.count()
    
    for element in learning_path:
        if num_prerequisite != 0:
            for element_course in element.courses:
                if element_course in course.prerequisites.all():
                    num_prerequisite = num_prerequisite - 1
        else:
            if element.credit + course.credit <= (int(credit_in_semester) if int(element.semester)%10 != 3 else int(credit_summer_semester)):
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
            if element.credit + course.credit <= (int(credit_in_semester) if int(element.semester)%10 != 3 else int(credit_summer_semester)):
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
    num_prerequisite = course.prerequisites.count()
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
                if element_course in course.prerequisites.all():
                    num_prerequisite = num_prerequisite - 1
                if element_course.course_name == english_course:
                    find_english_course = True
                if find_english_course and num_prerequisite == 0:
                    break    
        else:
            if element.credit + course.credit <= (int(credit_in_semester) if int(element.semester)%10 != 3 else int(credit_summer_semester)):
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
    added_course = False
    for element in learning_path:
        if element.credit + course.credit <= (int(credit_in_semester) if int(element.semester)%10 != 3 else int(credit_summer_semester)):
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