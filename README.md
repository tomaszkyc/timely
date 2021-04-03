<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** tomaszkyc, repo_name, twitter_handle, email, project_title, project_description
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/tomaszkyc/timely">
    <img src="app/static/images/favicon/android-chrome-192x192.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Timely</h3>

  <p align="center">
    Free countdown app which helps you measure focus time.
    <br />
    <a href="https://github.com/tomaszkyc/timely"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://timely-309119.ey.r.appspot.com">View Demo</a>
    ·
    <a href="https://github.com/tomaszkyc/timely/issues">Report Bug</a>
    ·
    <a href="https://github.com/tomaszkyc/timely/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Timely Screen Shot][product-screenshot]](https://example.com)

Project idea came from not so popular apps to countdown time. 
I was searching the solution for myself to use it on mobile, desktop and tablet. 
I haven't found such a good product so I make an own 
little app to help me with measuring my focus time.   

Now the app [is public available][live-demo] and anyone can use it with or without an account.

If you just want to test the app how it looks after the log in but you don't want to register - below is a test user account you can use:
```text
Login: user@domain.com
Password: password
```



### Built With

#### Backend

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) (Flask, Flask-Mail, flask-marshmallow, Flask-Migrate, Flask-RESTful, Flask-SQLAlchemy, Flask-WTF)
* [pytest](https://docs.pytest.org/en/stable/) for unit and functional tests
* Docker and Docker-Compose

#### Database

* [MySQL 5.8](https://dev.mysql.com/)

#### Frontend

* HTML/CSS
* [jQuery](https://jquery.com/)
* [Bootstrap](https://getbootstrap.com/)
* [TypeScript](https://www.typescriptlang.org/)
* [webpack and some plugins to minify css and js](https://webpack.js.org/)

#### Live demo

[The live demo][live-demo] was deployed on [Google Cloud Platform][gcp] using App Engine and Cloud SQL.


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Before installation make sure that you have installed [Docker][docker].

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/tomaszkyc/timely.git
   cd timely
   docker-compose up
   ```

2. Go to address `http://localhost:5001` and you will see a main page.


<!-- USAGE EXAMPLES -->
## Usage

You can deploy the app locally on some server and use it internally in your home network.



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/tomaszkyc/timely/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

For contact details please check [my Github profile][github-profile]

Project Link: [https://github.com/tomaszkyc/timely](https://github.com/tomaszkyc/timely)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/tomaszkyc/timely.svg?style=for-the-badge
[contributors-url]: https://github.com/tomaszkyc/timely/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/tomaszkyc/timely.svg?style=for-the-badge
[forks-url]: https://github.com/tomaszkyc/timely/network/members
[stars-shield]: https://img.shields.io/github/stars/tomaszkyc/timely.svg?style=for-the-badge
[stars-url]: https://github.com/tomaszkyc/timely/stargazers
[issues-shield]: https://img.shields.io/github/issues/tomaszkyc/timely.svg?style=for-the-badge
[issues-url]: https://github.com/tomaszkyc/timely/issues
[license-shield]: https://img.shields.io/github/license/tomaszkyc/timely.svg?style=for-the-badge
[license-url]: https://github.com/tomaszkyc/timely/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/tomaszkyc
[product-screenshot]: resources/images/home-page.png
[live-demo]: https://timely-309119.ey.r.appspot.com
[gcp]: https://cloud.google.com/
[docker]: https://www.docker.com/
[github-profile]: https://github.com/tomaszkyc