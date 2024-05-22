import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # URL of the Instagram page you want to scrape
url = 'https://www.instagram.com/'

# Initialize the Chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

# Open the Instagram page
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Instagram username and password
username = 'your_username'
password = 'your_password'


# Find the username and password fields, and login button
username_field = driver.find_element(By.XPATH,
                                     "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input")
password_field = driver.find_element(By.XPATH,
                                     "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input")
login_button = driver.find_element(By.XPATH,
                                   "/html/body/div[2]/div/div/div[2]/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button/div")

# Enter your username and password
username_field.send_keys(username)
password_field.send_keys(password)

# Click the login button
login_button.click()

time.sleep(5)

# URL of the Instagram account you want to scrape followers from
account_url = f"https://www.instagram.com/{username}/"

# Go to the Instagram account's followers page
driver.get(account_url)

# Wait for the page to load
time.sleep(10)

# Click on the followers button
followers_button = driver.get(f'https://www.instagram.com/{username}/followers/?next=%2F')

# Wait for the followers modal to load
time.sleep(10)

# Scroll down to load more followers
followers_list = driver.find_element(By.NAME, ' followers')
followers_count = len(followers_list.find_elements(By.CLASS_NAME, 'x1dm5mii'))

# Initialize scroll height
last_height = driver.execute_script("return arguments[0].scrollHeight", followers_list)

while True:
    # Scroll down to bottom
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", followers_list)

    # Wait to load page
    time.sleep(5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight", followers_list)
    if new_height == last_height:
        break
    last_height = new_height

# Find all follower usernames
followers = followers_list.find_elements(By.CLASS_NAME, 'x1dm5mii')

# Extract follower usernames
follower_usernames = [follower.text.split('\n')[0] for follower in followers]

# Print follower usernames
for username in follower_usernames:
    print(username)

# Save follower usernames to a text file
with open('follower_usernames.txt', 'w') as f:
    for username in follower_usernames:
        f.write(username + '\n')

# Go to the Instagram account's following page
driver.get(account_url)

# Wait for the page to load
time.sleep(7)

# Click on the following button
following_button = driver.get(f'https://www.instagram.com/your_username/following/?next=%2F')

# Wait for the following modal to load
time.sleep(7)

# Scroll down to load more following
following_list = driver.find_element(By.CLASS_NAME, '_aano')
following_count = len(following_list.find_elements(By.CLASS_NAME, 'x1dm5mii'))

# Initialize scroll height
last_height = driver.execute_script("return arguments[0].scrollHeight", following_list)

while True:
    # Scroll down to bottom
    driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", following_list)

    # Wait to load page
    time.sleep(7)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight", following_list)
    if new_height == last_height:
        break
    last_height = new_height

# Find all following usernames
following = following_list.find_elements(By.CLASS_NAME, 'x1dm5mii')

# Extract following usernames
following_usernames = [follow.text.split('\n')[0] for follow in following]

# Save following usernames to a text file
with open('following_usernames.txt', 'w') as f:
    for username in following_usernames:
        f.write(username + '\n')

# Find users who are not followed back
non_followers = [user for user in following_usernames if user not in follower_usernames]

# Save non-followers to a text file
with open('non_followers.txt', 'w') as f:
    for username in non_followers:
        f.write(username + '\n')

# Load the list of non-followers
with open('non_followers.txt', 'r') as f:
    non_followers = f.read().splitlines()

count = 0
for username in non_followers:
    # Go to the user's profile
    driver.get(f'https://www.instagram.com/your_username')
    time.sleep(7)

    # Click on the unfollow button
    unfollow_button = driver.find_element(By.CLASS_NAME, '_acan')
    unfollow_button.click()
    time.sleep(5)

    # Confirm unfollow
    confirm_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[8]/div[1]/div/div/div[1]/div/div')
    confirm_button.click()
    time.sleep(2)
    count +=1
    print(f"Unfollowed {count} {username}")
    if count >= 199:
        print("Maximum unfollow limit reached. Pausing for one hour...")
        time.sleep(3600)  # Pause for one hour (3600 seconds)
        count = 0  # Reset the count after one hour
    else:
        time.sleep(36)

driver.quit()