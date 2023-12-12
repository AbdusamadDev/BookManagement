import os
import time

count = 0
while True:
    os.system("git add --all")
    os.system(f'git commit -m "CLI commit {str(count)}"')
    count += 1
    os.system("git push -u origin main")
    time.sleep(60 * 3)

