import React, { Component } from 'react';
import InfoBox from './InfoBox';
import ScoreBox from './ScoreBox';
import NavBar from './NavBar';
import DetailsBox from './DetailsBox';
import SearchBar from './SearchBar';
import { api_review_data, api_live } from './api';


class ReviewPage extends Component {
    constructor(props) {
        super(props);

        const pageInfo = this.getPageInfo();

        this.state = {
            type: pageInfo[0],
            code: pageInfo[1],
            data: null,
            error: null,
            instructor_code: null,
            live_data: null
        };

        this.navigateToPage = this.navigateToPage.bind(this);
        this.getReviewData = this.getReviewData.bind(this);
        this.showInstructorHistory = this.showInstructorHistory.bind(this);
        this.loadPage = this.loadPage.bind(this);
        this.getReviewData();
    }

    componentDidMount() {
        window.onpopstate = this.loadPage;
    }

    componentWillUnmount() {
        window.onpopstate = null;
    }

    getPageInfo() {
        const pageInfo = window.location.pathname.substring(1).split("/");

        if (["course", "instructor", "department"].indexOf(pageInfo[0]) === -1) {
            pageInfo[0] = null;
            pageInfo[1] = null;
        }

        return pageInfo;
    }

    loadPage() {
        const pageInfo = this.getPageInfo();
        this.setState({
            type: pageInfo[0],
            code: pageInfo[1],
            data: null
        }, this.getReviewData);
    }

    getReviewData() {
        if (this.state.type && this.state.code) {
            api_review_data(this.state.type, this.state.code).then((result) => {
                if (result.error) {
                    this.setState({
                        error: result.error
                    });
                }
                else {
                    this.setState({
                        data: result
                    });
                }
            }).catch(() => {
                this.setState({
                    error: "Could not retrieve review information at this time. Please try again later!"
                });
            });
        }

        if (this.state.type === "course") {
            api_live(this.state.code).then((result) => {
                this.setState({ live_data: result });
            });
        }
        else {
            this.setState({ live_data: null });
        }
    }

    navigateToPage(value) {
        var loc;
        if (value.url) {
            loc = value.url.split("/");
        }
        else {
            loc = ["course", value];
        }
        this.setState({
            type: loc[0],
            code: loc[1],
            data: null,
            instructor_code: null
            },
            this.getReviewData
        );
        window.history.pushState(null, "Penn Course Review", window.location.protocol + "//" + window.location.host + "/" + loc[0] + "/" + loc[1]);
    }

    showInstructorHistory(instructor) {
        this.setState({
            instructor_code: instructor
        });
    }

    // TODO: implement cart page
    // TODO: implement footer (add feedback and logout links)
    // TODO: implement faq, about
    render() {
        if (!this.state.code) {
            return (
                <div id="content" className="row">
                    <div className="col-md-12">
                        <div id="title">
                            <img src="/static/image/logo.png" alt="Penn Course Review" /> <span className="title-text">Penn Course Review</span>
                        </div>
                    </div>
                    <SearchBar onSelect={this.navigateToPage} isTitle={true} />
                </div>
            );
        }

        return (
            <div>
                <NavBar onSelect={this.navigateToPage} />
                    { !this.state.error ? (this.state.data ?
                        <div id="content" className="row box-wrapper">
                            <div className="col-sm-12 col-md-4 sidebar-col">
                                <InfoBox type={this.state.type} code={this.state.code} data={this.state.data} live_data={this.state.live_data} />
                            </div>
                            <div className="col-sm-12 col-md-8 main-col">
                                <ScoreBox data={this.state.data} type={this.state.type} live_data={this.state.live_data} onSelect={this.state.type === "course" ? this.showInstructorHistory : this.navigateToPage} />
                                { this.state.type === "course" && <DetailsBox course={this.state.code} instructor={this.state.instructor_code} /> }
                            </div>
                        </div>
                        :
                        <div style={{ textAlign: 'center', padding: 45 }}>
                            <i className='fa fa-spin fa-cog fa-fw' style={{ fontSize: '150px', color: '#aaa' }}></i>
                            <h1 style={{ fontSize: '2em', marginTop: 15 }}>Loading {this.state.code}...</h1>
                        </div>) :
                        <div style={{ textAlign: 'center', padding: 45 }}>
                            <i className='fa fa-exclamation-circle' style={{ fontSize: '150px', color: '#aaa' }}></i>
                            <h1 style={{ fontSize: '1.5em', marginTop: 15 }}>{this.state.error}</h1>
                        </div>
                    }
            </div>
        );
    }
}


export default ReviewPage;
