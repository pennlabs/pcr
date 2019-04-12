import React, { Component } from 'react';
import InfoBox from './InfoBox';
import ScoreTable from './ScoreTable';
import NavBar from './NavBar';
import DetailsBox from './DetailsBox';
import { api_review_data } from './api';


class ReviewPage extends Component {
    constructor(props) {
        super(props);

        const pageInfo = window.location.pathname.substring(1).split("/");

        if (["course", "instructor", "department"].indexOf(pageInfo[0]) === -1) {
            pageInfo[0] = null;
            pageInfo[1] = null;
        }

        this.state = {
            type: pageInfo[0],
            code: pageInfo[1],
            data: null,
            error: null
        };

        this.navigateToPage = this.navigateToPage.bind(this);
        this.getReviewData = this.getReviewData.bind(this);
        this.getReviewData();
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
    }

    navigateToPage(value) {
        var loc = value.url.split("/");
        this.setState({
            type: loc[0],
            code: loc[1],
            data: null
            }, 
            this.getReviewData
        );
        window.history.pushState(null, "Penn Course Review", window.location.protocol + "//" + window.location.host + "/" + loc[0] + "/" + loc[1]);
    }

    render() {
        return (
            <div>
                <NavBar onSelected={this.navigateToPage} />
                    { !this.state.code ? <div>Enter a course, instructor, or department in the box above!</div> : !this.state.error ? (this.state.data ?
                        <div id="content" className="row box-wrapper">
                            <div className="col-sm-12 col-md-4 sidebar-col">
                                <InfoBox type={this.state.type} code={this.state.code} data={this.state.data} />
                            </div>
                            <div className="col-sm-12 col-md-8 main-col">
                                <ScoreTable data={this.state.data} type={this.state.type} />
                                { this.state.type === "course" && <DetailsBox /> }
                            </div>
                        </div>
                        :
                        <div style={{ textAlign: 'center', padding: 45 }}>
                            <i className='fa fa-spin fa-cog fa-fw' style={{ fontSize: '150px', color: '#aaa' }}></i>
                            <h1 style={{ fontSize: '2em', marginTop: 15 }}>Loading...</h1>
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
