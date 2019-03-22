import React, { Component } from 'react';
import InfoBox from './InfoBox';
import ScoreTable from './ScoreTable';
import NavBar from './NavBar';


class ReviewPage extends Component {
    constructor(props) {
        super(props)
    }


    render() {
        return (
            <div>
                <NavBar />
                <div id="content" className="row box-wrapper">
                    <div className="col-sm-12 col-md-4 sidebar-col">
                        <InfoBox />
                    </div>
                    <div className="col-sm-12 col-md-8 main-col">
                        <ScoreTable />
                    </div>
                </div>
            </div>
        );
    }
}


export default ReviewPage;
