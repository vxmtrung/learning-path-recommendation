from group_course.models import GroupCourse
from group_rule.models import GroupRule
def map_group_rule():
    group_course = GroupCourse.objects.filter(is_active=True)
    for group in group_course:
        rules = GroupRule.objects.filter(group=group)
        for rule in rules:
            if rule.rule.rule_code == "group_completion_rule":	
                group.total_course = int(rule.parameter['total'])
                group.minimum_course = int(rule.parameter['minimum'])
            elif rule.rule.rule_code == "alternative_rule":
                group.alternative = rule.parameter['alternative']
                if rule.parameter['alternative']:
                    group.alternative_group = GroupCourse.objects.get(group_course_code=rule.parameter['group_alternative'])
                else:
                    group.alternative_group = None
            elif rule.rule.rule_code == "mandatory_rule":
                group.mandatory = rule.parameter['mandatory']
            elif rule.rule.rule_code == "specifically_rule":
                group.specifically = rule.parameter['specifically']
    
    return group_course
