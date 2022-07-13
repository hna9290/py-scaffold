# StorePick Menu converter
This is an in-memory Menu Converter.There are two ways to use this converter.
1. As command line tool
2. As a web service - Swagger file at app/static/swagger.yaml

## Programming Tools & Frameworks
1. Python 3.8 - For Development, Unit testing, Integration testing
2. Terraform v0.12 - For creating AWS infrastructure
3. Docker v19.03 - For containerization of the app to be deployed as service
4. Docker-Compose - Ease of container management
5. [Jenkins](https://jenkins.p.morconnect.com/people/job/store-pick/) - As a CI tool
5. Swagger 3.0 - Specification to generate API docs


## Python Libraries
- Flask: Micro-framework for create REST API
- flask-swagger-ui: Gives a nice UI for testing and using API's - /swagger endpoint
- pylint: Python Lint
- mypy: Static type checker for Python. Great tool to prevent errors
- pytest: Unit testing framework
- coverage: Outputs code coverage reports
- behave: Framework for BDD
- fire: Nice tool to implement command line pattern

### Install python frameworks
Execute: **make init**

### Unit Testing, Coverage and Linting
Execute: **make coverage**

### Static Type Checking
Execute: **make mypy**

### Local Containerized Integration Testing
Execute: **make behave**

### Usage - Command Line Execution
- Execute - **make fire** [uses ./data.csv as input and generates ./data.json]
- Execute - **python3.8 -m app <source_csvpath> <destination json path>**

### Usage - Local Dockerized API
1. Execute - **make compose-build** [To build docker images]
2. Execute - **make up** [To run the containers]
3. Execute - **make down** [To stop execution and remove containers]

You can access the API's at 0.0.0.0:8087/swagger

### Usage - Deploy on AWS
- Multibranch pipeline is created in [Jenkins](https://jenkins.p.morconnect.com/people/job/store-pick/) which uses Jenkinsfile for deployment
- Following are steps in Jenkins Build
    1. Build and use Docker as agent 
    2. Initialise python environment, execute unit tests, coverage, pylint and mypy
    3. Execute dockerized local integration tests
    4. Build and push docker images to ECR
    5. Terraform the ECS service and related components
    6. Publish coverage reports
    
### Notes
- AWS ECS service endpoint works fine but is only accessible through Morrisons Netowrk
- Cloud Integration tests are not available as Jenkins network cannot execute ECS service. But current local integration tests can be reused for cloud integration tests as well.
- Currently, for this assignment purposes, any deployments are made in Nonprod people AWS account. But it can be easily made to support multiple environments.
