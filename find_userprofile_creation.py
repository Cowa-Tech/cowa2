import os

# Define the keywords to search for
keywords = [
    'UserProfile.objects.create',  # Direct creation
    'UserProfile.objects.get_or_create',  # Creation with get_or_create
    'UserProfile(',  # Creating UserProfile via constructor
    'create_user_profile',  # Call to the create_user_profile function
    'save_user_profile',  # Call to the save_user_profile function
    'post_save',  # Signal that might trigger creation
    'profile.save(',  # Saving a profile, possibly after creation
]

# Set the root directory to the current directory (where the script is located)
root_dir = os.path.dirname(os.path.abspath(__file__))

def search_files_for_keywords(root_dir, keywords):
    # Walk through the directory tree
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Only check Python files
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines):
                            for keyword in keywords:
                                if keyword in line:
                                    print(f"Found '{keyword}' in {file_path} on line {i + 1}")
                                    print(f"    -> {line.strip()}")
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

if __name__ == "__main__":
    search_files_for_keywords(root_dir, keywords)
