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
    }

    componentDidMount() {
        fetch("http://localhost:8000/api/display/" + encodeURIComponent(this.state.type) + "/" + encodeURIComponent(this.state.code) + "?token=public")
            .then(res => res.json())
            .then((result) => {
                this.setState(state => ({
                    data: result
                }));
            });
    }

    render() {
        return (
            <div>
                <NavBar />
                    { this.state.data ?
                        <div id="content" className="row box-wrapper">
                            <div className="col-sm-12 col-md-4 sidebar-col">
                                <InfoBox type={this.state.type} code={this.state.code} data={this.state.data} />
                            </div>
                            <div className="col-sm-12 col-md-8 main-col">
                                <ScoreTable data={this.state.data} />
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
