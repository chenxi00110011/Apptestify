import os

for i in range(1):
    # os.system('pytest -vs -k test_change_playback_time_seek_to_recorded_segment')
    os.system('pytest --tb=short --color=yes -m cloud')
