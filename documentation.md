# API Documentation

## Overview

This API allows users to query data based on specific parameters such as `iso`, `data`, and `year`. Each of these parameters can be a string or a list, allowing for flexible queries. The API returns data in CSV format, ready for download.

## Base URL

https://elzapqbt1h.execute-api.us-east-1.amazonaws.com/dev/query


## HTTP Method

- **GET**: Retrieve data based on query parameters.

## Implemented Query Parameters

### `iso`
- **Type**: `string` or `list`
- **Description**: The ISO country code(s) for which you want to retrieve data. Accepts a single ISO code or a comma-separated list of ISO codes.
- **Example**:
  - Single ISO: `iso=tan`

## Not yet implemented Query Parameters

### `data`
- **Type**: `string` or `list`
- **Description**: The specific data type(s) or categories you wish to query. This could represent different datasets or indicators.
- **Example**:
  - Single Data Type: `data=personnel`
  - Multiple Data Types: `data=personnel,resources`

<!-- ### `year`
- **Type**: `string` or `list`
- **Description**: The year(s) for which you want to retrieve data. Accepts a single year or a comma-separated list of years.
- **Example**:
  - Single Year: `year=2020`
  - Multiple Years: `year=2018,2019,2020` -->

<!-- ### `format`
- **Type**: `string` or `list`
- **Description**: The putput file format in which you'd like your data. Can be one of csv or shp
- **Example**:
  - Single Year: `format=csv` -->

## Example Request

To query data for the Tanzania, for personnel and resoruces, your request would look like this:


https://elzapqbt1h.execute-api.us-east-1.amazonaws.com/dev/query?iso=tan&data=personnel,resources


## Response Format

The API returns the data in CSV format. The CSV will be downloadable directly from the response.

