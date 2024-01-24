#Libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

#Variables
Series_name = ['Sarzamin%20Madari',
               'Accomplice',
                '11',
                'Seven',
                'Notebook',
                'Fereshtehs%20Sin',
                'Saye%20Baz',
                'The%20Marsh',
                ]

base_url = "https://fermovi1.xyz/Series/Iranian/{}/"

resolutions = ["480p", "720p", "1080p"]



#functions
def generate_urls(base_url, array, resolutions):
    # Initialize the Web URLs array
    web_urls = []

    # Loop through each value in the array
    for value in array:
        # Loop through each resolution
        for resolution in resolutions:
            # Format the URL with the value and resolution
            url = base_url.format(value) + resolution + "/"
            # Add the URL to the Web URLs array
            web_urls.append(url)

    # Return the Web URLs array
    return web_urls

def get_mp4_links(urls):
    # Initialize an empty list to store all .mp4 links
    all_mp4_links = []

    for url in urls:
        # Check if the URL starts with 'http://' or 'https://'
        if not url.startswith('http://') and not url.startswith('https://'):
            print(f"Invalid URL: {url}")
            continue

        # Send a GET request
        response = requests.get(url)

        # If the GET request is successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            page_content = response.content

            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(page_content, 'html.parser')

            # Find all links in the webpage
            # The 'a' tag in HTML corresponds to a link
            # The 'href' attribute contains the URL of the link
            links = soup.find_all('a')

            # Filter for .mp4 links
            mp4_links = [link.get('href') for link in links if '.mp4' in link.get('href')]

            # Add the .mp4 links from this url to the total list
            mp4_links = [url + link for link in mp4_links]
            
            all_mp4_links.extend(mp4_links)

    return all_mp4_links

def write_html(urls, filename='index.html'):
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Selector</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }
        #searchInput {
            padding: 8px;
            width: 300px;
        }
        #result {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>URL Selector</h1>
    
    <label for="searchInput">Search:</label>
    <input type="text" id="searchInput" oninput="filterResults()">
    
    <div id="result"></div>

    <script>
        const urls = %s;

        function filterResults() {
            const searchInput = document.getElementById("searchInput").value.toLowerCase();
            const resultDiv = document.getElementById("result");

            // Clear previous results
            resultDiv.innerHTML = "";

            // Filter URLs based on search input
            const filteredUrls = urls.filter(url => url.toLowerCase().includes(searchInput));

            // Display filtered results
            if (filteredUrls.length > 0) {
                filteredUrls.forEach(url => {
                    const link = document.createElement("a");
                    link.href = url;
                    link.target = "_blank";
                    link.textContent = url;
                    resultDiv.appendChild(link);
                    resultDiv.appendChild(document.createElement("br"));
                });
            } else {
                resultDiv.textContent = "No matching URLs found.";
            }
        }

        // Initial display of all URLs
        filterResults();
    </script>
</body>
</html>
""" % urls

    with open(filename, 'w') as f:
        f.write(html)
#main code
Download_Pages = generate_urls(base_url,Series_name,resolutions)
Download_links = get_mp4_links(Download_Pages)




write_html(Download_links,'web2.html')
