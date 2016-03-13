/**
 *  Boolean sensor.
 *  propTypes:
 *    name: Sensor name (String),
 *    peripheralType: Sensor type (String),
 *    id: Unique id (String),
 *    value: Sensor value (Number)
 */

import React from 'react';
import NameEdit from './NameEdit';

export default class BooleanSensor extends React.Component {
  /* If Limit Switch, show Open and Closed instead of 1 and 0.
   */
  formatBoolean(sensor) {
    if (sensor.peripheralType == "LimitSwitch") {
      return (sensor.value) ? "Open" : "Closed";
    } else {
      return sensor.value;
    };
  }
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
            {this.formatBoolean(this.props)}
          </h4>
        </div>
      </div>
    );
  }
}
BooleanSensor.propTypes = {
  name: React.PropTypes.string,
  peripheralType: React.PropTypes.string,
  id: React.PropTypes.string,
  value: React.PropTypes.number
};
