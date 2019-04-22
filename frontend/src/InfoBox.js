import React, { Component } from 'react';
import Tags from './Tags';
import ScoreboxRow from './ScoreboxRow';
import Popover from './Popover';
import { api_contact } from './api';

/**
 * Information box on the left most side, containing scores and descriptions
 * of course or professor.
 *
 */

class InfoBox extends Component {

    constructor(props) {
        super(props);

        this.state = {
            items: this.props.data,
            average_ratings: this.props.data.average_ratings,
            recent_ratings: this.props.data.recent_ratings,
            contact: null,
            inCourseCart: !!localStorage.getItem(this.props.data.code)
        };

        this.addToCourseCart = this.addToCourseCart.bind(this);
        this.removeFromCourseCart = this.removeFromCourseCart.bind(this);
    }

    componentDidMount() {
        if (this.props.type === "instructor") {
            api_contact(this.props.data.name).then((res) => {
                this.setState({
                    contact: res
                });
            });
        }
    }

    addToCourseCart(key) {
        return () => {
            var content;
            if (key === "average") {
                const average_reviews = {};
                const recent_reviews = {};
                Object.values(this.state.items.instructors).forEach(function(i) {
                    Object.keys(i.recent_reviews).forEach((j) => {
                        if (!(j in recent_reviews)) {
                            recent_reviews[j] = [];
                        }
                        recent_reviews[j].push(i.recent_reviews[j]);
                    });
                    Object.keys(i.average_reviews).forEach((j) => {
                        if (!(j in average_reviews)) {
                            average_reviews[j] = [];
                        }
                        average_reviews[j].push(i.average_reviews[j]);
                    });
                });
                Object.keys(average_reviews).forEach((i) => {
                    average_reviews[i] = (average_reviews[i].reduce((a, b) => a + b) / average_reviews[i].length).toFixed(2);
                });
                Object.keys(recent_reviews).forEach((i) => {
                    recent_reviews[i] = (recent_reviews[i].reduce((a, b) => a + b) / recent_reviews[i].length).toFixed(2);
                });
                content = {
                    name: "Average Professor",
                    average_reviews: average_reviews,
                    recent_reviews: recent_reviews
                };
            }
            else {
                content = this.state.items.instructors[key];
            }
            localStorage.setItem(this.state.items.code, JSON.stringify(content));
            this.setState({inCourseCart: true});
            window.onCartUpdated();
        };
    }

    removeFromCourseCart() {
        localStorage.removeItem(this.state.items.code);
        this.setState({inCourseCart: false});
        window.onCartUpdated();
    }

    // TODO: fix course cart selector styling
    render() {
        const pageType = this.props.type;
        const instructors = this.state.items.instructors;

        if (!this.state.items) {
            return <h1>Loading data...</h1>;
        }

        return (
            <div className="box">
            <div id="banner-info" data-type="course">
            { pageType === "course" &&
                <div className="course">
                <div className="title">{(this.state.items.code || "").replace('-', ' ')}

                <span className="float-right">
                {this.state.inCourseCart ?
                    <span onClick={this.removeFromCourseCart} className="courseCart btn btn-action" title="Remove from Cart">
                    <i className="fa fa-fw fa-trash-alt"></i>
                    </span>
                    :
                    <Popover button={
                        <span className="courseCart btn btn-action" title="Add to Cart">
                        <i className="fa fa-fw fa-cart-plus"></i>
                        </span>
                    }>
                    <div className="popover-title">Add to Cart</div>
                    <div className="popover-content">
                    <div id="divList">
                    <ul className="professorList">
                        <li>
                            <button onClick={this.addToCourseCart("average")}>Average Professor</button>
                        </li>
                    {Object.keys(instructors).map((key, i) =>
                        <li key={i}>
                            <button onClick={this.addToCourseCart(key)}>{instructors[key].name}</button>
                        </li>
                    )}
                    </ul>
                    </div>
                    </div>
                    </Popover>}{' '}

                <a target="_blank" rel="noopener noreferrer" title="Get Alerted" href={"https://penncoursealert.com/?course=" + this.props.code + "&source=pcr"} className="btn btn-action"><i className="fas fa-fw fa-bell"></i></a>
                </span>

                </div>

                {!!this.state.items.aliases.length && <div className="crosslist">(Also: {this.state.items.aliases.map((cls, i) => <span key={i}>{i > 0 && ", "}<a key={i} href={"/course/" + cls}>{cls}</a></span>)})</div>}

                <p className="subtitle">{this.state.items.name}</p>

                { (this.props.live_data && this.props.live_data.term) &&
                    <Tags {...this.props.live_data} existing_instructors={Object.values(this.state.items.instructors).map((a) => a.name)} />
                }
                </div>
            }

            { pageType === "instructor" &&
                    <div className="instructor">
                    <div className="title">{this.state.items.name}</div>
                    {this.state.contact &&
                        <div>
                        <p className="desc">Email: <a href={"mailto:" + this.state.contact.email}>{this.state.contact.email.toLowerCase()}</a></p>
                        </div>
                    }
                    </div>
            }

            { pageType === "department" &&
                    <div className="department">
                    <div className="title">{this.state.items.name}</div>
                    <p className="subtitle">{this.state.items.code}</p>
                    </div>
            }

            </div>

            { pageType !== "department" &&
                <div id="banner-score">
                <ScoreboxRow
                value="Average"
                instructor={this.state.average_ratings.rInstructorQuality}
                course={this.state.average_ratings.rCourseQuality}
                difficulty={this.state.average_ratings.rDifficulty}
                num_sections={this.state.items.num_sections}/>

                <ScoreboxRow
                value="Recent"
                instructor={this.state.recent_ratings.rInstructorQuality}
                course={this.state.recent_ratings.rCourseQuality}
                difficulty={this.state.recent_ratings.rDifficulty}
                num_sections={this.state.items.num_sections_recent}/>
                </div>
            }

            { pageType === "department" &&
                    <div className="department-content">
                    <div id="row-select-placeholder">
                    <object type="image/svg+xml" data="/static/image/selectrow.svg">
                    <img alt="Select Row" src="/static/image/selectrow.svg" />
                    </object>
                    <div id="row-select-text">Select a few rows to begin comparing courses.</div>
                    </div>
                    <div id="row-select-chart-container">
                    <canvas id="row-select-chart"></canvas>
                    <button id="chart-clear" className="btn btn-action">Clear Chart</button>
                    </div>
                    </div>
            }

            { pageType === "course" &&
                    <p className="desc">{this.state.items.description}</p>
            }

            </div>
        );
    }
}

export default InfoBox;
