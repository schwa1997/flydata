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

This folder contains the files related to the task 'Domain and Data Selection'.

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

#### 📁 Data Processing Folder

This folder contains the files related to the task 'Data Population'.

- 1. countries.bat
- 2. cities.xlax
- 3. airport.dat
- 4. routes.dat
- ...
