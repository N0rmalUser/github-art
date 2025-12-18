1. Create a new empty repository on GitHub (do not add a README, .gitignore, or license — keep it completely empty).
2. Update the configuration in main.py (e.g., paths, GitHub name/email if needed), then run the script. It will create a local folder (github_art by default) with the generated commits dated in the past (2021 in your current code).
3. In the created folder, run these commands (replace <YourUsername> and <repo-name> with your actual details):
    ```shell 
    git remote add origin https://github.com/<YourUsername>/<repo-name>.git
    git branch -M main
    git push -u origin main --force
    ```
4. The art should appear in your contribution graph within 5–60 minutes (sometimes it takes up to an hour for GitHub to process and display older commits).