""" 
Unit 16: Plotting Repositories

Ambrea Williams

Date: 08/08/2025

Description: Visualizes the Java repositories on GitHub using GitHub API and Plotly.
Refactored using OOP and SOLID design principles.
"""

import requests
import plotly.express as px


class GitHubAPIClient:
    def __init__(self, language="Java", per_page=30):
        """Initializes the GitHub API client with the specified language and number of repositories per page."""
        self.api_url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        self.params = {"per_page": per_page}

    def fetch_top_repositories(self):
        response = requests.get(self.api_url, headers=self.headers, params=self.params)
        response.raise_for_status()
        return response.json()


class RepoDataParser:
    def __init__(self, response_dict):
        """Initializes the parser with the response dictionary from the GitHub API."""
        self.repo_dicts = response_dict["items"]

    def extract_repo_data(self):
        """Extracts repository links, star counts, and labels from the repository data."""
        repo_links, stars, labels = [], [], []

        for repo in self.repo_dicts:
            name = repo["name"]
            url = repo["html_url"]
            owner = repo["owner"]["login"]
            stars_count = repo["stargazers_count"]
            description = repo["description"] or "No description provided."

            repo_links.append(f"<a href='{url}'>{name}</a>")
            stars.append(stars_count)
            labels.append(f"{owner}<br />{description}")

        return repo_links, stars, labels


class RepoPlotter:
    def __init__(self, repo_links, stars, labels, language="Java"):
        """Initializes the plotter with repository links, star counts, labels, and language."""
        self.repo_links = repo_links
        self.stars = stars
        self.labels = labels
        self.language = language

    def plot(self):
        """Generates a bar plot of the repositories."""
        fig = px.bar(
            x=self.repo_links,
            y=self.stars,
            hover_name=self.labels,
            labels={"x": "Repository", "y": "Stars"},
            title=f"Most-Starred {self.language} Projects on GitHub"
        )
        fig.update_layout(xaxis_tickangle=45)
        fig.show()


def main():
    """Main function to execute the program."""
    client = GitHubAPIClient(language="Java")
    response_data = client.fetch_top_repositories()

    parser = RepoDataParser(response_data)
    repo_links, stars, labels = parser.extract_repo_data()

    plotter = RepoPlotter(repo_links, stars, labels, language="Java")
    plotter.plot()


if __name__ == "__main__":
    main()
