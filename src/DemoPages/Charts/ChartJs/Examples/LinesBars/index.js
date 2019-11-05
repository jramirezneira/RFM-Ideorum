import React, {Fragment} from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group';
//import LineExample from '../line';
//import LineExample2 from '../line2';
//import BarExample from '../bar';
//import HorizontalBarExample from '../horizontalBar';
//import MixExample from '../mix';

import {
    Row, Col,
    Card, CardBody,
    CardTitle
} from 'reactstrap';

export default class ChartJsLinesBars extends React.Component {
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

                </ReactCSSTransitionGroup>
            </Fragment>
        );
    }
}
