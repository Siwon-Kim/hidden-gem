# :fork_and_knife: Hidden Gem: Share your favorite restaurants!
> "Hidden Gem" refers to hidden, lesser-known restaurants or eateries that one is familiar with. 
> Users can share information about their hidden gem by entering the URL containing the information and sharing it with others.

<img src="https://github.com/kangdh208/hiddengem/blob/master/26%EC%A1%B0-HiddenGem-compressed.gif" width="1000" height="500"/>

## 0. Deployment
Using AWS EC2
[Hidden Gem Website](http://100.25.193.224:5000/)

## 1. Project Period & Team members
 - 03/27/2023 ~ 03/30/2023
 - Onboarding Toy Project
 - Team members Information
<table class="tg">
<tbody>
    <tr>
        <td>강동현</td>
        <td>김시원</td>
        <td>김영기</td>
        <td>조우필</td>
    </tr>
    <tr>
        <td><a href="https://github.com/kangdh208">@kangdh208</a></td>
        <td><a href="https://github.com/Siwon-Kim">@Siwon-Kim</a></td>
        <td><a href="https://github.com/youngkikim14">@youngkikim14</a></td>
        <td><a href="https://github.com/Cho-woo-pil">@Cho-woo-pil</a></td>
    </tr>
</tbody>
</table>


## 2. Tech Stack
- back-end
  - Python
  - Flask
  - MongoDB

- front-end
  - javascript
  - jQuery
  - Bulma

- deploy
  - AWS EC2


## 3. User Stories
```
Users can share information about their hidden gem by entering the Mango Plate URL containing the information and sharing it with others.
Users can sign up, log in, and log out of the website.
Users can press the "like" button on the hidden gem post.
Users can delete their hidden gem posts.
```
- Login and Sign-up
   - Display Login and Sign-up buttons before logging in.
   - Display only the Logout button when logged in.
   - Logout option.

- Restaurant Sharing Feature on Main Page
   - Crawling of Mango Plate website through the link provided by the user.
   - Crawling of restaurant name, address, food category, and images.
   - User can attach comments and ratings.

- Like Button Feature
   - Like button for recommending restaurants.
   - Only one like per user is possible.
   - The button can be clicked again to cancel the like.소

- Delete Restaurant Post
   - Clicking the delete button removes the post.
   - Only the author has permission to delete the post.

- Edit restaurant post
  - Show the post edit toggle on the top when the edit button is clicked
  - Only the author has the authority to edit


## 4. Troubleshooting
### 1) Distinguishing Post Cards
* Task
   * When deleting a post, the corresponding card was being deleted.
* Issue
   * The system could not distinguish the cards and was deleting the first row on the database.
* Solution
   * Assign an ID value to the store API
   * Utilize the default _id generated by MongoDB
   * When using db.stores.find(), the _id is an ObjectId type and cannot be serialized to JSON directly, so it needs to be converted to a string with str(_id)
   * Assign the ID to the button tag's value attribute so that cards can be distinguished by ID
  
### 2) Implementation of Like button for each post

* Task
   * Each post should have a like button, and each user should be able to click it only once, and if clicked again, it should unlike it.
* Issue
   * When a user clicks the like button, it needs to be updated in the database, and the updated value needs to be fetched from the database to reflect the change on the webpage.
* Solution
   * Separate the functionality for displaying the number of likes on the webpage and updating the like count in the database.
   * Frontend: Simply update the number of likes displayed on the webpage when the user clicks the like button.
   * Backend: Store the updated like count in the database when the like button is clicked, and handle the case where a page reload is required to fetch the updated like count.

* Issue
   * The number of likes keeps increasing infinitely.
* Solution
   * Separate the cases of increasing and decreasing likes. 
   * Save the ID of the store that each user has liked in the DB, and determine whether they have liked the store based on this value. 
   * Decrease the number of likes if the user has already liked the store, and increase it if they are liking it for the first time. Also, save this information to the DB to handle cases where a reload is needed.

### 3) Post Editing

* Task 
   * Allow users to edit their comments and ratings on each post through a "Edit" button.
* Issue
   * Difficulty passing variables in the pop-up window.
* Solution
   * Implement a toggle on the update-box to call the edit page. 
   * Store the post's database ID as a global variable to be used in other functions. 
   * Implement the update function and pass the global ID, updated comment, and rating values to update the post.


### 4) Main Page and Login/Sign Up Page Integration
* Issue
   * The two backend files, app.py and account.py, were not integrated.
* Solution
   * Use Flask's blueprint to connect the two backend files. 
   * Divide the code into two backend files for convenient and organized coding and easy modification.

### 5) Further Improvements
* The HTML button styles for the Like button were hardcoded for each case during the reload.
* There is a 1-second delay when loading posts during the reload process.
* Implement duplicate checks for ID and nickname during sign-up.
* Add a save feature to the MySave page.
