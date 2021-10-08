from flask import Flask, render_template, request, json
import requests
from datetime import datetime, timezone
import dateutil.parser

# figure out heroku
# edge cases

app = Flask(__name__)

def change_repo_time_format(repos):
	for repo in repos:
		date = dateutil.parser.isoparse(repo["updated_at"]) # ISO 8601 extended format to datetime.datetime object
		date = date.replace(tzinfo=timezone.utc).astimezone(tz=None) #change timezone from UTC to local
		date = date.strftime("%H:%M, %d %b %Y")
		repo["updated_date_string"] = date


def get_user_url(user):
	base_url = "https://api.github.com/users/"
	return base_url + user

def get_user_repos_url(user):
	url = f"https://api.github.com/users/{user}/repos"
	return url

def get_org_repo_url(org):
	url = f"https://api.github.com/orgs/{org}/repos"
	return url

def apology(message):

	return render_template("oops.html", text=message)

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
		if type(info_user) is str:
			return(apology(info_user))
		ret_repos = get_repos_of_user_or_org(info_user)
		change_repo_time_format(ret_repos)
		return render_template("displayrepos.html", user=info_user, repos=ret_repos)
