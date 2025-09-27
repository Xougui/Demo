# DemoBot

DemoBot is a multi-purpose Discord bot with a variety of features, including moderation, utility, and fun commands. It's built with Python using the `discord.py` library.

## Features

*   **Ping Command**: Check the bot's latency.
*   **Mention Response**: Responds with helpful information when mentioned.
*   **Create Invite**: Creates a permanent server invite (for administrators).
*   **Private Messaging (MP)**: Send a private message to a user as the bot (for administrators).
*   **Counting Channel**: Set up a channel where users take turns counting up.
*   **Button and Select Menu Examples**: Demonstrates UI components like buttons and select menus.
*   **Persistent Components**: Shows how to create UI components that persist after the bot restarts.
*   **Command Logging**: Logs command usage to a designated channel.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.10 or higher installed. Then, install the required libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the bot:**
    *   Create a file named `.env` in the root directory of the project.
    *   Add the following lines to the `.env` file:
        ```
        DISCORD_TOKEN="your_bot_token_here"
        OWNER_ID="your_user_id_here"
        ```
    *   Replace `"your_bot_token_here"` with your actual Discord bot token.
    *   Replace `"your_user_id_here"` with your Discord user ID to be able to use owner-only commands.
    *   (Optional) In `main.py`, you can still customize the `log_channel_id` and `log_server_id` variables for command logging, and the status message in the `change_status` task.

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## Commands

Here is a list of the main commands available:

### General Commands

*   `/ping`: Displays the bot's current latency.
*   `!create_invite`: Creates a permanent invite to the server. (Requires 'Manage Server' permission).

### Fun & Utility

*   `/counter [channel]`: Sets up a counting channel. Users must count in sequential order without posting twice in a row. (Requires Administrator permission).
*   `/button`: Displays a message with various interactive buttons.
*   `/selector`: Displays a message with an interactive select menu.
*   `/testbutton`: Displays a message with a persistent button that works even after the bot restarts.
*   `/test-layout`: Shows an example of a more advanced message layout.

### Admin Commands

*   `/mp [member] [content]`: Sends a direct message to the specified member from the bot's account. (Requires Administrator permission).
*   `!start [seconds]`: Changes the interval for the bot's status rotation. (Bot owner only).

## Cogs

The bot's functionality is organized into cogs (extensions), which can be found in the `cog/` directory.

*   `mp.py`: Handles the private messaging command.
*   `counter.py`: Manages the counting channel feature.
*   `button.py`, `selecteur.py`, `layout_example.py`, `persistent.py`: Contain examples of various UI components.
*   `test_counter.py`: An alternative implementation of the counting game using local files.
*   `example_cog.py`: A simple example cog.