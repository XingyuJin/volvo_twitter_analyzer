import React, {Component} from 'react';
import PieGraphCard from '../components/PieGraphCard.jsx';
import LineGraphCard from '../components/LineGraphCard.jsx';
import AreaGraphCard from '../components/AreaGraphCard.jsx';
import TweetsCard from '../components/TweetsCard.jsx';
import WordCloudCard from '../components/WordCloudCard.jsx';
import axios from 'axios';


class MentionStatistics extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {}
        }
    };

    componentDidMount = () => {
        this.getData();
    }

    getData = () => {
        const url = "http://127.0.0.1:8000/api/mention";
        axios.get(url)
            .then(res => {
                    console.log(res.data);
                    this.setState({
                        data: res.data
                    })
                },
                error => console.log('An error occurred.', error),
            );
    }

    render() {
        const {data} = this.state;
        var scores = [];
        if (data && data.score_dist) {
            const score_dist = data.score_dist;
            scores = [
                {name: "positive", value: score_dist["positive"]},
                {name: "negative", value: score_dist["negative"]},
                {name: "neutral", value: score_dist["neutral"]},
            ]
        }
        var model_scores = [];
        if (data && data.model_score_list) {
            for (var i = 0; i <= 10; i++) {
                model_scores.push({
                    "key": i * 10,
                    "s60": data.model_score_list[0].score_dist[i],
                    "xc90": data.model_score_list[2].score_dist[i],
                    "xc40": data.model_score_list[4].score_dist[i],
                })
            }
        }

        var twitters = {};
        if (data && data.top_twitter) {
            data.top_twitter.forEach((item, i) => {
                if (item.type === "recent") {
                    twitters["recent_twitters"] = item.twitters;
                } else if (item.type === "top_like") {
                    twitters["top_like_twitters"] = item.twitters;
                } else if (item.type === "top_retweet") {
                    twitters["top_retweet_twitters"] = item.twitters;
                } else if (item.type === "top_influence") {
                    twitters["top_influence_twitters"] = item.twitters;
                }
            });
        }

        var words = [];
        if (data && data.word_cloud) {
            data.word_cloud.forEach((item, i) => {
                words.push({
                    text: item.word,
                    value: item.count,
                })
            });

        }

        var avg_scores = [];
        if (data && data.avg_score) {
            data.avg_score.forEach((item, i) => {
                avg_scores.push({
                    time: "Jan",
                    score: item
                })
            });

        }


        return (
            <div>
                {!data ? null :
                    <div className="AA-container">
                        <AreaGraphCard graphData={model_scores} type="Sentiment Score for Models"/>
                        <PieGraphCard graphData={scores} type="Sentiment Scores Distribution"/>
                        <LineGraphCard graphData={avg_scores} type="Sentiment Scores over Time"/>
                        <TweetsCard tweets={twitters} type="Latest Mentions"/>
                        <WordCloudCard words={words} type="Word Cloud"/>
                    </div>}
            </div>

        )
    }


}


export default MentionStatistics;
