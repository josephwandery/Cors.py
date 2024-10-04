import requests
import argparse
from tld import get_tld

def check_cors(url):
    try:
        response = requests.get(url, headers={'Origin': 'http://evil.com'})
        if 'Access-Control-Allow-Origin' in response.headers:
            if response.headers['Access-Control-Allow-Origin'] == '*':
                print(f'[!] Potential CORS misconfiguration found: {url}')
            elif 'evil.com' in response.headers['Access-Control-Allow-Origin']:
                print(f'[!] Potential CORS misconfiguration found: {url}')
            else:
                print(f'[-] No CORS misconfiguration found: {url}')
        else:
            print(f'[-] No CORS headers found: {url}')
    except requests.exceptions.RequestException as e:
        print(f'[!] Error checking {url}: {e}')

def main():
    parser = argparse.ArgumentParser(description='CORS Misconfiguration Scanner')
    parser.add_argument('-u', '--url', help='URL to scan')
    parser.add_argument('-i', '--input', help='File with list of URLs to scan')
    args = parser.parse_args()

    if args.url:
        check_cors(args.url)
    elif args.input:
        with open(args.input, 'r') as file:
            urls = file.readlines()
            for url in urls:
                check_cors(url.strip())
    else:
        print('Please provide a URL with -u or a file with -i')

if __name__ == '__main__':
    main()
