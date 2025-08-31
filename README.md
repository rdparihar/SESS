# Issues

## TMS
* [View](http://localhost:8000/timesheets/view/) --
  1. Change clander type to look like crete TMS
  2. Show Status column  in view TMS  (approved/pending)
  3. View TMS - enable/disable - edit/delete - tms entries based on status
* [Create](http://localhost:8000/timesheets/create/) - Create Page
  1. Show Status column  in Create TMS  (approved/pending)
  2. Create TMS - enable disable - tms entries based on status
  3. View TMS - enable/disable - edit/delete - tms entries based on status


## EMS
* [View](http://localhost:8000/employee/) --
    1. Employee profile  
    2. bla
* [Create](http://localhost:8000/employee/) --
  1. Other Details of Employee for detailed profiling 
  2. bla
 

## LMS
* [View](http://localhost:8000/employee/) --
  1. bla
  2. bla
* [Create](http://localhost:8000/employee/) --
  1. bla
  2. bla
  
## 02-08-2018
1. add links/dropdown for lms create/view
2. disable edit/delete in lms list based on status (enable only if status=pending)

## Testing

Install dependencies and run the Django test suite:

```bash
pip install -r requirements.txt
cd sess_dev
python manage.py test
```

The test suite covers key models and views in the timesheets, ems, and lms apps.
