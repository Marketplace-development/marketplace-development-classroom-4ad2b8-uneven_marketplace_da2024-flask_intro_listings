
# Plant Sitting

## Overview

Plant Sitting is a platform designed to help plant owners find reliable sitters to care for their plants while they're away. 
This project connects plant lovers in a supportive community, providing both owners and sitters with a seamless experience.

### More About US
-**Purpose of Your Platform**
The platform facilitates connections between plant owners (leavers) and plant caregivers (sitters) to ensure proper care for plants during the owner's absence. By focusing on plant sitting, it provides a niche service that addresses the specific needs of plant enthusiasts, offering peace of mind to plant owners.

-**Solving the Chicken-and-Egg Problem**
The platform uses dynamic badges, reviews, and personalized recommendations to attract early users. Gamified achievements (like "Cactus Whisperer") encourage participation, while incentives like fee waivers or featured listings for early adopters attract both leavers and sitters.

-**Unique Features**
Key differentiators include personalized badges rewarding user actions, dynamic pricing through proposals, and a rating system that builds trust. Additionally, geolocation-based listings and similarity recommendations enhance user experience, making it stand out from generic marketplaces.

-**Scalability**
The app is designed to scale by leveraging modular architecture, efficient database queries, and cloud-hosted databases like PostgreSQL. Features such as optimized search filters and a responsive interface ensure usability even with a growing user base and large transaction volumes.

-**Attracting Niche Users**
Niche users are engaged through plant-focused features like sensitivity categories, advanced care instructions, and eco-friendly badges. The leaderboard, based on reviews and activity, fosters community engagement, while tailored notifications keep users active on the platform.


## Features

### Core Features

- **User Accounts**
  - Register, login, and manage user profiles.
  - Profile details include custom user ratings and dynamically calculated badges.

- **Listings**
  - Create, edit, and delete plant care listings.
  - Specify plant care needs like species, water, light, and pruning requirements.

- **Dynamic Search**
  - Search and filter listings or users based on specific criteria.
  - Options for sorting by price or availability.

- **Chat System**
  - Private messaging system for communication between plant owners and sitters.

- **Booking System**
  - Book plant care services with options for custom price proposals.
  - Manage active and completed bookings seamlessly.

- **Review System**
  - Leave reviews for sitters or leavers after booking completion.
  - View reviews and ratings to foster community trust.

- **Leaderboard**
  - Highlight top sitters based on the number of reviews and average ratings.

- **Favorites**
  - Save favorite listings for quick access.

- **Dynamic Map**
  - Locate plant care listings on an interactive map.

- **Notifications**
  - Receive alerts for important actions, such as booking requests and custom price proposals.

- **Badges**
  - Gamify the user experience with dynamic badges based on user activity.

---

## Code Structure

### Main Methods

#### **Initialization**
- **`create_app()`**: Initializes the Flask application, database, and blueprints.
- **`load_user(user_id)`**: Loads a user for session management.

#### **Blueprints**
- **Main Blueprint** (`routes.py`)
  - Handles core functionalities like user registration, login, listings, bookings, and reviews.
- **Chat Blueprint** (`chat.py`)
  - Manages the chat widget and API for FAQs.

#### **Database Models**
- **User**: Represents user accounts with relationships to listings, bookings, and reviews.
- **Listing**: Stores details about plant care offerings.
- **Booking**: Tracks booking details, including sitter and leaver information.
- **Review**: Manages reviews and ratings for bookings.
- **Message**: Stores chat messages between users.
- **Favorite**: Tracks user-favorited listings.
- **Notification**: Alerts users about actions or events.
- **PriceProposal**: Tracks and manages custom price proposals for listings.

### Core Routes and Methods

#### **Home and Navigation**
- **`base()`**: Redirects to the login page for unauthenticated users.
- **`home()`**: Displays a list of active listings, with filtering and sorting options. Also shows unread notifications and messages for the logged-in user.
- **`about()`**: Displays an "About" page with information about the platform.

#### **User Management**
- **`register()`**: Handles user registration. Validates form input, ensures unique usernames, and saves new users to the database.
- **`login()`**: Authenticates users using their credentials and logs them in.
- **`logout()`**: Logs out the current user.
- **`account()`**: Displays the user's profile, including active and past bookings, active and booked listings, and badges.

#### **Listings**
- **`create_listing()`**: Allows users to create new plant care listings. Handles form validation, geolocation for addresses, and image uploads.
- **`edit_listing(listing_id)`**: Lets users update their existing listings, including re-geocoding addresses and updating pictures.
- **`confirm_delete_listing(listing_id)`**: Deletes a specific listing after confirmation.
- **`view_listing(listing_id)`**: Displays details of a specific listing, along with similar listings.
- **`search()`**: Searches users or listings based on keywords.

#### **Bookings**
- **`booking(listing_id)`**: Allows users to book a listing if it is available. Sends notifications to the listing owner upon booking.
- **`care_for_plant(listing_id)`**: Placeholder for additional functionality related to taking care of a plant.
- **`approve_price(listing_id)`**: Confirms a booking based on a price proposal.
- **`reject_price(listing_id)`**: Rejects a price proposal for a listing.

#### **Reviews**
- **`write_review(booking_id)`**: Enables users to write a review for a sitter or leaver after a completed booking.
- **`update_user_rating(user_id)`**: Recalculates a user's average rating based on reviews received.
- **`user_reviews(user_id)`**: Displays reviews about a specific user.

#### **Notifications**
- **`notifications()`**: Lists all notifications for the current user.
- **`mark_notification_read(notification_id)`**: Marks a specific notification as read.
- **`price_notifications()`**: Lists price-related notifications for the current user.
- **`answer_notification(notification_id)`**: Processes notifications related to price proposals.

#### **Favorites**
- **`favorites()`**: Displays the user's favorited listings.
- **`add_favorite(listing_id)`**: Adds or removes a listing from the user's favorites.
- **`remove_favorite(listing_id)`**: Explicitly removes a listing from the user's favorites.

#### **Chat between customers**
- **`chat_between_customers(listing_id)`**: Enables private messaging between a listing's leaver and interested sitters.
- **`messages()`**: Displays all messages received by the current user, grouped by sender and listing.

#### **Helpdesk Chat**
  - `chat_widget()`: Renders the FAQ chat widget.
  - `chat_api()`: Responds to user messages with predefined FAQ responses.

#### **Leaderboard**
- **`leaderboard()`**: Displays a leaderboard of users based on the number of reviews and average ratings.
- **`calculate_leaderboard()`**: Computes the leaderboard data.

#### **Price Proposals**
- **`propose_price(listing_id)`**: Allows users to propose a new price for a listing.
- **`approve_price(listing_id)`**: Confirms the booking with the proposed price.
- **`reject_price(listing_id)`**: Rejects a proposed price for a listing.

#### **API**
- **`api_listings()`**: Provides a JSON API for retrieving all listings except those belonging to the current user.

---

## Layout and Styling

- **HTML Templates**
  - Stored in the `/templates` directory.
  - Organized for modular reuse of components like navigation bars and forms.

- **CSS Styling**
  - Custom styles located in the `/static/css` directory.
  - Includes responsive design for mobile and desktop.

- **Static Files**
  - Images, JavaScript, and other assets are stored in `/static`.

---

## Known Limitations and Next Steps

- **Helpdesk Chat System (Chat with us):** The current chat system supports basic text messaging but lacks real-time updates and advanced features. It answers on "hello" and pricing",... 
  
- **Review System:** Reviews display reviewer IDs instead of usernames. This will be addressed in future updates to enhance readability and trust.

- **Dynamic Map:** Geolocation data is static and may not accurately represent real-time locations. We aim to integrate dynamic updates and more precise geolocation services.

- **Design and Responsiveness:** The UI prioritizes core functionality. We plan to introduce professional design and improve responsiveness for better user experience.

- **Badge System:** Currently static and predefined. Adjustments will be made based on real-world user interactions and feedback.

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- A virtual environment manager (optional but recommended)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/plant-sitting.git
   cd plant-sitting
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows, use venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:

   Update the `Config` class in `config.py` with your PostgreSQL credentials.

5. Apply database migrations:

   ```bash
   flask db upgrade
   ```

6. Run the application:

   ```bash
   flask run
   ```

   Access the app at `http://127.0.0.1:5000/`.

## Directory Structure

```plaintext
app/
├── static/             # CSS, JavaScript, and image files
├── templates/          # HTML templates for the Flask app
├── routes/             # Flask blueprint for app routes
├── models.py           # Database models (SQLAlchemy)
├── forms.py            # Flask-WTF forms for user input
├── config.py           # Application configuration
└── main.py             # Application entry point
```

## Contributors

This project was made possible thanks to the contributions of:

- **Pieter-Jan Blancquaert**
- **Yentl Malfait**
- **Thibault Mertens**  
- **Estelle Seurynck**
- **Sander Truyens**
- **Robin Van Huyck**  

Their combined effort, creativity, and dedication shaped the Plant Sitting platform into what it is today.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

## Contact

For questions or support, reach out to:

- Email: support@plantsitting.com
- Phone: +32 468 26 00 98

---
Start listing your plants or become a sitter today at **Plant Sitting**!
