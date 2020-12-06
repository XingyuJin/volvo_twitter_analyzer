import React, { PureComponent } from 'react';
import '../assets/css/Dashboard.css';



class SummaryCard extends PureComponent {


  render() {

    const { summary } = this.props;
    console.log(summary);
    return (
      <div className="card-big-container">
        <div className="card-title"> Account Summary </div>
        <div className="card-container">
            <p className="summary-card-entry">
              <span>Followers</span>
              <span>{summary.followers}</span>
            </p>
            <p className="summary-card-entry">
              <span>Following</span>
              <span>{summary.following}</span>
            </p>
            <p className="summary-card-entry">
              <span>Tweets</span>
              <span>{summary.tweets}</span>
            </p>
            <p className="summary-card-entry">
              <span>Likes</span>
              <span>{summary.likes}</span>
            </p>
        </div>
      </div>
    )
  }
}


export default SummaryCard;
