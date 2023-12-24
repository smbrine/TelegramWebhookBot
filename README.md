# TelegramWebhookBot

## Installation
### Prerequisites
- Python >=3.11
- pip
- Make (optional)

### Setting up the Environment
TelegramWebhookBot requires the following environment variables to run:

```env
TG_BOT_KEY

OR_API_KEY

NGROK_URL

BACKEND_API_URL
```

These variables are predefined but can be customized based on your database configuration.

The service will be available on `http://localhost:8002`.

## Usage
After running the application, you can access the self-documented API interface provided by FastAPI to explore and test available endpoints.

## Development
The project is currently in active development. Note that the Kubernetes file is still under development and not recommended for use at this stage.

## Makefile Usage
The Makefile includes commands for setting up the environment and running the application:

- `make setup`: Set up the Python virtual environment and install dependencies.
- `make run`: Run the application on `http://localhost:8002`.


## Contributing
There are no specific contribution guidelines. Feel free to change anything and offer updates to the project.

## Security
Currently, there are no specific security features implemented in the application.

## License
This project is licensed under the GNU General Public License.

