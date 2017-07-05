# Changelog

## v1.5.1 - 05.06.2017
 * Paging was working only for one patient and not e.g. 100

## v1.4.1 - 09.05.2017
 * Faster select all on whole page and patients
 * StudyDate is formatted now 20171231 -> 31.12.2017

## v1.4.0 - 11.02.2017
 * Added RIS Report urls

## v1.3.2 - 06.02.2017
 * Added feedback on transfer

## v1.3.1 - 03.02.2017
 * Fixed transfer to teamplay

## v1.3.0 - 31.01.2017
 * Added solr_api

## v1.2.0 - xx.01.2017
 * Now a HTTP post is sent to the backend, HTTP get still works. This was
   changed because a lot of the time, people come with lists of hundreds of
   patients to search for. With a 'GET' the urls get too long. That's why
   it was changed from 'GET' to 'POST'

## v1.1.3 - 14.12.2016
 * Download notification
 * Concat js files
 * More informationen on download status

## v1.1.2 - 09.12.2016
Download is now structured by patient_id, accession_number and series_number

## v1.1.1 - 06.12.2016
Increased group limit from 10 to 100

## v1.1.0 - 04.12.2016
Download progress visible

## v1.0.1 - 27.11.2016
New minor version

## v1.0.0 21.11.2016
Initial version