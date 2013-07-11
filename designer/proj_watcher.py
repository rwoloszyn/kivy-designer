import sys, os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class ProjectEventHandler(FileSystemEventHandler):
    '''ProjectEventHandler is the event handler for any event occurring on
       its current directory. See FileSystemEventHandler in python-watchdog 
       documentation for more information.
    '''
    def __init__(self, observer, proj_watcher):
        self._observer = observer
        self._proj_watcher = proj_watcher
        super(ProjectEventHandler, self).__init__()

    def on_any_event(self, event):
        '''An event handler for any event.
        '''
        self._proj_watcher.dispatch_proj_event(event)


class ProjectWatcher(object):
    '''ProjectWatcher is responsible for watching any changes in
       project directory. It will call self._callback whenever there
       are any changes. It can currently handle only one directory at
       a time.
    '''
    def __init__(self, callback):
        super(ProjectWatcher, self).__init__()
        self.proj_event = None
        self._observer = Observer()
        self._event_handler = ProjectEventHandler(self._observer, self)
        self._callback = callback

    def start_watching(self, project_dir):
        '''To start watching project_dir.
        '''
        self._project_dir = project_dir
        self._observer = Observer()
        self._event_handler = ProjectEventHandler(self._observer, self)
        self._watch = self._observer.schedule(self._event_handler,
                                              project_dir, recursive=True)
        self._observer.start()

    def stop_current_watching(self):
        '''To stop watching currently watched directory.
        '''
        self.stop()

    def on_project_modified(self, *args):
        pass

    def dispatch_proj_event(self, event):
        '''To dispatch event to self._callback.
        '''
        self.proj_event = event
        #Do not dispatch event if '.designer' is modified
        if '.designer' not in event.src_path:
            self._callback(event)

    def start(self):
        self._observer.start()
    
    def stop(self):
        '''To stop watching currently watched directory. This will also call
           join() on the thread created by Observer.
        '''
        try:
            self._observer.stop()
            self.join()
        except:
            pass

    def join(self):
        self._observer.join()
        
