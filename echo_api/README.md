# Echo API

A straightforward guide to install and use the Echo API extension.

## Installation

1. Open VS Code marketplace
2. Search for "echo api"
3. Look for the extension with a bird icon
4. Install the extension

## Import Configuration

1. Open the extension from the left panel
2. Locate the **HTTP1/2 Request** button
3. Click the dropdown arrow on the right side
4. Select **Import data**
5. Import the `echo_api.json` file from the current directory

## Setup Backend

1. Ensure the backend service is running using docker-compose in the root project:

   ```bash
   docker-compose up
   ```

2. Configure environment variables for the backend service
3. Follow any additional setup instructions in `backend/README.md`

## Run and Test

Once the backend is running and environment variables are configured, you can run and test the API endpoints through the extension.
