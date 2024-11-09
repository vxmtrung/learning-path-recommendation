class CourseNode:
    def __init__(self, course, is_course):
        self.course_node = course
        self.is_course = is_course
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_last_child(self):
        if self.children:
            return self.children[-1]
        return None