import urllib, urllib2
import xml.etree.ElementTree

def medlinePlus_query(search_terms):
    # Specify the base
    root_url = 'https://wsearch.nlm.nih.gov/ws/query'
    term_delimiter = '+'
    keywords = term_delimiter.join(search_terms.split(' '))

    search_url = '%s?db=%s&term="%s"' % (root_url, 'healthTopics', keywords)

    # Create our results list which we'll populate.
    results = []

    try:
        # Connect to the server and read the response generated.
        response = urllib2.urlopen(search_url).read()
        print search_url 
        e = xml.etree.ElementTree.fromstring(response)
        for doc in e.iter('document'):
            title = ''
            summary = ''
            for content in doc.iter('content'):
                if content.get('name') == 'title':
                    title = content.text
                elif content.get('name') == 'FullSummary':
                    summary = content.text

            entry = {
                'title': title,
                'link': doc.get('url'),
                'summary': summary
            }

            results.append(entry) 
        #print response 
        #print search_url   

    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError as e:
        print "Error when querying the MedlinePlus API: ", e

    # Return the list of results to the calling function.
    #print results
    return results

#medlinePlus_query("cancer")#
#print len(medlinePlus_query("nina nina nina"))