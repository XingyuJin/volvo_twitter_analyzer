import React, {Component} from 'react';
import '../assets/css/Dashboard.css';

import profilePic from '../assets/img/profile.png'
import {Form} from 'react-bootstrap';


class TweetsCard extends Component {

    constructor(props) {
        super(props);
        this.state = {
            mode: "top_like_twitters",
        }
    }

    toggle = (event) => {
        var mode = this.state.mode;
        const target = event.target;
        const checked = target.checked;
        const value = target.value;
        this.setState({
            mode: value
        })
    }

    render() {

        const {tweets, type} = this.props;
        const {mode} = this.state;

        const selectMode = () => {
            return (
                <div className="mode-form">
                    <Form>
                        <Form.Check
                            type="radio"
                            label="Top Liked"
                            name="top_like_twitters"
                            value="top_like_twitters"
                            className="mode-form-checkbox"
                            checked={mode == "top_like_twitters"}
                            onChange={e => this.toggle(e)}
                        />
                        <Form.Check
                            type="radio"
                            label="Top Retweeted"
                            name="top_retweet_twitters"
                            value="top_retweet_twitters"
                            className="mode-form-checkbox"
                            checked={mode == "top_retweet_twitters"}
                            onChange={e => this.toggle(e)}
                        />
                        <Form.Check
                            type="radio"
                            label="Most Recent"
                            name="recent_twitters"
                            value="recent_twitters"
                            className="mode-form-checkbox"
                            checked={mode == "recent_twitters"}
                            onChange={e => this.toggle(e)}
                        />
                        <Form.Check
                            type="radio"
                            label="Most Influential"
                            name="top_influence_twitters"
                            value="top_influence_twitters"
                            className="mode-form-checkbox"
                            checked={mode == "top_influence_twitters"}
                            onChange={e => this.toggle(e)}
                        />
                    </Form>
                </div>
            )
        }

        return (
            <div>
                {!tweets[mode] ? null :
                    <div className="tweets-card-big-container">
                        <div className="tweets-card-title">
                            {type}
                            {selectMode()}
                        </div>
                        <div className="tweets-card-container">
                            {tweets[mode].map(item =>
                                <div className="tweets-entry">
                                    <img src={profilePic} className="tweets-pic"/>
                                    <div className="tweets-text">
                                        <div className="tweets-author"> {item.author} </div>
                                        <div> {item.content} </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>}
            </div>
        )
    }
}


export default TweetsCard;
