from behave import *
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

dbx: dropbox.Dropbox


# Verify Dropbox API
@given('I have a valid access token')
def step_validate_token(context):
    global dbx
    access_token = 'sl.BfkmZ99REsrocNWMKdcqmIQItbJt2Rw0qmoFcRyUxcPxP3BZr3633NteZfX_Fk21FFkoeWAOgytMYaBz4adLOn' \
                   'Zky0OUiMzcjkQ4lqfip_3huRHbf66J-CLH5gB4_yi63D1EOrs'
    dbx = dropbox.Dropbox(access_token)
    assert dbx is not None


@then('I should get a valid response')
def step_validate_response(context):
    global dbx
    try:
        dbx.users_get_current_account()
    except:
        assert False


# Upload file to Dropbox
@when('I upload a file to Dropbox')
def step_upload_file(context):
    global dbx
    dbx.files_upload(b'Hello World!\nMarkiian Mazur', '/test.txt')


@then('I should see the file in my Dropbox folder')
def step_validate_file(context):
    global dbx
    files = dbx.files_list_folder('')
    assert 'test.txt' in [f.name for f in files.entries]


# Get file metadata
@then('I should see the file metadata')
def step_validate_metadata(context):
    global dbx
    metadata = dbx.files_get_metadata('/test.txt')
    assert metadata is not None


# Download file from Dropbox
@when('I download a file from Dropbox')
def step_download_file(context):
    global dbx
    dbx.files_download_to_file('./test.txt', '/test.txt')


@then('I should see the file in my local folder')
def step_validate_local_file(context):
    with open('./test.txt', 'rb') as f:
        assert f.read() == b'Hello World!\nMarkiian Mazur'


# Delete file from Dropbox
@when('I delete a file from Dropbox')
def step_delete_file(context):
    global dbx
    dbx.files_delete('/test.txt')


@then('I should not see the file in my Dropbox folder')
def step_validate_deleted_file(context):
    global dbx
    files = dbx.files_list_folder('')
    assert 'test.txt' not in [f.name for f in files.entries]


# Delete file from local folder
@given('I delete a file from my local folder')
def step_delete_local_file(context):
    import os
    os.remove('./test.txt')


@then('I should not see the file in my local folder')
def step_validate_deleted_local_file(context):
    import os
    assert not os.path.exists('./test.txt')
