/**
 * Simulates the robot runtime for development and testing purposes.
 *
 * NOTE: FakeRuntime is NOT transpiled or bundled by webpack like most of the other JS code
 * It will be run "as is" as a child-process of the rest of the application.
 * Some experimental features that are used elsewhere in Dawn may not be available here.
 */

const dgram = require('dgram');
const ProtoBuf = require('protobufjs');

const dawnBuilder = ProtoBuf.loadProtoFile('../ansible-protos/ansible.proto');
const DawnData = dawnBuilder.build('DawnData');
const runtimeBuilder = ProtoBuf.loadProtoFile('../ansible-protos/runtime.proto');
const RuntimeData = runtimeBuilder.build('RuntimeData');

const clientPort = 12346; // send port
const serverPort = 12345; // receive port
const hostname = 'localhost';
const client = dgram.createSocket('udp4');// sender
const server = dgram.createSocket('udp4'); // receiver
const SENDRATE = 1000;

/**
 * Handler to receive messages from Dawn.
 * We don't do anything besides decode it and print it out.
 */
server.on('message', (msg) => {
  // Decode and get the raw object.
  const data = DawnData.decode(msg).toRaw();
  console.log(`FakeRuntime received: ${JSON.stringify(data)}\n`);
});

server.bind(serverPort, hostname);

/**
 * Returns a random number between min and max.
 */
const randomFloat = (min, max) => ((max - min) * Math.random() + min);

/**
 * Generate fake data to send to Dawn
 */
const generateFakeData = () => [
  {
    robot_state: 0,
    sensor_data: [{
      device_type: 'MOTOR_SCALAR',
      device_name: 'Motor 1',
      value: randomFloat(-100, 100),
    },
      {
        device_name: 'Limit Switch 1',
        device_type: 'LimitSwitch',
        value: Math.round(randomFloat(0, 1)),
      }],
  },
];

/**
 * Send the encoded randomly generated data to Dawn
 */
setInterval(() => {
  const fakeData = generateFakeData();
  for (const item of fakeData) {
    const udpData = new RuntimeData(item);
    client.send(Buffer.from(udpData.toArrayBuffer()), clientPort, hostname);
  }
}, SENDRATE);
