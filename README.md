# post-it-blog
<img width="40px" align="left" src="https://github.com/mimisanchelo/stock/assets/80426185/23c2fe40-b0a0-416b-a4be-ce1fb2f00553"/>
<img width="40px" align="left" src="https://github.com/mimisanchelo/post-It-app/assets/80426185/846201e6-838d-4297-b73b-7a5b5e08ce60"/>
<img width="40px" align="left" src="https://github.com/mimisanchelo/post-It-app/assets/80426185/f1ec02bf-bd4b-4aa8-af8f-e8f5a46874d0"/>

<br></br>
This is a Python-based blog project built using the Flask web framework and Bootstrap. The application uses a PostgreSQL database, which was created with the help of SQLAlchemy. Passwords are hashed using sha256 to protect sensitive data.
<br></br>

## Features
Registered and logged-in users have access to features such as creating new posts, editing posts(only for author), deleting posts(only for author), leaving comments and likes on the posts, visiting and following other user`s profiles, editing personal data

These functionalities are disabled and hidden from non logged-in users. The routes for these functions are forbidden to prevent unauthorized access.

The project prioritizes cybersecurity by using an algorithm to sanitize each client's HTML input. The algorithm removes unwanted tags, attributes, unescaped characters, and unclosed or misnested tags.

## Preview
> <img width="75%" align="center" src="https://github.com/mimisanchelo/post-it-blog/assets/80426185/8f42a0d4-68eb-49fc-b8b5-863c1ca4a409"/>
> <img width="75%" align="center" src="https://github.com/mimisanchelo/post-it-blog/assets/80426185/51e5baf2-1298-435b-a0a9-01ab1c9f3ee7"/>
> <img width="75%" align="center" src="https://github.com/mimisanchelo/post-it-blog/assets/80426185/f69d5af5-4935-43bf-a327-8701991494cb"/>
> <img width="75%" align="center" src="https://github.com/mimisanchelo/post-it-blog/assets/80426185/42cadd72-3e2e-4740-82b9-5d728594d85e"/>
> <img width="75%" align="center" src="https://github.com/mimisanchelo/post-it-blog/assets/80426185/e88cdec7-37ca-4fe8-917a-906a59e90fc0"/>
> <img width="75%" align="center" src="https://github.com/mimisanchelo/post-it-blog/assets/80426185/fd790a06-3938-4820-b9f5-2ed1f88322e3"/>
> <img width="75%" align="center" src="https://github.com/mimisanchelo/post-it-blog/assets/80426185/ea09bd4c-8edc-406c-9f2e-8d901e68a5a5"/>

## Installation

1. Clone the repository:</br>
    ```python
   https://github.com/mimisanchelo/post-it-blog.git
    ```
   
1. Create virtual environment:
   
    ```python
   py -m venv venv
    ```
    ```python
    source venv/Scripts/activate
    ```

1. Install the required packages:
   
    ```python
   pip install -r requirements.txt
    ```
1. Create a PostgreSQL database.
1. Change environmental variables to your own database URL and email credentials.
1. Run the application
