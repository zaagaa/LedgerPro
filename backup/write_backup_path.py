import config

# Write backup path to a text file for use in .bat file
with open("backup_path.txt", "w") as f:
    f.write(config.BACKUP_DIR)
