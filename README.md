# Data Engineer Use Case
The purpose of this task is to present how to extract and parse data from a given source to be inserted into a database. Then, make the data available from the database via a REST API. 

Knowlege used: ETL, Database Design, API Development.

The idea is to enter data from the `data.json` file into an SQLite database, and make the data available through an API. The json-file contains 1000 randomly sampled CVEs' from 2019, with information related to each CVE.
CVE® is a list of entries—each containing an identification number, a description, and at least one public reference—for publicly known cybersecurity vulnerabilities.


### Specifications:

#### Database 

The json contains lots of information that we are not interested in, and to narrow the scope of the case only this information will be entered into the database. 

1. All CVEs', with its description and related dates.
2. All CPEs' excluding version data. CPEs' can have different configurations and operators, but you should regard all CPEs' as directly affected by a CVE, so don't mind the operator/children structure. 
3. The CVSS3 score related to each CVE. 
4. This will be implemented using SqlAlchemy.

#### API

1. An endpoint `/cpe/{vendor}/{product}` exists that returns a list of all CVEs related to that particular CPE.
2. An endpoint `/cve/{cve_id}` exists that returns a CVE with its corresponding CVSS3, CPEs, description, and dates. 
3. The API is implemented using Flask.

### Running the code locally

Open the instruction.txt file present in the repository for more information.