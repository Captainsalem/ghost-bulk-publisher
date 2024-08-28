/*
 * Copyright (c) 2024 Captain Salem
 * All rights reserved.
 *
 * Description: Script to convert Markdown files to HTML and publish them as posts using the Ghost Admin API.
 * Language: JavaScript
 * Type: Script
 * 
 * This script is licensed under the MIT License.
 * For full license terms, see the LICENSE file in the root directory of this project.
 *
 * Author: Captain Salem -> https://cloudenv.io
 * [S@mS3p!0l]
 * 
 */

// Required modules
const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');
const dotenv = require('dotenv');
const GhostAdminApi = require('@tryghost/admin-api');

// Load environment variables from .env file
dotenv.config();

// Initialize Ghost Admin API client
const api = new GhostAdminApi({
    url: process.env.GHOST_API_URL,
    key: process.env.GHOST_ADMIN_API_KEY,
    version: 'v5.0'
});

/**
 * Logs the status of environment variables, useful for debugging.
 */
function logEnvironmentVariables() {
    console.log('GHOST_API_URL:', process.env.GHOST_API_URL);
    console.log('GHOST_ADMIN_API_KEY:', process.env.GHOST_ADMIN_API_KEY ? 'Present' : 'Missing');
}

/**
 * Converts a Markdown file to HTML using Pandoc.
 * @param {string} filePath - The full path to the Markdown file.
 * @returns {Promise<string|null>} The converted HTML content, or null if an error occurs.
 */
async function convertMarkdownToHtml(filePath) {
    console.log('Converting file:', filePath);
    try {
        const htmlContent = execSync(`pandoc -f markdown -t html "${filePath}"`, { encoding: 'utf-8' });
        return htmlContent.trim();
    } catch (error) {
        console.error(`Error converting file to HTML: ${error.message}`);
        return null;
    }
}

/**
 * Publishes a post to Ghost using the Admin API.
 * @param {string} title - The title of the post.
 * @param {string} html - The HTML content of the post.
 * @param {string} tag - The tag to associate with the post.
 * @param {string} status - The status of the post ('draft', 'published', etc.).
 * @returns {Promise<void>}
 */
async function publishPost(title, html, tag, status) {
    console.log(`Publishing post: "${title}" with status: "${status}"`);
    try {
        const response = await api.posts.add({
            title,
            html,
            tags: [{ name: tag }],
            status
        }, { source: 'html' });

        console.log(`Post "${title}" published successfully.`, JSON.stringify(response));
    } catch (error) {
        console.error(`Failed to publish post "${title}": ${error.message}`);
    }
}

/**
 * Traverses the source directory, converts Markdown files to HTML, and publishes them as posts.
 * @returns {Promise<void>}
 */
async function publishPosts() {
    const srcDir = path.resolve(__dirname, 'src');
    console.log('Source Directory:', srcDir);

    const status = process.env.POST_STATUS || 'draft';

    try {
        const tagDirs = await fs.readdir(srcDir, { withFileTypes: true });
        const directories = tagDirs.filter(dirent => dirent.isDirectory());

        console.log('Tag Directories:', directories.map(dir => dir.name));

        for (const tagDir of directories) {
            const tag = tagDir.name;
            const tagPath = path.join(srcDir, tag);
            const mdFiles = (await fs.readdir(tagPath)).filter(file => file.endsWith('.md'));

            console.log(`Markdown Files in ${tagPath}:`, mdFiles);

            for (const mdFile of mdFiles) {
                const title = path.parse(mdFile).name;
                const markdownPath = path.join(tagPath, mdFile);
                const htmlData = await convertMarkdownToHtml(markdownPath);

                if (htmlData) {
                    await publishPost(title, htmlData, tag, status);
                }
            }
        }
    } catch (error) {
        console.error('Error processing data directory:', error.message);
    }
}

// Main execution
(async () => {
    logEnvironmentVariables();
    await publishPosts();
})();
