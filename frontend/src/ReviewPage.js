import React, { Component } from 'react';
import InfoBox from './InfoBox';
import ScoreTable from './ScoreTable';
import NavBar from './NavBar';
import DetailsBox from './DetailsBox';


class ReviewPage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            type: "course",
            code: "CIS-121",
            data: null
        };

        this.navigateToPage = this.navigateToPage.bind(this);
        this.getReviewData = this.getReviewData.bind(this);
        this.getReviewData();
    }

    getReviewData() {
        fetch("http://localhost:8000/api/display/" + encodeURIComponent(this.state.type) + "/" + encodeURIComponent(this.state.code) + "?token=public")
            .then(res => res.json())
            .then((result) => {
                this.setState({ 
                    data: result 
                });
            });
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
    }

    render() {
        return (
            <div>
                <NavBar onSelected={this.navigateToPage} />
                    { this.state.data ?
                        <div id="content" className="row box-wrapper">
                            <div className="col-sm-12 col-md-4 sidebar-col">
                                <InfoBox type={this.state.type} code={this.state.code} data={this.state.data} />
                            </div>
                            <div className="col-sm-12 col-md-8 main-col">
                                <ScoreTable data={this.state.data} />
                                { this.state.type === "course" && <DetailsBox /> }
                            </div>
                        </div>
                        :
                        <h1>Loading...</h1>
                    }
            </div>
        );
    }
}


export default ReviewPage;
