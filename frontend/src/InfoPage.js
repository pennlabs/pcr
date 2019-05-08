import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import NavBar from './NavBar';
import ErrorBox from './ErrorBox';
import Footer from './Footer';
import Popover from './Popover';
import { getColumnName } from './ScoreBox';


class InfoPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            showChooseCols: false,
            isAverage: localStorage.getItem("meta-column-type") !== "recent",
            courses: [],
            excludedCourses: [],
            boxValues: ['N/A', 'N/A', 'N/A', 'N/A'],
            boxLabels: ['rCourseQuality', 'rInstructorQuality', 'rDifficulty', 'rWorkRequired']
        };

        this.regenerateRatings = this.regenerateRatings.bind(this);
    }

    componentDidMount() {
        window.addEventListener('storage', this.regenerateRatings);
        this.regenerateRatings();
    }

    componentWillUnmount() {
        window.removeEventListener('storage', this.regenerateRatings);
    }

    regenerateRatings() {
        const courses = Object.keys(localStorage).filter((k) => !k.startsWith("meta-")).map((k) => {
            const out = JSON.parse(localStorage.getItem(k));
            if (typeof out !== 'object') {
                return null;
            }
            const typeDict = {};
            if (typeof out.info !== 'undefined') {
                out.info.forEach((v) => typeDict[v.category] = v);
                out.info = typeDict;
            }
            out.course = k;
            return out;
        }).filter((a) => a !== null);
        this.setState((state) => ({
            courses: courses,
            boxValues: state.boxLabels.map((type) => {
                const scoreList = courses.filter((a) => state.excludedCourses.indexOf(a.course) === -1).map((a) => (a.info[type] || {average: null, recent: null})[state.isAverage ? 'average' : 'recent']).filter((a) => a !== null && !isNaN(a)).map((a) => parseFloat(a));
                if (!scoreList.length) {
                    return "N/A";
                }
                else {
                    return (scoreList.reduce((a, b) => a + b) / scoreList.length).toFixed(1);
                }
            })
        }));
        window.onCartUpdated();
    }

    render() {
        var content = <ErrorBox>404 Page Not Found</ErrorBox>;

        if (this.props.match.params.page === "cart") {
            const checkboxValues = ["rCourseQuality", "rInstructorQuality", "rDifficulty", "rAmountLearned", "rWorkRequired", "rReadingsValue", "rCommAbility", "rInstructorAccess", "rStimulateInterest", "rTAQuality", "rRecommendMajor", "rRecommendNonMajor"];
            const checkboxLabels = ["Course Quality", "Instructor Quality", "Difficulty", "Amount Learned", "Amount of Work", "Value of Readings", "Instructor Communication", "Instructor Accessibility", "Ability to Stimulate Interest", "TA Quality", "Recommend for Majors", "Recommend for Non-Majors"];

            const propertyShortNames = {
                rCourseQuality: 'Course', rInstructorQuality: 'Instructor',
                rDifficulty: 'Difficulty', rAmountLearned: 'Learned',
                rWorkRequired: 'Workload', rReadingsValue: 'Reading',
                rCommAbility: 'Instr Comm', rInstructorAccess: 'Access',
                rStimulateInterest: 'Interest', rTAQuality: 'TA Quality',
                rRecommendMajor: 'Major', rRecommendNonMajor: 'Non-Major'
            };

            content = (
<center className="box" style={{ margin: '30px auto', maxWidth: 720 }}>
    <p className="courseCartHeader title">My Course Cart</p>
    <p className="courseCartDesc">The course cart is a feature for you to see all the relevant reviews for your selected courses at once with at-a-glance statistics. Search for courses to add them to your cart.</p>
    <div id="bannerScore">
        <div className="scoreboxrow courseCartRow">
            {this.state.boxLabels.map((a, i) =>
                <div key={i} className={"mb-2 scorebox " + ["course", "instructor", "difficulty", "workload"][i % 4]}>
                    <p className="num">{this.state.boxValues[i]}</p>
                    <p className="desc">{propertyShortNames[a]}</p>
                </div>
            )}
        </div>
    </div>
    <div className="clear"></div>
    <div className="fillerBox"></div>
    {this.state.showChooseCols &&
        <div className="box">
            <h3 style={{ fontSize: '1.5em' }}>Choose columns to display</h3>
            <div className="clearfix" style={{ textAlign: 'left' }}>
                {checkboxValues.map(
                    (a, i) => <div style={{ width: '50%', display: 'inline-block' }} key={i}><input type="checkbox" onChange={(e) => {
                        const pos = this.state.boxLabels.indexOf(a);
                        if (pos === -1) {
                            this.setState((state) => {
                                state.boxValues.push('N/A');
                                state.boxLabels.push(a);
                                return {
                                    boxValues: state.boxValues,
                                    boxLabels: state.boxLabels
                                };
                            });
                        }
                        else {
                            this.setState((state) => {
                                state.boxValues.splice(pos, 1);
                                state.boxLabels.splice(pos, 1);
                                return {
                                    boxValues: state.boxValues,
                                    boxLabels: state.boxLabels
                                };
                            });
                        }
                        this.regenerateRatings();
                    }} checked={this.state.boxLabels.indexOf(a) !== -1} value={a} id={"checkbox_" + a} name={a} className="mr-1" /><label htmlFor={"checkbox_" + a}>{checkboxLabels[i]}</label></div>
                )}
            </div>
        </div>
    }
    <button className="btn btn-primary mr-2" onClick={() => this.setState((state) => ({ showChooseCols: !state.showChooseCols }))}>Choose Categories</button>
    <div className="btn-group">
        <span className={"btn " + (this.state.isAverage ? "btn-primary" : "btn-secondary")} onClick={() => {this.setState({ isAverage: true }); this.regenerateRatings(); }}>Average</span>
        <span className={"btn " + (this.state.isAverage ? "btn-secondary" : "btn-primary")} onClick={() => {this.setState({ isAverage: false }); this.regenerateRatings(); }}>Most Recent</span>
    </div>
    <div className="clear"></div>
    <div id="boxHelpTag">Click a course to exclude it from the average.</div>
    <div id="courseBox">
        {this.state.courses.map((a, i) =>
            <Popover key={i} button={
            <div onClick={() => {this.setState((state) => ({
                excludedCourses: state.excludedCourses.indexOf(a.course) !== -1 ? state.excludedCourses.filter((b) => b !== a.course) : state.excludedCourses.concat([a.course])
            })); this.regenerateRatings()}} style={{ display: 'inline-block' }} className={"courseInBox" + (this.state.excludedCourses.indexOf(a.course) !== -1 ? " courseInBoxGrayed" : "")}>
                {a.course}
                <Link to={'/course/' + a.course}><i className="fa fa-link" /></Link>
                <i className="fa fa-times" onClick={() => {localStorage.removeItem(a.course); this.regenerateRatings()}} />
            </div>} hover><b>{a.course}</b><br />{a.instructor}<br />{Object.values(a.info).sort((x, y) => x.category.localeCompare(y.category)).map((b, i) => <div key={i}>{getColumnName(b.category)} <span className="float-right ml-3">{this.state.isAverage ? b.average : b.recent}</span></div>)}</Popover>
        )}
    </div>
</center>
            );
        }

        if (this.props.match.params.page === "about") {
            content = (<div className="center-narrow">
                <h1>Welcome</h1>
                <p>Welcome to the new Penn Course Review!</p>
                <p>The student-run Penn Course Review has served as a valuable guide for course selection since the 1960s. In 2014, Penn Course Review was completely redesigned to simplify the search experience. In 2018, we hope to continue providing you with the best insights on courses and have therefore updated this experience.</p>
                <p>Interested in building something on the Penn Course Review API? <a href="https://docs.google.com/spreadsheet/viewform?hl=en_US&formkey=dGZOZkJDaVkxdmc5QURUejAteFdBZGc6MQ#gid=0">Request API access</a>.</p>
                <p>Want easy access to Penn Course Review? Get the <a href="https://pennlabs.org/mobile/"> Penn Mobile App</a>!</p>

                <h1>About</h1>
                <p>Penn Course Review is a student-run service that provides numerical ratings for undergraduate courses and professors at the University of Pennsylvania. PCR has a long history of being a valuable and influential guide for course selection.</p>
                <p>PCR is developed and managed by <a href="https://pennlabs.org/">Penn Labs</a>, a student developer organization on Penn’s campus.</p>

                <p>The Penn Course Review compiles its information from online course evaluations conducted at the end of each semester by the Provost's office in conjunction with ISC.</p>
                <p>Your evaluations and comments feed the Review, so the more information you provide about your courses and professors, the more comprehensive Penn Course Review will be.</p>

                <p>If you want to look at courses on the go, <a href="https://pennlabs.org/mobile/">PennMobile</a> is available for download! In the courses section, you are able to view course descriptions and ratings!</p>
                <p>Version 2.0 was built by Eric Wang, Cassandra Li, Rohan Menezes, Vinai Rachakonda, Brandon Lin, Yonah Mann, Josh Doman and designed by Tiffany Chang.</p>
                <p>Thanks and happy searching,</p>
                <p><strong>Penn Labs</strong></p>

                <img alt="Penn Labs" src="/static/image/labs.png" style={{ width: 100 }} />

                <h1>Questions</h1>
                <p>If you have any questions, take a look at our <Link to="faq">FAQs</Link> section.</p>
            </div>);
        }

        if (this.props.match.params.page === "faq") {
            content = (
                <div id="faqs" className="center-narrow">
                  <h1>Frequently Asked Questions</h1>
                  <div>
                    <p className="question">
                      How do I use the website?
                    </p>
                    <p className="answer">
                      Each professor, course, and department has its own page. Summary ratings for the recent semester and for all semesters are provided at the left of each page, with more detailed rating information provided on the right. You can choose to view or hide each course rating criteria by clicking the plus icon on the top of the table. You can also toggle the view mode of ratings between aggregate and most recent on the right side of the page.

                      You can hover over the tags on the left side of the page or the stars on the right side of the page in order to learn more about courses offered in the upcoming semester.
                    </p>
                  </div>

                  <div>
                    <p className="question">
                      What's new?
                    </p>
                    <p className="answer">
                      The site includes new features intended to make PCR's content more intuitive and accessible. The new search function allows students to search by course name, number, or professor. In addition to the traditional ratings, the site now offers ratings that average the evaluations from every semester the course or professor has been reviewed. Students can choose which information is relevant to them by selecting which rating criteria appear on the page.
                    </p>
                  </div>

                  <div>
                    <p className="question">
                      How are courses rated?
                    </p>
                    <p className="answer">
                      At the end of each semester, the Provost's office, in conjunction with ISC, administers Penn's course evaluation form, which consists of eleven questions aimed at assessing the quality of the course and instructor. Each evaluation question is answered on a scale of Poor to Excellent. The ratings are translated numerically so that a rating of 0.00 corresponds a student evaluation of "Poor," 1.00 corresponds to an evaluation of "Fair," 2.00 to "Good," 3.00 to "Very Good," and 4.00 to "Excellent."
                    </p>
                  </div>

                  <div>
                    <p className="question">
                      How often is data updated?
                    </p>
                    <p className="answer">
                        Information pertaining to which sections are taught in the upcoming semester is updated every 24 hours.
                    </p>
                  </div>

                  <div>
                    <p className="question">
                      What do the colors mean?
                    </p>
                    <div className="answer">
                      Here's a guide to the color coded ratings.
                      <br /><br />
                      <div className="scorebox difficulty rating-bad">
                        <div className="num">0-2</div>
                      </div>
                      <div className="scorebox difficulty rating-okay">
                        <div className="num">2-3</div>
                      </div>
                      <div className="scorebox difficulty rating-good">
                        <div className="num">3-4</div>
                      </div>
                    </div>
                  </div>

                </div>
            );
        }

        return <div><NavBar />{content}<Footer /></div>;
    }
}


export default InfoPage;
