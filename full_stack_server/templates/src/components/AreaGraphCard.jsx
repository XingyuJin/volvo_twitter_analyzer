import React, {Component} from 'react';
import '../assets/css/Dashboard.css';
import {Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis,} from 'recharts';
import {Form} from 'react-bootstrap';


class AreaGraphCard extends Component {


    constructor(props) {
        super(props);
        this.state = {
            models: {
                "s60": true,
                "xc90": false,
                "xc40": false
            }
        }
    }

    toggle = (event) => {
        var models = this.state.models;
        const target = event.target
        const checked = target.checked
        const name = target.name
        models[name] = checked;
        this.setState({
            models: models,
        })
    }

    render() {

        const {graphData, type, isModel} = this.props;
        const {models} = this.state;

        const selectModel = () => {
            return (
                <div className="model-form">
                    <Form>
                        <Form.Check
                            type="checkbox"
                            id="checkbox"
                            label="s60"
                            name="s60"
                            className="model-form-checkbox"
                            checked={models["s60"]}
                            onChange={e => this.toggle(e)}
                        />
                        <Form.Check
                            type="checkbox"
                            id="checkbox"
                            label="xc90"
                            name="xc90"
                            className="model-form-checkbox"
                            checked={models["xc90"]}
                            onChange={e => this.toggle(e)}
                        />
                        <Form.Check
                            type="checkbox"
                            id="checkbox"
                            label="xc40"
                            name="xc40"
                            className="model-form-checkbox"
                            checked={models["xc40"]}
                            onChange={e => this.toggle(e)}
                        />
                    </Form>
                </div>
            )
        }

        return (
            <div className="card-big-container">
                <div className="card-title">
                    {type}
                    {selectModel()}
                </div>
                <ResponsiveContainer width={310} height="75%" className="area-chart-container">
                    <AreaChart data={graphData} margin={{top: 5, bottom: 5, left: -30}}>
                        <XAxis dataKey="key" interval={0} padding={{right: 10}}/>
                        <YAxis/>
                        <Tooltip/>
                        {!models["s60"] ? null : <Area type='monotone' dataKey="s60" stroke="#A6CEE3" fill="#A6CEE3"/>}
                        {!models["xc90"] ? null :
                            <Area type='monotone' dataKey="xc90" stroke="#A7E1AD" fill="#A7E1AD"/>}
                        {!models["xc40"] ? null :
                            <Area type='monotone' dataKey="xc40" stroke="#D9CCDF" fill="#D9CCDF"/>}
                    </AreaChart>
                </ResponsiveContainer>

            </div>
        )

    }

}


export default AreaGraphCard;
