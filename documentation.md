# API Documentation

## Overview

This API allows users to query data based on specific parameters such as `iso`, `data`, and `year`. Each of these parameters can be a string or a list, allowing for flexible queries. The API returns data in CSV format, ready for download.

## Base URL

https://b1godeo6y4.execute-api.us-east-1.amazonaws.com/dev/query


## HTTP Method

- **GET**: Retrieve data based on query parameters.

## Query Parameters

### `iso`
- **Type**: `string` or `list`
- **Description**: The ISO country code(s) for which you want to retrieve data. Accepts a single ISO code or a comma-separated list of ISO codes.
- **Example**:
  - Single ISO: `iso=usa`
  - Multiple ISOs: `iso=usa,can,mex`

### `data`
- **Type**: `string` or `list`
- **Description**: The specific data type(s) or categories you wish to query. This could represent different datasets or indicators.
- **Example**:
  - Single Data Type: `data=population`
  - Multiple Data Types: `data=population,gdp,inflation`

### `year`
- **Type**: `string` or `list`
- **Description**: The year(s) for which you want to retrieve data. Accepts a single year or a comma-separated list of years.
- **Example**:
  - Single Year: `year=2020`
  - Multiple Years: `year=2018,2019,2020`

## Example Request

To query data for the United States and Canada, for the population data type, across the years 2019 and 2020, your request might look like this:




## Response Format

The API returns the data in CSV format. The CSV will be downloadable directly from the response.

### Example Response

```csv
iso,data,year,value
USA,population,2019,329484123
USA,population,2020,331002651
CAN,population,2019,37411047
CAN,population,2020,37742154