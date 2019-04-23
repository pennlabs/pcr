import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import NavBar from './NavBar';
import Footer from './Footer';


class InfoPage extends Component {
    render() {
        var content;

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

                <h1>Questions</h1>
                <p>If you have any questions, take a look at our <Link to="faq">FAQs</Link> section.</p>
            </div>);
        }

        if (this.props.match.params.page === "faq") {
            content = (
                <div id="faqs" className="center-narrow">
                  <h1>Frequently Asked Questions</h1>
                  <div id="faq0">
                    <p className="question">
                      How do I use the website?
                    </p>
                    <p className="answer">
                      Each professor or course has its own page. Summary ratings for the recent semester and for all semesters are provided at the top of each page, with more detailed rating information provided below. You can choose to view or hide each course rating criteria by clicking the link on the right side of the page. You can also toggle the view mode of ratings between aggregate and most recent on the left side of the page.
                    </p>
                  </div>

                  <div id="faq1">
                    <p className="question">
                      What's new?
                    </p>
                    <p className="answer">
                      The site includes new features intended to make PCR's content more intuitive and accessible. The new search function allows students to search by course name, number, or professor. In addition to the traditional ratings, the site now offers ratings that average the evaluations from every semester the course or professor has been reviewed. Students can choose which information is relevant to them by selecting which rating criteria appear on the page.
                    </p>
                  </div>

                  <div id="faq2">
                    <p className="question">
                      How are courses rated?
                    </p>
                    <p className="answer">
                      At the end of each semester, the Provost's office, in conjunction with ISC, administers Penn's course evaluation form, which consists of eleven questions aimed at assessing the quality of the course and instructor. Each evaluation question is answered on a scale of Poor to Excellent. The ratings are translated numerically so that a rating of 0.00 corresponds a student evaluation of "Poor," 1.00 corresponds to an evaluation of "Fair," 2.00 to "Good," 3.00 to "Very Good," and 4.00 to "Excellent."
                    </p>
                  </div>

                  <div id="faq3">
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
