# post-it-blog
<img align="left" src="https://camo.githubusercontent.com/a1b2dac5667822ee0d98ae6d799da61987fd1658dfeb4d2ca6e3c99b1535ebd8/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d3336373041303f7374796c653d666f722d7468652d6261646765266c6f676f3d707974686f6e266c6f676f436f6c6f723d666664643534"/>
<img align="left" src="https://camo.githubusercontent.com/43c40e9f61f01e780f4cfed5dafda9e3494310ba1b6ea11e20c4949e556a47c3/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f666c61736b2d2532333030302e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d666c61736b266c6f676f436f6c6f723d7768697465"/>
<img align="left" src="https://camo.githubusercontent.com/5a3894ca48d276f159a9ae701311c7d8eb8f01851e2d46ea492789608e11a31c/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6a696e6a612d77686974652e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d6a696e6a61266c6f676f436f6c6f723d626c61636b"/>
<img align="left" src="https://camo.githubusercontent.com/29e7fc6c62f61f432d3852fbfa4190ff07f397ca3bde27a8196bcd5beae3ff77/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f706f7374677265732d2532333331363139322e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d706f737467726573716c266c6f676f436f6c6f723d7768697465"/>
<img align="left" src="https://camo.githubusercontent.com/b768ae6e4f89b74512e6de02a8367fd71465bc3d88ef1cf2f1622e2017c32bea/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f626f6f7473747261702d2532333536334437432e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d626f6f747374726170266c6f676f436f6c6f723d7768697465"/>
<img align="left" src="https://camo.githubusercontent.com/49fbb99f92674cc6825349b154b65aaf4064aec465d61e8e1f9fb99da3d922a1/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f68746d6c352d2532334533344632362e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d68746d6c35266c6f676f436f6c6f723d7768697465"/>
<img align="left" src="https://camo.githubusercontent.com/e6b67b27998fca3bccf4c0ee479fc8f9de09d91f389cccfbe6cb1e29c10cfbd7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f637373332d2532333135373242362e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d63737333266c6f676f436f6c6f723d7768697465"/>
<img align="left" src="https://camo.githubusercontent.com/05020a4e2cf996983147d3a6bc5eff61195b8a5270914acc37018f8e6d7dcf14/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f52656e6465722d253436453342372e7376673f7374796c653d666f722d7468652d6261646765266c6f676f3d72656e646572266c6f676f436f6c6f723d7768697465"/>

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
