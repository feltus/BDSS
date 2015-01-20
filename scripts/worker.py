import errno
import logging
import os
import signal
import sys
import time

from daemon import daemon, pidfile

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, root_dir)

from BDSS.background import start_job_loop

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, name, path, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(fh)
        self.log_level = log_level

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

class WorkerDaemonError(Exception):
    pass

class WorkerDaemon():

    def __init__(self):
        if not os.path.exists(os.path.join(root_dir, 'tmp')):
            os.mkdir(os.path.join(root_dir, 'tmp'), 0755)
        self.pidfile_path = os.path.join(root_dir, 'tmp', 'worker.pid')
        self.ctx = daemon.DaemonContext()
        self.ctx.pidfile = pidfile.TimeoutPIDLockFile(self.pidfile_path, 5)

    def is_pidfile_stale(self):
        stale = False
        pid = self.ctx.pidfile.read_pid()
        if pid is not None:
            try:
                os.kill(pid, signal.SIG_DFL)
            except OSError, exc:
                if exc.errno == errno.ESRCH:
                    stale = True
        return stale

    def start(self):
        if self.is_pidfile_stale():
            self.ctx.pidfile.break_lock()

        if self.ctx.pidfile.is_locked():
            raise WorkerDaemonError('PID file %s already locked' % self.pidfile_path)

        try:
            self.ctx.open()
        except pidfile.AlreadyLocked:
            raise WorkerDaemonError('PID file %s already locked' % self.pidfile_path)

        if not os.path.exists(os.path.join(root_dir, 'log')):
            os.mkdir(os.path.join(root_dir, 'log'), 0755)

        sys.stdout = StreamToLogger('STDOUT', os.path.join(root_dir, 'log', 'worker.log'), logging.INFO)
        sys.stderr = StreamToLogger('STDERR', os.path.join(root_dir, 'log', 'worker.log'), logging.ERROR)

        start_job_loop()

    def run_foreground(self):
        if self.is_pidfile_stale():
            self.ctx.pidfile.break_lock()

        try:
            self.ctx.pidfile.acquire()
        except pidfile.AlreadyLocked:
            raise WorkerDaemonError('PID file %s already locked' % self.pidfile_path)

        try:
            start_job_loop()
        except KeyboardInterrupt:
            self.ctx.pidfile.release()

    def stop(self):
        if not self.ctx.pidfile.is_locked():
            raise WorkerDaemonError('PID file %s is not locked' % self.pidfile_path)

        if self.is_pidfile_stale():
            self.ctx.pidfile.break_lock()
        else:
            pid = self.ctx.pidfile.read_pid()
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError, exc:
                raise WorkerDaemonError('Failed to terminate process %d', pid)

    def restart(self):
        self.stop()
        self.start()

if __name__ == '__main__':
    if len(sys.argv) < 2 or not sys.argv[1] in ('start', 'stop', 'restart', 'fg'):
        print >> sys.stderr, 'Usage: worker.py start|stop|restart'
        sys.exit(1)

    action = sys.argv[1]

    d = WorkerDaemon()
    try:
        if action == 'start':
            d.start()
        elif action == 'fg':
            d.run_foreground()
        elif action == 'stop':
            d.stop()
        elif action == 'restart':
            d.restart()
    except WorkerDaemonError as e:
        print >> sys.stderr, e.message
