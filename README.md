# Discord.py Demo Bot

Welcome to the Discord.py Demo Bot! This repository is designed to be a clean, well-documented, and easy-to-understand resource for beginners learning to create Discord bots with the `discord.py` library. It includes examples of basic commands, event handling, UI components, and project organization using cogs.

## Features

*   **Slash Commands**: Modern, user-friendly commands for all features.
*   **UI Component Examples**: Demonstrations of buttons, select menus, and advanced layouts.
*   **Persistent Views**: An example of a view that works even after the bot restarts.
*   **Modular Cogs**: Functionality is organized into separate modules (cogs) for clarity and scalability.
*   **Configuration with `.env`**: Securely manage your bot's token and other settings.
*   **Command Logging**: A dedicated cog to log command usage to a specified channel.
*   **Counting Game**: A simple but complete example of a guild-specific, persistent feature.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Xougui/demobot.git
    cd demobot
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.10 or higher installed. Then, install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the bot:**
    *   Rename the `.env.example` file to `.env`.
    *   Open the `.env` file and fill in the required values:
        - `DISCORD_TOKEN`: Your bot's unique token from the Discord Developer Portal.
        - `OWNER_ID`: Your Discord user ID for owner-only commands.
        - `LOG_CHANNEL_ID`: The ID of the channel where command usage should be logged.
        - `LOG_SERVER_ID`: The ID of the server where the logging channel is located.

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## Commands

Here is a list of the main commands available:

### General Commands
*   `/ping`: Displays the bot's current latency.
*   `!create_invite`: Creates a permanent invite to the server (requires 'Manage Server' permission).

### Fun & Utility
*   `/counter [channel]`: Sets up a channel for the counting game (requires Administrator permission).
*   `/buttons`: Displays a message with various interactive buttons.
*   `/select_menu`: Displays a message with an interactive select menu.
*   `/layout_example`: Shows an example of an advanced message layout.
*   `/testbutton`: Displays a persistent button that works after a bot restart.

### Admin Commands
*   `/dm [member] [content]`: Sends a direct message to a member from the bot (requires Administrator permission).
*   `!start [seconds]`: Changes the interval for the bot's status rotation (Bot owner only).

## Project Structure

The bot's functionality is organized into cogs (extensions), which can be found in the `cog/` directory.

*   `counter.py`: Manages the counting channel feature.
*   `dm.py`: Handles the direct messaging command.
*   `logging.py`: Logs all command usage to a designated channel.
*   `button.py`, `selector.py`, `layout_example.py`: Contain examples of various UI components.
*   `persistent.py`: An example of a persistent UI view.
*   `example_cog.py`: A simple boilerplate cog for reference.

The `data/` directory is used to store persistent data, such as the state of the counting game in `counter.json`.