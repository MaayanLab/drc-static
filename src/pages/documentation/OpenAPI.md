---
layout: '@/layouts/Documentation.astro'
title: OpenAPI & SmartAPI
label: OpenAPI
short_description:  >
                The OpenAPI specification allows for the standardization of 
                application programming interfaces (APIs), and facilitates 
                their interoperability. 


                The SmartAPI project builds on top of the OpenAPI specifications 
                to maximize the findability, accessibility, interoperability, 
                and reusability (FAIRness) of web-based tools, especially those 
                within the biomedical sphere. Through richer metadata descriptions, 
                SmartAPI enables users to search and use a connected network of tools. 
---
# OpenAPI and SmartAPI

## Table of Contents
  - [Introduction](#introduction)
  - [Creating API Specifications](#creating-api-specifications)
    - [Requests](#requests)
    - [Responses](#responses)
  - [Resources](#resources)

## Introduction
Application programming interfaces (APIs) provide a set of protocols that broadly allow different software programs to communicate. In the biomedical sciences, many tools and resources have APIs that facilitate querying, downloading, or computing on the available data. For instance, the GTEx DCC provides APIs for programmatically retrieving RNA-seq data, while the GlyGen APIs return information related to different glycans, proteins, and motifs. 

The <a href="https://spec.openapis.org/oas/latest.html" target="_blank">OpenAPI specification language</a>, developed by the <a href="https://www.openapis.org/" target="_blank">OpenAPI initiative</a>, is a standardized language for succinctly describing an API’s functionality, including its inputs and outputs, without requiring users to have any prior knowledge of the backend. OpenAPI specifications are programming-language agnostic, and the standardized format is supported by resources such as <a href="https://swagger.io/" target="_blank">Swagger</a>, which allows for the efficient testing, development, and publishing of API specifications. Within the CFDE, the OpenAPI specification language has the potential to improve the interoperability of DCC APIs with each other and with tools external to the consortium. 

The <a href="https://github.com/SmartAPI/smartAPI-Specification/blob/OpenAPI.next/versions/3.0.0.md" target="_blank">SmartAPI specification language</a> extends OpenAPI to capture more metadata to maximize the findability, accessibility, interoperability, and reusability (FAIRness) of web-based APIs, especially within the context of biomedical big data. Specifically, SmartAPIs allow for additional metadata fields, such as requiring an API version and a link to the original tool terms of service as well as including a space to list more contacts or external resources related to the API. In addition to the specifications, SmartAPI also provides an editor for writing and testing APIs as well as a registry of 200+ APIs that have already been deployed and published, including several DCC tools. Currently, SmartAPI is supported by the Biomedical Data Translator program from the National Center for Advancing Translational Sciences (NCATS). 

## Creating API Specifications

As an example, the following tutorial will adapt two endpoints from the <a href="https://smart-api.info/ui/8113167e81987d36b707ae4aa795b17e" target="_blank">FAIRshake v2 API specifications</a>. Note that this document is not meant to be a comprehensive manual for API development, but rather an introductory guide for writing OpenAPI/SmartAPI specifications. 

1. Initialize your root document with metadata and server information. OpenAPI/SmartAPI specifications can be written in either JSON or YAML, but the information contained should be generally the same regardless of format, and include the following required fields, as well as any relevant optional fields: 

  - `openapi`: Semantic version number of OpenAPI specification
  - `info`: API metadata
    - `termsOfService`: URL to terms of service for API 
    - `version`: Semantic Version of the API definition
    - `contact`: Name, email, and role of contact information
  - `servers`: List of available servers called by API
  - `paths`: List of endpoints/operations for the API

    <br /><br />
    **JSON**
    ```
    {
      "openapi": "3.0",
      "info": {
        "title": "FAIRshake API",
        "version": "1.0",
        "description": "Web interface for scoring biomedical digital objects", 
        "termsOfService": "https://fairshake.cloud/",
        "contact": {
          "name": "John Doe",
          "email": "johndoe@email.com",
          "x-role": "responsible developer"
        }
      },
      "servers": [
        {
          "url": "https://fairshake.cloud",
        }
      ],
      "paths": { ... }
    }
    ```

    **YAML**
    ```
    openapi: 3.0
    info: 
      title: FAIRshake API
      version: 1.0
      description: Web interface for scoring biomedical digital objects
      termsOfService: https://fairshake.cloud/
      contact:
        name: John Doe
        email: johndoe@email.com
        x-role: responsible developer
    servers:
    - url: https://fairshake.cloud
    paths:
      ...
    ```

2. Identify the core functionality: What queries are available, and from which servers? What types of information can be extracted? Are any credentials needed to access certain data? 

  - In our tutorial, we are concerned with two endpoints: a POST request which creates a new digital object from an integer `id`, a pre-defined `type`, a string `url`, and a list of `authors`; and a GET request to search through a list of existing digital objects using the `url` parameter. 

### Requests

3. For each potential endpoint, determine the type of request method (POST, GET, DELETE, etc.) and the required input values and content type. Each of these should be listed under `paths` in the document. 

  - For a POST method, the input will take the form of a Request Body Object, which also requires a media type. The most common media types are `text/plain` for plaintext inputs, `application/json` for JSON-formatted inputs, and `multipart/form-data` for single or multiple file upload inputs. Below, we define our example POST request. 

    <br /><br />
    **Example input**
    ```
    {
      "id": 1,
      "type": "tool",
      "title": "NewDigitalObject",
      "url": "https://newdigitalobject.com",
      "authors": [
        "John Doe", 
        "Jane Doe"
      ]
    }
    ```

    **JSON**
    ```
    "paths": {
      "/create_digital_object": {
        "post": {
          "operationId": "create_digital_object",
          "description": "Create a digital object",
          "requestBody": {
            "required": true,
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "required": [
                    "url", 
                    "title"
                  ],
                  "properties": {
                    "id": {
                      "type": "integer"
                    },
                    "type": {
                      "type": "string",
                      "enum": [
                        "data",
                        "repo",
                        "test",
                        "tool"
                      ]
                    },
                    "title": {
                      "type": "string"
                    },
                    "url": {
                      "type": "string",
                      "maxLength": 255,
                      "minLength: 1
                    },
                    "authors": {
                      "type": "array",
                      "items": {
                        "type": "string",
                      },
                      "uniqueItems": true
                    }
                  }
                }
              }
            }
          },
          "responses": { ... }
        }
      }
    }
    
    ```

    **YAML**
    ```
    paths:
      /create_digital_object:
        post: 
          operationId: create_digital_object
          description: Create a digital object
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  type: object
                  required:
                  - url
                  - title
                  properties:
                    id:
                      type: integer
                    type: 
                      type: string
                      enum: 
                      - data
                      - repo
                      - test
                      - tool
                    title:
                      type: string
                    url:
                      type: string
                      maxLength: 255
                      minLength: 1
                    authors:
                      type: array
                      items:
                        type: string
                      uniqueItems: true
    ```

  - For a GET method, the input may require defined parameters, which can usually be located within the path or the header of a request. In the example below, we search for our newly added digital object by its title.
    
    <br /><br />
    **Example path**
    ```
    https://fairshake.cloud/get_digital_object?title=NewDigitalObject"
    ```

    **JSON**
    ```
    "paths": {
      "/create_digital_object": { ... },
      "/get_digital_object": {
        "get": {
          "operationId": "get_digital_object",
          "description": "Get a list of digital objects",
          "parameters": [
            {
              "name": "url",
              "in": "query",
              "description": "URL of digital object",
              "required": false,
              "type": "string"
            },
            {
              "name": "title",
              "in": "query",
              "description": "Title of digital object",
              "required": true,
              "type": "string"
            }
          ],
          "responses": { ... }
        }
      }
    }
    ```

    **YAML**
    ```
    paths:
      /create_digital_object:
        ...
      /get_digital_object:
        get:
          operationId: get_digital_object
          description: Get a list of digital objects
          parameters:
          - name: url
            in: query
            description: URL of digital object
            required: false
            type: string
          - name: title
            in: query
            description: Title of digital object
            required: true
            type: string
    ```

### Responses

4. For each potential endpoint, determine the type of response that should be returned for each status. The requested data should be returned only when the status code is 20X (200, 201, etc.). Defining the schema for a response will be similar to defining a schema for an input or request body. In our example GET request, a successful response is a list of digital objects that all must follow the same schema as the POST request defined earlier for submitting a digital object. 

    <br /><br />
    **Example response**
    ```
    {
      "count": 1
      "results": [
        {
          "id": 1,
          "type": "tool",
          "title": "NewDigitalObject",
          "url": "https://newdigitalobject.com",
          "authors": [
            "John Doe", 
            "Jane Doe"
          ]
        }
      ]
    }
    ```

    **JSON**
    ```
    "paths": {
      "/get_digital_object": {
        "get": {
          "operationId": "get_digital_object",
          "description": "Get a list of digital objects",
          "parameters": { ... },
          "responses": {
            "200": {
              "description": "Successfully get a list of digital objects",
              "content": {
                "application/json": {
                  "schema": {
                    "type": "object",
                    "properties": {
                      "count": {
                        "type": "integer"
                      },
                      "results": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "id": {
                              "type": "integer
                            },
                            "type": {
                              "type": "string",
                              "enum": [
                                "data",
                                "repo",
                                "test", 
                                "tool"
                              ]
                            },
                            "url": {
                              "type": "string",
                            },
                            "authors": {
                              "type": "array",
                              "items": {
                                "type": "string",
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    ```

    **YAML**
    ```
    paths:
      /get_digital_object:
        get:
          operationId: get_digital_object
          description: Get a list of digital objects
          parameters:
            ...
          responses:
            200:
              description: Successfully get a list of digital objects
              content:
                application/json:
                  schema:
                    type: object
                    properties: 
                      count: 
                        type: integer
                      results:
                        type: array
                        items:
                          type: object
                          properties: 
                            id: 
                              type: integer
                            type: 
                              type: string
                              enum:
                              - data
                              - repo
                              - test
                              - tool
                            url:
                              type: string
                            authors:
                              type: array
                              items:
                                type: string
    ```
  Note that OpenAPI/SmartAPI allow for the definition of `Components`, which are reusable objects within a single API specification. These can be `schemas`, `parameters`, `requestBodies`, or other objects that may come up in multiple paths. In the examples above, the digital object schema could have been defined as a `schema` component, and the reference `#/components/schemas/DigitalObject` could have been used in place of its full definition under the `create_digital_object` `requestBody` and `responses` as well as the `get_digital_object` `responses`.

  - For error codes (4XX, 5XX), you may choose to “catch” these errors by defining some behavior that should occur if the error is triggered. 

  5. Fill in the rest of the path specifications according to the general steps above, based on your API. For more complicated requests or schemas that aren't covered here, refer to the full OpenAPI or SmartAPI documentation. 

## Resources

- <a href="https://smart-api.info/registry" target="_blank">SmartAPI Registry</a>
- <a href="https://github.com/SmartAPI/smartAPI-Specification/tree/OpenAPI.next/examples/v3.0" target="_blank">Example SmartAPI v3.0 specifications</a>
- <a href="https://editor.swagger.io/" target="_blank">Swagger Editor</a>

<br />
While not required, it is highly recommended to use a dedicated OpenAPI or SmartAPI editor, such as Swagger, to generate API specifications. Such tools designated for writing OpenAPIs/SmartAPIs can help with debugging and auto-formatting, as well as with testing and publishing API documentation. 

#### Return to [Documentation](./)
