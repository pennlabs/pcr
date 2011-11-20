from django import template

from templatetag_sugar.parser import Variable
from templatetag_sugar.register import tag


register = template.Library()

ERROR = u"\u00A0" #empty strin

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


PRETTIFY_SEMESTER = { 
    "A": "Spring",
    "B": "Summer",
    "C": "Fall"
}


@register.filter(name='score')
def score(score):
  if score is None:
    return ERROR
  else:
    return "%.2f" % score


@register.filter(name='semester')
def semester(semester):
  try:
    return "%s %s" % (PRETTIFY_SEMESTER[semester[-1]], semester[:-1])
  except KeyError:
    return semester


@register.filter(name='no_hyphen')
def no_hyphen(title):
  return title.replace("-", " ")


@tag(register, [Variable])
def capitalize(name):
  """Capitalize but account for roman numerals, so no "Calculus Iii" """
  roman_numerals = set(['I', 'II', 'III', 'IV']) 
  def cap_word(word): 
    return word.upper() if word.upper() in roman_numerals else word.capitalize()
  return " ".join(cap_word(word) for word in name.split(" "))


@tag(register, [Variable])
def format_comment(comment):
  return (comment or "").replace("\n", "<br />")
