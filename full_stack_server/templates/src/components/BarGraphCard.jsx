import React, {Component} from 'react';
import '../assets/css/Dashboard.css';
import {Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis,} from 'recharts';


class BarGraphCard extends Component {


    constructor(props) {
        super(props);
        this.state = {}
    }


    render() {

        const {graphData, type} = this.props;

        return (
            <div>
                {!graphData ? null :
                    <div className="card-big-container">
                        <div className="card-title"> {type} </div>
                        <ResponsiveContainer width={310} height="75%" className="bar-chart-container">
                            <BarChart data={graphData} margin={{top: 5, bottom: 5, left: -30}}>
                                <XAxis dataKey="time" interval={2} padding={{right: 15}}/>
                                <YAxis/>
                                <Tooltip/>
                                <Bar dataKey="count" fill="#A6CEE3"/>
                            </BarChart>
                        </ResponsiveContainer>

                    </div>}
            </div>
        )

    }

}


export default BarGraphCard;
