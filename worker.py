import errno
import logging
import os
import signal
import sys
import time

from BDSS.background import start_job_loop
from daemon import daemon, pidfile

containing_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, containing_dir)
from BDSS.background import start_job_loop

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

class WorkerDaemonError(Exception):
    pass

class WorkerDaemon():

    def __init__(self):
        self.pidfile_path = os.path.join(containing_dir, 'worker.pid')
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

        try:
            self.ctx.open()
        except pidfile.AlreadyLocked:
            raise WorkerDaemonError('PID file %s already locked' % self.pidfile_path)



        logging.basicConfig(
            filename=os.path.join(containing_dir, 'BDSS', 'worker.log'),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG,
            filemode='a'
        )

        stdout_logger = logging.getLogger('STDOUT')
        stderr_logger = logging.getLogger('STDERR')

        sys.stdout = StreamToLogger(stdout_logger, logging.INFO)
        sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)

        os.umask(022)

        start_job_loop()

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
    if len(sys.argv) < 2 or not sys.argv[1] in ('start', 'stop', 'restart'):
        print >> sys.stderr, 'Usage: worker.py start|stop|restart'
        sys.exit(1)

    action = sys.argv[1]

    d = WorkerDaemon()
    if action == 'start':
        d.start()
    elif action == 'stop':
        d.stop()
    elif action == 'restart':
        d.restart()
