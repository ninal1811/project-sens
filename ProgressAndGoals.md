# Progress

## API Server

The following lists what was completed during the Fall 2025 semester.

- Created an API server for geographical data.
- Implemented 14 API endpoints including CRUD operations for cities and states, country retrieval, health checks, and utility endpoints (`/cities/create`, `/countries`, `/states/read`, `/health`, etc).
- Each endpoint includes corresponding unit tests.
- All endpoints are documented using Swagger.
- Relevant data is cached to improve performance.
- The project was deployed to PythonAnywhere.

This fulfills the following requirements established.

- Create an API server for a geographic database.
- Implement CRUD operations on related datasets.
- Include a dozen or more endpoints.
- Ensure all endpoints have unit tests.
- Deploy the project to the cloud using CI/CD.


# Goals

These are the goals we want to accomplish in the Spring 2026 semester.

- Create a robust frontend on React that displays popular food around the world by geographic region.
- Load more countries, states, and cities data to MongoDB
- Load data related to popular food by region.
- Work on the backend API Server to process data related to food (add queries, tests, etc).
- Handle security.

## Create a robust frontend on React that displays popular food around the world by region

- Build a React frontend application.
- Display regions and associated popular foods.
- Connect the frontend to the backend API.
- Ensure each API endpoint has a corresponding frontend view.
- We will use React + Vite to build the frontend and use React Testing Library + Vitest for testing purposes.

Purpose: Allows backend data to be better visualized.

## Load more countries, states, and cities data to MongoDB

- Find additional geographic data from Kaggle.
- Create ETL scripts to load geographic data into MongoDB.
- Note: For countries that have provinces, we will count the provinces as states.
- Note: Our Geographic regions will be: North America, Africa, and Asia

Purpose: Expand the geographic database to provide comprehensive coverage across multiple regions, enabling richer data exploration and more meaningful food-by-region associations.

## Load data related to popular food by region

- Source food data from reliable databases 
- Define schema for food data including fields like food name, region/country association, description, and category.
- Create ETL scripts to process and load food data into MongoDB.
- Link food entries to existing geographic entities (countries, states, cities).

Purpose: Enrich the dataset with culturally relevant food information, creating the foundation for users to discover and explore regional cuisines alongside geographic data.

## Work on the backend API Server to process data related to food (add queries, tests, etc)

- Add new API endpoints for food data.
- Implement query functionality for filtering by region or country.
- Add unit tests for all new endpoints.

Purpose: Extend the API's capabilities to handle food-related queries efficiently, ensuring reliable data retrieval and maintaining code quality through comprehensive testing.

## Work on the security
- Add parameterized queries to prevent NoSQL injection attacks in MongoDB operations.
- Add rate limiting to API endpoints to prevent abuse and DoS attacks.
- Store API keys and configuration in environment variables, never hardcode in source.
- Add security-focused unit tests using React Testing Library for input handling.

Purpose: Ensure the geographic and food data API is secure, resilient, and safe for public-facing use by implementing industry-standard backend, database, and deployment security controls.
