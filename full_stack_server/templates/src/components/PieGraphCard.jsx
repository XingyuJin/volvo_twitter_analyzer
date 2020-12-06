import React, { PureComponent } from 'react';
import '../assets/css/Dashboard.css';
import {
  PieChart,
  Pie,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Label,
} from 'recharts';


class PieGraphCard extends PureComponent {

  render() {

    const { graphData, type } = this.props;

    return (

      <div className="card-big-container">
        <div className="card-title">  {type} </div>
        <ResponsiveContainer width={290} height="65%" className="pie-chart-container">
          <PieChart >
            <Pie dataKey="value" nameKey="name" isAnimationActive={false} data={graphData} cx={120} cy={80} fill="#D9CCDF" label/>
            <Tooltip/>
         </PieChart>
       </ResponsiveContainer>
      </div>
    )

  }

}


export default PieGraphCard;
