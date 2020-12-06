import React, {Component} from 'react';
import SummaryCard from '../components/SummaryCard.jsx';
import BarGraphCard from '../components/BarGraphCard.jsx';
import PieGraphCard from '../components/PieGraphCard.jsx';
import {Form} from 'react-bootstrap';
import axios from 'axios';


class AccountAnalytics extends Component {

    constructor(props) {
        super(props);
        this.state = {
            mode: 3,
        };
    }

    componentDidMount = () => {
        this.getData(3);
    }

    getData = (mode) => {
        const url = "http://127.0.0.1:8000/api/account?duration_mode=" + mode;
        axios.get(url)
            .then(res => {
                    console.log(res.data);
                    this.setState({
                        data: res.data,
                        mode: mode,
                    })
                },
                error => console.log('An error occurred.', error),
            );
    }

    toggle = (event) => {
        const target = event.target;
        const value = target.value;
        console.log(value);
        this.getData(value);
    }

    render() {

        const {data, mode} = this.state;
        var regions = []
        if (data && data.region_dist_list) {
            data.region_dist_list.map(item => {
                regions.push({
                    name: item["country_code"],
                    value: item["percentage"]
                })
            })
        }

        const selectMode = () => {
            return (
                <Form inline className="aa-mode-form">
                    <Form.Check
                        inline
                        type="radio"
                        label="Year"
                        name="Year"
                        value={0}
                        className="aa-mode-form-checkbox"
                        checked={mode == 0}
                        onChange={e => this.toggle(e)}
                    />
                    <Form.Check
                        inline
                        type="radio"
                        label="Month"
                        name="Month"
                        value={1}
                        className="aa-mode-form-checkbox"
                        checked={mode == 1}
                        onChange={e => this.toggle(e)}
                    />
                    <Form.Check
                        inline
                        type="radio"
                        label="Week"
                        name="Week"
                        value={2}
                        className="aa-mode-form-checkbox"
                        checked={mode == 2}
                        onChange={e => this.toggle(e)}
                    />
                    <Form.Check
                        inline
                        type="radio"
                        label="Day"
                        name="Day"
                        value={3}
                        className="aa-mode-form-checkbox"
                        checked={mode == 3}
                        onChange={e => this.toggle(e)}
                    />
                </Form>
            )
        }


        return (
            <div>
                {selectMode()}
                {!data ? null :
                    <div className="AA-container">
                        <SummaryCard summary={data.summary_resp}/>
                        <PieGraphCard graphData={regions} type="Follower Region Distribution"/>
                        <BarGraphCard graphData={data.new_follower_count} type="New Retweets"/>
                        <BarGraphCard graphData={data.new_comment_count} type="New Comments"/>
                        <BarGraphCard graphData={data.new_like_count} type="New Likes"/>
                        <BarGraphCard graphData={data.new_mention_count} type="New Mentions"/>
                    </div>}
            </div>

        )
    }
}


export default AccountAnalytics;
