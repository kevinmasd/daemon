/**
 *  Scalar Sensor.
 *  propTypes:
 *    name: Sensor name (String),
 *    peripheralType: Sensor type (String),
 *    id: Unique id (String),
 *    value: Sensor value (Number)
 */

import React from 'react';
import NameEdit from './NameEdit';
import numeral from 'numeral';

export default class ScalarSensor extends React.Component {
  render() {
    return (
    <div style={{overflow: 'auto'}}>
      <div style={{overflow: 'auto', width: '100%'}}>
        <h4 style={{float: 'left'}}>
          <NameEdit name={this.props.name} id={this.props.id} />
          <small>
            {this.props.peripheralType}
          </small>
        </h4>
        <h4 style={{float: 'right'}}>
          {numeral(this.props.value).format('0.00')}
        </h4>
      </div>
    </div>
    );
  }
}
ScalarSensor.propTypes = {
  name: React.PropTypes.string,
  peripheralType: React.PropTypes.string,
  id: React.PropTypes.string,
  value: React.PropTypes.number
}