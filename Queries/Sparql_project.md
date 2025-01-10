# Table of Contents

1. [Model-Aircraft-Manufacturer](#model-aircraft-manufactuere)

   1. [Most Popular Aircraft Models by Manufacturer](#1-most-popular-aircraft-models-by-manufacturer)
   2. [Number of Unique PIPER Models](#2-number-of-unique-piper-models)
   3. [Total Aircraft Count for PIPER](#3-total-aircraft-count-for-piper)
   4. [Aircraft Count by CIRRUS Model](#4-aircraft-count-by-cirrus-model)

2. [Routes-Airports-City-State](#routes-airports-city-state)

   1. [Top 10 Airports by Departure Routes](#1-top-10-airports-by-departure-routes)
   2. [Airport Sharing by City Population](#2-airport-sharing-by-city-population)
   3. [Airport Sharing by State Population](#3-airport-sharing-by-state-population)

3. [Route-Flights-Weather](#route-flights-weather)
   1. [Carrier Delays](#1-the-carriers-with-a-total-delay-time-over-all-the-flights-in-minutes-ordered-by-most-delay)
   2. [Model Delays](#2-shows-the-average-delay-time-per-aircraft-model-ordered-by-highest-average-delay)

---

# Model-Aircraft-Manufactuere

## 1. Most Popular Aircraft Models by Manufacturer

### Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

SELECT  ?model_name ?manufacturer_name (COUNT(?aircraft) as ?nr_aircrafts)
WHERE {
  ?aircraft a fly:Aircraft ;
           fly:hasModel ?model .

  ?model a fly:Model ;
         fly:name ?model_name ;
         fly:hasManufacturer ?manufacturer .

  ?manufacturer a fly:Manufacturer ;
                fly:name ?manufacturer_name .
}
GROUP BY ?manufacturer_name ?model_name
ORDER BY DESC(?nr_aircrafts)
LIMIT 10

```

### Result

| Model     | Manufacturer       | Number of Aircrafts |
| --------- | ------------------ | ------------------- |
| PA-28-140 | PIPER              | 4244                |
| SR22      | CIRRUS DESIGN CORP | 3849                |
| 172M      | CESSNA             | 3570                |
| PA-28-180 | PIPER              | 3492                |
| J3C-65    | PIPER              | 3166                |
| 172N      | CESSNA             | 3136                |
| PA-28-181 | PIPER              | 2739                |
| SR22T     | CIRRUS DESIGN CORP | 2449                |
| 182P      | CESSNA             | 2096                |
| PA-18-150 | PIPER              | 2033                |

### Explanation

This query shows:

- Most popular aircraft models and their manufacturers
- PIPER and CIRRUS DESIGN CORP dominate the top 10
- PA-28-140 is the most common model with 4,244 aircraft

## 2. Number of Unique PIPER Models

Following the last query, we can see that PIPER has the most popular aircraft models. Now we want to know how many unique models PIPER has manufactured.

### Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

SELECT ?manufacturer_name (COUNT(DISTINCT ?model) as ?number_of_models)
WHERE {
  ?model a fly:Model ;
         fly:hasManufacturer ?manufacturer .

  ?manufacturer a fly:Manufacturer ;
                fly:name ?manufacturer_name .

  FILTER(?manufacturer_name = "PIPER")
}
GROUP BY ?manufacturer_name
```

### Result

| Manufacturer | Number of Models |
| ------------ | ---------------- |
| PIPER        | 261              |

### Explanation

This query shows:

- PIPER has manufactured 261 different aircraft models
- Uses DISTINCT to count unique models only
- Filters specifically for PIPER manufacturer

## 3. Total Aircraft Count for PIPER

Following the last query, we can see that PIPER has the most popular aircraft models. Now we want to know how many aircraft PIPER has manufactured.

### Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

SELECT ?manufacturer_name (COUNT(?aircraft) as ?total_aircrafts)
WHERE {
  ?aircraft a fly:Aircraft ;
           fly:hasModel ?model .

  ?model a fly:Model ;
         fly:hasManufacturer ?manufacturer .

  ?manufacturer a fly:Manufacturer ;
                fly:name ?manufacturer_name .

  FILTER(?manufacturer_name = "PIPER")
}
GROUP BY ?manufacturer_name
```

### Result

| Manufacturer | Total Aircraft |
| ------------ | -------------- |
| PIPER        | 44,584         |

### Explanation

This query reveals:

- Total PIPER aircraft: 44,584
- Averages about 171 aircraft per model (44,584/261)
- Shows PIPER's significant market presence

## 4. Aircraft Count by CIRRUS Model

Following the last query, we can see that CIRRUS DESIGN CORP has the second most popular aircraft models. Now we want to know how many aircraft CIRRUS DESIGN CORP's each model has manufactured.

### Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

SELECT ?model_name (COUNT(?aircraft) as ?number_of_aircrafts)
WHERE {
  ?aircraft a fly:Aircraft ;
           fly:hasModel ?model .

  ?model a fly:Model ;
         fly:name ?model_name ;
         fly:hasManufacturer ?manufacturer .

  ?manufacturer a fly:Manufacturer ;
                fly:name ?manufacturer_name .

  FILTER(?manufacturer_name = "CIRRUS DESIGN CORP")
}
GROUP BY ?model_name
ORDER BY DESC(?number_of_aircrafts)
```

### Result

| Model Name | Number of Aircraft |
| ---------- | ------------------ |
| SR22       | 3849               |
| SR22T      | 2449               |
| SR20       | 1339               |
| SF50       | 560                |
| SR10       | 3                  |
| SRT        | 1                  |
| EX18       | 1                  |

### Explanation

This query shows:

- SR22 is CIRRUS's most produced model (3,849 aircraft)
- Company focuses on fewer models than PIPER
- Seven different models in production
- Strong focus on SR series (SR22, SR22T, SR20)

# Routes-Airports-City-State

## 1. Top 10 Airports by Departure Routes

In this query we want to know which airports have the most departure routes or the most arrival routes. Here we will focus on the departure routes.

### code

```SQL

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?airport_name ?city_name ?state_name (COUNT(?route) as ?nr_routes) where {
?airport a fly:Airport;
fly:name ?airport_name;
fly:isLocatedInCity ?city.
?city a fly:City;
fly:name ?city_name;
fly:isLocatedInState ?state.
?state a fly:State;
fly:name ?state_name.
?route a fly:Route;
fly:hasDepartureAirport ?airport.
} group by ?airport ?airport_name ?city_name ?state_name
order by desc(?nr_routes)
limit 10
```

### Result

| Airport                                                    | City        | State                | Number of Routes |
| ---------------------------------------------------------- | ----------- | -------------------- | ---------------- |
| Denver International Airport                               | Denver      | Colorado             | 173              |
| Chicago O'Hare International Airport                       | Chicago     | Illinois             | 161              |
| Hartsfield Jackson Atlanta International Airport           | Atlanta     | Georgia              | 152              |
| Charlotte Douglas International Airport                    | Charlotte   | North Carolina       | 141              |
| McCarran International Airport                             | Las Vegas   | Nevada               | 125              |
| Minneapolis-St Paul International/Wold-Chamberlain Airport | Minneapolis | Minnesota            | 111              |
| George Bush Intercontinental Houston Airport               | Houston     | Texas                | 110              |
| Ronald Reagan Washington National Airport                  | Washington  | District of Columbia | 100              |
| Phoenix Sky Harbor International Airport                   | Phoenix     | Arizona              | 99               |
| Los Angeles International Airport                          | Los Angeles | California           | 96               |

### Explanation

- Denver International Airport has the most departure routes with 173 routes
- Chicago O'Hare International Airport has the second most departure routes with 161 routes
- Hartsfield Jackson Atlanta International Airport has the third most departure routes with 152 routes
- Charlotte Douglas International Airport has the fourth most departure routes with 141 routes
- Los Angeles International Airport has the fifth most departure routes with 96 routes

## 2. Airport Sharing by City Population

Based on the last query, we can see that the most departure routes are in the cities of Denver, Chicago, Atlanta, Charlotte, and Las Vegas. Now we want to know which cities have the most and least airports per population.

### Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

SELECT ?city_name ?nr_airp ?population ?people_per_airport
WHERE {
  {
    SELECT ?city_name (COUNT(?air) as ?nr_airp) (?pop as ?population)
           ((?pop/?nr_airp) as ?people_per_airport)
    WHERE {
      ?city a fly:City;
            fly:name ?city_name;
            fly:population ?pop.
      ?air a fly:Airport;
           fly:isLocatedInCity ?city.
    }
    GROUP BY ?city_name ?pop
    HAVING(?nr_airp > 0)
  }
  {
    # Top 5
    SELECT ?city_name ?nr_airp ?population ?people_per_airport
    WHERE {
      {
        SELECT ?city_name (COUNT(?air) as ?nr_airp) (?pop as ?population)
               ((?pop/?nr_airp) as ?people_per_airport)
        WHERE {
          ?city a fly:City;
                fly:name ?city_name;
                fly:population ?pop.
          ?air a fly:Airport;
               fly:isLocatedInCity ?city.
        }
        GROUP BY ?city_name ?pop
        HAVING(?nr_airp > 0)
      }
    } ORDER BY DESC(?people_per_airport) LIMIT 5
  }
  UNION
  {
    # Bottom 5
    SELECT ?city_name ?nr_airp ?population ?people_per_airport
    WHERE {
      {
        SELECT ?city_name (COUNT(?air) as ?nr_airp) (?pop as ?population)
               ((?pop/?nr_airp) as ?people_per_airport)
        WHERE {
          ?city a fly:City;
                fly:name ?city_name;
                fly:population ?pop.
          ?air a fly:Airport;
               fly:isLocatedInCity ?city.
        }
        GROUP BY ?city_name ?pop
        HAVING(?nr_airp > 0)
      }
    } ORDER BY ?people_per_airport LIMIT 5
  }
}
ORDER BY DESC(?people_per_airport)
```

### Result

| City               | Number of Airports | Population | People per Airport |
| ------------------ | ------------------ | ---------- | ------------------ |
| TOP 5              |                    |            |                    |
| Los Angeles        | 2                  | 11,922,389 | 5,961,195          |
| New York           | 4                  | 18,908,608 | 4,727,152          |
| Boston             | 1                  | 4,328,315  | 4,328,315          |
| San Francisco      | 1                  | 3,364,979  | 3,364,979          |
| Minneapolis        | 1                  | 2,892,569  | 2,892,569          |
| BOTTOM 5           |                    |            |                    |
| Manley Hot Springs | 1                  | 17         | 17                 |
| Elfin Cove         | 1                  | 16         | 16                 |
| Lake Minchumina    | 1                  | 14         | 14                 |
| Nikolski           | 1                  | 12         | 12                 |
| Bettles            | 1                  | 0          | 0                  |

### Explanation

This query:

1. Calculates the number of people per airport for each city
2. Shows both the cities with highest and lowest airport sharing
3. Only includes cities that have at least one airport (HAVING clause)
4. Orders results to show both extremes (most and least people per airport)
5. Bettles, Alaska (often referred to as Bettles City) does have a small population, but it is one of the least populated areas in the United States. As of recent counts, the population is typically under 20 residents, making it more of a small community than a city. Bettles primarily serves as a hub for outdoor activities and as a gateway to the nearby Gates of the Arctic National Park and Preserve.

The results show that:

- Large cities like New York have many people sharing each airport (2.7M people per airport)
- Smaller cities, especially in Alaska, have fewer people per airport
- This reflects both population density and geographic/accessibility needs

## 3. Airport Sharing by State Population

Based on the last query, we can see that the most departure routes are in the cities of Denver, Chicago, Atlanta, Charlotte, and Las Vegas. Now we want to know which states have the most and least airports per population.

### Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

SELECT ?state ?nr_airp ?total_population ?people_per_airport
WHERE {
  {
    SELECT ?state (COUNT(?air) as ?nr_airp) (SUM(?pop) as ?total_population)
    ((?total_population/?nr_airp) as ?people_per_airport)
    WHERE {
      ?cty a fly:City;
      fly:isLocatedInState ?st;
      fly:population ?pop;
      fly:name ?city.
      ?air a fly:Airport;
      fly:isLocatedInCity ?cty.
      ?st a fly:State;
      fly:name ?state.
    } GROUP BY ?state
  }
  {
    # Top 3
    SELECT ?state ?nr_airp ?total_population ?people_per_airport
    WHERE {
      # Subquery repeated here
      {
        SELECT ?CITY (COUNT(?air) as ?nr_airp) (SUM(?pop) as ?total_population)
        ((?total_population/?nr_airp) as ?people_per_airport)
        WHERE {
          ?cty a fly:City;
          fly:isLocatedInState ?st;
          fly:population ?pop;
          fly:name ?city.
          ?air a fly:Airport;
          fly:isLocatedInCity ?cty.
          ?st a fly:State;
          fly:name ?state.
        } GROUP BY ?state
      }
    } ORDER BY DESC(?people_per_airport) LIMIT 3
  }
  UNION
  {
    # Bottom 3
    SELECT ?state ?nr_airp ?total_population ?people_per_airport
    WHERE {
      # Subquery repeated here
      {
        SELECT ?state (COUNT(?air) as ?nr_airp) (SUM(?pop) as ?total_population)
        ((?total_population/?nr_airp) as ?people_per_airport)
        WHERE {
          ?cty a fly:City;
          fly:isLocatedInState ?st;
          fly:population ?pop;
          fly:name ?city.
          ?air a fly:Airport;
          fly:isLocatedInCity ?cty.
          ?st a fly:State;
          fly:name ?state.
        } GROUP BY ?state
      }
    } ORDER BY ?people_per_airport LIMIT 3
  }
}
ORDER BY DESC(?people_per_airport)

```

### Result

| State                | Number of Airports | Total Population | People per Airport |
| -------------------- | ------------------ | ---------------- | ------------------ |
| TOP 3                |                    |                  |
| District of Columbia | 2                  | 10,232,756       | 5,116,378          |
| New York             | 24                 | 79,064,833       | 3,294,368          |
| Illinois             | 24                 | 35,529,902       | 1,480,413          |
| BOTTOM 3             |                    |                  |
| Vermont              | 5                  | 150,177          | 30,035             |
| Wyoming              | 13                 | 289,688          | 22,284             |
| Alaska               | 144                | 1,178,370        | 8,183              |

### Explanation

- There's a massive disparity between the most and least dense states in terms of airport service
- Urban areas (DC, NY) show high population pressure on airport infrastructure
- Rural/remote states (Alaska) show extensive airport networks serving smaller populations
- The data suggests that airport distribution is influenced by both population density and geographic factors

# Route-Flights-Weather

## 1. Carriers with Total Delay Time

### code

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?Carrier (SUM(?delay) as ?tot_delay) where {
?Car a fly:Carrier;
fly:name ?Carrier.
?flight a fly:Flight;
fly:isOperatedBy ?Car;
fly:ActualArrivalDelayTime ?delay.
} group by ?Carrier
order by desc (?tot_delay )

```

## results

Spirit Airlines,398096
| Carrier | Total Delay (minutes) |
|---------|---------------------|
| American Airlines | 1,913,523 |
| United Airlines | 737,631 |
| Southwest Airlines | 643,731 |
| SkyWest | 624,190 |
| Delta Air Lines | 608,954 |
| JetBlue Airways | 536,392 |
| Spirit Airlines | 398,096 |
| Frontier Airlines | 348,656 |
| Comair | 329,258 |
| Alaska Airlines | 189,913 |
| Midwest Airlines | 174,630 |
| Pinnacle Airlines | 154,721 |
| Capital Cargo International Airlines | 148,660 |
| West Air Sweden | 148,660 |
| Red Jet Andes | 148,660 |
| American Eagle Airlines | 147,806 |
| Allegiant Air | 131,971 |
| Air Wisconsin | 84,293 |
| Mesa Airlines | 55,576 |
| Horizon Air | 49,823 |
| GoJet Airlines | 45,634 |
| Gandalf Airlines | 45,634 |
| CommutAir | 27,173 |
| Hawaiian Airlines | 18,327 |

## 2. Average Delay Time per Aircraft Model

### code

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?model_name (AVG(?delay) as ?avg_delay) (COUNT(?flight) as ?nr_flights) where {
?flight a fly:Flight;
fly:ActualArrivalDelayTime ?delay;
fly:hasAircraft ?aircraft.
?aircraft fly:hasModel ?model.
?model fly:name ?model_name.
} group by ?model_name
order by desc(?avg_delay)
limit 10

```

### results

| Aircraft Model | Average Delay (minutes) | Number of Flights |
| -------------- | ----------------------- | ----------------- |
| 777-323ER      | 67.76                   | 63                |
| 777-223        | 38.19                   | 177               |
| 767-424ER      | 33.47                   | 70                |
| A319-115       | 33.47                   | 3,292             |
| A320-214       | 28.40                   | 4,022             |
| 787-8          | 27.79                   | 389               |
| A321-253N      | 27.37                   | 736               |
| A319-112       | 27.23                   | 7,272             |
| 767-432ER      | 23.63                   | 57                |
| A321-231       | 23.49                   | 27,025            |

## 2.1 Analysis of Delay Categories

This query breaks down delays by their categories to understand which types of delays have the biggest impact on flight operations.

### Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

SELECT ?type ?total ?avg ?flights
WHERE {
  {
    BIND("Late Type E" AS ?type)
    {
      SELECT (SUM(?LateE) AS ?total) (AVG(?LateE) AS ?avg) (COUNT(?flight) AS ?flights)
      WHERE {
        ?flight a fly:Flight ;
                fly:LateE ?LateE .
        FILTER(?LateE > 0)
      }
    }
  }
  UNION
  {
    BIND("Late Type F" AS ?type)
    {
      SELECT (SUM(?LateF) AS ?total) (AVG(?LateF) AS ?avg) (COUNT(?flight) AS ?flights)
      WHERE {
        ?flight a fly:Flight ;
                fly:LateF ?LateF .
        FILTER(?LateF > 0)
      }
    }
  }
  UNION
  {
    BIND("Late Type G" AS ?type)
    {
      SELECT (SUM(?LateG) AS ?total) (AVG(?LateG) AS ?avg) (COUNT(?flight) AS ?flights)
      WHERE {
        ?flight a fly:Flight ;
                fly:LateG ?LateG .
        FILTER(?LateG > 0)
      }
    }
  }
  UNION
  {
    BIND("Late Type H" AS ?type)
    {
      SELECT (SUM(?LateH) AS ?total) (AVG(?LateH) AS ?avg) (COUNT(?flight) AS ?flights)
      WHERE {
        ?flight a fly:Flight ;
                fly:LateH ?LateH .
        FILTER(?LateH > 0)
      }
    }
  }
  UNION
  {
    BIND("Late Type I" AS ?type)
    {
      SELECT (SUM(?LateI) AS ?total) (AVG(?LateI) AS ?avg) (COUNT(?flight) AS ?flights)
      WHERE {
        ?flight a fly:Flight ;
                fly:LateI ?LateI .
        FILTER(?LateI > 0)
      }
    }
  }
}
ORDER BY DESC(?total)
```

### Results

| Delay Type  | Total Minutes | Average Minutes | Affected Flights |
| ----------- | ------------- | --------------- | ---------------- |
| Late Type I | 4,527,160     | 58.0            | 78,029           |
| Late Type E | 3,769,101     | 46.9            | 80,372           |
| Late Type G | 2,278,113     | 29.9            | 76,227           |
| Late Type F | 687,215       | 68.9            | 9,971            |
| Late Type H | 14,808        | 22.3            | 664              |

### Explanation

The analysis reveals:

- Late Type I (Carrier-caused) delays have the highest total impact with over 4.5M minutes of total delay, affecting 78,029 flights with an average delay of 58 minutes
- Late Type E (Late Aircraft) delays are the second most significant cause with 3.7M total minutes, affecting the most flights (80,372) with an average delay of 47 minutes
- Late Type G (NAS) delays account for 2.2M total minutes across 76,227 flights with a lower average delay of 30 minutes
- Late Type F (Weather) delays affect fewer flights (9,971) but have the highest average delay time per flight at 69 minutes
- Late Type H (Security) delays are relatively rare with only 664 affected flights and 14,808 total minutes of delay, averaging 22 minutes per delay
