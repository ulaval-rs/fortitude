# Fortitude

Fortitude is an application that allows you to manage access to different DICOM servers, such as Orthanc

The idea came about after years of using the DICOM Orthanc server in a hospital.
Different projects involved different people (e.g. professionals, students).
Each of these projects has different ethical requirements
or required to have a connection to a non-research clinical PACS.
Access to the Orthanc server, therefore, had to be restricted by project and by user.
One solution is to dedicate one instance of the Orthanc server per project.
However, managing credentials and connections to other PACSs was becoming complex.
Fortitude focuses precisely on these issues.
Fortitude acts as a "layer" on top of Orthanc server instances.
It offers the functionality of account creation, account management,
certain Orthanc configurations management, and more!


### Project status: in development

The project is under development, and therefore should not be used.

## Roadmap

### Users
- [x] User creation (POST `users/create`)
- [x] Retrieve an authentication token (POST `users/login`)
- [x] Activate User (through Django admin)
- [ ] User change password
  
### Permissions Group
- [ ] Create new group
- [ ] Add User to group
- [ ] Dedicate a group per Orthanc server instance

### Orthanc support
- [x] Add new Orthanc server connection (through Django admin)
- [x] Delete an Orthanc instance connection (through Django admin)
- [x] Get the list of configured Orthanc servers (GET `orthanc/servers/`)
- [x] Forward a GET call to a specific Orthanc server (GET `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [x] Forward a POST call to a specific Orthanc server (POST `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [x] Forward a DELETE call to a specific Orthanc server (DELETE `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [x] Forward a PUT call to a specific Orthanc server (PUT `orthanc/servers/<server_name>/<orthanc_route_to_call>`)
- [ ] Configure modalities of a specific Orthanc server (through the Django admin)

### DICOMWeb support
- [ ] Add new DICOMWeb server connection (through Django admin)
- [ ] Delete a DICOMWeb server connection (through Django admin)
- [ ] Get the list of configured DICOMWeb servers (GET `dicomweb/servers/`)
- [ ] Forward a GET call to a specific DICOMWeb server (GET `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Forward a POST call to a specific DICOMWeb server (POST `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Forward a DELETE call to a specific DICOMWeb server (DELETE `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Forward a PUT call to a specific DICOMWeb server (PUT `dicomweb/servers/<server_name>/<dicomweb_route_to_call>`)
- [ ] Configure modalities of a specific DICOMWeb server (through the Django admin)
