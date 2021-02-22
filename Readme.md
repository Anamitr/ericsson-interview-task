# Ericsson Python interview task

This project was created as part of the recruitment process for Internship in
AI/Machine Learning area (Python) at Ericsson

Its goal was to automate user notification task concerning scheduled service 
support days. Input data is grafik.xlsx file. On a given weekday program is 
supposed to send emails on appropriate addresses informing about following week 
service days and their total number.

Script prints emails to be sent, writes them to ./out dir and also keeps them 
available if you use an interactive mode.

As far as I understand configuring email server and actually sending emails 
wasn't part of the task.

### Usage
####Data preprocess
Before actual notification service is run, input file must be preprocessed. Use 
following flag:
```bash
python service_shift_notifier.py --unmerge-cells
```
#### Periodical execution
To execute every chosen weekday you can setup a cronjob. Example (Monday):
```bash
0 7 * * 1 python path/to/script/service_shift_notifer.py
```
Or execute every day and use script ```NOTIFICATION_WEEK_DAY ```variable to 
set a day.

#### Test
Script can be tested using ```--date-stub```, ```-d``` argument with following 
date format:
```bash
python service_shift_notifier.py --date-stub=2021-02-08
```

#### Email sending simulation
Setup debuggin email server. On this console you will observe sending emails:
```bash
python -m smtpd -n -c DebuggingServer localhost:1025
```
Run script with ```-s``` or ```--simulate-email-send``` flag. Example:
```bash
python service_shift_notifier.py -d 2021-02-08 --simulate-email-send
```
### Script execution description
####Data import

First job is to unmerge merged cells. Otherwise, during import to pandas, their 
info would be lost.
File .xls is converted to .xlsx using libreoffice cmd. Unmerging 
is performed by following external project:
[unMergeExcelCell](https://github.com/zanran/unMergeExcelCell). It needs to be 
cloned to this project main directory.

Next, dataframes containing MoC and Engineer info are loaded (name, email, phone) 
and whole year calendar properly red. Based on current date the next week's 
calendar is extracted.

#### Generating emails

Based on next week's calendar and engineer list, proper emails are generated. 
EmailModel class was created to contain required information like email target 
(recipient), title and content. As requested, it contains list of weekdays with 
assigned service and their total number.

### Example output

Example output is quite long, so refer to out/example_out.txt.
Also output for 2021-02-08 was included.
