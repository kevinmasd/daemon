/**
 *  Motor.
 *  propTypes:
 *   name: Motor name (String)
 *   id: Unique id (String)
 *   value: Speed from -100 to 100 (Number)
 */

import React from 'react';
import {ProgressBar} from 'react-bootstrap';
import NameEdit from './NameEdit';
import numeral from 'numeral';

export default class Motor extends React.Component {
  render() {
    return (
    <div style={{overflow: 'auto'}}>
      <div style={{overflow: 'auto', width: '100%'}}>
        <h4 style={{float: 'left'}}>
          <NameEdit name={this.props.name} id={this.props.id} />
          <small>
            Motor
          </small>
        </h4>
        <h4 style={{float: 'right'}}>
          {numeral(this.props.value).format('+0.00')}
        </h4>
      </div>
      <ProgressBar now={Math.abs(this.props.value)}></ProgressBar>
    </div>
    );
  }
}
Motor.propTypes = {
  name: React.PropTypes.string,
  id: React.PropTypes.string,
  value: React.PropTypes.number
};