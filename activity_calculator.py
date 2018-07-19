import os

from image_analyser import load_image_to_array, detect_by_subtraction

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))


def compute_activity_score(camera_id):
    # if the previous one is there compute and save a score. Delete previous and rename current to previous
    previous_directory = UPLOAD_FOLDER + '/' + camera_id + '/previous/'
    current_directory = UPLOAD_FOLDER + '/' + camera_id + '/current/'

    if not has_previous_image(previous_directory):
        os.makedirs(previous_directory)
        for filename in os.listdir(current_directory):
            os.rename(current_directory + filename, previous_directory + filename)

    if has_previous_image(previous_directory):

        for filename in os.listdir(previous_directory):
            img0 = load_image_to_array(previous_directory + filename, res=(400, 300))
            os.remove(previous_directory + filename)
        for filename in os.listdir(current_directory):
            img1 = load_image_to_array(current_directory + filename, res=(400, 300))
            os.rename(current_directory + filename, previous_directory + filename)
        result = detect_by_subtraction(img0, img1)
        return result
    return


def has_previous_image(previous_directory):
    return os.path.exists(previous_directory)