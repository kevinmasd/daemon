/**
 *  Generic Peripheral.
 *  propTypes:
 *    name: Sensor name (String),
 *    peripheralType: Sensor type (String),
 *    id: Unique id (String),
 *    value: Sensor value (Number)
 *  defaultProps:
 *    peripheralType: 'peripheralType was undefined'
 */

import React from 'react';
import NameEdit from './NameEdit';

export default class GenericPeripheral extends React.Component {
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
            {this.props.value}
          </h4>
        </div>
      </div>
    );
  }
}
GenericPeripheral.propTypes = {
  name: React.PropTypes.string,
  peripheralType: React.PropTypes.string,
  id: React.PropTypes.string,
  value: React.PropTypes.number
};
GenericPeripheral.defaultProps = {peripheralType: 'peripheralType was undefined'};
