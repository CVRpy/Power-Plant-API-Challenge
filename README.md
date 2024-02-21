# Power Plant Production Plan API

This Flask application calculates the production plan for a set of power plants based on the given load and fuel costs.

## Building and Launching the API

1. Clone this repository:
git clone <repository-url>


2. Navigate to the project directory:
cd power-plant-api


3. Build the Docker image:
docker build -t power-plant-api .

4. Run the Docker container:
docker run -p 8888:8888 power-plant-api


## Endpoints

- **POST** `/productionplan`: Calculate the production plan based on the given payload.

## Example Payloads and Responses

Example payload JSON files are provided in the `example_payloads/` directory. You can use these files to test the API.

## Dependencies

pip install -r requirements.txt

## License

Rami - SPAAS TEAM :)