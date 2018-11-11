# Penn Course Review API overview #

*Version 2, 12/1/2012*

**Purpose**: This document (1) helps us write the API and (2) is used by API consumers to understand its functionality.

## Notes ##

This document borrows heavily from the original Penn Registrar Courses API documentation, of which this PCR API is a super-set.
Whenever we link to things, we link to the canonical alias for them. In general, things that use IDs (i.e., shorter things) are canonical. Everything is permanent unless we specify explicitly.

## Usage ##

The Penn Course Review API is a simple RESTful API to the data available on PennCourseReview.com. The easiest way to explain it is to look at some queries.

All queries should be of the form http://api.penncoursereview.com/v1/[query]?token=[token].  Results are returned as JSON Objects, which you should be able to turn into a dictionary in whatever language you are working with.

For the following examples, we'll be using the public token.  To make requests with the public access token, simply append the string "?token=public" to the end of each query.  For reference, a sample query might look like `http://api.penncoursereview.com/v1/coursehistories/CIS-120?token=public`.

## Departments ##

### List all academic departments at Penn ###

#### Request ####

`GET /depts`

#### Response ####

    {
      "result": {
         "values": [
            {
               "id": "AAMW", 
               "name": "", 
               "path": "/depts/aamw"
            }, 
            {
               "id": "ACCT", 
               "name": "ACCOUNTING", 
               "path": "/depts/acct"
            }, 
            {
               "id": "AFAM", 
               "name": "AFRO-AMERICAN STUDIES", 
               "path": "/depts/afam"
            }, 

            ...

         ],
      }
      "retrieved": "2012-09-13 01:18:18.234678", 
      "valid": true, 
      "version": "0.3"
    }
    
### List all coursehistories for a certain academic department ###

#### Request ####

`GET /depts/:dept`

#### Response ####

    {
      "result": {
          "coursehistories": [
             {
                "aliases": [
                   "ACCT-011"
                ], 
                "id": 1, 
                "name": "FINANCIAL ACCOUNTING", 
                "path": "/coursehistories/1"
             }, 
             {
                "aliases": [
                   "ACCT-012"
                ], 
                "id": 2, 
                "name": "MANAGERIAL  ACCOUNTING", 
                "path": "/coursehistories/2"
             }, 
            ...
          ], 
          "id": "ACCT", 
          "name": "ACCOUNTING", 
          "path": "/depts/acct", 
          "reviews": {
             "path": "/depts/acct/reviews"
          }
       }, 
       "retrieved": "2012-12-01 16:46:06.504405", 
       "valid": true, 
       "version": "0.3"
    }
    
### List all reviews for an academic department ###

#### Request ####

*(Note: not available with the public token)*

`GET /depts/:dept/reviews`

#### Response ####

    {
      "result": {
          "values": [
             {
                "comments": "", 
                "id": "1-001-1-JACK-TOPIOL", 
                "instructor": {
                   "first_name": "JACK", 
                   "id": "1-JACK-TOPIOL", 
                   "last_name": "TOPIOL", 
                   "name": "JACK TOPIOL", 
                   "path": "/instructors/1-JACK-TOPIOL"
                }, 
                "num_reviewers": 17, 
                "num_students": 21, 
                "path": "/courses/1/sections/001/reviews/1-JACK-TOPIOL", 
                "ratings": {
                   "rAmountLearned": "3.13", 
                   "rCommAbility": "2.81", 
                   "rCourseQuality": "3.00", 
                   "rDifficulty": "2.94", 
                   "rInstructorAccess": "2.81", 
                   "rInstructorQuality": "3.19", 
                   "rReadingsValue": "3.06", 
                   "rRecommendMajor": "3.25", 
                   "rRecommendNonMajor": "2.31", 
                   "rStimulateInterest": "2.75", 
                   "rWorkRequired": "2.50"
                }, 
                "section": {
                   "aliases": [
                      "ACCT-011-001"
                   ], 
                   "id": "1-001", 
                   "name": "FINANCIAL ACCOUNTING", 
                   "path": "/courses/1/sections/001", 
                   "primary_alias": "ACCT-011-001", 
                   "sectionnum": "001"
                }
             },
             ...
           ]
         },
       "retrieved": "2012-12-01 16:52:39.141708", 
       "valid": true, 
       "version": "0.3"
    }
    
## Instructors ##

### List all instructors ###

#### Request ####

`GET /instructors`

#### Response ####

    {
      "result": {
        "values": [
           {
              "depts": [
                 "ACCT"
              ], 
              "first_name": "JACK", 
              "id": "1-JACK-TOPIOL", 
              "last_name": "TOPIOL", 
              "name": "JACK TOPIOL", 
              "path": "/instructors/1-JACK-TOPIOL"
           }, 
           ...
        ]
      },
      "retrieved": "2012-09-13 01:34:41.497783", 
      "valid": true, 
      "version": "0.3"
    }
    
### List information for a specific instructor ###

#### Request ####

`GET /instructor/:instructor_id`

#### Response ####

    {
      "result": {
          "first_name": "MIDORI", 
          "id": "4856-MIDORI-MORRIS", 
          "last_name": "MORRIS", 
          "name": "MIDORI MORRIS", 
          "path": "/instructors/4856-MIDORI-MORRIS", 
          "reviews": {
             "path": "/instructors/4856-MIDORI-MORRIS/reviews", 
             "values": [
                {
                   "id": "17571-003-4856-MIDORI-MORRIS", 
                   "instructor": {
                      "first_name": "MIDORI", 
                      "id": "4856-MIDORI-MORRIS", 
                      "last_name": "MORRIS", 
                      "name": "MIDORI MORRIS", 
                      "path": "/instructors/4856-MIDORI-MORRIS"
                   }, 
                   "path": "/courses/17571/sections/003/reviews/4856-MIDORI-MORRIS", 
                   "section": {
                      "aliases": [
                         "JPAN-011-003"
                      ], 
                      "id": "17571-003", 
                      "name": "BEGINNING JAPANESE I", 
                      "path": "/courses/17571/sections/003", 
                      "primary_alias": "JPAN-011-003", 
                      "sectionnum": "003"
                   }
                },
                ...
             ]
          }, 
          "sections": {
             "path": "/instructors/4856-MIDORI-MORRIS/sections", 
             "values": [
                {
                   "aliases": [
                      "JPAN-011-003"
                   ], 
                   "id": "17571-003", 
                   "name": "BEGINNING JAPANESE I", 
                   "path": "/courses/17571/sections/003", 
                   "primary_alias": "JPAN-011-003", 
                   "sectionnum": "003"
                },
                ...
             ]
          }
       }, 
       "retrieved": "2012-12-01 17:22:50.636923", 
       "valid": true, 
       "version": "0.3"
    }
         
### List all sections for a specific instructor ###

#### Request ####

`GET /instructors/:instructor_id`

#### Response ####

    {
      "result": {
        "values": [
           {
              "aliases": [
                 "JPAN-011-003"
              ], 
              "courses": {
                 "aliases": [
                    "JPAN-011"
                 ], 
                 "id": 17571, 
                 "name": "BEGINNING JAPANESE I", 
                 "path": "/courses/17571", 
                 "primary_alias": "JPAN-011", 
                 "semester": "2009C"
              }, 
              "group": null, 
              "id": "17571-003", 
              "instructors": [
                 {
                    "first_name": "MIDORI", 
                    "id": "4856-MIDORI-MORRIS", 
                    "last_name": "MORRIS", 
                    "name": "MIDORI MORRIS", 
                    "path": "/instructors/4856-MIDORI-MORRIS"
                 }
              ], 
              "meetingtimes": [], 
              "name": "BEGINNING JAPANESE I", 
              "path": "/courses/17571/sections/003", 
              "primary_alias": "JPAN-011-003", 
              "reviews": {
                 "path": "/courses/17571/sections/003/reviews", 
                 "values": [
                    {
                       "id": "17571-003-4856-MIDORI-MORRIS", 
                       "instructor": {
                          "first_name": "MIDORI", 
                          "id": "4856-MIDORI-MORRIS", 
                          "last_name": "MORRIS", 
                          "name": "MIDORI MORRIS", 
                          "path": "/instructors/4856-MIDORI-MORRIS"
                       }, 
                       "path": "/courses/17571/sections/003/reviews/4856-MIDORI-MORRIS", 
                       "section": {
                          "aliases": [
                             "JPAN-011-003"
                          ], 
                          "id": "17571-003", 
                          "name": "BEGINNING JAPANESE I", 
                          "path": "/courses/17571/sections/003", 
                          "primary_alias": "JPAN-011-003", 
                          "sectionnum": "003"
                       }
                    }
                 ]
              }, 
              "sectionnum": "003"
           },
           ...
        ]
      }, 
      "retrieved": "2012-12-01 17:26:42.285606", 
      "valid": true, 
      "version": "0.3"
    }
    
### List reviews of all sections taught by instructor ###

#### Request ####

`GET /instructors/:instructor_id/reviews`

#### Response ####

    {
      "result": {
      "values": [
      {
        "comments": "", 
        "id": "17571-003-4856-MIDORI-MORRIS", 
        "instructor": {
           "first_name": "MIDORI", 
           "id": "4856-MIDORI-MORRIS", 
           "last_name": "MORRIS", 
           "name": "MIDORI MORRIS", 
           "path": "/instructors/4856-MIDORI-MORRIS"
        }, 
        "num_reviewers": 11, 
        "num_students": 12, 
        "path": "/courses/17571/sections/003/reviews/4856-MIDORI-MORRIS", 
        "ratings": {
           "rAbilitiesChallenged": "3.80", 
           "rArticulateGoals": "3.90", 
           "rClassPace": "2.60", 
           "rCourseQuality": "3.45", 
           "rExamsConsistent": "3.60", 
           "rGradeFairness": "3.40", 
           "rHomeworkValuable": "3.70", 
           "rInstructorAccess": "3.60", 
           "rInstructorAttitude": "3.60", 
           "rInstructorConcern": "3.40", 
           "rInstructorEffective": "2.80", 
           "rInstructorQuality": "3.27", 
           "rInstructorRapport": "3.20", 
           "rNativeAbility": "3.70", 
           "rOralSkills": "3.60", 
           "rReadingsValue": "3.50", 
           "rSkillEmphasis": "3.80", 
           "rStimulateInterest": "3.20", 
           "rTAQuality": "3.14", 
           "rWorkRequired": "2.30"
        }, 
        "section": {
           "aliases": [
              "JPAN-011-003"
           ], 
           "id": "17571-003", 
           "name": "BEGINNING JAPANESE I", 
           "path": "/courses/17571/sections/003", 
           "primary_alias": "JPAN-011-003", 
           "sectionnum": "003"
        }
      },
      ...
      "retrieved": "2012-12-01 17:34:13.986830", 
      "valid": true, 
      "version": "0.3"
    }
    
    
## Semesters ##

### List all semesters ###

#### Request ####

`GET /semesters`

#### Response ####

    {
      "result": {
        "values": [
            {
              "id": "2002A", 
              "name": "Spring 2002", 
              "path": "/semesters/2002a", 
              "seasoncode": "A", 
              "year": 2002
            },
            ...
        ]
      }, 
      "retrieved": "2012-12-05 16:53:20.146256", 
      "valid": true, 
      "version": "0.3"
    }
    
### List all academic departments for a given semester ###

#### Request ####

`GET /semesters/:semester`

For example:

`GET /semesters/2012b`

#### Response ####

    {
      "result": {
        "depts": [
          {
            "id": "ACCT", 
            "name": "ACCOUNTING", 
            "path": "/semesters/2012b/acct"
          },
          ...
        ], 
        "id": "2012B", 
        "name": "Summer 2012", 
        "path": "/semesters/2012b", 
        "seasoncode": "B", 
        "year": 2012
      }, 
      "retrieved": "2012-12-05 16:55:07.385537", 
      "valid": true, 
      "version": "0.3"
    }
    
### List all of an academic department's courses for a given semester ###

#### Request ####

`GET /semesters/:semester/:dept`

For example,

`GET /semesters/2012b/writ`

#### Response ####

    {
      "result": {
        "courses": [
          {
            "aliases": [
              "WRIT-150"
            ], 
          "id": 28466, 
          "name": "MASTERING THE PROPOSAL: Mastering the Proposal", 
          "path": "/courses/28466", 
          "primary_alias": "WRIT-150", 
          "semester": "2012B"
          }
        ], 
        "id": "WRIT", 
        "name": "WRITING PROGRAM", 
        "path": "/semesters/2012b/writ"
      }, 
      "retrieved": "2012-12-05 16:57:50.231427", 
      "valid": true, 
      "version": "0.3"
    }
    
## Coursehistories ##

Coursehistories are objects that represent a certain course over time.  Coursehistories have no associated semester and are useful for easily accessing all instances of a given course.

Coursehistories can be accessed either via the coursehistory's unique ID number or the coursehistory's Penn course code (i.e. CIS-110).

### List information about a specific coursehistory ###

#### Request ####

`GET /coursehistories/:ID`

`GET /coursehistories/:coursecode`

For example,

`GET /coursehistories/250`

`GET /coursehistories/CHEM-101`

#### Response ####

    {
      "result": {
        "aliases": [
          "CHEM-101"
        ], 
        "courses": [
          {
            "aliases": [
              "CHEM-101"
            ], 
            "id": 250, 
            "name": "GENERAL CHEMISTRY I", 
            "path": "/courses/250", 
            "primary_alias": "CHEM-101", 
            "semester": "2002A"
          },
          ...
        ], 
        "id": 250, 
        "name": "GENERAL CHEMISTRY I", 
        "path": "/coursehistories/250", 
        "reviews": {
          "path": "/coursehistories/250/reviews"
        }
      }, 
      "retrieved": "2012-12-05 17:06:12.004212", 
      "valid": true, 
      "version": "0.3"
    }

## Courses ##

A Course is a class offered in a specific semester.  Courses are grouped together into Coursehistories, and have child Section and Review resources.

### List information about a Course ###

#### Request ####

`GET /courses/:courseID`

`GET /courses/:course_name:`, where `:course_name` is a string like `2011c-CIS-110`

For example:

`GET /courses/24160`

`GET /courses/2011c-CIS-110`

#### Response ####

    {
      "result": {
        "aliases": [
          "CIS-110"
        ], 
        "coursehistories": {
          "path": "/coursehistories/3834"
        }, 
        "credits": null, 
        "description": "How do you program computers to accomplish tasks? How do you break down a complex task into simpler ones? CIS 110 is a Java lite course that covers the fundamentals of object-oriented programming such as objects, classes, state, methods, loops, arrays, inheritance, and recursion using the Java programming language. ", 
        "id": 24160, 
        "name": "INTRO TO COMP PROG", 
        "path": "/courses/24160", 
        "primary_alias": "CIS-110", 
        "reviews": {
          "path": "/courses/24160/reviews"
        }, 
        "sections": {
          "path": "/courses/24160/sections", 
          "values": [
            {
              "aliases": [
                "CIS-110-001"
              ], 
              "id": "24160-001", 
              "name": "INTRO TO COMP PROG", 
              "path": "/courses/24160/sections/001", 
              "primary_alias": "CIS-110-001", 
              "sectionnum": "001"
            }, 
            {
              "aliases": [
                "CIS-110-002"
              ], 
              "id": "24160-002", 
              "name": "INTRO TO COMP PROG", 
              "path": "/courses/24160/sections/002", 
              "primary_alias": "CIS-110-002", 
              "sectionnum": "002"
            }
          ]
        }, 
        "semester": "2011C"
      }, 
      "retrieved": "2012-12-05 17:19:12.194126", 
      "valid": true, 
      "version": "0.3"
    }
    
### List all reviews of a Course ###

#### Request ####

`GET /courses/:ID/reviews`

`GET /courses/:course_name/reviews`

#### Response ####

    {
      "result": {
        "values": [
          {
            "comments": "This counts as a Formal Reasoning course for College students. In this course, students learn how to program computers to accomplish tasks and break down a complex task into simpler ones. CIS 110 is a Java lite course that covers the fundamentals of object-oriented programming such as objects, classes, state, methods, loops, arrays, inheritance, and recursion using the Java programming language. Students found this class to be 'worthwhile.' They reported that they learned alot in this course, and that they found the material engaging. The majority of students felt that they left the course with a 'good command of the basics of Java.' Many students highly recommended the course to students who want to learn the basics of computer programming and are willing to make the class a priority. Students praised Professor Osera as a 'fun' and 'engaging' lecturer. Many students felt that there was a disconnection between the homework and material covered in class. Professor Osera clearly defined the assignments and goals of the course, which students found to be helpful. Students described this course 'challenging,' 'intense,' 'demanding,' and 'time consuming,' and reported spending between 6 to 10 hours a week on homework. Nevertheless, students felt that the level of difficulty allowed them to learn more. Students found the textbook, recitations, and tutors helpful. Some students feel that this course is too fast-paced for beginners.", 
            "id": "24160-001-5317-PETER-MICHAEL-S--OSERA", 
            "instructor": {
              "first_name": "PETER-MICHAEL S.", 
              "id": "5317-PETER-MICHAEL-S--OSERA", 
              "last_name": "OSERA", 
              "name": "PETER-MICHAEL S. OSERA", 
              "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
            }, 
            "num_reviewers": 134, 
            "num_students": 142, 
            "path": "/courses/24160/sections/001/reviews/5317-PETER-MICHAEL-S--OSERA", 
            "ratings": {
              "rAmountLearned": "3.25", 
              "rCommAbility": "2.96", 
              "rCourseQuality": "2.95", 
              "rDifficulty": "2.90", 
              "rInstructorAccess": "3.16", 
              "rInstructorQuality": "3.09", 
              "rReadingsValue": "2.50", 
              "rRecommendMajor": "3.72", 
              "rRecommendNonMajor": "2.63", 
              "rStimulateInterest": "3.17", 
              "rWorkRequired": "3.36"
            }, 
            "section": {
              "aliases": [
                "CIS-110-001"
              ], 
              "id": "24160-001", 
              "name": "INTRO TO COMP PROG", 
              "path": "/courses/24160/sections/001", 
              "primary_alias": "CIS-110-001", 
              "sectionnum": "001"
            }
          }, 
          {
            "comments": "CIS 110 is a Java lite course that covers the fundamentals of object-oriented programming such as objects, classes, state, methods, loops, arrays, inheritance, and recursion using the Java programming language. Students for the most part enjoyed this course, claiming that they learned a lot. They also felt that the class was 'informative,' 'very interesting,' and 'rewarding.' Some students even expressed that this was one of the most fun classes that they hadtaken at Penn. Students were very pleased with Professor Osera, expressing that he was an 'awesome teacher.' Students were also pleased with the fact that Professor Osera put in alot of hard work to formulate the curriculum that was easy to understand and that fostered critical thinking development. The homework assignments in this class require a lot of time and patience. However, this class was recommended for both majors and non-majors alike who have an interest in learning about programming. For students in the College, this class fulfills the Formal Reasoning category.", 
            "id": "24160-002-5317-PETER-MICHAEL-S--OSERA", 
            "instructor": {
              "first_name": "PETER-MICHAEL S.", 
              "id": "5317-PETER-MICHAEL-S--OSERA", 
              "last_name": "OSERA", 
              "name": "PETER-MICHAEL S. OSERA", 
              "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
            }, 
            "num_reviewers": 84, 
            "num_students": 91, 
            "path": "/courses/24160/sections/002/reviews/5317-PETER-MICHAEL-S--OSERA", 
            "ratings": {
              "rAmountLearned": "3.49", 
              "rCommAbility": "3.22", 
              "rCourseQuality": "3.17", 
              "rDifficulty": "2.64", 
              "rInstructorAccess": "3.21", 
              "rInstructorQuality": "3.37", 
              "rReadingsValue": "2.37", 
              "rRecommendMajor": "3.85", 
              "rRecommendNonMajor": "2.72", 
              "rStimulateInterest": "3.44", 
              "rWorkRequired": "3.32"
            }, 
            "section": {
              "aliases": [
                "CIS-110-002"
              ], 
              "id": "24160-002", 
              "name": "INTRO TO COMP PROG", 
              "path": "/courses/24160/sections/002", 
              "primary_alias": "CIS-110-002", 
              "sectionnum": "002"
            }
          }
        ]
      }, 
      "retrieved": "2012-12-05 17:23:25.297448", 
      "valid": true, 
      "version": "0.3"
    }

### List all of a Course's Sections ###

#### Request ####

`GET /courses/:ID/sections`

`GET /courses/:course_name/sections`

#### Response ####

    {
      "result": {
        "values": [
          {
            "aliases": [
              "CIS-110-001"
            ], 
            "courses": {
              "aliases": [
                "CIS-110"
              ], 
              "id": 24160, 
              "name": "INTRO TO COMP PROG", 
              "path": "/courses/24160", 
              "primary_alias": "CIS-110", 
              "semester": "2011C"
            }, 
            "group": null, 
            "id": "24160-001", 
            "instructors": [
              {
                "first_name": "PETER-MICHAEL S.", 
                "id": "5317-PETER-MICHAEL-S--OSERA", 
                "last_name": "OSERA", 
                "name": "PETER-MICHAEL S. OSERA", 
                "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
              }
            ], 
            "meetingtimes": [], 
            "name": "INTRO TO COMP PROG", 
            "path": "/courses/24160/sections/001", 
            "primary_alias": "CIS-110-001", 
            "reviews": {
              "path": "/courses/24160/sections/001/reviews", 
              "values": [
                {
                  "id": "24160-001-5317-PETER-MICHAEL-S--OSERA", 
                  "instructor": {
                    "first_name": "PETER-MICHAEL S.", 
                    "id": "5317-PETER-MICHAEL-S--OSERA", 
                    "last_name": "OSERA", 
                    "name": "PETER-MICHAEL S. OSERA", 
                    "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
                  }, 
                  "path": "/courses/24160/sections/001/reviews/5317-PETER-MICHAEL-S--OSERA", 
                  "section": {
                    "aliases": [
                      "CIS-110-001"
                    ], 
                    "id": "24160-001", 
                    "name": "INTRO TO COMP PROG", 
                    "path": "/courses/24160/sections/001", 
                    "primary_alias": "CIS-110-001", 
                    "sectionnum": "001"
                  }
                }
              ]
            }, 
            "sectionnum": "001"
          }, 
          ...
        ]
      }, 
      "retrieved": "2012-12-05 17:26:24.307622", 
      "valid": true, 
      "version": "0.3"
    }
    
## Sections ##

A Section is a meeting of a Course, and is denoted by a number appended to the course code (CIS-110-001).  Sections are associated with the Instructors that teach the Section, and with PCR reviews of that Instructor and Section.

### List information about a particular Section ###

#### Request ####

`GET /courses/:ID/sections/:section_ID`

`GET /courses/:course_name/sections/:section_ID`

For example:

`GET /courses/24160/sections/001`

`GET /courses/2011c-CIS-110/sections/001`

#### Response ####

    {
      "result": {
        "aliases": [
          "CIS-110-001"
        ], 
        "courses": {
          "aliases": [
            "CIS-110"
          ], 
          "id": 24160, 
          "name": "INTRO TO COMP PROG", 
          "path": "/courses/24160", 
          "primary_alias": "CIS-110", 
          "semester": "2011C"
        }, 
        "group": null, 
        "id": "24160-001", 
        "instructors": [
          {
            "first_name": "PETER-MICHAEL S.", 
            "id": "5317-PETER-MICHAEL-S--OSERA", 
            "last_name": "OSERA", 
            "name": "PETER-MICHAEL S. OSERA", 
            "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
          }
        ], 
        "meetingtimes": [], 
        "name": "INTRO TO COMP PROG", 
        "path": "/courses/24160/sections/001", 
        "primary_alias": "CIS-110-001", 
        "reviews": {
          "path": "/courses/24160/sections/001/reviews", 
          "values": [
            {
              "id": "24160-001-5317-PETER-MICHAEL-S--OSERA", 
              "instructor": {
                "first_name": "PETER-MICHAEL S.", 
                "id": "5317-PETER-MICHAEL-S--OSERA", 
                "last_name": "OSERA", 
                "name": "PETER-MICHAEL S. OSERA", 
                "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
              }, 
              "path": "/courses/24160/sections/001/reviews/5317-PETER-MICHAEL-S--OSERA", 
              "section": {
                "aliases": [
                  "CIS-110-001"
                ], 
                "id": "24160-001", 
                "name": "INTRO TO COMP PROG", 
                "path": "/courses/24160/sections/001", 
                "primary_alias": "CIS-110-001", 
                "sectionnum": "001"
              }
            }
          ]
        }, 
        "sectionnum": "001"
      }, 
      "retrieved": "2012-12-05 17:33:20.914777", 
      "valid": true, 
      "version": "0.3"
    }
    
### List all reviews for a Section ###

*(Note: There is usually only one review per Section, but there may be multiple reviews if the Section was taught by multiple Instructors.)*

#### Request ####

`GET /courses/:ID/sections/:section_ID/reviews`

`GET /courses/:course_name/sections/:section_ID/reviews`

#### Response ####

    {
      "result": {
        "values": [
          {
            "comments": "This counts as a Formal Reasoning course for College students. In this course, students learn how to program computers to accomplish tasks and break down a complex task into simpler ones. CIS 110 is a Java lite course that covers the fundamentals of object-oriented programming such as objects, classes, state, methods, loops, arrays, inheritance, and recursion using the Java programming language. Students found this class to be 'worthwhile.' They reported that they learned alot in this course, and that they found the material engaging. The majority of students felt that they left the course with a 'good command of the basics of Java.' Many students highly recommended the course to students who want to learn the basics of computer programming and are willing to make the class a priority. Students praised Professor Osera as a 'fun' and 'engaging' lecturer. Many students felt that there was a disconnection between the homework and material covered in class. Professor Osera clearly defined the assignments and goals of the course, which students found to be helpful. Students described this course 'challenging,' 'intense,' 'demanding,' and 'time consuming,' and reported spending between 6 to 10 hours a week on homework. Nevertheless, students felt that the level of difficulty allowed them to learn more. Students found the textbook, recitations, and tutors helpful. Some students feel that this course is too fast-paced for beginners.", 
            "id": "24160-001-5317-PETER-MICHAEL-S--OSERA", 
            "instructor": {
              "first_name": "PETER-MICHAEL S.", 
              "id": "5317-PETER-MICHAEL-S--OSERA", 
              "last_name": "OSERA", 
              "name": "PETER-MICHAEL S. OSERA", 
              "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
            }, 
            "num_reviewers": 134, 
            "num_students": 142, 
            "path": "/courses/24160/sections/001/reviews/5317-PETER-MICHAEL-S--OSERA", 
            "ratings": {
              "rAmountLearned": "3.25", 
              "rCommAbility": "2.96", 
              "rCourseQuality": "2.95", 
              "rDifficulty": "2.90", 
              "rInstructorAccess": "3.16", 
              "rInstructorQuality": "3.09", 
              "rReadingsValue": "2.50", 
              "rRecommendMajor": "3.72", 
              "rRecommendNonMajor": "2.63", 
              "rStimulateInterest": "3.17", 
              "rWorkRequired": "3.36"
            }, 
            "section": {
              "aliases": [
                "CIS-110-001"
              ], 
              "id": "24160-001", 
              "name": "INTRO TO COMP PROG", 
              "path": "/courses/24160/sections/001", 
              "primary_alias": "CIS-110-001", 
              "sectionnum": "001"
            }
          }
        ]
      }, 
      "retrieved": "2012-12-05 17:36:44.032085", 
      "valid": true, 
      "version": "0.3"
    }
    
### List review for a single Instructor of a Section ###

*(Note: There is usually only one review per Section, but there may be multiple reviews if the Section was taught by multiple Instructors.  Use this request to obtain review data for a single Instructor within a Section.)*

#### Request ####

`GET /courses/:ID/sections/:section_ID/reviews/:instructor_ID`

`GET /courses/:course_name/sections/:section_ID/reviews/:instructor:ID`

For example,

`GET /courses/24160/sections/001/reviews/5317-PETER-MICHAEL-S--OSERA`

`GET /courses/2011c-CIS-110/sections/001/reviews/5317-PETER-MICHAEL-S--OSERA`

#### Response ####

    {
      "result": {
        "values": [
          {
            "comments": "This counts as a Formal Reasoning course for College students. In this course, students learn how to program computers to accomplish tasks and break down a complex task into simpler ones. CIS 110 is a Java lite course that covers the fundamentals of object-oriented programming such as objects, classes, state, methods, loops, arrays, inheritance, and recursion using the Java programming language. Students found this class to be 'worthwhile.' They reported that they learned alot in this course, and that they found the material engaging. The majority of students felt that they left the course with a 'good command of the basics of Java.' Many students highly recommended the course to students who want to learn the basics of computer programming and are willing to make the class a priority. Students praised Professor Osera as a 'fun' and 'engaging' lecturer. Many students felt that there was a disconnection between the homework and material covered in class. Professor Osera clearly defined the assignments and goals of the course, which students found to be helpful. Students described this course 'challenging,' 'intense,' 'demanding,' and 'time consuming,' and reported spending between 6 to 10 hours a week on homework. Nevertheless, students felt that the level of difficulty allowed them to learn more. Students found the textbook, recitations, and tutors helpful. Some students feel that this course is too fast-paced for beginners.", 
            "id": "24160-001-5317-PETER-MICHAEL-S--OSERA", 
            "instructor": {
              "first_name": "PETER-MICHAEL S.", 
              "id": "5317-PETER-MICHAEL-S--OSERA", 
              "last_name": "OSERA", 
              "name": "PETER-MICHAEL S. OSERA", 
              "path": "/instructors/5317-PETER-MICHAEL-S--OSERA"
            }, 
            "num_reviewers": 134, 
            "num_students": 142, 
            "path": "/courses/24160/sections/001/reviews/5317-PETER-MICHAEL-S--OSERA", 
            "ratings": {
              "rAmountLearned": "3.25", 
              "rCommAbility": "2.96", 
              "rCourseQuality": "2.95", 
              "rDifficulty": "2.90", 
              "rInstructorAccess": "3.16", 
              "rInstructorQuality": "3.09", 
              "rReadingsValue": "2.50", 
              "rRecommendMajor": "3.72", 
              "rRecommendNonMajor": "2.63", 
              "rStimulateInterest": "3.17", 
              "rWorkRequired": "3.36"
            }, 
            "section": {
              "aliases": [
                "CIS-110-001"
              ], 
              "id": "24160-001", 
              "name": "INTRO TO COMP PROG", 
              "path": "/courses/24160/sections/001", 
              "primary_alias": "CIS-110-001", 
              "sectionnum": "001"
            }
          }
        ]
      }, 
      "retrieved": "2012-12-05 17:36:44.032085", 
      "valid": true, 
      "version": "0.3"
    }
    
## More information about Review data ##

Reviews cannot be accessed from the top level -- they must be accessed through a Course, Instructor, or Section.  Reviews accessed through a Section will contain the full-text review in addition to numerical ratings; Reviews accessed through Courses and Instructors will only contain numerical ratings.

### Rating names conversion chart ###

Below is a table that associates the names of numerical ratings inside PCR with their plain-English questions:

<table class='table table-striped table-condensed table-bordered'>
  <thead>
    <tr><th>Rating</th><th>Question</th></tr>
  </thead>
  <tbody>
    <tr><td>rCourseQuality</td><td>Overall Quality of the course.</td></tr>
    <tr><td>rInstructorQuality</td><td>Overall Quality of the instructor.</td></tr>
    <tr><td>rDifficulty</td><td>Please rate the difficulty of the course. (0=easy to 4=difficult)</td></tr>
    <tr><td>rCommAbility</td><td>Instructor's ability to communicate the subject matter.</td></tr>
    <tr><td>rInstructorAccess</td><td>Instructor's accessibility and willingness to to discuss course content and any problems.</td></tr>
    <tr><td>rReadingsValue</td><td>Value of assigned readings.</td></tr>
    <tr><td>rAmountLearned</td><td>Amount learned from this course in terms of knowledge, concepts, skills and thinking ability.</td></tr>
    <tr><td>rWorkRequired</td><td>Please rate the amount of work required for this course. (0=very little to 4=very much)</td></tr>
    <tr><td>rRecommendMajor</td><td>Would you recommend this course to a major? (0=no to 4=strongly)</td></tr>
    <tr><td>rRecommendNonMajor</td><td>Would you recommend this course to a non-major? (0=no to 4=strongly)</td></tr>
    <tr><td>rStimulateInterest</td><td>Was the instructor able to stimulate your interest in the material?</td></tr>
    <tr><td>rArticulateGoals</td><td>Were the goals of the course clearly articulated?</td></tr>
    <tr><td>rSkillEmphasis</td><td>Was the emphasis placed on the language skills (speaking, listening, reading writing) appropriate in terms of the defined goals of the course?</td></tr>
    <tr><td>rHomeworkValuable</td><td>Were homework exercises (and compositions, where appropriate) valuable reinforcement of classroom work?</td></tr>
    <tr><td>rExamsConsistent</td><td>Were the exams consistent with assignments, materials, and method of instruction?</td></tr>
    <tr><td>rAbilitiesChallenged</td><td>Were your linguistic abilities in reading, writing, speaking, and listening sufficiently challenged?</td></tr>
    <tr><td>rClassPace</td><td>How would you rate the pace of the course? (0=much to slow; 1=too slow; 2=just right; 3=too fast; 4=much too fast)</td></tr>
    <tr><td>rOralSkills</td><td>Did the instructor organize appropriate activities in class to encourage the use of oral skills?</td></tr>
    <tr><td>rInstructorConcern</td><td>Was the instructor concerned that students learn the materials?</td></tr>
    <tr><td>rInstructorRapport</td><td>Please evaluate the rapport between the class and the instructor. (0=bad, 4=excellent)</td></tr>
    <tr><td>rInstructorAttitude</td><td>Please rate the instructor's attitude towards the course.</td></tr>
    <tr><td>rInstructorEffective</td><td>Please rate the instructor's effectiveness in presenting and explaining course materials.</td></tr>
    <tr><td>rGradeFairness</td><td>Please rate the fairness of the grading process in the course.</td></tr>
    <tr><td>rNativeAbility</td><td>Do you feel that the skills learned in this course would help you survive in a native environment?</td></tr>
    <tr><td>rTAQuality</td><td>Please evaluate the overall quality of the teaching assistant/drill instructor in the course.</td></tr>
  </tbody>
</table>