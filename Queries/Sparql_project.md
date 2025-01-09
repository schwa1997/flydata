1. Shows for every manufacturer which models they produce and how many aircrafts per model there are:

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
order by ?manufacturer_name ?model_name
```

2. Shows all the airports you can fly to from every departure airport:

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?departure_airport ?arrival_airport where {
?dep a fly:Airport;
fly:name ?departure_airport.
?arr a fly:Airport;
fly:name ?arrival_airport.
?route a fly:Route;
fly:hasDepartureAirport ?dep;
fly:hasArrivalAirport ?arr.
} group by ?departure_airport ?arrival_airport

```

3. Same as above but now with the number of flights that flew that specific route, ordered by descending number of flights:

```sql

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
?air a ?Airport;
fly:isLocatedInCity ?cty.
?st a fly:State;
fly:name ?state.
}group by ?state ?city
order by desc (?nr_airp)

```

5. number of airports per state with the total population of that state:

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?state (COUNT(?air) as ?nr_airp) (SUM(?pop) as ?total_population) where{
?cty a fly:City;
fly:isLocatedInState ?st;
fly:population ?pop;
fly:name ?city.
?air a ?Airport;
fly:isLocatedInCity ?cty.
?st a fly:State;
fly:name ?state.
}group by ?state
order by desc (?nr_airp)

```

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

10. Shows carriers with their fleet size and most common aircraft model:

```sql

prefix fly: <http://www.semanticweb.org/nele/ontologies/2024/10/flydata/>

select ?carrier_name
(COUNT(distinct ?aircraft) as ?fleet_size)
?most_common_model
(COUNT(?aircraft_model) as ?model_count) where {
?carrier a fly:Carrier;
fly:name ?carrier_name.
?aircraft fly:isOwnedByCarrier ?carrier;
fly:hasModel ?aircraft_model.
?aircraft_model fly:name ?most_common_model.
} group by ?carrier_name ?most_common_model
order by ?carrier_name desc(?model_count)

```
