import sys
import time

from runtimeUtil import *

# TODO:
# 0. modify self.state to acually store (name, value) pairs
class StateManager(object):

  """input is a multiprocessing.Queue object to support multiple
  processes requesting state data
  """
  def __init__(self, badThingsQueue, inputQueue, runtimePipe):
    self.initRobotState()
    self.badThingsQueue = badThingsQueue
    self.input = inputQueue
    self.commandMapping = self.makeCommandMap()
    # map process names to pipes
    self.hibikeMapping = self.makeHibikeMap()
    self.hibikeResponseMapping = self.makeHibikeResponseMap()
    self.processMapping = {PROCESS_NAMES.RUNTIME: runtimePipe}

  def makeCommandMap(self):
    commandMapping = {
      SM_COMMANDS.RESET : self.initRobotState,
      SM_COMMANDS.ADD : self.addPipe,
      SM_COMMANDS.GET_VAL : self.getValue,
      SM_COMMANDS.SET_VAL : self.setValue,
      SM_COMMANDS.STUDENT_MAIN_OK : self.studentCodeTick,
      SM_COMMANDS.CREATE_KEY : self.createKey,
      SM_COMMANDS.SEND_ANSIBLE : self.send_ansible,
      SM_COMMANDS.RECV_ANSIBLE: self.recv_ansible,
      SM_COMMANDS.GET_TIME : self.getTimestamp
    }
    return commandMapping

  def makeHibikeMap(self):
    hibikeMapping = {
      HIBIKE_COMMANDS.ENUMERATE: self.hibikeEnumerateAll,
      HIBIKE_COMMANDS.SUBSCRIBE: self.hibikeSubscribeDevice,
      HIBIKE_COMMANDS.READ: self.hibikeReadParams,
      HIBIKE_COMMANDS.WRITE: self.hibikeWriteParams
    }
    return hibikeMapping

  def makeHibikeResponseMap(self):
    hibikeResponseMapping = {
      HIBIKE_RESPONSE.DEVICE_SUBBED: self.hibikeResponseDeviceSubbed
    }
    return hibikeResponseMapping

  def initRobotState(self):
    self.state = {
     "incrementer" : [2, 0],
     "int1" : [112314, 0],
     "float1": [987.123, 0],
     "bool1" : [True, 0],
     "dict1" : [{"inner_dict1_int" : [555, 0], "inner_dict_1_string": ["hello", 0]}, 0],
     "list1" : [[[70, 0], ["five", 0], [14.3, 0]], 0],
     "string1" : ["abcde", 0],
     "runtime_meta" : [{"studentCode_main_count" : [0, 0]}, 0],
     "hibike" : [{"device_subscribed" : [0, 0]}, 0]
    }

  def addPipe(self, processName, pipe):
    self.processMapping[processName] = pipe
    pipe.send(RUNTIME_CONFIG.PIPE_READY.value)

  def createKey(self, keys):
    currDict = self.state
    path = []
    for key in keys:
      try:
        if key not in currDict:
          currDict[key] = [{}, 0]
        path.append(currDict[key])
        currDict = currDict[key][0]
      except TypeError:
        error = StudentAPIKeyError(
          "key '{}' is defined, but does not contain a dictionary.".format(key))
        self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(error)
        return
    currTime = time.time()
    for item in path:
      item[1] = currTime
    self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(None)

  def getValue(self, keys):
    result = self.state
    try:
      for i, key in enumerate(keys):
        result = result[key][0]
      self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(result)
    except:
      error = StudentAPIKeyError(self.dictErrorMessage(i, keys, result))
      self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(error)

  def setValue(self, value, keys):
    currDict = self.state
    try:
      path = []
      for i, key in enumerate(keys[:-1]):
        path.append(currDict[key])
        currDict = currDict[key][0]
      if len(keys) > 1:
        i += 1
      else:
        i = 0
      if keys[i] not in currDict:
        raise Exception
      path.append(currDict[keys[i]])
      currDict[keys[i]][0] = value
      currTime = time.time();
      for item in path:
        item[1] = currTime
      self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(value)
    except:
      error = StudentAPIKeyError(self.dictErrorMessage(i, keys, currDict))
      self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(error)

  def send_ansible(self):
    self.processMapping[PROCESS_NAMES.UDP_SEND_PROCESS].send(self.state)

  def recv_ansible(self, new_state):
    self.state["bytes"][0] = new_state

  def getTimestamp(self, keys):
    currDict = self.state
    timestamp = 0
    try:
      for i, key in enumerate(keys):
        currDict, timestamp = currDict[key]
      self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(timestamp)
    except:
      error = StudentAPIKeyError(self.dictErrorMessage(i, keys, result))
      self.processMapping[PROCESS_NAMES.STUDENT_CODE].send(error)

  def studentCodeTick(self):
    self.state["runtime_meta"][0]["studentCode_main_count"][0] += 1

  def hibikeEnumerateAll(self, pipe):
    pipe.send([HIBIKE_COMMANDS.ENUMERATE, []])

  def hibikeSubscribeDevice(self, pipe, uid, delay, params):
    pipe.send([HIBIKE_COMMANDS.SUBSCRIBE, [uid, delay, params]])

  def hibikeWriteParams(self, pipe, uid, param_values):
    pipe.send([HIBIKE_COMMANDS.WRITE, [uid, param_values]])

  def hibikeReadParams(self, pipe, uid, params):
    pipe.send([HIBIKE_COMMANDS.READ, [uid, params]])

  def hibikeResponseDeviceSubbed(self, uid, delay, params):
    self.state["hibike"][0]["device_subscribed"][0] += 1

  def dictErrorMessage(self, erroredIndex, keys, currDict):
    keyChain = ""
    i = 0
    while (i < erroredIndex):
      # Assembles a string representation of the dictionary indexing that occurred
      keyChain += "['" + keys[i] + "']" if (type(keys[i]) is str) else "[" + str(keys[i]) + "]"
      i += 1
    keys = [None] if len(keys) == 0 else keys
    erroredKey = "'" + keys[erroredIndex] + "'" if type(keys[erroredIndex]) is str else str(keys[erroredIndex])
    errorMessage = "KeyError: key " + erroredKey + " not found in state" + keyChain + "\n"

    if type(currDict) is dict:
      # Converts all available keys to strings, and adds commas and spaces at the end of each element
      availableKeys = [("'" + el + "', " if type(el) is str else str(el) + ", ") for el in currDict.keys()]
      if len(availableKeys) > 0:
        # Removes comma and space from last item in availableKeys
        availableKeys[-1] = availableKeys[-1][:-2]
      errorMessage += "Available keys in state" + keyChain + ": " + "".join(availableKeys)
    else:
      errorMessage += "state" + keyChain + " is of type " + type(currDict).__name__

    return errorMessage

  def start(self):
    # TODO: Make sure request is a list/tuple before attempting to access
    # And that there are the correct number of elements
    while True:
      request = self.input.get(block=True)
      cmdType = request[0]
      args = request[1]

      if(len(request) != 2):
        self.badThingsQueue.put(BadThing(sys.exc_info(), "Wrong input size, need list of size 2", event = BAD_EVENTS.UNKNOWN_PROCESS, printStackTrace = False))
      elif cmdType in self.commandMapping:
        command = self.commandMapping[cmdType]
        command(*args)
      elif cmdType in self.hibikeMapping:
        command = self.hibikeMapping[cmdType]
        command(self.processMapping[PROCESS_NAMES.HIBIKE], *args)
      elif cmdType in self.hibikeResponseMapping:
        command = self.hibikeResponseMapping[cmdType]
        command(*args)
      else:
        self.badThingsQueue.put(BadThing(sys.exc_info(), "Unknown process name: %s" % (request,), event = BAD_EVENTS.UNKNOWN_PROCESS, printStackTrace = False))
