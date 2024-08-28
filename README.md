# Ghost Bulk Publisher

This script converts Markdown files to HTML and publishes them as posts using the Ghost Admin API.

## Description

The `Ghost Bulk Publisher` script automates the process of converting Markdown files located in a specified directory into HTML format and then publishing these as posts on a Ghost blog. It uses Pandoc for the conversion and the Ghost Admin API for publishing.

## Environment Setup

### Prerequisites

- Node.js (version 20.x or higher)
- Pandoc (to convert Markdown to HTML)
- A Ghost blog with API access

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Captainsalem/ghost-bulk-publisher
   cd ghost-bulk-publisher
   ```

1. Create a `.env` file in the root directory of the project and add your Ghost API credentials:

   ```javascript
   GHOST_API_URL=https://your-ghost-blog.com
   GHOST_ADMIN_API_KEY=your-ghost-admin-api-key
   POST_STATUS=draft
   ```

   - `GHOST_API_URL`: The URL of your Ghost blog.
   - `GHOST_ADMIN_API_KEY`: The Admin API key from your Ghost installation.
   - `POST_STATUS`: (Optional) The default status for the posts. Possible values are `draft` or `published`.

## How to Use

1. Prepare your Markdown files:

   - Organize your Markdown files in the `src` directory.
   - Use subdirectories to categorize your posts by tags (each subdirectory name will be used as a tag).

   Example structure:

   ```javascript
   data/
   ├── tag1/
   │   ├── post1.md
   │   └── post2.md
   └── tag2/
       ├── post3.md
       └── post4.md
   ```

2. Run the script:

   ```
   node bulk_uploader.js
   ```

   The script will:

   - Convert each Markdown file to HTML using Pandoc.
   - Publish each converted file as a post on your Ghost blog.
   - Apply the directory name as a tag to the post.

3. Check your Ghost blog to verify that the posts have been published.
## Docx to MD

You will also find a python script that offers multithreaded docx to markdown conversion. This is useful if you have a bulk of docx files you wish to convert to md before publishing.

-- This is an edge case and not required for publishing articles. 

## License

This script is licensed under the MIT License. See the [LICENSE](https://github.com/Captainsalem/LICENSCE) file for more details.