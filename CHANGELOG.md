# Changelog

## v2.3.1 - 19.06.2018
 * Transfer targets are configurable
 * Reorganized information shown

## v2.3.0 - 28.05.2018
 * Changed Id of parent from 'StudyInstanceUID' to 'PatientID - AccessionNumber'
 * Moved StudyInstanceUID to series level
 * Added query possibility for the Patient age

## v2.2.0 - 27.04.2018
 * Added excel export

## v2.1.3 - 21.03.2018
 * Added resend on the status page
 * Removed automatically refresh
 * More result size information is shown and collapse/expand all

## v2.1.2 - 15.03.2018
 * Added API for search
 * changed again filtering for children (now done with fq aka filter)

## v2.1.1 - 13.03.2018
 * Clear SeriesDescriptionFilter if not set
 * RisReport should have now the '*'

## v2.1.0 - 09.03.2018
 * Added SeriesDescription search and filter functionality
 * Increased child limit to 200 (default 10)

## v2.0.0 - 27.02.2018
 * Ris integrated
 * Download reports integrated

## v1.5.2 - 24.10.2017
 * Downloading a series creates a additional file called `download_done.txt`
   to indicate the finishing of a download. Needed for consumers of meta to
   know when a download is finished.

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