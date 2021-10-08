# Github Repo Displayer

A live version of the app can be found on Heroku, check out
https://github-repo-displayer.herokuapp.com/  

Repo Displayer is a Python Flask application where the user can search for a Github user/organization. The app will display information about the user's public repositories and some basic information of the user themselves.  
  
The program will connect to the Github API endpoint a few times. First the program will receive the username being searched for after requesting it from the form displayed on the index page. The program will then search for information on that user through the API return the information in json format. If however, the main function receives a string instead of a json object, it will display an apologetic template displaying the error message (most commonly that the username was not found). This is the only edgecase I handle separately with its own template, in all other errors happening during the endpoint-connection will simply raise an exception, display the error message and exit the program.  
  
After receiving information on the user, the program check to see if that username belongs to a user or an organization, because repositories of these two "types" must be searched with a different URL. After the second attempt to connect to the Github API is over successfully and repository-information is returned, the certain date-time info for each repository will be adjusted from the ISO extended format to a more natural date and time string.
  
A new html template will be rendered that displays the searched-for user's public repositories and showcases some additional information, including the profile picture and full name of the user themselves.
