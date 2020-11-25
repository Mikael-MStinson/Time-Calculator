# Time Calculator
 A small tool for calculating total time and deductable time spent on a job

## Application and Usage

Used to calculate the total time spent on a job/project even if the time spent is fragmented.

For example, the input ```1000 on 1100 230 on 300 415 on 430``` will return the following report ```start time: 1000, end time: 1145, deduct: 0, total: 1.75```

As of now, the end time is calculated by taking the total time and adding it to the start time.
In the previous example, even though work was complete at 4:30 pm, the end time for the time entry is calculated as 11:45 am, because that is 1.75 hours after 10:00 am.

### Deducting Time
The program will also take into account deductable time, which is marked by the keyword "off".

For example, if you spent 9:00 am to 9:30 am driving, 9:30 am to 10:30 am working, and 10:30 am to 11:00 am driving, and time spent drivign is deductable, you can enter the following ```900 off 930 on 1030 off 1100``` and you will get the following report ```start time: 900, end time: 1100, deduct: 1.0, total: 1.0```

### Formatting Your Time Entries

When entering your time, any time stamps should be entered as a 3-4 digit number. For example ```10:30 am``` should be entered as ```1030```. You do not need to convert to millitary time when entering time stamps after 12:00 pm. Entering ```100``` for 1:00 pm works fine.

A time entry will always consist of 2 timestamps and a deductability marker, arranged like this ```1000 on 1100``` or like this ```230 off 345```.
For successive time entries, the common timestamps can be combined into one. Example ```1000 on 1100 1100 off 1200``` can be written as ```1000 on 1100 off 1200```.

### Understanding the Report

The returned report will consist of 4 elements.
* the start time - this is the first timestamp in the sequence
* the end time - this is the first timestamp in the sequence plus the total time spent on the job. both duductable and billable.
* time deducted - this is the total amount of time deducted from the time entry.
* billable time - this is the total time minus time deducted. this serves as a checksum for when these values are entered into your time tracking program.
