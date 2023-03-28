<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<br />
<!-- PROJECT LOGO -->
<div align="center">
  <a href="">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/H%26M-Logo.svg/640px-H%26M-Logo.svg.png" alt="Logo" width="100" height="80">
  </a>

  <h3 align="center">H&M Capstone</h3>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project
For my second term capstone project, several Key Performance Indicators had to be obtained with pandas, given real H&M data. However, given that this was a capstone project, and trying to implement all the knowledge gained so far about Python, Javascript and Data Analytics/Pandas, I decided that the best way to integrate all this stacks was through an E commerce platform.

The main components of the project are:
* An e-commerce web, that uses the data given by H&M to simulate a real retailer. 
* A web application with streamlit to display and treat the KPI's based on filters.
* An API that connects the database with the streamlit application.
* A Database to provide the API, and serve the backend server. The database has tables storing the H&M data and application users.

### E-Commerce Website
This service provides the web simulating the H&M shop. It uses flask in the back end, and Javascript for the front end, and it's deployed in GCP App Enngine. The servers obtain the data directly from the database (for the sake of showing porpoises), using MySQL. The backend (server.py) provides data and templates for the following pages:
 * Index: that shows the catalog and obtains the categories of the articles displayed.
 * Login: logs the user through forms and opens a session for the user. If the user is an admin, a page showing the KPI's will be shown, if not it redirects back to the index
 * Register: to register new users. The passwords of the users are hashed in the database.
 * Search: provides article search functionality. Through a form, the item is queried in the database, and its result sent to the search page.
 * Cart: renders the cart page.

For the front end and Javascript description, visit the following <a href="https://github.com/rescolarandres/E-commerce-platform-in-Python-and-JS">link</a>


### Streamlit application
This service provides the user a simple way of interacting with the data in a streamlit application. It is coded in python and deployed in GCP App Engine. This service obtains the data from the API, through json files that are then converted to pandas dataframes. The application is composed of two main files:
1. Filters.py: a class to compute filters to add to the application. It is in this class, where the data is loaded and filtered depending on the users filters.
2. streammlit.py: which computes the kpi's (one per function) with pandas, and displays them in the application.
<img src="https://github.com/rescolarandres/Retailer-KPI-s-in-Streamlit/blob/main/streamlit.png">

### API
An API was created in python and deployed in GCP App Engine, to provide the streamlit application with the corresponding data. It has several endpoints to retrieve the data, and one endpoint to upload new tables to the CloudSQL database. The API requires authorization to be used. 
<img src="https://github.com/rescolarandres/Retailer-KPI-s-in-Streamlit/blob/main/api.png">


### Built With

Major frameworks/libraries used to bootstrap the project:

* [![Python][Python.com]][Python-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>






<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Architecture -->
## Architecture




<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
![Python.com](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![alt text](https://github.com/rescolarandres/Retailer-KPI-s-in-Streamlit/blob/main/arquitecture.png)
