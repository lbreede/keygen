# keygen :key:

[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/lbreede/keygen/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3](https://img.shields.io/badge/Python-3-ff69b4.svg)](https://www.python.org/downloads/release/python-3117/)
[![GitHub followers](https://img.shields.io/github/followers/lbreede.svg?style=social&label=Follow)](https://github.com/lbreede?tab=followers)
[![GitHub stars](https://img.shields.io/github/stars/lbreede/keygen.svg?style=social&label=Star)](https://github.com/lbreede/keygen/stargazers/)

## Description

A fun excursion in the world of software product keys and keygens.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Features](#features)
- [License](#license)

## Installation

To install and use this project, follow these steps:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/lbreede/keygen.git
    ```

2. Navigate to the project directory:
    ```bash
    cd keygen
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. For convenience, you can run both the product key and the keygen UI from the main file:
    ```bash
    python main.py
    ```
2. In the product key window, guess a key and press "Next >" to see if it's a valid key (probably not).

3. Press "Generate" to generate a valid key.

4. Press "Copy to Clipboard" to copy the generated key.

5. Return to the product key window and paste the key into the field.

6. Press "Next >" and see if the key is now valid (hopefully yes).

That's it! You have successfully used the Keygen program.

## Features

In the `key_manager.py` file, you can find the `KeyManager` protocol which defines the interface for a key manager.
Currently, there is only one implementation of this protocol, the `Win95KeyManager` used to generate and validate Windows 95 product keys.

### Win95KeyManager

The `Win95KeyManager` is implementing the following rules, found on [Product key - Wikipedia](https://en.m.wikipedia.org/wiki/Product_key#Windows_95_retail_key):

Windows 95 retail product keys take the form XXX-XXXXXXX. To determine whether the key is valid, Windows 95 performs the following checks:

- The first 3 characters must not be equal to 333, 444, 555, 666, 777, 888 or 999.
- The last 7 characters must all be numbers from 0-8.
- The sum of the last 7 numbers must be divisible by 7 with no remainder.
- The fourth character is unchecked.

If all checks pass, the product key is valid.

## License

This project is licensed under the [MIT License](LICENSE).
