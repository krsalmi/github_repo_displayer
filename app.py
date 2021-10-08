from flask import Flask, render_template, request, json
import requests
from datetime import datetime, timezone
import dateutil.parser

# Python Flask app to search for Github user through the Github API and display
# information of that user's public repositories.

app = Flask(__name__)

# Changes the date-time from an ISO extended format to
# an easier to read date-time string. Also adjusts the time to fit the local 
# timezone.
def change_iso_format_time(date_to_change):
	new_date = dateutil.parser.isoparse(date_to_change) # ISO 8601 extended format to datetime.datetime object
	new_date = date.replace(tzinfo=timezone.utc).astimezone(tz=None) #change timezone from UTC to local
	new_date = date.strftime("%H:%M, %d %b %Y")
	return new_date

# Loops through repositories and reformats the "updated_at" times of each repo
# with the help of change_is_format_time(). Does the same to the user's "created_at" info
def change_time_formats(repos, user):
	for repo in repos:
		new_date = change_iso_format_time(repo["updated_at"])
		repo["updated_date_string"] = new_date
	user["created_date_string"] = change_iso_format_time(user["created_at"])

# Url to search for a specific user
def get_user_url(user):
	base_url = "https://api.github.com/users/"
	return base_url + user

# Url to search for a user's repositories
def get_user_repos_url(user):
	url = f"https://api.github.com/users/{user}/repos"
	return url

# Url to search for an organizations repositories
def get_org_repo_url(org):
	url = f"https://api.github.com/orgs/{org}/repos"
	return url

# Renders an apologetic template in the case that a username
# was not found successfully
def apology(message):
	return render_template("oops.html", text=message)


# Connects to the Github API endpoint and returns the response in json format. 
# Only the edge case where a searched for username could not be
# returned is handled separately, in all other errors an 
# exception is raised.

def connect_to_endpoint(url):
	response = requests.request("GET", url)
	if response.status_code != 200:
		if "https://api.github.com/users/" in url:
			return(response.reason)
		else:
			raise Exception(
				"Request returned an error: {} {}".format(
					response.status_code, response.text
				)
		)
	return response.json()

# Checks to see if the username belongs to a user or an organization
# and fetches the search urls accordingly
def get_repos_of_user_or_org(info_user):
	print(info_user)
	if info_user["type"] == "User":
		url = get_user_repos_url(info_user["login"])
	else:
		url = get_org_repo_url(info_user["login"])
	ret_repos = connect_to_endpoint(url)
	return ret_repos


@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		return render_template("index.html")
	else:
		name = request.form.get("name")
		info_user = connect_to_endpoint(get_user_url(name))
		# if connect_to_endpoint() returned a string instead of a json object, 
		# it is an error message and an apology template will be rendered
		if type(info_user) is str:
			return(apology(info_user))
		ret_repos = get_repos_of_user_or_org(info_user)
		change_time_formats(ret_repos, info_user)
		return render_template("displayrepos.html", user=info_user, repos=ret_repos)
