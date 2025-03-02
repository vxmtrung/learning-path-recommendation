from courses.models import Course
from .course_node import CourseNode

def create_course_tree(course_list):
    # Initialize root node
    init_course_node = Course(
        course_id="Semester1",
        course_code="Semester1",
        course_name="Semester 1",
        semester=None,
        count_learner=None,
        average_score=None,
        credit=None,
        note=None,
        description=None
    )
    root = CourseNode(init_course_node, False)

    current_semester = 1
    current_node = root
    
    # Travel Sorted_Courses to create Course Tree
    # Node semester n contains the subjects belonging to semester n and node semester n+1
    for course in course_list:
        # If subject belonging other semester, create new node semester and add this node to new node semester
        if course.semester > current_semester:
            current_semester = course.semester
            
            # Create new node semester
            new_course_semester = Course(
                course_id=f'Semester{current_semester}',
                course_code=f'Semester{current_semester}',
                course_name=f'Semester {current_semester}',
                semester=None,
                count_learner=None,
                average_score=None,
                credit=None,
                note=None,
                description=None
            )
            new_node = CourseNode(new_course_semester, False)
            current_node.add_child(new_node)
            current_node = current_node.get_last_child()
            
            # Add this course to new node semeter
            new_course_node = CourseNode(course, True)
            current_node.add_child(new_course_node)
        else:
            # Add this course to current node semeter
            new_course_node = CourseNode(course, True)
            current_node.add_child(new_course_node)

    return root

def print_tree(node, level=0):
    indent = "  " * level
    print(f"{indent}{node.course_node.course_name}")
    for child in node.children:
        print_tree(child, level + 1)