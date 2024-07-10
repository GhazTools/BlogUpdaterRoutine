"""
file_name = main.py
Created On: 2024/07/09
Lasted Updated: 2024/07/09
Description: _FILL OUT HERE_
Edit Log:
2024/07/09
    - Created file
"""

# STANDARD LIBRARY IMPORTS

# THIRD PARTY LIBRARY IMPORTS

# LOCAL LIBRARY IMPORTS
from src.vault_reader import VaultReader


if __name__ == "__main__":
    vault_reader = VaultReader()
    # print(vault_reader.extract_image_data())

    print("All images", len(vault_reader.images))
    print("Images not in db", len(vault_reader.images_to_add))

    print("All blog posts", len(vault_reader.blog_posts))
    print("Blog posts not in db", len(vault_reader.blog_posts_to_add))
