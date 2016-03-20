import json
import urllib, urllib2

# Add your HEALTHFINDER_API_KEY

HEALTHFINDER_API_KEY = 'gemefgmnusizifyl'

def healthfinder_query(search_terms):
    # Specify the base
    root_url = 'http://healthfinder.gov/developer/Search.json'
    term_delimiter = '%20'
    keywords = term_delimiter.join([x for x in search_terms.split(' ') if x])

    search_url = '%s?api_key=%s&keyword="%s"' % (root_url, HEALTHFINDER_API_KEY, keywords)

    # Create our results list which we'll populate.
    results = []

    try:
        # Connect to the server and read the response generated.
        response = urllib2.urlopen(search_url).read()
        # Convert the string response to a Python dictionary object.
        json_response = json.loads(response)
        print search_url
        #check if either result or topic does not exist
        if 'Result' not in json_response or 'Topics' not in json_response['Result']:
            return []
        # Loop through each page returned, populating out results list.
        #print type(json_response['Result']['Topics']), json_response['Result']['Topics']

        # If there is only one thing to return turn it into list of dictionaries 
        topics = json_response['Result']['Topics']
        if isinstance(topics, dict):
            topics = [topics]

        for result in topics:
            #print type(result), result
            if 'Sections' not in result:
                continue
            # Each section description that is not empty for all sections
            summary = []
            for section in result['Sections']:
                if section['Description']:
                    summary.append(section['Description'])

            entry = {
                'title': result['Title'],
                'link': result['AccessibleVersion'],
                'summary': ' '.join(summary)
            }
            results.append(entry)

    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError as e:
        print "Error when querying the healthfinder API: ", e

    # Return the list of results to the calling function.
    # print results
    return results
if __name__=="__main__":
    print healthfinder_query("cancer")