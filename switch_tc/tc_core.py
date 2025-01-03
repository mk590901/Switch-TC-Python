from queue import Queue
from typing import Callable, Dict, List, Optional, Union

class IQHsmStateMachineHelper :
    def get_state(self) -> str :
        raise NotImplementedError

    def set_state(self, state: str) :
        raise NotImplementedError

    def executor(self, event: str) -> Optional['ThreadedCodeExecutor'] :
        raise NotImplementedError

class QHsmHelper(IQHsmStateMachineHelper) :
    def __init__(self, state: str) :
        self._state = state
        self.runner = Runner(self)
        self._container: Dict[str, ThreadedCodeExecutor] = {}

    def insert(self, state: str, event: str, executor: 'ThreadedCodeExecutor') :
        self._container[create_key(state, event)] = executor

    def post(self, event: str, data: Optional[object] = None) :
        self.runner.post(event, data)

    def executor(self, event: str) -> Optional['ThreadedCodeExecutor'] :
        key = create_key(self._state, event)
        if key not in self._container :
            print(f'runSync.error: {self._state}->{event}')
            return None
        executor = self._container.get(key)
        return executor

    def get_state(self) -> str :
        return self._state

    def set_state(self, state: str) :
        self._state = state

class EventWrapper :
    def __init__(self, event: str, data: Optional[object]) :
        self._event = event
        self._data = data

    def data(self) -> Optional[object]:
        return self._data

    def event(self) -> str:
        return self._event

class Runner:
    def __init__(self, helper: Optional[IQHsmStateMachineHelper]) :
        self._events_queue: Queue[EventWrapper] = Queue()
        self._helper = helper

    def post(self, event: str, data: Optional[object] = None) :
        self._events_queue.put(EventWrapper(event, data))
        while not self._events_queue.empty() :
            event_wrapper = self._events_queue.get()
            executor = self._helper.executor(event_wrapper.event()) if self._helper else None
            if executor :
                executor.execute_sync(data)

class ThreadedCodeExecutor :
    def __init__(self, helper: IQHsmStateMachineHelper, target_state: str, functions: List[Callable]) :
        self._helper = helper
        self._target_state = target_state
        self._functions = functions
        self.runner = Runner(helper)

    def post(self, event: str, data: Optional[object] = None) :
        self.runner.post(event, data)

    def execute_sync(self, data: Optional[object] = None) :
        self._helper.set_state(self._target_state)
        for func in self._functions :
            func(data)

def create_key(s: str, t: str) -> str :
    return f'{s}.{t}'
