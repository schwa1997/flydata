<img src="https://www.unidformazione.com/wp-content/uploads/2018/04/unipd-universita-di-padova.png" alt="University of Padova Logo" style="float: right; width: 150px;">

# ✈️ FLYDATA - Graph Databases Course - Prof. Gianmaria Silvello

## 🎓 University of Padova - COMPUTING ENGINEERING A.A. 2024-25

### 🎯 Objective

Our project focuses on flight-related data, including flights, airlines, routes, airports, cities, countries, and flying conditions like weather. The goal is to model this data in a graph database to uncover insights, such as the impact of weather on flight punctuality and quantitative analysis of cities and routes.

### 💻 Required Software

- **Protégé 5.5.0 or later**

  - Ontology editor for creating and maintaining the .ttl files
  - Download: https://protege.stanford.edu/

- **Neo4j Desktop 1.5.0 or later**

  - Graph database platform for storing and querying the flight data
  - Download: https://neo4j.com/download/

- **Python 3.8+**

  - Required for data processing scripts
  - Recommended IDE: PyCharm or VS Code
  - Required packages:
    - pandas
    - numpy
    - neo4j-driver
    - rdflib

- **GraphDB Free**
  - RDF database for querying the ontology
  - Download: https://graphdb.ontotext.com/

### 📁 File Structure

#### 📁 Data Selection Folder

Contains documentation about our chosen datasets and domain:

- 📄 domain_selection.pdf
  - Group name and members
  - Dataset sources and URLs
  - Domain description and rationale
  - Technical challenges
  - Dataset characteristics

Our group will decide on the open dataset(s) to model and process for the project. The submission should include a PDF file with the following information:

- 👥 Group name
- 👤 Component names
- 🔗 URLs where the data is available
- 📝 A brief description of the domain of interest
- 🎯 Reasons for selecting the domain for the project
- ⚠️ Main challenges related to the dataset
- 📈 Main characteristics of the selected dataset(s)

#### 📁 Ontology Folder

This folder contains the files related to the task 'Ontology'.

- flydata.ttl
  This is build by Protege, and it contains the ontology of the project.
- flydata(with data).ttl
  This is the ontology with the data loaded. You can see the data loaded by opening the file in Protege.

#### 📁 Data Collection Folder

This folder contains the files related to the task 'Data Collection'.

- CSVData
  - airports.csv
  - cities.csv
  - countries.csv
  - routes.csv
  - ...
- OriginalData
  - airports.dat
  - cities.xlsx
  - countries.bat
  - routes.dat
  - ...

##### DataConversion.py

This script converts the original data into CSV format.

#### 📁 Serialization Folder

#### - ttl folder

- weather.ttl (:hasAirport)
- Flight.ttl (:hasAircraft, :isOperatedBy( carrier ),:hasRoute)
- airport,ttl(:isLocatedInCity)
- cities.ttl(:isLocatedInState)
- Aircraft.ttl (isOwnedByCarrier,:hasModel ),
- Carrier.ttl(:hasRoute)
- Model.ttl
- Route.ttl(:hasArrivalAirport, :hasDepartureAirport）
- city.ttl (:isLocatedInState)
- states.ttl
- ...

#### - script

You should use Jupyter Notebook to run the script.
