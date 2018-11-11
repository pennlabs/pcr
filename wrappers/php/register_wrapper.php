<?php

/**
 * Thin PHP Wrapper for Penn Registrar RESTful API 
 * for PennApps 2010
 * Supports PHP5.2 and up
 *
 * @author alexeym@seas.upenn.edu
 * @version 0.1 (it's not beta, it's just buggy)
 */
class Courses {
    const API_ROOT = "http://pennapps.com/api/courses";
    const CURRENT_SEMESTER_CODE = 'current'; 
 
    public static function getSemesters() {
        return self::get('/course'); 
    }

    public static function getDepartments($semester_code) {
        return self::get('/course/'.$semester_code);
    }

    public static function getCourses($semester_code, $dept_code) {
        return self::get('/course/'.$semester_code.'/'.$dept_code);
    }

    public static function getSection($semester_code, $dept_code, $course_code) {
        return self::get('/course/'
            .$semester_code.'/'.$dept_code.'/'.$course_code);
    }

    public static function getProfessor($prof_code) {
        return self::get('/instructor/'.$prof_code);
    }

    public static function getBuilding($building_code) {
        return self::get('/building/'.$building_code);
    }
  
    /**
     * Search for courses that match some parameters
     * $param args array of arguments to search by.  Valid arguments include: 
     *   case-insensitive match: 
     *     dept, building, type [lec/lab/rec/etc], day[mtwrfsu]
     *   case-insensitive 'contains' search:
     *     name (course title), instructor, description (tbd)
     *   numerical comparison: sectionnum, coursenum, start, end
     *     time is a 4-digit int, IE 1700 for 5:00PM)
     *     append _(lt/lte/gt/gte) to above for (</<=/>/>=)
     *       IE, 'start_lt'=>1200
     */
    public static function search($args) {
        return self::get('/course/search', $args);
    }
  
    /**
     * If you just feel like using the returned paths, use this function
     * @param args (optional) array ie, array('dept' => 'cis);
     */
    public static function get($path, $args='') {
        $arg_str = empty($args) ? '' : '?'.http_build_query($args);
        return json_decode(file_get_contents(self::API_ROOT.$path.$arg_str)); 
    }
}

// ********************Test Code************************

//echo "<pre>";
//var_dump(Courses::getSemesters());

