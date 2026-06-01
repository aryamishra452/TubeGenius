from utils.database import *

initialize_database()

save_history(
    video_url="https://youtube.com/test",
    video_title="Sample Video",
    summary_type="Detailed Notes",
    content="Testing database..."
)

print(get_all_history())