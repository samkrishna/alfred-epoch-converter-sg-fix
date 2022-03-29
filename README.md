![icon](https://raw.githubusercontent.com/snooze92/alfred-epoch-converter/master/icon.png)

# Alfred epoch converter (fix for Singapore local timestamps)

## Changes from the original repo

- Removed µs and ns values
- Uses `pytz` package to convert local datetime to epoch correctly (timestamp is hardcoded to Asia/Singapore)
  - In Singapore, the original repo's timestamp is off by 30min (eg. when typing 2022-01-01 00:00:00, it returns 1640968200 for the local timestamp instead of 1640966400). This is because Singapore's timezone changed from GMT+07:30 to GMT+08:00 in 1982 ([source](https://en.wikipedia.org/wiki/Singapore_Standard_Time#History)), so the `(dt - datetime.datetime.fromtimestamp(0)).total_seconds()` computation is off by 30min.

Makes it easy to work with epoch timestamps!

## Convert epoch timestamp to human-readable time

You can easily type an epoch timestamp with any precision and convert it into a human readable string:
![convert-epoch](https://raw.githubusercontent.com/snooze92/alfred-epoch-converter/master/imgs/convert-epoch.gif)

Select the option you want, press enter, and the value is copied into your clipboard:
![convert-epoch-notification](https://raw.githubusercontent.com/snooze92/alfred-epoch-converter/master/imgs/convert-epoch-notification.gif)

If you have an epoch timestamp in your clipboard, no need to type or paste it. The workflow will recognize it for you:
![convert-clipboard-epoch](https://raw.githubusercontent.com/snooze92/alfred-epoch-converter/master/imgs/convert-clipboard-epoch.gif)

## Convert human-readable time to epoch timestamp

You can easily type a human-readable time and convert it into an epoch timestamp with any precision:
![convert-time](https://raw.githubusercontent.com/snooze92/alfred-epoch-converter/master/imgs/convert-time.gif)

Select the option you want, press enter, and the value is copied into your clipboard:
![convert-time-notification](https://raw.githubusercontent.com/snooze92/alfred-epoch-converter/master/imgs/convert-time-notification.gif)

If you have a human-readable time in your clipboard, no need to type or paste it. The workflow will recognize it for you:
![convert-clipboard-time](https://raw.githubusercontent.com/snooze92/alfred-epoch-converter/master/imgs/convert-clipboard-time.gif)

## Download & installation

You can download the workflow file from [GitHub](https://github.com/snooze92/alfred-epoch-converter/releases/latest), then double-click to install.
The workflow is also released on [Packal](http://www.packal.org/workflow/epoch-converter-0).

## Usage

- `ts <timestamp>` will guess the precision and display as human readable, both Local and GMT
- `ts <YYYY-mm-dd>` will give epoch timestamps on that date, at midnight
- `ts <YYYY-mm-dd> <HH:MM:SS>` will give epoch timestamps on that date, at that time (both space and T are supported as separator, seconds are optional)
- `ts <HH:MM:SS>` will give epoch timestamps for today, at that time (seconds are optional)
- `ts` will display the current time as a UNIX epoch timestamp with different precisions, as well as attempt converting what is in your clipboard
