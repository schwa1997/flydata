# 1. Shows for every manufacturer which models they produce and how many aircrafts per model there are:

## Code

```sql
prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?manufacturer_name ?model_name (COUNT(?aircraft) as ?nr_aircrafts) where {
?aircraft a fly:Aircraft ;
fly:hasModel ?model.
?model a fly:Model;
fly:name ?model_name;
fly:hasManufacturer ?manufacturer.
?manufacturer a fly:Manufacturer;
fly:name ?manufacturer_name.
} group by ?manufacturer_name ?model_name
order by desc(?nr_aircrafts)
LIMIT 10

```

## Result

| Manufacturer | Model | Number of Aircrafts |
| ------------ | ----- | ------------------- |
|              |       |                     |
|              |       |                     |
|              |       |                     |

## Explanation

This query groups the aircraft by manufacturer and model, counting the number of aircraft for each combination. The result shows the manufacturer, model, and the total number of aircraft for each model.


# 2. Show the top 10 airports that have the most routes departing from them, and which city and state they are in:

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

## Result

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

## Explanation

This query selects the top 10 airports with the most routes departing from them and the top 5 with the most routes arriving at them. It counts the number of routes for each airport and orders the results by the number of routes in descending order.

3. Same as above but now with the number of flights that flew that specific route, ordered by descending number of flights:

```SQL

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?departure_airport ?arrival_airport (COUNT(?flight) as ?nr_flights) where {
?dep a fly:Airport;
fly:name ?departure_airport.
?arr a fly:Airport;
fly:name ?arrival_airport.
?route a fly:Route;
fly:hasDepartureAirport ?dep;
fly:hasArrivalAirport ?arr.
?flight a fly:Flight;
fly:hasRoute ?route.

} group by ?departure_airport ?arrival_airport
order by desc (?nr_flights)

```

4.  Shows a state, a city and the number of airports in that city ordered by descending number of airports:

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?state ?city (COUNT(?air) as ?nr_airp) where {
?cty a fly:City;
fly:isLocatedInState ?st;
fly:name ?city.
?air a fly:Airport;
fly:isLocatedInCity ?cty.
?st a fly:State;
fly:name ?state.
}group by ?state ?city
order by desc (?nr_airp)

```

# 5. The most busiest and least busiest 3 states by airport busyness (people per airport)

## Code

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

## Result

| State                | Number of Airports | Total Population | People per Airport |
| -------------------- | ------------------ | ---------------- | ------------------ |
| District of Columbia | 2                  | 10,232,756       | 5,116,378          |
| New York             | 24                 | 79,064,833       | 3,294,368          |
| Illinois             | 24                 | 35,529,902       | 1,480,413          |
| Vermont              | 5                  | 150,177          | 30,035             |
| Wyoming              | 13                 | 289,688          | 22,284             |
| Alaska               | 144                | 1,178,370        | 8,183              |

## Explanation

There's a massive disparity between the most and least dense states in terms of airport service
Urban areas (DC, NY) show high population pressure on airport infrastructure
Rural/remote states (Alaska) show extensive airport networks serving smaller populations
The data suggests that airport distribution is influenced by both population density and geographic factors

6. The carriers with a total delay time over all the flights in minutes ordered by most delay:

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

7. Shows the average delay time per aircraft model, ordered by highest average delay:

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

```

8. Shows weather conditions that caused flight cancellations:

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?airport_name ?weather_type (COUNT(?flight) as ?cancelled_flights) where {
?flight a fly:Flight;
fly:cancellationCode "B"; # Weather-related cancellations
fly:hasRoute ?route.
?route fly:hasDepartureAirport ?airport.
?airport fly:name ?airport_name.
?weather fly:hasAirport ?airport;
fly:weatherType ?weather_type;
fly:weatherDate ?weather_date.
?flight fly:flightDate ?flight_date.
FILTER(DAY(?weather_date) = DAY(?flight_date))
} group by ?airport_name ?weather_type
order by desc(?cancelled_flights)

```

9. Shows the busiest routes by number of flights and their average delays:

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?dep_name ?arr_name
(COUNT(?flight) as ?total_flights)
(AVG(?delay) as ?avg_delay) where {
?flight a fly:Flight;
fly:hasRoute ?route;
fly:ActualArrivalDelayTime ?delay.
?route fly:hasDepartureAirport ?dep;
fly:hasArrivalAirport ?arr.
?dep fly:name ?dep_name.
?arr fly:name ?arr_name.
} group by ?dep_name ?arr_name
order by desc(?total_flights)
limit 10

```
