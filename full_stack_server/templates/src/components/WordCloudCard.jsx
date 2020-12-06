import React, { PureComponent } from 'react';
import '../assets/css/Dashboard.css';
import ReactWordcloud from "react-wordcloud";
import { words } from "../assets/dummytext.js";

class WordCloudCard extends PureComponent {


  render() {

    const { words, type } = this.props;
    // const { type } = this.props;
    const options = {
      rotations: 2,
      rotationAngles: [-90, 0],
    };
    const callbacks = {
      getWordTooltip: () => console.log(),
    }

    return (
      <div>
      {!words ? null :
      <div className="card-big-container">
        <div className="card-title"> {type}</div>
        <div className="wordcloud-container">
          <ReactWordcloud className="wordcloud" callbacks={callbacks} words={words}/>
        </div>
      </div>}
      </div>
    )
  }
}


export default WordCloudCard;
