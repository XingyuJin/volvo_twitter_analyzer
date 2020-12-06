import React, { PureComponent } from 'react';
import '../assets/css/Dashboard.css';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Label,
} from 'recharts';


class LineGraphCard extends PureComponent {

  render() {

    const { graphData, type } = this.props;
    //
    // const CustomizedAxisTick = React.createClass({
    //   render () {
    //
    //     const values = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"];
    //
    //    	return (
    //     	<g>
    //         <text x={0} y={0} dy={16} textAnchor="end" fill="#666" transform="rotate(-35)">{values}</text>
    //       </g>
    //     );
    //   }
    // });

    return (

      <div className="card-big-container">
        <div className="card-title"> {type}</div>
        <ResponsiveContainer width={310} height="75%" className="line-chart-container">
          <LineChart data={graphData} margin={{top: 5, bottom: 5, left: -30}}>
            <XAxis tick={false}/>
            <YAxis />
            <Line type="monotone" dataKey="score" stroke="#A6CEE3" strokeWidth={2} dot={false}/>
            <Tooltip labelFormatter={label => `Day ${label}`}/>
         </LineChart>
       </ResponsiveContainer>
      </div>
    )

  }

}

class CustomizedAxisTick extends PureComponent {
  render() {
    const values = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"];
    return (
      <g>
        <text x={-20} y={0} dy={0} dx={0} textAnchor="end" fill="#666" transform="rotate(-35)">{values}</text>
      </g>
    )
  }
}



export default LineGraphCard;
