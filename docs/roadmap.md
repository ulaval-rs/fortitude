# Roadmap

## Frontend
### Users
- [ ] User Creation
- [ ] User login
- [ ] User retrieve token
- [ ] User Change password
- [ ] As admin, see audit

### DICOM server (both DICOMWeb and Orthanc)
- [ ] List servers
- [ ] Show server information
- [ ] Patients/Studies/Series/Instances explorer
- [ ] Images viewer (probably with https://github.com/ivmartel/dwv)


## Backend
### Users
- [x] User creation (POST `users/create`)
- [x] Retrieve an authentication token (POST `users/login`)
- [x] Activate User (through Django admin)
- [ ] User change password

### Audit
- [ ] Trace which user called which route in logs

### Orthanc
- [x] Add new Orthanc server connection (through Django admin)
- [x] Delete an Orthanc instance connection (through Django admin)
- [x] Get the list of configured Orthanc servers (GET `orthanc/servers/`)
- [ ] Get information about the Orthanc server (GET `orthanc/servers/<server_name>`)
- [x] Forward a GET call to an Orthanc server (GET `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [x] Forward a POST call to an Orthanc server (POST `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [x] Forward a DELETE call to an Orthanc server (DELETE `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [x] Forward a PUT call to an Orthanc server (PUT `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [x] Restrict access to Orthanc server (through the Django admin)
- [x] Give access per user to Orthanc server (through the Django admin)
- [ ] Configure modalities of an Orthanc server (through the Django admin)

### DICOMWeb
- [ ] Add new DICOMWeb server connection (through Django admin)
- [ ] Delete a DICOMWeb server connection (through Django admin)
- [ ] Get the list of configured DICOMWeb servers (GET `dicomweb/servers/`)
- [ ] Get information about the DICOMWeb server (GET `dicomweb/servers/<server_name>/`)
- [ ] Forward a GET call to a DICOMWeb server (GET `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Forward a POST call to a DICOMWeb server (POST `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Forward a DELETE call to a DICOMWeb server (DELETE `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Forward a PUT call to a DICOMWeb server (PUT `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Restrict access to DICOMWeb server (through the Django admin)
- [ ] Give access per user to DICOMWeb server (through the Django admin)


### Other
- [ ] Async forward calls
- [ ] Dockerize the application
- [ ] Make the app installable through PyPi