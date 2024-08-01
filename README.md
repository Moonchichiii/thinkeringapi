# thinkeringapi

# Thinkering Blog API

## Table of Contents

1. [Project Goals](#project-goals)
2. [User Stories](#user-stories)
3. [Design](#design)
 - [Class Diagram](#class-diagram)
 - [Kanban Board](#kanban-board)
4. [Technologies](#technologies)
5. [Dependencies](#dependencies)
6. [Setup and Installation](#setup-and-installation)
 - [Pre-pre checks](#pre-pre-checks)
 - [Cloning the Repository](#1-cloning-the-repository)
 - [Virtual Environment Setup](#virtual-environment-setup)
 - [Install Dependencies](#install-dependencies)
8. [Usage](#usage)
9. [Running Tests](#running-tests)
 - [Unit Tests](#unit-tests)
 - [Coverage](#coverage)
10. [Deployment](#deployment)
11. [Acknowledgements](#acknowledgements)
12. [Contributing](#contributing)
13. [Project Structure](#project-structure)

## Project Goals

To create a robust and scalable backend API for a social media platform that allows users to manage blog posts, comments, likes, profiles, and receive notifications, supported by a chatbot assistant.

## User Stories

- As a user, I want to register an account and log in to access the platform's features.
- As a user, I want to create and manage blog posts.
- As a user, I want to interact with other users' posts through comments and likes.
- As a user, I want to receive notifications for activities related to my posts.
- As a user, I want to update my profile information.
- As a user, I want to use a chatbot assistant to help me interact with the platform.

## Design

### Class Diagram



### Kanban Board



- **Development Process:** Agile development approach with thorough planning, including a class diagram and wireframes.
- **Feature Tracking & Task Management:** Features categorized and managed through a Kanban board.

(Include a link to the project board here.)

## Technologies

- **Django:** Primary web framework for backend development.
- **Django REST Framework (DRF):** Building RESTful APIs.
- **Simple JWT:** Authentication using JSON Web Tokens.
- **Cloudinary:** Media management for images and videos.
- **django-cors-headers:** Handling Cross-Origin Resource Sharing (CORS).
- **Python Decouple:** Managing environment variables.
- **Django Filters:** Filtering querysets based on request parameters.
- **Gunicorn:** WSGI HTTP server for serving Django applications in production.
- **PostgreSQL (via psycopg2-binary):** Database backend.

## Dependencies

- `asgiref==3.7.2`
- `cloudinary==1.40.0`
- `dj-database-url==2.1.0`
- `django==5.0.6`
- `django-allauth==0.51.0`
- `django-cloudinary-storage==0.3.0`
- `django-compressor==4.3`
- `django-cors-headers==4.3.1`
- `django-csp==3.6`
- `django-filter==24.2`
- `django-rest-auth==0.9.5`
- `django-storages==1.13.2`
- `django-request==1.6.3`
- `django-vite==3.0.4`
- `djangorestframework==3.15.2`
- `djangorestframework-simplejwt==5.3.1`
- `dj-rest-auth==2.2.7`
- `gunicorn==22.0.0`
- `openai==1.35.10`
- `pillow==10.3.0`
- `psycopg2-binary==2.9.9`
- `python-decouple==3.8`
- `setuptools==70.3.0`
- `whitenoise==6.7.0`

## Setup and Installation

### Pre-pre checks

- Python 3.12.3
- Visual Studio Code

### 1. Cloning the Repository
git clone https://github.com/yourusername/thinkeringblogapi.git
cd thinkeringblogapi`` 

### Virtual Environment Setup
``python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate` `` 

### Install Dependencies

`pip install -r requirements.txt` 

## Usage

-   **Blog Operations:**
    -   Create, read, update, and delete blog posts
    -   Comment on posts
    -   Like posts
-   **User Profiles:**
    -   View and update user profiles
    -   Manage avatar images
-   **Chatbot Assistant:**
    -   Interact with the API using natural language queries
-   **Notifications:**
    -   Receive notifications for interactions

## Running Tests

-   **To run the test suite:**

`python manage.py test` 

### Unit Tests

### Coverage

## Deployment

### Heroku Deployment

_Include deployment instructions here._

## Acknowledgements

## Contributing

1.  **Fork the repository**
2.  **Create a new branch:**

`git checkout -b feature-name` 

3.  **Commit your changes:**

`git commit -m 'Add some feature'` 

4.  **Push to the branch:**

`git push origin feature-name` 

5.  **Create a pull request**

## Project Structure

Directory/File

Description

`backend/`

Main project directory containing settings and URLs

`users/`

User management application

`profiles/`

User profiles application

`posts/`

Blog posts application

`comments/`

Comments on blog posts application

`likes/`

Likes on posts application

`ratings/`

Ratings for posts application

`followers/`

Followers and following application

`tags/`

Tags for categorizing posts

`notifications/`

Notifications application

`chatbot/`

Chatbot assistant application

`requirements.txt`

List of project dependencies

`manage.py`

Django management script

[Back to top](#)


## Project Structure

| Directory/File       | Description                                         |
|----------------------|-----------------------------------------------------|
| `backend/`           | Main project directory containing settings and URLs |
| `users/`             | User management application                         |
| `profiles/`          | User profiles application                           |
| `posts/`             | Blog posts application                              |
| `comments/`          | Comments on blog posts application                  |
| `likes/`             | Likes on posts application                          |
| `ratings/`           | Ratings for posts application                       |
| `followers/`         | Followers and following application                 |
| `tags/`              | Tags for categorizing posts                         |
| `notifications/`     | Notifications application                           |
| `chatbot/`           | Chatbot assistant application                       |
| `requirements.txt`   | List of project dependencies                        |
| `manage.py`          | Django management script                            |
