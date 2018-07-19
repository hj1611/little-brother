import os

UPLOAD_FOLDER = '/home/zopadev/little-brother'


def compute_activity_score(camera_id):
    # if the previous one is there compute and save a score. Delete previous and rename current to previous
    previous_directory = UPLOAD_FOLDER + '/' + camera_id + '/previous/'
    current_directory = UPLOAD_FOLDER + '/' + camera_id + '/current/'

    if not has_previous_image(previous_directory):
        os.makedirs(previous_directory)
        for filename in os.listdir(current_directory):
            os.rename(current_directory + filename, previous_directory + filename)

    if has_previous_image(previous_directory):
        # compute and save score
        for filename in os.listdir(previous_directory):
            os.remove(previous_directory + filename)
        for filename in os.listdir(current_directory):
            os.rename(current_directory + filename, previous_directory + filename)
    return


def has_previous_image(previous_directory):
    return os.path.exists(previous_directory)