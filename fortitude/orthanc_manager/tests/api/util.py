DICOM_FILE_PATH = './fortitude/orthanc_manager/tests/data/CT_small.dcm'


def make_dicom_data() -> bytes:
    with open(DICOM_FILE_PATH, 'rb') as file:
        return file.read()


def make_bad_dicom_data() -> bytes:
    return b'bad-dicom-data'
