# courseraider
A web app designed for students to provide feedback to teachers on a frequent basis.
## Problem
Students are unable to evaluate teachers when it matters, during the school year. 
## Solution
A simple web app that the teacher can use to gauge student interests.
* Students can simply scan the QR code or the dynamic link to fill out a survey created by the teacher beforehand. 
* Teacher can analyze trends and feedback using a simple dashboard. 
## Implmentation
Backend is written in flask.

Frontend is written in react.

## Video demo
<a href="https://youtu.be/jJWkSmi-GXw" target="_blank"><img src="http://img.youtube.com/vi/jJWkSmi-GXw/0.jpg" 
alt="IMAGE ALT TEXT HERE" width="480" height="360" border="10" /></a>

## API Endpoints
* POST Survey /api/v1/survey/submit/<class_id>/
* GET Survey /api/v1/survey/<class_id>/
* POST Question /api/v1/questions
* GET Question /api/v1/questions/<class_id>/
* GET BitLy Link (activates class’s survey) /v1/questions/activate/<class_id>/
* GET Deactivate /api/v1/questions/deactivate/<class_id>/
* GET Performance /api/v1/performance/<class_id>/
* GET All Performances /api/v1/performance/all
* GET Delete Questions /api/v1/questions/delete/<class_id>/
* GET QRCode /api/v1/questions/qrcode?url=<link>/
