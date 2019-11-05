import React, {Fragment} from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
import DoughnutExample from '../doughnut';
//import PieExample from '../pie';
//import DynamicDoughnutExample from '../dynamicDoughnut';
//import RadarExample from '../radar';
//import PolarExample from '../polar';

import {
    Row, Col,
    Card, CardBody,
    CardTitle
} from 'reactstrap';

export default class ChartJsCircular extends React.Component {
    render() {
        return (
            <Fragment>
                <ReactCSSTransitionGroup
                    component="div"
                    transitionName="TabsAnimation"
                    transitionAppear={true}
                    transitionAppearTimeout={0}
                    transitionEnter={false}
                    transitionLeave={false}>

                        <DoughnutExample/>



                </ReactCSSTransitionGroup>
            </Fragment>
        );
    }
}
