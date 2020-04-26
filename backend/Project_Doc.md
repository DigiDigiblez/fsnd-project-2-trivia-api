# Super Trivia App

## Introduction
This is a basic trivia app developed as a 2nd of 5 projects for the 2020 Udacity Full Stack Nanodegree. It allows you to search for trivia questions, add your own, delete the boring ones, and even play a quiz of the eggheads with your brainy friends. Enjoy :)

It's more than just a degree as people know it, well to me anyway. It's an opportunity to work sleepless nights, grinding to perfection in an industry I love.


### Coding style & conventions
This project comprises of coding standards on both the back end and the front end.
The back end uses [pep 8 style](https://www.python.org/dev/peps/pep-0008/), while the front end uses [ESLint](https://eslint.org/) and [Prettier](https://prettier.io/).
The front end style config files have been trailed and tested so sticking to them makes for great conventions and best practices throughout the code.

For IDEs like WebStorm and PyCharm, you can go to `Preferences | Tools | File Watchers` and add automatic watchers for ESLint and Prettier on any files you choose. Upon pressing save the watchers will auto-lint your changes for ease of use.

## Getting Started
### Setup Front End
As the front end uses NPM, navigate to the frontend directory and use `npm i` to install the dependencies in the `package.json` file. This will generate a `package-lock.json` file. It's advisable to commit this file as and when it is updated.

Once the dependencies are installed, run `npm start` to run the front end.

### Setup Back End
Firstly, navigate to the backend directory and load `psql`. Create a database using command, e.g. `CREATE DATABASE trivia;`. Now exit `psql` and execute in the backend directory `psql trivia < trivia.psql;` to fill the database with dummy data to load the application with. If the database ends up breaking at some point just use `DROP DATABASE trivia;` and `CREATE DATABASE trivia;` and fill it again to get back to normal.

Now, you can setup the project and run it by executing the `run.sh` bash file provided, through either the terminal, or by right-clicking it and running. This will initialise and run your backend.

### Setup Test Suite
Additionally, you will also need to create a test database in psql, e.g. `CREATE DATABASE trivia_test;`, and fill that also with the same dummy data using `psql trivia_test < trivia.psql;`. Run the tests by right-clicking and running the `test_flaskr.py` file. All tests should pass successfully. It they don't the database might not be correctly setup properly, so refer back to the abovementioned steps to resolve this.

## API Reference
Please refer to the [API reference docs](./API_Doc.md) file to understand how the API operates.

## Authorial decrees
- Carl Bowen: Developed this app
- Udacity: Provided the template for this app

## Acknowledgements
- God and the Lord Jesus Christ, for helping me through this project! ❤️ ❤️ ❤️
- Team Udacity, for all their hard work in building great nanodegrees for great students of all walks of life