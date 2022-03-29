# encoding: utf-8

import datetime
import re
import subprocess
import sys
import time
import pytz
from workflow import Workflow, ICON_CLOCK, ICON_NOTE

reload(sys)
sys.setdefaultencoding('utf-8')

LOGGER = None # Set in the main...
MAX_SECONDS_TIMESTAMP = 10000000000
MAX_SUBSECONDS_ITERATION = 4


def get_divisor(timestamp):
    for power in range(MAX_SUBSECONDS_ITERATION):
        divisor = pow(1e3, power)
        if timestamp < MAX_SECONDS_TIMESTAMP * divisor:
            return int(divisor)
    return 0


def convert(timestamp, converter):
    divisor = get_divisor(timestamp)
    LOGGER.debug('Found divisor [{divisor}] for timestamp [{timestamp}]'.format(**locals()))
    if divisor > 0:
        seconds, subseconds = divmod(timestamp, divisor)
        subseconds_str = '{:.9f}'.format(subseconds / float(divisor))
        return converter(seconds).isoformat() + subseconds_str[1:].rstrip('0').rstrip('.')


def add_epoch_to_time_conversion(wf, timestamp, descriptor, converter):
    converted = convert(timestamp, converter)
    description = descriptor + ' time for ' + str(timestamp)
    if converted is None:
        raise Exception('Timestamp [{timestamp}] is not supported'.format(**locals()))
    else:
        LOGGER.debug('Returning [{converted}] as [{description}] for [{timestamp}]'.format(**locals()))
        wf.add_item(title=converted, subtitle=description, arg=converted, valid=True, icon=ICON_CLOCK)

def add_time_to_epoch_conversion(wf, dt, descriptor, epoch, multiplier):
    converted = str(int((dt - epoch).total_seconds() * multiplier))
    description = descriptor + ' epoch for ' + str(dt)
    wf.add_item(title=converted, subtitle=description, arg=converted, valid=True, icon=ICON_CLOCK)

def attempt_conversions(wf, input, prefix=''):
    try:
        timestamp = int(input)
        add_epoch_to_time_conversion(wf, timestamp, '{prefix}Local'.format(**locals()), datetime.datetime.fromtimestamp)
        add_epoch_to_time_conversion(wf, timestamp, '{prefix}UTC'.format(**locals()), datetime.datetime.utcfromtimestamp)
    except:
        LOGGER.debug('Unable to read [{input}] as an epoch timestamp'.format(**locals()))

    try:
        match = re.match('(\d{4}-\d{2}-\d{2})?[ T]?((\d{2}:\d{2})(:\d{2})?(.\d+)?)?', str(input))
        date, time, hour_minutes, seconds, subseconds = match.groups()
        if date or time:
            dt = datetime.datetime.strptime(
                (date or datetime.datetime.now().strftime('%Y-%m-%d')) + ' ' +
                (hour_minutes or '00:00') + (seconds or ':00') +
                ('.000000' if subseconds is None else subseconds[:7]),
                '%Y-%m-%d %H:%M:%S.%f'
            )
            dt_utc = pytz.utc.localize(dt)
            dt_local = pytz.timezone('Asia/Singapore').localize(dt)
            epoch = datetime.datetime.fromtimestamp(0, tz=pytz.utc)

            add_time_to_epoch_conversion(wf, dt_local, '{prefix}Local s'.format(**locals()), epoch, 1)
            add_time_to_epoch_conversion(wf, dt_local, '{prefix}Local ms'.format(**locals()), epoch, 1e3)

            add_time_to_epoch_conversion(wf, dt_utc, '{prefix}UTC s'.format(**locals()), epoch, 1)
            add_time_to_epoch_conversion(wf, dt_utc, '{prefix}UTC ms'.format(**locals()), epoch, 1e3)
    except Exception as e:
        LOGGER.debug('Unable to read [{input}] as a human-readable datetime'.format(**locals()))


def add_current(wf, unit, multiplier):
    converted = str(int(time.time() * multiplier))
    description = 'Current timestamp ({unit})'.format(**locals())
    LOGGER.debug('Returning [{converted}] as [{description}]'.format(**locals()))
    wf.add_item(title=converted, subtitle=description, arg=converted, valid=True, icon=ICON_NOTE)


def get_clipboard_data():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    exit_code = p.wait()
    return p.stdout.read()


def main(wf):
    if len(wf.args) > 0:
        query = wf.args[0]
        if query:
            LOGGER.debug('Got query [{query}]'.format(**locals()))
            attempt_conversions(wf, query)

    clipboard = get_clipboard_data()
    if clipboard:
        LOGGER.debug('Got clipboard [{clipboard}]'.format(**locals()))
        attempt_conversions(wf, clipboard, prefix='(clipboard) ')

    add_current(wf, 's', 1)
    add_current(wf, 'ms', 1e3)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    LOGGER = wf.logger
    sys.exit(wf.run(main))
