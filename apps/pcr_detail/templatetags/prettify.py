from __future__ import division
import re

from django import template


register = template.Library()

# review attributes, ordered left-to-right
ATTRIBUTES = (
    # general
    u"rCourseQuality",
    u"rInstructorQuality",
    u"rDifficulty",

    # class

    u"rAmountLearned",
    u"rWorkRequired",
    u"rReadingsValue",

    u"rHomeworkValuable",
    u"rExamsConsistent",
    u"rAbilitiesChallenged",
    u"rSkillEmphasis",

    # instructor

    u"rCommAbility",
    u"rInstructorAccess",
    u"rStimulateInterest",
    u"rArticulateGoals",

    u"rInstructorConcern",
    u"rInstructorRapport",
    u"rInstructorAttitude",
    u"rInstructorEffective",

    u"rOralSkills",
    u"rGradeFairness",
    u"rNativeAbility",
    u"rClassPace",

    u"rTAQuality",

    u"rRecommendMajor",
    u"rRecommendNonMajor"
)


PRETTIFY_REVIEWBITS = {
    u"rInstructorQuality": "Instructor Quality",
    u"rCourseQuality": "Course Quality",
    u"rDifficulty": "Difficulty",
    u"rCommAbility": "Instructor Communication",
    u"rInstructorAccess": "Instructor Accessibility",
    u"rReadingsValue": "Value of Readings",
    u"rAmountLearned": "Amount Learned",
    u"rWorkRequired": "Amount of Work",
    u"rRecommendMajor": "Recommend for Majors",
    u"rRecommendNonMajor": "Recommend for Non-Majors",
    u"rStimulateInterest": "Ability to Stimulate Interest",
    u"rArticulateGoals": "Ability to Articulate Goals",
    u"rSkillEmphasis": "Skill Emphasis",
    u"rHomeworkValuable": "Value of Homework",
    u"rExamsConsistent": "Exams Consistent",
    u"rAbilitiesChallenged": "Abilities Challenged",
    u"rClassPace": "Class Pace",
    u"rOralSkills": "Oral Skills",
    u"rInstructorConcern": "Instructor Concern",
    u"rInstructorRapport": "Instructor Rapport",
    u"rInstructorAttitude": "Instructor Attitude",
    u"rInstructorEffective": "Instructor Effectiveness",
    u"rGradeFairness": "Grade Fairness",
    u"rNativeAbility": "Native Ability",
    u"rTAQuality": "TA Quality"
}


@register.filter(name='reviewbit')
def reviewbit(reviewbit):
    try:
        return PRETTIFY_REVIEWBITS[reviewbit]
    except KeyError:
        return reviewbit


@register.filter(name='get_alias')
def get_alias(coursehistory, instructor):
    return coursehistory.alias(instructor)


@register.filter(name="columns")
def attributes(reviews):
    for attribute in ATTRIBUTES:
        for review in reviews:
            if attribute in review.ratings:
                yield attribute
                break


@register.filter(name="sectionname")
def sectionname(reviews):
    names = set(review.section.name.strip() for review in reviews)
    if len(names) > 1:
        return "Various"
    else:
        return names.pop()

@register.filter(name="sectionnameall")
def sectionnameall(reviews):
    names = [review.section.name.strip() for review in reviews]
    return ", ".join(names)


@register.filter(name='recent')
def recent(reviews):
    try:
        most_recent = max([r.section.course.semester for r in reviews])
        recent_courses = [
            r for r in reviews if r.section.course.semester == most_recent]
        return recent_courses
    except ValueError:
        return ""


@register.filter(name='average')
def average(reviews, attribute):
    average = 0.0
    valid = 0
    for review in reviews:
        try:
            average += review.ratings[attribute]
            valid += 1
        except KeyError:
            continue
    try:
        return average / valid
    except ZeroDivisionError:
        return ""


@register.filter(name='rating_class')
def rating_class(score):
    if isinstance(score, str):
        return ""
    score = round(score, 1)
    if score < 2:
        return "rating-bad"
    elif score < 3:
        return "rating-okay"
    else:
        return "rating-good"


PRETTIFY_SEMESTER = {
    "A": "Spring",
    "B": "Summer",
    "C": "Fall"
}


@register.filter(name='semester')
def semester(semester):
    try:
        return "%s %s" % (PRETTIFY_SEMESTER[semester[-1]], semester[:-1])
    except IndexError:
        return semester
    except KeyError:
        return semester


@register.filter(name='no_hyphen')
def no_hyphen(title):
    return title.replace("-", " ")


@register.filter(name='subtitle')
def subtitle(coursehistory):
    names = set(
        section.name for course in coursehistory.courses for section in course.sections)
    if len(names - set(["RECITATATION", "Recitation", "LECTURE", "Lecture"])) > 1:
        return "(Recent Title) %s" % coursehistory.name
    else:
        return coursehistory.name


# NOTE: Find another way to do this if possible.
@register.filter(name="get")
def get(item, arg):
    try:
        return getattr(item, arg)
    except AttributeError:
        try:
            return item.get(arg)
        except AttributeError:
            return ""
        except KeyError:
            return ""


@register.filter(name="capitalize_improved")
def capitalize(name):
    """Capitalize but account for roman numerals, so no "Calculus Iii" """
    # split into words, punctuation, and whitespace
    tokens = re.findall(r"(\w+|[\s.,?&/:\(\)]+)", name)
    roman_numerals = set(['I', 'II', 'III', 'IV'])

    def cap_word(word):
        return word.upper() if word.upper() in roman_numerals else word.capitalize()
    return "".join(cap_word(token) for token in tokens)


@register.filter(name="format_comment")
def format_comment(comment):
    return (comment or "").replace("\n", "<br />")
